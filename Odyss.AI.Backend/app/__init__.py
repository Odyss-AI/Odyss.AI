from quart import Quart
from app.routes import main
from app.utils.db import init_db_service
from setup import setup_virtualenv

def create_app():

    app = Quart(__name__)
    # Initialisiere den MongoDBService
    init_db_service()

    print("Odyss.AI Backend is running")
    app.config.from_object('app.config.Config')

    app.register_blueprint(main)

    return app