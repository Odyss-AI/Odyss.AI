import aiohttp
import asyncio

from app.config import Config
from app.models.user import Document

async def extract_pdf_information_with_ocr(doc: Document):
    async with aiohttp.ClientSession() as session:
        async with session.post(Config.OCR_URL, json=doc.model_dump(by_alias=True)) as response:
            response_data = await response.json()
            return Document(**response_data)