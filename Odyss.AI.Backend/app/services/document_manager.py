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
from app.utils.pdfconverter import save_and_convert_file

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
            filename, id = self.generate_filename(file.filename)

            # Convert file to PDF, OCR just uses PDFs
            converted_file = save_and_convert_file(file, id)

            # Save PDF temporarly on shared volume for give OCR service access to the file
            # path = self.get_temp_path(username, filename)
            # fileid = await self.save_file(converted_file, path, db, id)
            # if fileid is None:
            #     logging.error(f"Error creating embeddings: {file.filename} from user {username}")
            #     return None, "Error while saving document in DB"

            # Get all PDF informations (text/images)
            # new_doc = await extract_pdf_information_with_ocr(self.get_new_doc(filename, fileid, file.filename, path))
            # if new_doc is None:
            #     logging.error(f"Error extracting information: {file.filename} from user {username}")
            #     return "Error extracting information while using ocr"
            
            # TODO: Upload extracted prictures to mongoDB

            # Create embeddings for the document
            # embeddings = await self.sim_search.create_embeddings_async(new_doc)
            # if embeddings is None:
            #     logging.error(f"Error creating embeddings: {file.filename} from user {username}")
            #     return None, "Error creating embeddings"
            
            # # Save the embeddings in QDrant
            # is_save_successfull = await self.sim_search.save_embedding_async(id, embeddings)
            # if not is_save_successfull:
            #     logging.error(f"Error saving embeddings: {file.filename} from user {username}")
            #     return None, "Error saving embeddings"

            # # Create a summary for the document
            # prompt = summary_prompt_builder(new_doc.textList)
            # new_doc.summary = await call_mistral_api_async(prompt)
            # if new_doc.summary is None:
            #     logging.error(f"Error creating summary: {file.filename} from user {username}")
            #     return None, "Error creating summary"

            # # Save new_doc in the database
            # doc_id = await db.add_document_to_user_async(username, new_doc)
            # if doc_id is None:
            #     logging.error(f"Error saving document: {file.filename} from user {username}")
            #     return None, "Error saving document"
            
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
        _, file_extension = os.path.splitext(original_filename)
        return f"{file_hash}{file_extension}", file_hash
    
    def get_temp_path(self, username, filename):
        return "shared_data/" + username + "_" + filename 
    
    async def save_file(self, converted_file, path, db, id):
        with open(path, "w") as file:
            file.write(converted_file)
        fileid = await db.upload_pdf(converted_file, file.filename, id)
        return fileid
    
    def get_new_doc(self, name: str, fileId: str, original_name: str, path: str):
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
