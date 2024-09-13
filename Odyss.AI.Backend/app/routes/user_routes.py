from quart import request, jsonify
from app.routes import main
from app.db import get_db  # Importiere den globalen db_service und die Initialisierungsfunktion

# Benutzer hinzufügen
@main.route('/users/adduser', methods=['POST'])
async def add_user():
    try:
        db = get_db()

        data = await request.get_json()  # JSON-Daten aus der Anfrage asynchron lesen
        username = data.get('username')

        if not username:
            return jsonify({"error": "Username ist erforderlich"}), 400

        # Benutzer erstellen
        user_id = await db.create_user_async(username)

        if user_id:
            return jsonify({"message": "Benutzer erfolgreich erstellt", "user_id": user_id}), 201
        else:
            return jsonify({"error": "Benutzername existiert bereits"}), 409
    except Exception as e:
        return jsonify({"error": f"Fehler beim Hinzufügen des Benutzers: {e}"}), 500

# Benutzer abrufen
@main.route('/users/getuser', methods=['GET'])
async def get_user():
    try:
        db = get_db()
        username = request.args.get('username')

        # Benutzer abrufen
        user = await db.get_user_async(username)

        if user:
            return jsonify({"message": "Benutzer gefunden", "user": user}), 200
        else:
            return jsonify({"error": "Benutzer nicht gefunden"}), 404
    except Exception as e:
        return jsonify({"error": f"Fehler beim Abrufen des Benutzers: {e}"}), 500
