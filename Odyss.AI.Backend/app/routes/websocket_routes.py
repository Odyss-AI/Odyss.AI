import json
import datetime 

from quart import Quart, websocket, jsonify
from app.routes import main
from app.utils.db import get_db
from app.models.chat import Chat, Message
from app.services.message_manager import MessageManager
from bson.objectid import ObjectId


db = get_db()
msg_manager = MessageManager()

@main.route('/', methods=['GET'])
def home():
    return "<h1>Hallo bei Odyss.AI</h1>"

@main.websocket('/chat')
async def chat():
    while True:
        message = await websocket.receive()
        data = json.loads(message)
        
        username = data.get('username')
        msg = data.get('message')
        chat_id = data.get('chat_id')

        if not chat_id:
            chat_id = None
        
        if not username:
            await websocket.send(json.dumps({"error": "Nicht authentifiziert"}))
            continue
        else:
            user = await db.get_user_async(username)
            if user is None:
                await websocket.send(json.dumps({"error": "Benutzer nicht gefunden"}))
                continue

        msg = Message(
            id=str(ObjectId()),
            is_user=True,
            content=msg,
            timestamp=datetime.datetime.now()
        )

        llm_res = await msg_manager.handle_message(msg, username, chat_id)
        
        await websocket.send(json.dumps(str(llm_res)))

