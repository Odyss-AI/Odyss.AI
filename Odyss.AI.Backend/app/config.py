import os
from dotenv import load_dotenv

class Config:
    def __init__(self, env_file=None):
        # Lade die spezifische .env-Datei oder die Standard-.env-Datei
        if env_file:
            load_dotenv(env_file)
        else:
            load_dotenv()  # Lädt .env standardmäßig

        # Allgemeine Konfigurationen
        self.environment = os.getenv("ENVIRONMENT", "linux")

        # MongoDB Konfiguration
        self.mongodb_connection_string = os.getenv("MONGODB_CONNECTION_STRING")

        # Lokale Dokumentpfade und URLs
        self.local_doc_path = os.getenv("LOCAL_DOC_PATH")
        self.tei_url = os.getenv("TEI_URL")

        # Qdrant Konfiguration
        self.qdrant_host = os.getenv("QDRANT_HOST")
        self.qdrant_port = os.getenv("QDRANT_PORT")

        # Mistral Key
        self.mistral_api_base = os.getenv("MISTRAL_API_BASE")

        # OCR Endpunkte
        self.service_endpoint_selection = os.getenv("SERVICE_ENDPOINT_SELECTION", "TESERACT")
        self.ocr_endpoint = self.get_ocr_endpoint()

        #Image Tagger Endpunkt
        self.image_tagger = os.getenv("IMAGE_TAGGER")

        #OpenAI API Key
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.openai_api_base = os.getenv("OPENAI_API_BASE")

    def get_ocr_endpoint(self):
        """Wählt den OCR-Service-Endpunkt basierend auf der Auswahl in der .env."""
        selection = self.service_endpoint_selection.upper()
        if selection == "NOUGAT":
            return os.getenv("NOUGAT_OCR")
        elif selection == "PADDLE":
            return os.getenv("PADDLE_OCR")
        elif selection == "TESERACT":
            return os.getenv("TESERACT_OCR")
        else:
            raise ValueError("Ungültiger OCR-Endpunkt gewählt")
        
env_file = f".env.{os.getenv('ENVIRONMENT', 'linux')}"
config = Config(env_file)