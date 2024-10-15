from quart import Quart
from quart_cors import cors
from app.routes import main
# from setup import setup_virtualenv


def create_app():

    app = Quart(__name__)
    app = cors(app, allow_origin="*")
    app.config.from_object('app.config.Config')
    
    app.register_blueprint(main)

    return app