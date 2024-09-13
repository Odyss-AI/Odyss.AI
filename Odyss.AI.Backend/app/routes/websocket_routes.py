from quart import Quart, websocket, jsonify
import json
from app.routes import main
from app.utils.db import get_db

db = get_db()

@main.route('/', methods=['GET'])
def home():
    return "<h1>Hallo bei Odyss.AI</h1>"

@main.websocket('/chat')
async def chat():
    while True:
        message = await websocket.receive()
        data = json.loads(message)
        
        username = data.get('username')
        chat_id = data.get('chat_id')
        files = data.get('files')
        
        if not username:
            await websocket.send(json.dumps({"error": "Nicht authentifiziert"}))
            continue
        else:
            user = await db.get_user_async(username)
            if user is None:
                await websocket.send(json.dumps({"error": "Benutzer nicht gefunden"}))
                continue

        # Hier könnte man die Nachricht weiter verarbeiten, z.B. speichern oder an andere Clients senden
        response = {
            "username": username,
            "message": data.get('message'),
            "chat_id": chat_id,
            "files": files
        }
        
        await websocket.send(json.dumps("Hallo, ich bin ein Chatbot!"))

