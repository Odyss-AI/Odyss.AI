import aiohttp
import asyncio
import logging
import json

from app.config import config
from app.models.user import Document

async def extract_pdf_information_with_ocr(doc: Document):
    try:
        async with aiohttp.ClientSession() as session:
            payload = doc.model_dump_json()
            async with session.post(config.get_ocr_endpoint(), data=payload) as response:
                response_data = await response.json()
                return Document(**response_data)
    except Exception as e:
        logging.error(f"Error extracting information while using ocr: {e}")
        return None