import aiohttp
import asyncio

from app.config import config
from app.models.user import Document

async def extract_pdf_information_with_ocr(doc: Document):
    async with aiohttp.ClientSession() as session:
        async with session.post(config.ocr_endpoint, json=doc.model_dump(by_alias=True)) as response:
            response_data = await response.json()
            return Document(**response_data)