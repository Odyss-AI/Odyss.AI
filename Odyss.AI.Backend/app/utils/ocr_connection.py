import request
import asyncio

from 

asnyc def extract_pdf_information_nougatocr(doc: Document):
    ocr_url = "http://ocr:5050/ocr/nougatocr"

    response = requests.post(ocr_url, json.model_dump(doc))
    print(response.json())

asnyc def extract_pdf_information_paddleocr(doc: Document)):
    ocr_url = "http://ocr:5050/ocr/paddleocr" 

    response = requests.post(ocr_url, json=data)
    print(response.json())

asnyc def extract_pdf_information_tesseractocr(doc: Document)):
    ocr_url = "http://ocr:5050/ocr/tesseractocr"

    response = requests.post(ocr_url, json=data)
    print(response.json())