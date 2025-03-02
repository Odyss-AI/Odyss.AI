import datetime
import logging

from app.utils.db import get_db
from app.models.chat import Chat, Message
from app.models.user import TextChunk, Document
from app.utils.ml_connection import query_mixtral_with_ssh_async, call_chatgpt_api_async
from app.utils.prompts import qna_prompt_builder
from bson.objectid import ObjectId
from app.services.caching import CachingService
from app.services.db_service import MongoDBService
from app.services.sim_search_service import SimailaritySearchService
from app.models.enum import AvailibleModels
from typing import List, Optional
from app.utils.time_logger import TimeLogger

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
        time_logger = TimeLogger("Message handling")

        # Load the chat from the cache or the database
        chat = await self.get_chat_async(db, message, user, chat_id)
        if chat is None:
            raise ValueError("Failed to get or create chat")
        time_logger.exit_func(f"Get chat {str(chat.id)}", "Get documents")

        docs = await self.get_docs_async(db, user, chat.doc_ids)
        if docs is None:
            raise ValueError("Failed to get documents")
        time_logger.exit_func(f"Get documents {str(chat.doc_ids)}", "Search similar documents")

        sim_chunks = []
        if len(docs) != 0:
            sim_chunks = await self.sim_search.search_similar_documents_async(chat.doc_ids, message.content)
            if sim_chunks is None:
                raise ValueError("Failed to get similar chunks")
        time_logger.exit_func(f"Search similar documents {str(sim_chunks)}", "Get chunks")

        chunks = []
        if len(docs) != 0:
            chunks = self.get_chunks_from_docs(docs, sim_chunks)
            if not chunks:
                raise ValueError("Failed to get chunks")
        time_logger.exit_func(f"Get chunks str(chunks)", "Build prompt and call LLM API")

        try:
            prompt = qna_prompt_builder(chunks, message.content)
            if message.selected_model == AvailibleModels.CHATGPT.value:
                answer = await call_chatgpt_api_async(prompt)
            else:
                answer = await query_mixtral_with_ssh_async(prompt)
        except Exception as e:
            print(f"Error building prompt or calling LLM API: {e}")
            logging.error(f"Error building prompt or calling LLM API: {e}")
            return None, f"Error building prompt or calling LLM API: {e}", chat.id
        time_logger.exit_func(f"Build prompt and call LLM API str(answer)", "Write bot message")

        if answer is None:
            answer = "Sorry, I could not generate a response."

        bot_msg = await self.write_bot_msg_async(db, chat, answer)
        if bot_msg is None:
            raise ValueError("Failed to write bot message")
        time_logger.exit_func(f"Write bot message str(bot_msg.id)", "Finishing process")

        time_logger.exit_process()
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
        try:
            chat = await self.cache.get(chat_id, Chat)

            # If the chat is in the cache, add the message to it
            if chat:
                await db.add_message_to_chat_async(chat.id, message)
                chat.messages.append(message)

            # If the chat is not in the cache, retrieve it from the database
            else:
                chat = await db.get_chat_async(chat_id)
                if chat:
                    await db.add_message_to_chat_async(chat.id, message)
                    chat.messages.append(message)

            # Update the cache
            if chat:        
                await self.cache.set(chat.id, chat)
                
            return chat
        except Exception as e:
            logging.error(f"Error in get_chat_async: {e}")
            return None
    
    async def get_docs_async(self, db: MongoDBService, user: str, doc_ids: list = []):
        """
        Retrieves the documents from the database based on the provided document IDs.

        Args:
            db (MongoDBService): The database service instance.
            user (str): The username.
            doc_ids (list, optional): A list of document IDs. Defaults to None.

        Returns:
            list: A list of document objects.
        """

        try:
            if not doc_ids:
                return []

            # If someone will implement caching, there are some errors while searching for the documents in the caching service

            # # Check which documents are already in the cache
            # cached_docs = await self.cache.get_cached_documents(doc_ids)
            # cached_doc_ids = {doc.id for doc in cached_docs}
            
            # # Check which documents are missing in the cache
            # missing_doc_ids = [doc_id for doc_id in doc_ids if doc_id not in cached_doc_ids]

            # # Retrieve the missing documents from the database
            # if missing_doc_ids:
            #     missing_docs = await db.get_documents_by_ids_async(user, missing_doc_ids)
            #     # Cache the missing documents
            #     await self.cache.cache_documents(missing_docs)
            # else:
            #     missing_docs = []

            # # Combine the cached and missing documents
            # docs = cached_docs + missing_docs

            docs = await db.get_documents_of_user_async(user)
            if docs is None:
                return []
            
            # Filter the documents based on doc_ids
            filtered_docs = [doc for doc in docs if doc.doc_id in doc_ids]

            return filtered_docs

        except Exception as e:
            logging.error(f"Error in get_docs_async: {e}")
            return None
    
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
        try:
            bot_msg = Message(
                id=str(ObjectId()),
                is_user=False,
                content=answer,
                timestamp=str(datetime.datetime.now())
            )

            await db.add_message_to_chat_async(chat.id, bot_msg)
            chat.messages.append(bot_msg)
            await self.cache.update(chat.id, chat)

            return bot_msg
        except Exception as e:
            logging.error(f"Error in write_bot_msg_async: {e}")
            print(f"Error in write_bot_msg_async: {str(e)}")
            return None
    
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

        try:
            chunk_id_to_score = {chunk_id: score for chunk_id, score in chunk_ids}
        except Exception as e:
            logging.error(f"Error processing chunk_ids: {e}")
            return result

        try:
            for doc in docs:
                for chunk in doc.textList:
                    if chunk.id in chunk_id_to_score:
                        result.append([chunk.text, chunk_id_to_score[chunk.id]])
        except AttributeError as e:
            logging.error(f"Error accessing document attributes: {e}")
        except Exception as e:
            logging.error(f"Unexpected error in get_chunks_from_docs: {e}")

        return result