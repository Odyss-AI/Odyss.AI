import os
import aiofiles
import hashlib
import aiohttp
import asyncio
import uuid

from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct
from app.config import Config
from datetime import datetime
from app.models.user import Document
from app.services.ocr_service import OCRService
from app.utils.test_data_provider import get_test_document
from app.utils.db import get_db
from app.utils.helpers import mistral_api
from app.utils.prompts import summary_prompt_builder

class DocumentManager:

    def __init__(self, qdrant_host='localhost', qdrant_port=6333):
        self.local_file_path = Config.LOCAL_DOC_PATH
        self.tei_url = Config.TEI_URL + "/embed"
        self.ocr_service = OCRService()
        self.qdrant_client = QdrantClient(host=qdrant_host, port=qdrant_port)
        self.collection_name = 'doc_embeddings'
        self.qdrant_client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config={'size': 1024, 'distance': 'Cosine'}
        )
        self.db = get_db()

    async def handle_document(self, file, username, is_local = True):
        try:
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
            # embeddings = await self.create_embeddings_async(new_doc)

            # Embeddings in Qdrant speichern
            # await self.save_embedding_async(id, embeddings)

            # TODO: Zusammenfassung des Dokuments erstellen mit LLM
            prompt = summary_prompt_builder(new_doc.textList)
            summary = await mistral_api(prompt)
            new_doc.summary = summary

            # Save new_doc in the database
            #await self.db.add_document_to_user_async(username, new_doc)

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
    
    async def fetch_embedding_async(self, to_embed: str):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.tei_url, json={"inputs": to_embed}) as response:
                    if response.status == 200:
                        response_json = await response.json()  # Stelle sicher, dass await verwendet wird
                        if isinstance(response_json, list) and len(response_json) > 0 and isinstance(response_json[0], list):
                            return response_json[0]  # Rückgabe des ersten Elements der Liste
                        else:
                            print("Fehler: Unerwartetes Format der API-Antwort.")
                            return None
                    else:
                        print(f"Fehler: {response.status}")
                        return None
        except aiohttp.ClientError as e:
            print(f"HTTP-Fehler: {e}")
            return None

    async def create_embeddings_async(self, doc: Document):
        tasks = []
        for chunk in doc.textList:
            tasks.append(self.fetch_embedding_async(chunk.text))
        for img in doc.imgList:
            tasks.append(self.fetch_embedding_async(img.imgtext))
            tasks.append(self.fetch_embedding_async(img.llm_output))
        
        embeddings = await asyncio.gather(*tasks)
        
        return embeddings
    
    async def save_embedding_async(self, doc_id: str, embeddings: list):
        try:
            points = [
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embedding,
                    payload={"doc_id": doc_id}
                )
                for embedding in embeddings
            ]
            self.qdrant_client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            print(f"Embeddings für Dokument {doc_id} erfolgreich gespeichert.")
        except Exception as e:
            print(f"Fehler beim Speichern der Embeddings: {e}")

        
    
