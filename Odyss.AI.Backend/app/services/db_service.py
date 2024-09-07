from pymongo import MongoClient
from bson.objectid import ObjectId
from app.models.user import User, Document

class MongoDBService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MongoDBService, cls).__new__(cls)
        return cls._instance

    def __init__(self, db_name, collection_name, uri="mongodb+srv://odyssai:odyssai123@metadatadocs.vxscg8a.mongodb.net/?retryWrites=true&w=majority&appName=metadataDocs"):
        if not hasattr(self, 'client'):
            self.client = MongoClient(uri)
            self.db = self.client[db_name]
            self.collection = self.db[collection_name]

    def create_user(self, username):
        if self.collection.find_one({"username": username}):
            return None  # Benutzername existiert bereits
        user = User(id=str(ObjectId()), username=username)
        result = self.collection.insert_one(user.model_dump(by_alias=True))
        return user.id
    
    def get_user(self, username):
        user = self.collection.find_one({"username": username})
        if user:
            return {"username": user["username"], "id": str(user["_id"])}
        return None

    def add_document_to_user(self, username, document_data):
        user = self.collection.find_one({"username": username})
        if not user:
            return None  # Benutzer nicht gefunden
        document = Document(**document_data)
        document.ID = str(ObjectId())  # Generiere eine eindeutige ID für das Dokument
        self.collection.update_one(
            {"username": username},
            {"$push": {"documents": document.model_dump(by_alias=True)}}
        )
        return document.ID

    def get_documents_of_user(self, username):
        user = self.collection.find_one({"username": username})
        if not user:
            return None  # Benutzer nicht gefunden
        return [Document(**doc) for doc in user.get("documents", [])]

    def delete_document_of_user(self, username, document_id):
        result = self.collection.update_one(
            {"username": username},
            {"$pull": {"documents": {"ID": document_id}}}
        )
        return result.modified_count > 0

    def _convert_object_id(self, document):
        if document and "_id" in document:
            document["_id"] = str(document["_id"])
        return document