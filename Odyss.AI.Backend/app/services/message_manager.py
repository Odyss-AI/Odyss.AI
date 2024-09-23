import datetime

from app.utils.db import get_db
from app.models.chat import Chat, Message
from app.models.user import TextChunk, Document
from app.utils.helpers import call_mistral_api_async
from app.utils.prompts import qna_prompt_builder
from bson.objectid import ObjectId
from app.services.caching import CachingService
from app.services.db_service import MongoDBService
from app.services.sim_search_service import SimailaritySearchService
from typing import List, Optional

class MessageManager:
    """
    A class to manage messages, handle chat interactions, and perform similarity searches.
    """
        
    def __init__(self):
        self.cache = CachingService()
        self.sim_search = SimailaritySearchService()

    async def handle_message_async(self, message: Message, user: str, chat_id: str = None):
        """
        Handles an incoming message, processes it, and generates a response.

        Args:
            message (Message): The incoming message object.
            user (str): The username.
            chat_id (str, optional): The chat ID. If None, a new chat is created.

        Returns:
            tuple: A tuple containing the bot's response message, the relevant chunks, and the chat ID.
        """
        
        db = get_db()

        # Load the chat from the cache or the database
        chat = await self.get_chat_async(db, message, user, chat_id)

        # Load the documents from the database
        chat = await self.get_docs_async(db, user, chat)

        # Search for similar text chunks in the documents
        sim_chunks = await self.sim_search.search_similar_documents_async(chat.doc_ids, message.content)
        docs = await db.get_documents_of_user_async(user)
        chunks = self.get_chunks_from_docs(docs, sim_chunks)

        # Build the prompt for the LLM
        prompt = qna_prompt_builder(chunks, message.content)
        answer = await call_mistral_api_async(prompt)

        # Build the answer
        bot_msg = await self.write_bot_msg_async(db, chat, answer)

        return bot_msg, chunks, chat.id

    async def get_chat_async(self, db: MongoDBService, message: Message, user: str, chat_id: str = None):
        """
        Retrieves the chat from the cache or the database. If the chat does not exist, it creates a new one.

        Args:
            db (MongoDBService): The database service instance.
            message (Message): The incoming message object.
            user (str): The username.
            chat_id (str, optional): The chat ID. If None, a new chat is created.

        Returns:
            Chat: The chat object.
        """
        
        if chat_id is None:
            chat = await db.create_chat_async(user, message)
            await self.cache.set(chat.id, chat)
            return chat
        
        chat = await self.cache.get(chat_id, Chat)
        # chat = None
        if not chat:
            chat = await db.get_chat_async(chat_id)
            if chat:
                await db.add_message_to_chat_async(chat.id, message)
                chat.messages.append(message)
                await self.cache.set(chat_id, chat)
            else:
                chat = await db.create_chat_async(user, message)
                await self.cache.set(chat.id, chat)
        else:
            chat.messages.append(message)
            self.cache.update(chat_id, chat)
            await db.add_message_to_chat_async(chat.id, message)

        return chat
    
    async def get_docs_async(self, db:MongoDBService, user: str, chat: Chat, doc_ids: list = None):
        """
        Retrieves the documents associated with the user and updates the chat's document IDs.

        Args:
            db (MongoDBService): The database service instance.
            user (str): The username.
            chat (Chat): The chat object.
            doc_ids (list, optional): A list of document IDs. If provided, it checks if the chat's document IDs match.

        Returns:
            Chat: The updated chat object.
        """
        
        if doc_ids and set(chat.doc_ids) == set(doc_ids):
            return chat
    
        documents = await db.get_documents_of_user_async(user)
        if(chat.doc_ids and len(chat.doc_ids) > 0):
            chat.doc_ids = [
                doc for doc in chat.doc_ids 
                if doc in [d.doc_id for d in documents]]
        else:
            chat.doc_ids = [doc.doc_id for doc in documents]

        return chat
    
    async def write_bot_msg_async(self, db: MongoDBService, chat: Chat, answer: str):
        """
        Writes the bot's response message to the chat and updates the cache.

        Args:
            db (MongoDBService): The database service instance.
            chat (Chat): The chat object.
            answer (str): The bot's response message.

        Returns:
            Message: The bot's response message object.
        """
        
        bot_msg = Message(
            id=str(ObjectId()),
            is_user=False,
            content=answer,
            timestamp=datetime.datetime.now()
        )

        await db.add_message_to_chat_async(chat.id, bot_msg)
        chat.messages.append(bot_msg)
        await self.cache.update(chat.id, chat)

        return bot_msg
    
    def get_chunks_from_docs(self, docs: list[Document] = [], chunk_ids: list = None):
        """
        Retrieves the text chunks from the documents based on the provided chunk IDs.

        Args:
            docs (list[Document], optional): A list of document objects. Defaults to an empty list.
            chunk_ids (list, optional): A list of chunk IDs and their scores. Defaults to None.

        Returns:
            list: A list of text chunks and their scores.
        """
        
        result = []
        if chunk_ids is None:
            return result

        chunk_id_to_score = {chunk_id: score for chunk_id, score in chunk_ids}

        for doc in docs:
            for chunk in doc.textList:
                if chunk.id in chunk_id_to_score:
                    result.append([chunk.text, chunk_id_to_score[chunk.id]])
        
        return result