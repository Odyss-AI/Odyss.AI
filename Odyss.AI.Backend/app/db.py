from app.services.db_service import MongoDBService

# Globale Variable für den MongoDBService
db_service = None

def init_db_service():
    global db_service
    if db_service is None:
        try:
            print("Initialisiere db_service...")
            db_service = MongoDBService(db_name="odyss_ai", collection_name="users")
            print("MongoDB-Verbindung erfolgreich hergestellt")
        except Exception as e:
            print(f"Fehler beim Herstellen der MongoDB-Verbindung: {e}")
            # Hier können Sie entscheiden, ob Sie die Anwendung beenden oder fortfahren möchten
            # raise e  # Optional: Anwendung beenden
    else:
        print("db_service ist bereits initialisiert")

def get_db():
    return db_service