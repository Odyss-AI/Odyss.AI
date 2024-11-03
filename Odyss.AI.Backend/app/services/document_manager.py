import os
import aiofiles
import hashlib
import aiohttp
import asyncio
import uuid
import logging

from bson import ObjectId

from app.config import config
from datetime import datetime
from app.models.user import Document
from app.utils.test_data_provider import get_test_document
from app.utils.db import get_db
from app.utils.ml_connection import query_mixtral_async
from app.utils.ocr_connection import extract_pdf_information_with_ocr
from app.utils.prompts import summary_prompt_builder
from app.services.sim_search_service import SimailaritySearchService
from app.utils.pdf_converter import save_and_convert_file

class DocumentManager:
    """
    A class to manage document handling, including saving, processing, and storing documents.
    """

    def __init__(self):
        # self.tei_url = Config.TEI_URL + "/embed"
        self.sim_search = SimailaritySearchService()

    async def handle_document_async(self, file, username, is_local = True):
        """
        Handles the document upload, processing, and storage asynchronously. Refer software architecture pattern Integration Operation Segregation Principle (IOSP)

        Args:
            file: The file object to be processed.
            username (str): The username of the user uploading the document.
            is_local (bool, optional): Flag indicating if the file should be saved locally. Defaults to True.

        Returns:
            tuple: A tuple containing the Document object and a status message.
        """
        
        try:
            db = get_db()
            # Generate a unique name for the document
            hash_doc, hash = self.generate_filename(file.filename)

            # Convert file to PDF, OCR just uses PDFs
            converted_file_path, converted_file = await save_and_convert_file(file, hash_doc, db)
            if self.handle_error(converted_file_path is None, "Error converting file", file, username):
                return None, "Error converting file"

            # Upload the PDF to MongoDB and get the file objectID back
            mongo_file_id = await db.upload_pdf_async(converted_file, file.filename, hash, username)
            if self.handle_error(mongo_file_id is None, "Error uploading file on MongoDB", file, username):
                return None, "Error uploading file on MongoDB"

            # Get all PDF informations (text/images)
            new_doc = self.get_new_doc(str(mongo_file_id), hash, file.filename, converted_file_path)
            new_doc = await extract_pdf_information_with_ocr(new_doc)
            if self.handle_error(new_doc is None, "Error extracting information while using ocr", file, username):
                return None, "Error extracting information while using ocr"

            # TODO: Upload extracted pictures to mongoDB
            
            # TODO: Tag Images

            # Create embeddings for the document
            embeddings = await self.sim_search.create_embeddings_async(new_doc)
            if self.handle_error(embeddings is None, "Error creating embeddings", file, username):
                return None, "Error creating embeddings"

            # Save the embeddings in QDrant
            is_save_successfull = await self.sim_search.save_embedding_async(id, embeddings)
            if self.handle_error(not is_save_successfull, "Error saving embeddings", file, username):
                return None, "Error saving embeddings"

            # Create a summary for the document
            prompt = summary_prompt_builder(new_doc.textList)
            new_doc.summary = await query_mixtral_async(prompt)
            if self.handle_error(new_doc.summary is None, "Error creating summary", file, username):
                return None, "Error creating summary"

            # Save new_doc in the database
            doc_id = await db.add_document_to_user_async(username, new_doc)
            if self.handle_error(doc_id is None, "Error saving document", file, username):
                return None, "Error saving document"

            return new_doc, "File uploaded successfully"
        except Exception as e:
            logging.error(f"Error handling document {file.filename} from {username}: {str(e)}")
            return None, str(e)
    
    def generate_filename(self, original_filename):
        file_hash = hashlib.sha256(original_filename.encode('utf-8')).hexdigest()
        _, file_extension = os.path.splitext(original_filename)
        return f"{file_hash}{file_extension}", file_hash
    
    def get_new_doc(self, mongo_obj_id: str, hash: str, original_name: str, path: str):
        return Document(
            id = str(ObjectId()),
            doc_id = hash,
            mongo_file_id = mongo_obj_id,
            name = original_name,
            timestamp = datetime.now(),
            summary = "",
            imgList = [],
            textList = [],
            path = path
        )
    
    def handle_error(self, condition, error_message, file, username):
        if condition:
            logging.error(f"{error_message}: {file.filename} from user {username}")
            return None, error_message
        return condition
