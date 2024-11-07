from quart import request, jsonify
from app.routes import main
from bson import json_util
from app.models.user import User
from app.models.chat import Chat
from app.utils.db import get_db  # Importiere den globalen db_service und die Initialisierungsfunktion

# Benutzer hinzufügen
@main.route('/v1/user/add', methods=['POST'])
async def add_user():
    try:
        db = get_db()

        data = await request.get_json()  # JSON-Daten aus der Anfrage asynchron lesen
        username = data.get('username')

        if not username:
            return jsonify({"error": "Username ist erforderlich"}), 400

        # Benutzer erstellen
        user = await db.create_user_async(username)
        res = {
            "user": user, 
            "chats": []
        }

        if user:
            return json_util.dumps(res), 201
        else:
            return jsonify({"error": "Benutzername existiert bereits"}), 409
    except Exception as e:
        return jsonify({"error": f"Fehler beim Hinzufügen des Benutzers: {e}"}), 500

# Benutzer abrufen
@main.route('/v1/user/get', methods=['GET'])
async def get_user():
    try:
        db = get_db()
        username = request.args.get('username')

        # Benutzer abrufen
        user = await db.get_user_async(username)
        chats = await db.get_chats_by_user_async(username)
        res = {
            "user": user, 
            "chats": chats
        }

        if user:
            return json_util.dumps(res), 200
        else:
            return jsonify({"error": "Benutzer nicht gefunden"}), 404
    except Exception as e:
        return jsonify({"error": f"Fehler beim Abrufen des Benutzers: {e}"}), 500
    
@main.route('/v1/user/chat/get', methods=['GET'])
async def get_chats():
    try:
        db = get_db()
        username = request.args.get('username')

        # Chats abrufen
        chats = await db.get_chats_by_user_async(username)
        if chats:
            return jsonify({"message": "Chats gefunden", "chats": [chat.model_dump(by_alias=True) for chat in chats]}), 200
        return jsonify({"error": "Chats nicht gefunden"}), 404
    except Exception as e:
        return jsonify({"error": f"Fehler beim Abrufen der Chats: {e}"}), 500

# Chat hinzufügen
@main.route('/v1/user/chat/add', methods=['POST'])
async def add_chat():
    try:
        db = get_db()

        data = await request.get_json()
        username = data.get('username')
        docs = data.get('docs')
        chat_name = data.get('name')

        if not username:
            return jsonify({"error": "Username ist erforderlich"}), 400

        # Chat hinzufügen
        chat = await db.create_chat_async(username, chat_name, docs)
        if chat:
            return jsonify(chat.model_dump(by_alias=True)), 201
        return jsonify({"error": "Fehler beim Hinzufügen des Chats"}), 400
    except Exception as e:
        return jsonify({"error": f"Fehler beim Hinzufügen des Chats: {e}"}), 500
    
# Delete Chats
@main.route('/v1/user/chat/delete', methods=['DELETE'])
async def delete_chat():
    try:
        db = get_db()
        chat_id = request.args.get('chatid')

        # Chat löschen
        chat = await db.delete_chat_async(chat_id)
        if chat:
            return jsonify({"message": "Chat gelöscht"}), 200
        return jsonify({"error": "Chat nicht gefunden"}), 404
    except Exception as e:
        return jsonify({"error": f"Fehler beim Löschen des Chats: {e}"}), 500