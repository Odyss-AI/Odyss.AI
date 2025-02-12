from flask import Flask, request, jsonify
import cv2
import numpy as np
from tensorflow.keras.models import load_model

app = Flask(__name__)

# Laden des Modells
model = load_model('diagram_classifier.h5')  # Pfad zu deinem Modell

# Klassenbezeichnungen
chart_classes = ['bar_chart', 'diagram', 'flow_chart', 'graph', 'just_img', 'pie_chart', 'table']

class ImageTaggerService:
    def load_and_preprocess_image(self, img_data):
        img = cv2.imdecode(np.frombuffer(img_data, np.uint8), cv2.IMREAD_COLOR)  # Bild aus Byte-Daten laden
        if img is None:
            raise ValueError("Could not decode image")
        img = cv2.resize(img, (128, 128))  # Bildgröße anpassen
        return img

    def detect_chart_type(self, image):
        input_image = np.expand_dims(image, axis=0)  # Dimension anpassen für das Modell
        predictions = model.predict(input_image)
        predicted_class = chart_classes[np.argmax(predictions)]  # Vorhergesagte Klasse
        return predicted_class

image_tagger = ImageTaggerService()

@app.route('/tag/image', methods=['POST'])
def tag_image():
    # Überprüfe, ob überhaupt eine Datei im POST-Request enthalten ist
    if not request.files:
        return jsonify({'error': 'No image provided'}), 400

    # Extrahiere die erste Datei aus request.files
    img_file = next(iter(request.files.values()))

    # Überprüfe, ob die Datei eine gültige Endung hat
    if not img_file.filename.endswith(('.jpg', '.jpeg', '.png')):
        return jsonify({'error': 'Unsupported file format. Please upload a .jpg, .jpeg, or .png file.'}), 400

    # Lese die Bilddaten aus der Datei
    img_data = img_file.read()

    try:
        # Verarbeite und klassifiziere das Bild
        img = image_tagger.load_and_preprocess_image(img_data)
        tag = image_tagger.detect_chart_type(img)
        return jsonify({'tag': tag})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
        app.run(host="0.0.0.0", port="5150",debug=True)