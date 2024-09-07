from flask import render_template
from app.routes import main

@main.route('/', methods=['GET'])
def home():
    return "<h1>Hallo bei Odyss.AI</h1>"