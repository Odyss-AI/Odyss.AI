import os
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
        if cls._instance is None:
            cls._instance = super(MongoDBService, cls).__new__(cls)
        return cls._instance

    def __init__(self, db_name, collection_name, uri=Config.MONGODB_CONNECTION_STRING):
        if not hasattr(self, 'client'):
            self.client = AsyncIOMotorClient(uri)
            self.db = self.client[db_name]
            self.user_collection = self.db[collection_name]
            self.chat_collection = self.db["chats"]


    async def create_user_async(self, username):
        existing_user = await self.user_collection.find_one({"username": username})
        if existing_user:
            return None  # Benutzername existiert bereits
        user = User(id=str(ObjectId()), username=username)
        await self.user_collection.insert_one(user.model_dump(by_alias=True))
        return user.id

    async def get_user_async(self, username):
        user = await self.user_collection.find_one({"username": username})
        if user:
            return {"username": user["username"], "id": str(user["_id"])}
        return None
    
    async def get_documents_of_user_async(self, username):
        user = await self.user_collection.find_one({"username": username})
        if not user:
            return None
        return [Document(**doc) for doc in user.get("documents", [])]
    
    async def get_chunks_by_ids_async(self, username: str, chunk_ids: list, doc_ids=None):
        user = await self.user_collection.find_one({"username": username})
        if not user:
            return None
        
        documents = user.get("documents", [])
        chunks = []
        
        for doc in documents:
            if doc_ids is None or doc.get("id") in doc_ids:
                for chunk in doc.get("textchunks", []):
                    if chunk.get("chunk_id") in chunk_ids:
                        chunks.append(chunk)
        
        return chunks

    async def add_document_to_user_async(self, username, document: Document):
        user = await self.user_collection.find_one({"username": username})
        if not user:
            return None
        docs = await self.get_documents_of_user_async(username)
        for doc in docs:
            if doc.get('doc_id') == document.doc_id:
                return doc.id
        document.id = str(ObjectId())  # Generiere eine eindeutige ID für das Dokument
        await self.user_collection.update_one(
            {"username": username},
            {"$push": {"documents": document.model_dump(by_alias=True)}}
        )
        return document.id

    async def delete_document_of_user(self, username, document_id):
        result = await self.user_collection.update_one(
            {"username": username},
            {"$pull": {"documents": {"ID": document_id}}}
        )
        return result.modified_count > 0
    
    async def get_chat(self, chat_id):
        chat = await self.chat_collection.find_one({"chat_id": chat_id})
        chat = Chat(chat)
        return chat
    
    async def get_chats_by_user(self, user):
        chats_cursor = self.chat_collection.find({"user_id": user})
        chats = []
        async for chat in chats_cursor:
            chats.append(Chat(chat))
        return chats
    
    async def create_chat(self, user: str, message: Message):
        chat = Chat( id=str(ObjectId()),
            user_id=user,
            messages=[message],
            doc_ids=[] )
        await self.chat_collection.insert_one(chat.model_dump(by_alias=True))
        return chat
    
    async def add_message_to_chat(self, chat_id: str, message: Message):
        chat = await self.get_chat(chat_id)
        if not chat:
            return None
        message.id = str(ObjectId())
        chat.messages.append(message)
        await self.chat_collection.update_one(
            {"chat_id": chat_id},
            {"$set": {"messages": chat.messages}}
        )

    async def get_messages_from_chat(self, chat_id):
        chat = await self.get_chat(chat_id)
        if chat:
            return chat.get("messages", [])
        return []

    

    def _convert_object_id(self, document):
        """
        Converts the ObjectId of a document to a string.

        Args:
            document (dict): The document to convert.

        Returns:
            dict: The document with the ObjectId converted to a string.
        """
        
        if document and "_id" in document:
            document["_id"] = str(document["_id"])
        return document
