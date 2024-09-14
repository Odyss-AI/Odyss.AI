import datetime

from app.utils.db import get_db
from app.models.chat import Chat, Message
from app.models.user import TextChunk
from app.utils.helpers import mistral_api
from app.utils.prompts import qna_prompt_builder
from bson.objectid import ObjectId
from app.services.caching import CachingService
from app.services.db_service import MongoDBService
from app.services.sim_search_service import SimailaritySearchService
from bson.objectid import ObjectId

class MessageManager:
    def __init__(self):
        self.cache = CachingService()
        self.sim_search = SimailaritySearchService()

    async def handle_message(self, message: Message, user: str, chat_id: str = None):
        db = get_db()

        # Lade den Chat aus der Datenbank oder dem Cache
        chat = await self.get_chat(db, message, user, chat_id)

        # Lade die Dokumente des Benutzers aus der Datenbank
        chat = await self.get_docs(db, user, chat)

        # Suche in der Vaktordatenbank nach ähnlichen Textabschnitten, filtere vorher nach den zu durchsuchenden Dokumenten
        # Mache das nur wenn es Dokumente gibt, die durchsucht werden sollen
        sim_chunks = await self.sim_search.search_similar_documents(chat.doc_ids, message.content)
        docs = await db.get_documents_of_user_async(user)
        chunks = self.get_chunks_from_docs(docs, sim_chunks)

        # Schicke eine Liste der ähnlichen Textabschnitte an das LLM + die Frage
        prompt = qna_prompt_builder(chunks, message.content)
        answer = await mistral_api(prompt)

        # Die Antwort des LLM wird in die Datenbank geschrieben
        bot_msg = await self.write_bot_msg(chat, answer)

        # Die Antwort wird an den Benutzer zurückgegeben
        return bot_msg

    async def get_chat(self, db: MongoDBService, message: Message, user: str, chat_id: str = None):
        # Checke im Cache, ob der Chat dort bereits geladen ist, wenn nicht, lade den Chat aus der Datenbank
        # Checke ob dieser Chat bereits existiert, wenn nicht, erstelle einen neuen Chat
        if chat_id is None:
            chat = await db.create_chat_async(user, message)
            # await self.cache.set(chat.id, chat)
            return chat
        
        # chat = await Chat(self.cache.get(chat_id))
        chat = None
        if not chat:
            chat = Chat(await self.db.chats.find_one({"_id": ObjectId(chat_id)}))
            if chat:
                chat.messages.append(message)
                # await self.caching_service.set(chat_id, chat)
                await self.db.add_message_to_chat(chat.id, message)
        else:
            chat.messages.append(message)
            # self.cache.update(chat_id, chat)
            await self.db.add_message_to_chat(chat.id, message)

        return chat
    
    async def get_docs(self, db:MongoDBService, user: str, chat: Chat, doc_ids: list = None):
        if doc_ids and set(chat.doc_ids) == set(doc_ids):
            return chat
    
        # Wenn es eine Liste mit Dokumenten IDs übergeben wurde, 
        # prüfe ob diese Dokumente existieren und extrahiere diese aus der gezogenen Dokumentenliste
        documents = await db.get_documents_of_user_async(user)
        if(chat.doc_ids and len(chat.doc_ids) > 0):
            chat.doc_ids = [
                doc for doc in chat.doc_ids 
                if doc in [d.doc_id for d in documents]]
        else:
            chat.doc_ids = [doc.doc_id for doc in documents]

        return chat
    
    async def write_bot_msg(self, db: MongoDBService, chat: Chat, answer: str):
        bot_msg = Message(
            id=str(ObjectId()),
            is_user=False,
            content=answer,
            timestamp=datetime.datetime.now()
        )

        await db.add_message_to_chat(chat.id, bot_msg)
        chat.messages.append(bot_msg)
        await self.cache.update(chat.id, chat)

        return bot_msg
    
    def get_chunks_from_docs(self, docs: list = [], chunk_ids: list = None):
        result = []
        for doc in docs:
            if chunk_ids is None or doc.chunk_id in chunk_ids:
                result.append(doc.text)
        return result