import os
import hashlib
from datetime import datetime
from app.models.user import Document

class DocumentManager:

    def __init__(self, file_path):
        self.local_file_path = file_path

    def handle_document(self, file, username, is_local = True):
        filename = self.generate_filename(file.filename)
        try:
            filepath = self.save_document_local(file, filename) if is_local else self.save_document_onedrive(file, filename)
            if filepath is None:
                return None, "File already exists"
            
            new_doc = self.get_new_doc(filename, filepath, file.filename)

            # sende new_doc an OCR, dort wird der Text ausgelesen und die Bilder erkannt
            # zurück kommt das Objekt mit den Text aufgesplittet und Bildern (hier die URLs hinterlegt)

            # für die Texte werden Embeddings erstellt und in VektorDb gespeichert

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
    
