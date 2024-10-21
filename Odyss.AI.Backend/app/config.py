import os

from dotenv import load_dotenv

load_dotenv()

def get_ocr_url(base: str):
        url_selection = os.getenv("URL_SELECTION", "default")

        if url_selection == "nougat":
            return base + "ocr/nougatocr"
        elif url_selection == "paddle":
            return "http://ocr:5050/ocr/paddleocr" 
        else url_selection == "prod":
            return "http://ocr:5050/ocr/tesseractocr"

class Config:
    MONGODB_CONNECTION_STRING = os.getenv("MONGODB_CONNECTION_STRING")
    LOCAL_DOC_PATH = os.getenv("LOCAL_DOC_PATH")
    TEI_URL = os.getenv("TEI_URL")
    OCR_URL = get_ocr_url("http://ocr:5050/")
    QDRANT_HOST= os.getenv("QDRANT_HOST")
    QDRANT_PORT = os.getenv("QDRANT_PORT")
    MISTRAL_KEY = os.getenv("MISTRAL_KEY")
    DEBUG = False
    TESTING = False

class DevConfig:
    MONGODB_CONNECTION_STRING = os.getenv("MONGODB_CONNECTION_STRING")
    LOCAL_DOC_PATH = os.getenv("LOCAL_DOC_PATH")
    TEI_URL = os.getenv("TEI_URL")
    QDRANT_HOST= os.getenv("QDRANT_HOST")
    QDRANT_PORT = os.getenv("QDRANT_PORT")
    MISTRAL_KEY = os.getenv("MISTRAL_KEY")
    DEBUG = True

class ProdConfig:
    MONGODB_CONNECTION_STRING = os.getenv("MONGODB_CONNECTION_STRING")
    LOCAL_DOC_PATH = os.getenv("LOCAL_DOC_PATH")
    TEI_URL = os.getenv("TEI_URL")
    QDRANT_HOST= os.getenv("QDRANT_HOST")
    QDRANT_PORT = os.getenv("QDRANT_PORT")
    MISTRAL_KEY = os.getenv("MISTRAL_KEY")
    OCR_URL = get_ocr_url("http://ocr:5050/")
    DEBUG = False
    TESTING = False
