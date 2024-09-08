from flask import request, jsonify
from app.routes import main
from app.db import get_db

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
    
@main.route('/docs/adddoc', methods=['POST'])
def add_document():
    try:
        db = get_db()
        data = request.get_json()
        username = data.get('username')
        document_data = data.get('documents')
        
        if not username:
            return jsonify({"error": "Username ist erforderlich"}), 400
        if not document_data:
            return jsonify({"error": "Dokumentdaten sind erforderlich"}), 400
        
        # Hier Onedrive Service einbinden, um Dokument hochzuladen und URL in DB speichern

        # Dokument hinzufügen
        for doc in document_data:
            document_id = db.add_document_to_user(username, doc)
            if not document_id:
                return jsonify({"error": "Fehler beim Hinzufügen des Dokuments"}), 500
        
        if document_id:
            return jsonify({"message": "Dokument erfolgreich hinzugefügt", "document_id": document_id}), 201
        return jsonify({"error": "Benutzer nicht gefunden"}), 404
    except Exception as e:
        return jsonify({"error": f"Fehler beim Hinzufügen des Dokuments: {e}"}), 500