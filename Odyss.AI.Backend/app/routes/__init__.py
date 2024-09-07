from flask import Blueprint

main = Blueprint('main', __name__)

from app.routes import document_routes
from app.routes import user_routes
from app.routes import websocket_routes