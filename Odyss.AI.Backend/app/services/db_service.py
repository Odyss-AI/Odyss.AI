import os
import asyncio
import logging
import hashlib

from motor.motor_asyncio import AsyncIOMotorClient
from bson.objectid import ObjectId
from app.models.user import User, Document
from app.models.chat import Message, Chat
from app.config import Config

class MongoDBService:
    """
    MongoDBService is a singleton class that provides methods to interact with a MongoDB database.
    It allows for creating users, retrieving users, adding documents to users, retrieving documents of users,
    and deleting documents of users.

    Attributes:
        _instance (MongoDBService): The singleton instance of the MongoDBService class.
        client (MongoClient): The MongoDB client used to connect to the database.
        db (Database): The database instance.
        collection (Collection): The collection instance within the database.

    Methods:
        __new__(cls, *args, **kwargs): Ensures that only one instance of the class is created (singleton pattern).
        __init__(self, db_name, collection_name, uri): Initializes the MongoDB client, database, and collection.
        create_user(self, username): Creates a new user in the database.
        get_user(self, username): Retrieves a user from the database by username.
        add_document_to_user(self, username, document_data): Adds a document to a user's document list.
        get_documents_of_user(self, username): Retrieves all documents associated with a user.
        delete_document_of_user(self, username, document_id): Deletes a document from a user's document list.
        _convert_object_id(self, document): Converts the ObjectId of a document to a string.
    """
        
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Ensures that only one instance of the class is created (singleton pattern).

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            MongoDBService: The singleton instance of the MongoDBService class.
        """
        if cls._instance is None:
            cls._instance = super(MongoDBService, cls).__new__(cls)
        return cls._instance

    def __init__(self, db_name, uri=Config.MONGODB_CONNECTION_STRING):
        if not hasattr(self, 'client'):
            self.client = AsyncIOMotorClient(uri, serverSelectionTimeoutMS=10000)
            self.db = self.client[db_name]
            self.user_collection = self.db["users"]
            self.chat_collection = self.db["chats"]
            self.files_collection = self.db["files"]
            self.extracted_images_collection = self.db["extracted_images"]
            


    async def create_user_async(self, username):
        """
        Creates a new user in the database asynchronously.

        Args:
            username (str): The username of the new user.

        Returns:
            User: The created user object, or None if the username already exists or an error occurs.
        """
        
        try:
            existing_user = await self.user_collection.find_one({"username": username})
            if existing_user:
                return None  # Benutzername existiert bereits
            user = User(id=str(ObjectId()), username=username)
            await self.user_collection.insert_one(user.model_dump(by_alias=True))
            return user
        except Exception as e:
            logging.error(f"Error creating user: {e}")
            return None

    async def get_user_async(self, username):
        """
        Retrieves a user from the database by username asynchronously.

        Args:
            username (str): The username of the user to retrieve.

        Returns:
            dict: The user document, or None if the user is not found or an error occurs.
        """
        
        try:
            user = await self.user_collection.find_one({"username": username})
            if user:
                return user
            return None
        except asyncio.CancelledError:
            logging.error("Die Operation wurde abgebrochen.")
            raise
        except Exception as e:
            logging.error(f"Error getting user: {e}")
            return None
    
    async def get_documents_of_user_async(self, username):
        """
        Retrieves all documents associated with a user asynchronously.

        Args:
            username (str): The username of the user whose documents are to be retrieved.

        Returns:
            list: A list of Document objects, or None if the user is not found or an error occurs.
        """
        
        try:
            user = await self.user_collection.find_one({"username": username})
            if not user:
                logging.info(f"User {username} not found.")
                return None
            documents = user.get("documents", [])
            return [Document(**doc) for doc in documents]
        except Exception as e:
            logging.error(f"Error getting documents of user {username}: {e}")
            return None
    
    async def get_chunks_by_ids_async(self, username: str, chunk_ids: list, doc_ids=None):
        """
        Retrieves text chunks by their IDs asynchronously.

        Args:
            username (str): The username of the user whose chunks are to be retrieved.
            chunk_ids (list): A list of chunk IDs to retrieve.
            doc_ids (list, optional): A list of document IDs to filter the chunks. Defaults to None.

        Returns:
            list: A list of chunks and their scores, or None if the user is not found or an error occurs.
        """
        
        try:
            user = await self.user_collection.find_one({"username": username})
            if not user:
                return None
            
            documents = user.get("documents", [])
            chunks = []
            
            for doc in documents:
                if doc_ids is None or doc.get("id") in doc_ids:
                    for chunk in doc.get("textchunks", []):
                        if chunk.get("chunk_id") in chunk_ids[0]:
                            chunks.append([chunk, chunk_ids[1]])
            
            return chunks
        except Exception as e:
            logging.error(f"Error getting chunks by IDs: {e}")
            return None

    async def add_document_to_user_async(self, username, document: Document):
        """
        Adds a document to a user's document list asynchronously.

        Args:
            username (str): The username of the user to add the document to.
            document (Document): The document to add.

        Returns:
            str: The ID of the added document, or None if the user is not found or an error occurs.
        """
        
        try:
            async with await self.client.start_session() as session:
                async with session.start_transaction():
                    user = await self.get_user_async(username)
                    if not user:
                        return None
                    
                    docs = await self.get_documents_of_user_async(username)
                    for doc in docs:
                        if doc.get('doc_id') == document.doc_id:
                            return doc.id
                    
                    document.id = str(ObjectId())  # Generiere eine eindeutige ID für das Dokument
                    await self.user_collection.update_one(
                        {"username": username},
                        {"$push": {"documents": document.model_dump(by_alias=True)}},
                        session=session
                    )

                    return document.id
        except asyncio.CancelledError:
            logging.error("Die Operation wurde abgebrochen.")
            raise
        except Exception as e:
            logging.error(f"Fehler beim Hinzufügen des Dokuments: {e}")
            return None


    async def delete_document_of_user_async(self, username, document_id):
        """
        Deletes a document from a user's document list asynchronously.

        Args:
            username (str): The username of the user to delete the document from.
            document_id (str): The ID of the document to delete.

        Returns:
            bool: True if the document was successfully deleted, False otherwise.
        """
        
        try:
            result = await self.user_collection.update_one(
                {"username": username},
                {"$pull": {"documents": {"ID": document_id}}}
            )
            return result.modified_count > 0
        except Exception as e:
            logging.error(f"Error deleting document of user: {e}")
            return False
    
    async def get_chat_async(self, chat_id):
        """
        Retrieves a chat from the database by chat ID asynchronously.

        Args:
            chat_id (str): The ID of the chat to retrieve.

        Returns:
            Chat: The chat object, or None if the chat is not found or an error occurs.
        """
        
        try:
            chat = await self.chat_collection.find_one({"id": chat_id})
            if chat:
                return Chat(**chat) 
            return None
        except Exception as e:
            logging.error(f"Error getting chat: {e}")
            return None
    
    async def get_chats_by_user_async(self, user):
        """
        Retrieves all chats associated with a user asynchronously.

        Args:
            user (str): The user ID whose chats are to be retrieved.

        Returns:
            list: A list of Chat objects, or None if an error occurs.
        """
        
        try:
            chats_cursor = self.chat_collection.find({"user_id": user})
            chats = []
            async for chat in chats_cursor:
                chats.append(Chat(**chat))
            return chats
        except Exception as e:
            logging.error(f"Error getting chats by user: {e}")
            return None
    
    async def create_chat_async(self, user: str, message: Message):
        """
        Creates a new chat in the database asynchronously.

        Args:
            user (str): The user ID associated with the chat.
            message (Message): The initial message of the chat.

        Returns:
            Chat: The created chat object, or None if an error occurs.
        """
        
        try:
            chat = Chat( 
                id=str(ObjectId()),
                user_id=user,
                messages=[message],
                doc_ids=[] )
            await self.chat_collection.insert_one(chat.model_dump(by_alias=True))
            return chat
        except Exception as e:
            logging.error(f"Error creating chat: {e}")
            return None
    
    async def add_message_to_chat_async(self, chat_id: str, message: Message):
        """
        Adds a message to a chat asynchronously.

        Args:
            chat_id (str): The ID of the chat to add the message to.
            message (Message): The message to add.

        Returns:
            bool: True if the message was successfully added, False otherwise.
        """
        
        try:
            chat = await self.get_chat_async(chat_id)
            if not chat:
                return None
            
            message_dict = message.model_dump(by_alias=True)

            result = await self.chat_collection.update_one(
                {"id": chat_id},
                {"$push": {"messages": message_dict}}
            )

            return result.modified_count > 0
        except Exception as e:
            logging.error(f"Error adding message to chat: {e}")
            return None

    async def get_messages_from_chat_async(self, chat_id):
        """
        Retrieves all messages from a chat asynchronously.

        Args:
            chat_id (str): The ID of the chat to retrieve messages from.

        Returns:
            list: A list of messages, or an empty list if the chat is not found or an error occurs.
        """
        
        try:
            chat = await self.get_chat(chat_id)
            if chat:
                return chat.get("messages", [])
            return []
        except Exception as e:
            logging.error(f"Error getting messages from chat: {e}")
            return []

    

    def _convert_object_id(self, document):
        """
        Converts the ObjectId of a document to a string.

        Args:
            document (dict): The document to convert.

        Returns:
            dict: The document with the ObjectId converted to a string.
        """
        try:
            if document and "_id" in document:
                document["_id"] = str(document["_id"])
            return document
        except Exception as e:
            logging.error(f"Error converting ObjectId: {e}")
            return document

    def hash_filename_and_file(self, filename: str, file_content: bytes) -> str:
        combined_data = filename.encode() + file_content    
        return hashlib.sha256(combined_data).hexdigest()

    async def upload_pdf(self, file, filename: str):
        """db_service = get_db()
        db = db_service.db
        If in other file retrieve db like this.
        """
        file_content = await file.read()
        hashed_filename_and_file = self.hash_filename_and_file(filename, file_content)

        user = await self.users_collection.find_one({"username": username})
        if user and hashed_filename_and_file in user.get("pdf_list", []):
            logging.info(f'File {filename} already exists for user {username}. Skipping upload.')
            return None
        
        fs = gridfs.GridFS(self.db.delegate, collection=self.files_collection.name)
        
        file_id = fs.put(file, filename=filename, contentType='application/pdf')
        logging.info(f'File uploaded successfully with ObjectID: {file_id}')
        return file_id
    
    async def upload_image(self, file):
        """db_service = get_db()
        db = db_service.db
        If in other file retrieve db like this.
        """
        fs = gridfs.GridFS(self.db.delegate, collection=self.extracted_images_collection.name)
        
        file_id = fs.put(file, filename=file.name, contentType='image/jpeg')
        logging.info(f'Image uploaded successfully with ObjectID: {file_id}')
        return file_id


    async def get_pdf_async(self, file_id):
        """db_service = get_db()
        db = db_service.db
        If in other file retrieve db like this.
        """
        fs = gridfs.GridFS(self.db.delegate, collection=self.files_collection.name)
        
        try:
            file = fs.get(file_id)
            return file.read()
        except gridfs.errors.NoFile:
            logging.error(f'No file found with ObjectID: {file_id}')
            return None


    async def get_image_async(self, file_id):
        """db_service = get_db()
        db = db_service.db
        If in other file retrieve db like this.
        """
        fs = gridfs.GridFS(self.db.delegate, collection=self.extracted_images_collection.name)
        
        try:
            file = fs.get(file_id)
            return file.read()
        except gridfs.errors.NoFile:
            logging.error(f'No file found with ObjectID: {file_id}')
            return None