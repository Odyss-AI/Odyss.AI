import aiohttp
import logging
from datetime import datetime

from app.config import config
from app.models.user import Document

async def extract_pdf_information_with_ocr(doc: Document):
    try:
        async with aiohttp.ClientSession() as session:
            payload = doc.model_dump_json()
            headers = {'Content-Type': 'application/json'}
            async with session.post(config.ocr_endpoint, data=payload, headers=headers) as response:
                response_data = await response.json()
                
                # Konvertiere das Datum in das ISO 8601-Format
                if 'timestamp' in response_data:
                    response_data['timestamp'] = datetime.strptime(
                        response_data['timestamp'], '%a, %d %b %Y %H:%M:%S %Z'
                    ).isoformat()
                
                return Document(**response_data)
    except Exception as e:
        logging.error(f"Error extracting information while using ocr: {e}")
        return None