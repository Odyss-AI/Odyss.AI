import os
from quart import Quart, request, jsonify
from app.utils.ml_connection import allowed_file
from app.routes import main
from app.utils.db import get_db
from app.services.document_manager import DocumentManager
from app.config import config

doc_manager = DocumentManager()

@main.route('/v1/doc/get', methods=['GET'])
async def get_documents():
    try:
        db = get_db()
        username = request.args.get('username')

        documents = await db.get_documents_of_user_async(username)
        if documents is None:
                    return jsonify({"error": "User not found"}), 404
        
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
        return jsonify({"error": f"Error while getting document: {e}"}), 500

@main.route('/v1/doc/upload', methods=['POST'])
async def upload_document():
    try:
        db = get_db()
        username = request.args.get('username')
        chat_id = request.args.get('chatId')
        file_data = await request.files 

        if not username:
            return jsonify({"error": "Username is requiered"}), 400
        
        if await db.get_user_async(username) is None:
            return jsonify({"error": "User was not found"}), 400

        for key, f in file_data.items():
            if f and allowed_file(f.filename):
                new_doc, msg = await doc_manager.handle_document_async(f, username, chat_id)
                if new_doc is None:
                    return jsonify({'error': str(msg)}), 400

                return jsonify({'message': str(msg), 'file': new_doc.model_dump(by_alias=True)}), 200
            else:
                return jsonify({'error': 'File type not allowed'}), 400

    except Exception as e:
        return jsonify({"error": f"Error while adding document: {str(e)}"}), 500
    
@main.route('/v1/doc/upload/filepath', methods=['GET'])
async def upload_document_path():
    try:
        db = get_db()
        filepath = request.args.get('filepath')

        id = await db.upload_pdf(filepath)

        if id:
            file = await db.get_files(id)

        return jsonify({"message": "Document was succesful uploaded", "id": id}), 200

    except Exception as e:
        return jsonify({"error": f"Error while adding document: {str(e)}"}), 500

