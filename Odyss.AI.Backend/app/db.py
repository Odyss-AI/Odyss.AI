from app.services.db_service import MongoDBService

db_service = None

def init_db_service():
    global db_service
    if db_service is None:
        try:
            print("Initialize database connection ...")
            db_service = MongoDBService(db_name="odyss_ai", collection_name="users")
            print("MongoDB-Connection is established")
        except Exception as e:
            print(f"Error while opening connection to MongoDB: {e}")
            raise e  # Anwendung beenden
    else:
        print("Database connection is already established")

# Access MongoDB connection in other services
def get_db():
    return db_service