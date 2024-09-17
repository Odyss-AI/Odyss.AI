import os
from quart import Quart, request, jsonify
from app.utils.helpers import allowed_file
from app.routes import main
from app.utils.db import get_db
from app.services.document_manager import DocumentManager
from app.config import Config

# Document Manager initialisieren
doc_manager = DocumentManager()

# Dokumente des Benutzers abrufen
@main.route('/docs/getdocs', methods=['GET'])
async def get_documents():
    try:
        db = get_db()
        username = request.args.get('username')

        # Dokumente des Benutzers abrufen
        documents = await db.get_documents_of_user_async(username)
        if documents is not None:
            return jsonify({"message": "Dokumente gefunden", "documents": [doc.model_dump(by_alias=True) for doc in documents]}), 200
        return jsonify({"error": "Benutzer nicht gefunden"}), 404
    except Exception as e:
        return jsonify({"error": f"Fehler beim Abrufen der Dokumente: {e}"}), 500

# Dokument hochladen
@main.route('/docs/upload', methods=['POST'])
async def upload_document():
    try:
        username = request.args.get('username')
        file_data = await request.files  # PDF-Datei direkt aus dem Request-Body

        if not username:
            return jsonify({"error": "Username ist erforderlich"}), 400

        for key, f in file_data.items():
            if f and allowed_file(f.filename):
                new_doc, msg = await doc_manager.handle_document(f, username, is_local=True)
                if new_doc is None:
                    return jsonify({'error': str(msg)}), 400

                return jsonify({'message': str(msg), 'file': new_doc.model_dump(by_alias=True)}), 200
            else:
                return jsonify({'error': 'File type not allowed'}), 400

    except Exception as e:
        return jsonify({"error": f"Fehler beim Hinzufügen des Dokuments: {str(e)}"}), 500

