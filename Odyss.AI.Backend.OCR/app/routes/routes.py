from app.user import Document
from quart import Quart, request, jsonify
from app.service.nougatocr import OCRNougat
from app.service.paddleocr import OCRPaddle
from app.service.tesseractocr import OCRTesseract
from app.routes import main

@main.route("/ocr/paddleocr", methods=["POST"])
async def paddleocr() : 
    data = await request.json
    doc = Document(**data)
    ocrnougat = OCRPaddle()
    doc = ocrnougat.extract_text(doc)

    return jsonify(doc.model_dump())

@main.route("/ocr/nougatocr", methods=["POST"])
async def nougatocr() : 
    data = await request.json
    doc = Document(**data)
    ocrnougat = OCRNougat()
    doc = ocrnougat.extract_text(doc)

    return jsonify(doc.model_dump())

@main.route("/ocr/tesseractocr", methods=["POST"])
async def tesseractocr() : 
    data = await request.json
    doc = Document(**data)
    ocrtasseract = OCRTesseract()
    doc = ocrnougat.extract_text(doc)

    return jsonify(doc.model_dump())

