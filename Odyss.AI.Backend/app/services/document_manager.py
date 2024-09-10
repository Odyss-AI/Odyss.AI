import os
import hashlib
from datetime import datetime
from app.models.user import Document
from app.services.ocr_service import OCRService

class DocumentManager:

    def __init__(self, file_path):
        self.local_file_path = file_path
        self.ocr_service = OCRService()

    def handle_document(self, file, username, is_local = True):
        filename = self.generate_filename(file.filename)
        try:
            # Save the document either locally or on OneDrive
            filepath = self.save_document_local(file, filename) if is_local else self.save_document_onedrive(file, filename)
            if filepath is None:
                return None, "File already exists"
            
            # Create a new document object with necessary metadata
            new_doc = self.get_new_doc(filename, filepath, file.filename)

            # Send new_doc to OCR, where the text is read out and the images are recognized
            # The object with the text split up and images (here the URLs are stored) comes back
            new_doc = self.ocr_service.extract_text(new_doc)

            # Text gets embedded and stored in the vector database

            # Images get tagged and informations with special LLM are stored in the vector database after embedding

            # Summary is generated from the text through LLM

            # Save new_doc in the database

            return new_doc, "File uploaded successfully"
        except Exception as e:
            return None, e
    
    def generate_filename(self, original_filename):
        # Create a unique filename based on the original filename
        file_hash = hashlib.sha256(original_filename.encode('utf-8')).hexdigest()
        # Save the file extension
        _, file_extension = os.path.splitext(original_filename)
        return f"{file_hash}{file_extension}"

    def save_document_local(self, file, filename):
        filepath = os.path.join(self.local_file_path, filename)
        if os.path.exists(filepath):
            return None
        file.save(filepath)
        return filepath
    
    def get_new_doc(self, name, path, original_name):
        return Document(
            ID = name,
            Name = original_name,
            Timestamp = datetime.now(),
            URL_von_Dokument = path,
            Zusammenfassung = "",
            Bilder = [],
            TextObjekt = []
        )
    
