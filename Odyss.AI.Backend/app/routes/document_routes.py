from flask import render_template
from app.routes import main

@main.route('/documents', methods=['GET'])
def get_documents():
    return "Liste der Dokumente"