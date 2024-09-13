import os
import aiofiles
import hashlib
import aiohttp
import asyncio
import uuid

from app.config import Config
from datetime import datetime
from app.models.user import Document
from app.services.ocr_service import OCRService
from app.utils.test_data_provider import get_test_document
from app.utils.db import get_db
from app.utils.helpers import mistral_api
from app.utils.prompts import summary_prompt_builder
from app.services.sim_search_service import SimailaritySearchService

class DocumentManager:

    def __init__(self):
        self.local_file_path = Config.LOCAL_DOC_PATH
        self.tei_url = Config.TEI_URL + "/embed"
        self.sim_search = SimailaritySearchService()

    async def handle_document(self, file, username, is_local = True):
        try:
            db = get_db()
            filename, id = self.generate_filename(file.filename)
            filepath = await self.save_document_local_async(file, filename) if is_local else self.save_document_onedrive(file, filename)
            # if filepath is None:
            #     return None, "File already exists"
            
            # Create a new document object with necessary metadata
            # new_doc = self.get_new_doc(filename, filepath, file.filename)

            # Send new_doc to OCR, where the text is read out and the images are recognized
            # The object with the text split up and images (here the URLs are stored) comes back
            # new_doc = self.ocr_service.extract_text(new_doc)
            new_doc = get_test_document(id)

            # Embeddings mit TEI erstellen
            embeddings = await self.sim_search.create_embeddings_async(new_doc)

            # Embeddings in Qdrant speichern
            await self.sim_search.save_embedding_async(id, embeddings)

            # Zusammenfassung des Dokuments erstellen mit LLM
            prompt = summary_prompt_builder(new_doc.textList)
            summary = await mistral_api(prompt)
            new_doc.summary = summary

            # Save new_doc in the database
            await db.add_document_to_user_async(username, new_doc)

            return new_doc, "File uploaded successfully"
        except Exception as e:
            return None, e
    
    def generate_filename(self, original_filename):
        # Create a unique filename based on the original filename
        file_hash = hashlib.sha256(original_filename.encode('utf-8')).hexdigest()
        # Save the file extension
        _, file_extension = os.path.splitext(original_filename)
        return f"{file_hash}{file_extension}", file_hash

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


        
    
