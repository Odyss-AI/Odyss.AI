import os
import hashlib
import logging
import time

from bson import ObjectId

from datetime import datetime
from app.models.user import Document
from app.utils.db import get_db
from app.utils.ml_connection import query_mixtral_with_ssh_async, query_pixtral_with_ssh_async
from app.utils.ocr_connection import extract_pdf_information_with_ocr
from app.services.sim_search_service import SimailaritySearchService
from app.utils.pdf_converter import save_and_convert_file
from app.utils.batching import create_summary_with_batches
from app.utils.time_logger import TimeLogger

class DocumentManager:
    """
    A class to manage document handling, including saving, processing, and storing documents.
    """

    def __init__(self):
        self.sim_search = SimailaritySearchService()

    async def handle_document_async(self, file, username, chat_id):
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
            time_logger = TimeLogger("Document handling")
            
            hash_doc, hash = self.generate_filename(file.filename)
            converted_file_path, converted_file = await save_and_convert_file(file, hash_doc, db)
            if converted_file is None:
                return None, "Error saving file locally"
            time_logger.exit_func("Save and convert file locally", "Save file in MongoDB")

            mongo_file_id = await db.upload_pdf_async(converted_file, file.filename, hash, username)
            time_logger.exit_func("Save file in MongoDB", "Extract PDF information with OCR")
            
            new_doc = self.get_new_doc(str(mongo_file_id), hash, file.filename, converted_file_path)
            new_doc = await extract_pdf_information_with_ocr(new_doc)
            if new_doc.imgList is not None and len(new_doc.imgList) > 0 and new_doc.textList is not None and len(new_doc.textList) > 0:
                return None, "Document is empty"
            time_logger.exit_func("Extract PDF information with OCR", "Extract image information with Pixtral (or create Embeddings if no pictures in doc)")

            if new_doc.imgList is not None and len(new_doc.imgList) > 0:
                new_doc = await query_mixtral_with_ssh_async(new_doc)
                time_logger.exit_func("Extract image information with Pixtral", "Create embeddings")

            self.delete_local_file(new_doc)
            time_logger.exit_func("Delete local file", "Create embeddings")

            embeddings = await self.sim_search.create_embeddings_async(new_doc)
            if embeddings is None:
                return None, "Error creating embeddings"
            time_logger.exit_func("Create embeddings", "Save embeddings")
            
            is_save_successfull = await self.sim_search.save_embedding_async(hash, embeddings)
            if not is_save_successfull:
                return None, "Error saving embeddings"
            time_logger.exit_func("Save embeddings", "Create summary")

            new_doc.summary = await create_summary_with_batches(new_doc.textList, 1000, 8192)
            if not new_doc.summary:
                return None, "Error creating summary"
            time_logger.exit_func("Create summary", "Upload to MongoDB (user+chat)")
            
            new_doc.mongo_file_id = await db.add_document_to_user_async(username, new_doc)
            time_logger.exit_func(f"Add document {new_doc.doc_id} to user {username}", f"Add document {new_doc.doc_id} to chat {chat_id}")
            
            is_doc_added_to_chat = await db.add_document_to_chat_async(chat_id, hash)
            if not is_doc_added_to_chat:
                return None, "Error adding document to chat"
            time_logger.exit_func(f"Add document {new_doc.doc_id} to chat {username}", "Finishing process")

            time_logger.exit_process()
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

    def delete_local_file(self, new_doc):
        try:
            for img in new_doc.imgList:
                if os.path.exists(img.link):
                    os.remove(img.link)
                    img.link = "Image is successfully evaluated and deleted"
        except Exception as e:
            logging.error(f"Error while deleting image: {e}")
            print(f"Error while deleting image: {str(e)}")
            return None