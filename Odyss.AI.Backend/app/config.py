import os

from dotenv import load_dotenv

load_dotenv()

def get_ocr_url(base: str):
        url_selection = os.getenv("OCR", "default")

        if url_selection == "nougat":
            return base + "ocr/nougatocr"
        elif url_selection == "paddle":
            return "http://ocr:5050/ocr/paddleocr" 
        elif url_selection == "prod":
            return "http://ocr:5050/ocr/tesseractocr"

class Config:
    MONGODB_CONNECTION_STRING = os.getenv("MONGODB_CONNECTION_STRING")
    TEI_URL = os.getenv("TEI_URL")
    OCR_URL = get_ocr_url(os.getenv("BASE_DOC_PATH"))
    QDRANT_HOST= os.getenv("QDRANT_HOST")
    QDRANT_PORT = os.getenv("QDRANT_PORT")
    MISTRAL_KEY = os.getenv("MISTRAL_KEY")
