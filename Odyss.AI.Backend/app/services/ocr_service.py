

class OCRService:
    def __init__(self):
        self.ocr = None

    def extract_text(self, doc):
        # Emil tob dich aus, in doc bekommst du das Dokumentenobjekt übergeben 
        # Schau in user.py nach: Darin ist die URL, Name, usw.
        # Du kannst dir ein Tool wie Insomnia holen, um direkt ein Dokument über den
        # Endpunkt zu senden und zu schauen, was du bekommst: 
        # document_routes.py -> document_manager.py --> OCRService

        # Splitte den ausgelesenen Text in kleine Abschnitte und speichere
        # diese in doc.textlist als liste von TextChunk Objekten
        # Die TextChunks haben die Attribute ID, Text und Page
        # return das Dokumentenobjekt, daraus wird anschließend die Emebddings erstellt

        # Die erkannten Bilder werden in doc.imgList als Liste von Image Objekten gespeichert
        # Die Image Objekte haben die Attribute ID, Link, Page, Type, Imgtext und LLM_Output
        # Die Bilder sollen in OneDrie gespeichert werden, muss noch implementiert werden

        # Wichtig: Mach so viele Methoden darunter wie du brauchst für die OCR Logik, 
        # aber alle sollen hierin aufgerufen werden
        # So ist deine Logik abgekapselt und du kannst machen was du willst solange 
        # du das Dokumentenobjekt zurückgibst mit den entsprechenden Werten eingefügt

        return doc