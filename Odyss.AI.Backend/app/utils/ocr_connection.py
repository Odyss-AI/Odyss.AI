import request
import asyncio

from app.config import Config

async def extract_pdf_information_with_ocr(doc: Document):
    response = requests.post(Config.OCR_URL, json.model_dump(doc))
    return Document(**response)