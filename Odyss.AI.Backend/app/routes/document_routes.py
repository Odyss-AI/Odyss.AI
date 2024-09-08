from flask import request, jsonify
from app.utils.helpers import allowed_file
from app.routes import main
from app.db import get_db
from app.services.document_manager import DocumentManager

UPLOAD_FOLDER = r'C:\Users\efitt\Documents'
doc_manager = DocumentManager(UPLOAD_FOLDER)

@main.route('/docs/getdocs', methods=['GET'])
def get_documents():
    try:
        db = get_db()
        username = request.args.get('username')

        # Dokumente des Benutzers abrufen
        documents = db.get_documents_of_user(username)
        if documents is not None:
            return jsonify({"message": "Dokumente gefunden", "documents": [doc.model_dump(by_alias=True) for doc in documents]}), 200
        return jsonify({"error": "Benutzer nicht gefunden"}), 404
    except Exception as e:
        return jsonify({"error": f"Fehler beim Abrufen der Dokumente: {e}"}), 500

@main.route('/docs/upload', methods=['POST'])
def upload_document():
    try:
        username = request.args.get('username')
        file_data = request.files  # PDF-Datei direkt aus dem Request-Body
        
        if not username:
            return jsonify({"error": "Username ist erforderlich"}), 400
        
        for key, f in file_data.items():
            if f and allowed_file(f.filename):
                new_doc, msg = doc_manager.handle_document(f, username, is_local=True)
                if new_doc is None:
                    return jsonify({'error': msg}), 400
                
                return jsonify({'message': msg, 'file': new_doc.model_dump(by_alias=True)}), 200
            else:
                return jsonify({'error': 'File type not allowed'}), 400

    except Exception as e:
        return jsonify({"error": f"Fehler beim Hinzufügen des Dokuments: {e}"}), 500