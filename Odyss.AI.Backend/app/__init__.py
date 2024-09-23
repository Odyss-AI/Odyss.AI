import logging
import sys

from quart import Quart
from quart_cors import cors
from app.routes import main
from app.utils.db import init_db_service
from setup import setup_virtualenv

def create_app():

    app = Quart(__name__)
    app = cors(app, allow_origin="*")

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', stream=sys.stdout)

    logging.info("Starting Odyss.AI backend ...")

    # Initialize the database service
    init_db_service()

    app.config.from_object('app.config.Config')

    app.register_blueprint(main)

    logging.info("Odyss.AI is running")
    return app