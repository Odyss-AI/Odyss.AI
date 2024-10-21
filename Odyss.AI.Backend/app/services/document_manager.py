import os
import aiofiles
import hashlib
import aiohttp
import asyncio
import uuid
import logging

from bson import ObjectId

from app.config import Config
from datetime import datetime
from app.models.user import Document
from app.utils.test_data_provider import get_test_document
from app.utils.db import get_db
from app.utils.ml_connection import call_mistral_api_async
from app.utils.ocr_connection import extract_pdf_information_with_ocr
from app.utils.prompts import summary_prompt_builder
from app.services.sim_search_service import SimailaritySearchService
from app.utils.pdfconverter import convert_docx_or_pptx_to_pdf

class DocumentManager:
    """
    A class to manage document handling, including saving, processing, and storing documents.
    """

    def __init__(self):
        self.local_file_path = Config.LOCAL_DOC_PATH
        self.tei_url = Config.TEI_URL + "/embed"
        self.sim_search = SimailaritySearchService()

    async def handle_document_async(self, file, username, is_local = True):
        """
        Handles the document upload, processing, and storage asynchronously.

        Args:
            file: The file object to be processed.
            username (str): The username of the user uploading the document.
            is_local (bool, optional): Flag indicating if the file should be saved locally. Defaults to True.

        Returns:
            tuple: A tuple containing the Document object and a status message.
        """
        
        try:
            db = get_db()
            filename, id = self.generate_filename(file.filename)

            # Convert file to PDF, OCR just uses PDFs
            converted_file = convert_docx_or_pptx_to_pdf(file)

            # Save PDF temporarly on shared volume for give OCR service access to the file
            path = "shared_data/" + username + "_" + filename 
            with open(path, "w") as file:
                file.write(converted_file)
            fileid = await db.upload_pdf(converted_file, file.filename, id)

            if fileid is None:
                return None, "Error while saving document in DB"
            
            # Create a new document object with necessary metadata
            new_doc = self.get_new_doc(filename, fileid, file.filename, path)

            # Get all PDF informations (text/images)
            new_doc = await extract_pdf_information_with_ocr(new_doc)

            # TODO: Upload extracted prictures to mongoDB

            # Create embeddings for the document
            embeddings = await self.sim_search.create_embeddings_async(new_doc)

            if embeddings is None:
                logging.error(f"Error creating embeddings: {file.filename} from user {username}")
                return None, "Error creating embeddings"
            
            # Save the embeddings in QDrant
            is_save_successfull = await self.sim_search.save_embedding_async(id, embeddings)
            if not is_save_successfull:
                logging.error(f"Error saving embeddings: {file.filename} from user {username}")
                return None, "Error saving embeddings"

            # Create a summary for the document
            prompt = summary_prompt_builder(new_doc.textList)
            summary = await call_mistral_api_async(prompt)
            new_doc.summary = summary

            if new_doc.summary is None:
                logging.error(f"Error creating summary: {file.filename} from user {username}")
                return None, "Error creating summary"


            # für die Texte werden Embeddings erstellt und in VektorDb gespeichert
            #embeddings = await self.create_text_embedding_async(new_doc)

            # Summary is generated from the text through LLM

            # Save new_doc in the database
            doc_id = await db.add_document_to_user_async(username, new_doc)

            if doc_id is None:
                logging.error(f"Error saving document: {file.filename} from user {username}")
                return None, "Error saving document"
            
            return new_doc, "File uploaded successfully"
        except Exception as e:
            logging.error(f"Error handling document {file.filename} from {username}: {e}")
            return None, e
    
    def generate_filename(self, original_filename):
        """
        Generates a unique filename based on the original filename.

        Args:
            original_filename (str): The original filename of the document.

        Returns:
            tuple: A tuple containing the generated filename and the file hash.
        """

        file_hash = hashlib.sha256(original_filename.encode('utf-8')).hexdigest()
        # Save the file extension
        _, file_extension = os.path.splitext(original_filename)
        return f"{file_hash}{file_extension}", file_hash

    async def save_document_local_async(self, file, filename):
        """
        Saves the document locally asynchronously.

        Args:
            file: The file object to be saved.
            filename (str): The name of the file to be saved.

        Returns:
            str: The file path where the document is saved, or None if the file already exists.
        """
        
        filepath = os.path.join(self.local_file_path, filename)
        
        if os.path.exists(filepath):
            return None
        
        loop = asyncio.get_event_loop()
        content = await loop.run_in_executor(None, file.read)  
        
        async with aiofiles.open(filepath, 'wb') as out_file:
            await out_file.write(content) 
        
        return filepath
    
    def get_new_doc(self, name: str, fileId: str, original_name: str, path: str):
        """
        Creates a new Document object with the provided metadata.

        Args:
            name (str): The unique name of the document.
            path (str): The file path of the document.
            original_name (str): The original name of the document.

        Returns:
            Document: The created Document object.
        """
        
        return Document(
            id = str(ObjectId()),
            doc_id=name,
            name = original_name,
            timestamp = datetime.now(),
            doclink = str(fileId),
            summary = "",
            imgList = [],
            textList = [],
            path = path
        )
    
    async def fetch_embedding_async(self, to_embed: str):
        async with aiohttp.ClientSession() as session:
            async with session.post(self.tei_url, json={"inputs": to_embed}) as response:
                if response.status == 200:
                    return await response.json().get("embedding")
                return None
    
    async def create_text_embedding_async(self, doc: Document):
        tasks = []
        for chunk in doc.textList:
            tasks.append(self.fetch_embedding_async(doc.id, chunk.text))
        
        embeddings = await asyncio.gather(*tasks)
        
        return embeddings
    
    async def save_embedding_async(self, doc_id: str, embedding: str):
        # Speichere das Embedding in der VektorDb
        pass

        
    
