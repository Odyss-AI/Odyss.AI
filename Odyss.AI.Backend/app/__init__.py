from flask import Flask
from app.routes import main
from app.utils.db import init_db_service  # Importiere die Initialisierungsfunktion

def create_app():
    app = Flask(__name__)
    # Initialisiere den MongoDBService
    init_db_service()

    print("Odyss.AI Backend is running")
    app.config.from_object('app.config.Config')

    app.register_blueprint(main)

    return app