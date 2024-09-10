from pymongo import MongoClient
from bson.objectid import ObjectId
from app.models.user import User, Document

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

    def __init__(self, db_name, collection_name, uri="mongodb+srv://odyssai:odyssai123@metadatadocs.vxscg8a.mongodb.net/?retryWrites=true&w=majority&appName=metadataDocs"):
        if not hasattr(self, 'client'):
            self.client = MongoClient(uri)
            self.db = self.client[db_name]
            self.collection = self.db[collection_name]



    def create_user(self, username):
        """
        Creates a new user in the database.

        Args:
            username (str): The username of the new user.

        Returns:
            str: The ID of the created user, or None if the user already exists.
        """
                
        if self.collection.find_one({"username": username}):
            return None
        user = User(id=str(ObjectId()), username=username)
        result = self.collection.insert_one(user.model_dump(by_alias=True))
        return user.id
    

    
    def get_user(self, username):
        """
        Retrieves a user from the database by username.

        Args:
            username (str): The username of the user to retrieve.

        Returns:
            dict: A dictionary containing the user's username and ID, or None if the user does not exist.
        """

        user = self.collection.find_one({"username": username})
        if user:
            return {"username": user["username"], "id": str(user["_id"])}
        return None



    def add_document_to_user(self, username, document_data):
        """
        Adds a document to a user's document list.

        Args:
            username (str): The username of the user to add the document to.
            document_data (dict): The data of the document to add.

        Returns:
            str: The ID of the added document, or None if the user does not exist.
        """
                
        user = self.collection.find_one({"username": username})
        if not user:
            return None
        document = Document(**document_data)
        document.ID = str(ObjectId())
        self.collection.update_one(
            {"username": username},
            {"$push": {"documents": document.model_dump(by_alias=True)}}
        )
        return document.ID
    


    def get_documents_of_user(self, username):
        """
        Retrieves all documents associated with a user.

        Args:
            username (str): The username of the user to retrieve documents for.

        Returns:
            list: A list of Document objects, or None if the user does not exist.
        """

        user = self.collection.find_one({"username": username})
        if not user:
            return None
        return [Document(**doc) for doc in user.get("documents", [])]



    def delete_document_of_user(self, username, document_id):
        """
        Deletes a document from a user's document list.

        Args:
            username (str): The username of the user to delete the document from.
            document_id (str): The ID of the document to delete.

        Returns:
            bool: True if the document was deleted, False otherwise.
        """

        result = self.collection.update_one(
            {"username": username},
            {"$pull": {"documents": {"ID": document_id}}}
        )
        return result.modified_count > 0

    

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