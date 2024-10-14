import os
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
    ocrpaddle = OCRPaddle()
    doc = ocrpaddle.extract_text(doc)

    return jsonify(doc.model_dump())

@main.route("/ocr/nougatocr", methods=["POST"])
async def nougatocr() : 
    data = await request.json
    doc = Document(**data)
    ocrnougat = OCRNougat()
    doc = ocrnougat.extract_text(doc)

    return jsonify(doc.model_dump())

@main.route("/ocr/tesseractocr", methods=["POST"])
async def tesseractocr():
    # JSON-Daten von der Anfrage abrufen
    data = await request.json
    doc = Document(**data)

    # Den Dateipfad aus der Anfrage abrufen
    document_path = doc.doclink

    # Prüfen, ob der Pfad existiert und auf eine Datei verweist
    if not os.path.exists(document_path):
        return jsonify({"error": "Document not found"}), 404

    # Prüfen, ob es sich um eine Datei handelt
    if not os.path.isfile(document_path):
        return jsonify({"error": "Provided path is not a valid file"}), 400

    # Tesseract OCR verwenden, um Text aus dem Dokument zu extrahieren
    ocrtesseract = OCRTesseract()

    # Hier musst du sicherstellen, dass `extract_text` die Datei vom Dateipfad lesen kann
    try:
        doc = ocrtesseract.extract_text(doc, document_path)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Das fertige Dokument als JSON zurückgeben
    return jsonify(doc.model_dump()), 200
