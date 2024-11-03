import json
import datetime 

from quart import Quart, websocket, jsonify
from app.routes import main
from app.utils.db import get_db
from app.models.chat import Chat, Message
from app.services.message_manager import MessageManager
from bson.objectid import ObjectId
from app.utils.converters import convert_datetime, convert_to_model

msg_manager = MessageManager()

@main.route('/', methods=['GET'])
def home():
    return "<h1>Hallo bei Odyss.AI</h1>"

@main.websocket('/chat')
async def chat():
    db = get_db()
    
    while True:
        message = await websocket.receive()
        data = json.loads(message)
        
        username = data.get('username')
        msg = data.get('message')
        chat_id = data.get('chatId')
        model = data.get('model')

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
            timestamp=datetime.datetime.now(),
            selected_model=model
        )

        llm_res, chunks, chat_id = await msg_manager.handle_message_async(msg, username, chat_id)
        
        if llm_res is None:
            await websocket.send(json.dumps({"error": chunks}))
            continue

        llm_res_dict = llm_res.model_dump(by_alias=True)
        llm_res_dict = convert_datetime(llm_res_dict)

        res = {
            "chatId": chat_id,
            "message": llm_res_dict,
            "chunks": [chunk.model_dump(by_alias=True) if hasattr(chunk, 'model_dump') else convert_to_model(chunk).model_dump(by_alias=True) for chunk in chunks]
        }

        await websocket.send(json.dumps(res))
