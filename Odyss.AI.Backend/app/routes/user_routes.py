from flask import request, jsonify
from app.routes import main
from app.utils.db import get_db  # Importiere den globalen db_service und die Initialisierungsfunktion

@main.route('/users/adduser', methods=['POST'])
def add_user():
    try:
        db = get_db()

        data = request.get_json()  # JSON-Daten aus der Anfrage lesen
        username = data.get('username')
        
        if not username:
            return jsonify({"error": "Username ist erforderlich"}), 400
        
        # Benutzer erstellen
        user_id = db.create_user(username)
        
        if user_id:
            return jsonify({"message": "Benutzer erfolgreich erstellt", "user_id": user_id}), 201
        else:
            return jsonify({"error": "Benutzername existiert bereits"}), 409
    except Exception as e:
        return jsonify({"error": f"Fehler beim Hinzufügen des Benutzers: {e}"}), 500

@main.route('/users/getuser', methods=['GET'])
def get_user():
    try:
        db = get_db()
        username = request.args.get('username')

        # Benutzer abrufen
        user = db.get_user(username)
        
        if user:
            return jsonify({"message": "Benutzer gefunden", "user": user}), 200
        else:
            return jsonify({"error": "Benutzer nicht gefunden"}), 404
    except Exception as e:
        return jsonify({"error": f"Fehler beim Abrufen des Benutzers: {e}"}), 500    
