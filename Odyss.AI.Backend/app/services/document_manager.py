import os
import aiofiles
import hashlib
import aiohttp
import asyncio

from app.config import Config
from datetime import datetime
from app.models.user import Document
from app.services.ocr_service import OCRService
from app.utils.test_data_provider import get_test_document

class DocumentManager:

    def __init__(self):
        self.local_file_path = Config.LOCAL_DOC_PATH
        self.tei_url = Config.TEI_URL + "/embed"
        self.ocr_service = OCRService()

    async def handle_document(self, file, username, is_local = True):
        try:
            filename = self.generate_filename(file.filename)
            filepath = await self.save_document_local_async(file, filename) if is_local else self.save_document_onedrive(file, filename)
            if filepath is None:
                return None, "File already exists"
            
            new_doc = self.get_new_doc(filename, filepath, file.filename)

            # sende new_doc an OCR, dort wird der Text ausgelesen und die Bilder erkannt
            # zurück kommt das Objekt mit den Text aufgesplittet und Bildern (hier die URLs hinterlegt)
            new_doc = self.ocr_service.extract_text(new_doc)
            # new_doc = get_test_document()

            # für die Texte werden Embeddings erstellt und in VektorDb gespeichert
            # await self.create_text_embedding_async(new_doc)

            # die Bilder werden in getaggt, entsprechend in LLM ausgelesen und Embeddings erstellt

            # Speicher new_doc in der Datenbank unter dem User

            return new_doc, "File uploaded successfully"
        except Exception as e:
            return None, e
    
    def generate_filename(self, original_filename):
        # Erzeuge einen SHA-256-Hash basierend auf dem ursprünglichen Dateinamen
        file_hash = hashlib.sha256(original_filename.encode('utf-8')).hexdigest()
        # Behalte die ursprüngliche Dateiendung bei
        _, file_extension = os.path.splitext(original_filename)
        return f"{file_hash}{file_extension}"

    async def save_document_local_async(self, file, filename):
        filepath = os.path.join(self.local_file_path, filename)
        
        if os.path.exists(filepath):
            return None  # Datei existiert bereits
        
        # Asynchrones Schreiben der Datei
        loop = asyncio.get_event_loop()
        content = await loop.run_in_executor(None, file.read)  # Lese den Inhalt synchron
        
        async with aiofiles.open(filepath, 'wb') as out_file:
            await out_file.write(content)  # Schreibe asynchron
        
        return filepath
    
    def get_new_doc(self, name, path, original_name):
        return Document(
            id = name,
            name = original_name,
            timestamp = datetime.now(),
            doclink = path,
            summary = "",
            imgList = [],
            textList = []
        )
    
    async def fetch_embedding_async(self, to_embed: str):
        async with aiohttp.ClientSession() as session:
            async with session.post(self.tei_url, json={"inputs": to_embed}) as response:
                if response.status == 200:
                    return await response.json().get("embedding")
                return None
            
    async def save_embedding_async(self, doc_id: str, embedding: str):
        # Speichere das Embedding in der VektorDb
        pass
    
    async def create_text_embedding_async(self, doc: Document):
        tasks = []
        for text in doc.textList:
            tasks.append(self.fetch_embedding(text.text))
        
        embeddings = await asyncio.gather(*tasks)
        
        for text, embedding in zip(doc.textList, embeddings):
            text.embedding = embedding

        
    
