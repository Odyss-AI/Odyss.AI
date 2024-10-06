# ocr_routes.py
from quart import Blueprint, request, jsonify
from app.utils.db import get_db
from app.models import Document, Image, TextChunk
from .ocr_service import OCRProcessor  # Importieren der OCRProcessor-Klasse

ocr_bp = Blueprint('ocr', __name__)  # Erstellen eines Blueprints für die OCR-Routen
ocr_processor = OCRProcessor()  # Instanz der OCRProcessor-Klasse erstellen

@ocr_bp.route('/ocr/upload', methods=['POST'])
async def upload_document():
    try:
        db = get_db()
        username = request.args.get('username')
        file_data = await request.files

        if not username:
            return jsonify({"error": "Username ist erforderlich"}), 400

        if await db.get_user_async(username) is None:
            return jsonify({"error": "Benutzer nicht gefunden"}), 404

        for key, f in file_data.items():
            if f:
                # OCR-Verarbeitung durchführen
                ocr_result = await ocr_processor.process_document(f)

                # Hier sollten Sie die Logik hinzufügen, um das OCR-Ergebnis in Ihre Dokumentklasse zu speichern

                return jsonify({'message': 'Dokument erfolgreich hochgeladen', 'ocr_result': ocr_result}), 200
            else:
                return jsonify({'error': 'Dateityp nicht erlaubt'}), 400

    except Exception as e:
        return jsonify({"error": f"Fehler beim Hinzufügen des Dokuments: {str(e)}"}), 500
