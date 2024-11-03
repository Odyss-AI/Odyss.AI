from datetime import datetime

class Document:
    def model_dump(self, by_alias=False):
        # Beispielmethode, die ein Dictionary zurückgibt
        return {
            "date": datetime.now(),  # Beispiel für ein datetime-Objekt
            # Weitere Felder hier
        }

def default_converter(o):
    if isinstance(o, datetime):
        return o.isoformat()
    raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable")

class ChunkModel:
    def __init__(self, chunk):
        self.chunk = chunk

    def model_dump(self, by_alias=False):
        # Beispielhafte Implementierung der model_dump Methode
        return {"chunk": self.chunk}

def convert_to_model(chunk):
    # Konvertiere chunk in ein Objekt der Klasse ChunkModel
    return ChunkModel(chunk)

def convert_datetime(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            obj[key] = convert_datetime(value)
    elif isinstance(obj, list):
        obj = [convert_datetime(item) for item in obj]
    elif isinstance(obj, datetime.datetime):
        obj = obj.isoformat()
    return obj