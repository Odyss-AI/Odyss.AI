from quart import request, jsonify
from app.routes import main
from bson import json_util
from app.models.user import User
from app.models.chat import Chat
from app.utils.db import get_db

@main.route('/v1/user/add', methods=['POST'])
async def add_user():
    try:
        db = get_db()

        data = await request.get_json()
        username = data.get('username')

        if not username:
            return jsonify({"error": "No username was provided"}), 400

        user = await db.create_user_async(username)
        res = {
            "user": user, 
            "chats": []
        }

        if user:
            return json_util.dumps(res), 201
        else:
            return jsonify({"error": "User exists already"}), 409
    except Exception as e:
        return jsonify({"error": f"Error while adding user: {e}"}), 500

@main.route('/v1/user/get', methods=['GET'])
async def get_user():
    try:
        db = get_db()
        username = request.args.get('username')

        user = await db.get_user_async(username)
        chats = await db.get_chats_by_user_async(username)
        res = {
            "user": user, 
            "chats": chats
        }

        if user:
            return json_util.dumps(res), 200
        else:
            return jsonify({"error": "User was not found"}), 404
    except Exception as e:
        return jsonify({"error": f"Error while getting user: {e}"}), 500
    
@main.route('/v1/user/chat/get', methods=['GET'])
async def get_chats():
    try:
        db = get_db()
        username = request.args.get('username')

        chats = await db.get_chats_by_user_async(username)
        if chats:
            return jsonify({"message": "One ore more chats were found", "chats": [chat.model_dump(by_alias=True) for chat in chats]}), 200
        return jsonify({"error": "Chat not found"}), 404
    except Exception as e:
        return jsonify({"error": f"Error while getting chat: {e}"}), 500

@main.route('/v1/user/chat/add', methods=['POST'])
async def add_chat():
    try:
        db = get_db()

        data = await request.get_json()
        username = data.get('username')
        docs = data.get('docs')
        chat_name = data.get('name')

        if not username:
            return jsonify({"error": "No username was provided"}), 400

        chat = await db.create_chat_async(username, chat_name, docs)
        if chat:
            return jsonify(chat.model_dump(by_alias=True)), 201
        return jsonify({"error": "Error while adding chat"}), 400
    except Exception as e:
        return jsonify({"error": f"Error while adding chat {str(e)}"}), 500
    
@main.route('/v1/user/chat/delete', methods=['DELETE'])
async def delete_chat():
    try:
        db = get_db()
        chat_id = request.args.get('chatid')

        chat = await db.delete_chat_async(chat_id)

        if chat:
            return jsonify({"message": "Chat delted"}), 200
    
        return jsonify({"error": "Chat not found"}), 404
    except Exception as e:
        return jsonify({"error": f"Error while deleting chat {str(e)}"}), 500