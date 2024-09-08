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
    
@main.route('/docs/upload/text', methods=['POST'])
def upload_document_plain_text():
    try:
        db = get_db()
        data = request.get_json()
        username = data.get('username')
        document_data = data.get('documents')
        
        if not username:
            return jsonify({"error": "Username ist erforderlich"}), 400
        if not document_data:
            return jsonify({"error": "Dokumentdaten sind erforderlich"}), 400
        
        # Call Doc Manager, um Dokumente zu speichern in Onedrive, Text auslesen, Metadaten extrahieren, usw.

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
    

@main.route('/docs/upload', methods=['POST'])
def upload_document():
    try:
        username = request.args.get('username')
        file_data = request.data  # PDF-Datei direkt aus dem Request-Body
        
        if not username:
            return jsonify({"error": "Username ist erforderlich"}), 400
        if not file_data:
            return jsonify({'error': 'Empty PDF content'}), 400
        
        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        if file and allowed_file(file.filename):

            # Save file on filesystem just for testing
            filepath = doc_manager.save_document_local(file)

            # Call Doc Manager, um Dokumente zu speichern in Onedrive, Text auslesen, Metadaten extrahieren, usw.


            return jsonify({'message': 'File uploaded successfully', 'filepath': filepath}), 200
        else:
            return jsonify({'error': 'File type not allowed'}), 400
        # Call Doc Manager, um Dokumente zu speichern in Onedrive, Text auslesen, Metadaten extrahieren, usw.


    except Exception as e:
        return jsonify({"error": f"Fehler beim Hinzufügen des Dokuments: {e}"}), 500