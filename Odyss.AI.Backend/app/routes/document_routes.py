import os
from quart import Quart, request, jsonify
from app.utils.ml_connection import allowed_file
from app.routes import main
from app.utils.db import get_db
from app.services.document_manager import DocumentManager
from app.config import config

# Document Manager initialisieren
doc_manager = DocumentManager()

# Dokumente des Benutzers abrufen
@main.route('/v1/doc/get', methods=['GET'])
async def get_documents():
    try:
        db = get_db()
        username = request.args.get('username')

        # Dokumente des Benutzers abrufen
        documents = await db.get_documents_of_user_async(username)
        if documents is None:
                    return jsonify({"error": "Benutzer nicht gefunden"}), 404
        
        res = [
            {
                "mongo_file_id": doc.mongo_file_id,
                "doc_id": doc.doc_id,
                "summary": doc.summary,
                "name": doc.name
            }
            for doc in documents
        ]

        return jsonify(res), 200

    except Exception as e:
        return jsonify({"error": f"Fehler beim Abrufen der Dokumente: {e}"}), 500

# Dokument hochladen
@main.route('/v1/doc/upload', methods=['POST'])
async def upload_document():
    try:
        db = get_db()
        username = request.args.get('username')
        chat_id = request.args.get('chatId')
        file_data = await request.files  # PDF-Datei direkt aus dem Request-Body

        if not username:
            return jsonify({"error": "Username ist erforderlich"}), 400
        
        # Prüfen, ob der Benutzername in der Datenbank vorhanden ist
        if await db.get_user_async(username) is None:
            return jsonify({"error": "Benutzer nicht gefunden"}), 400

        for key, f in file_data.items():
            if f and allowed_file(f.filename):
                new_doc, msg = await doc_manager.handle_document_async(f, username, chat_id)
                if new_doc is None:
                    return jsonify({'error': str(msg)}), 400

                return jsonify({'message': str(msg), 'file': new_doc.model_dump(by_alias=True)}), 200
            else:
                return jsonify({'error': 'File type not allowed'}), 400

    except Exception as e:
        return jsonify({"error": f"Fehler beim Hinzufügen des Dokuments: {str(e)}"}), 500
    
@main.route('/v1/doc/upload/filepath', methods=['GET'])
async def upload_document_path():
    try:
        db = get_db()
        filepath = request.args.get('filepath')

        id = await db.upload_pdf(filepath)

        if id:
            file = await db.get_files(id)

        return jsonify({"message": "Dokument erfolgreich hochgeladen", "id": id}), 200

    except Exception as e:
        return jsonify({"error": f"Fehler beim Hinzufügen des Dokuments: {str(e)}"}), 500

