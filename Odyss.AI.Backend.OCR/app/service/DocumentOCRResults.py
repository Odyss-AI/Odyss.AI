from difflib import SequenceMatcher
from rapidfuzz.distance import Levenshtein
from PyPDF2 import PdfReader
import time
from app.service.tesseractocr import OCRTesseract  # Importiere TesseractOCR
from app.service.paddleocr import OCRPaddle        # Importiere PaddleOCR
from app.service.nougatocr import OCRNougat        # Importiere NougatOCR
from app.user import Document

class Document:
    def __init__(self, path):
        self.path = path
        self.textList = []  # Beispielweise werden Textchunks hier gespeichert

class DocumentOCRResults:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.ground_truth = self._extract_ground_truth()
        self.ocr_results = {}

    def _extract_ground_truth(self):
        try:
            print("Lese Ground Truth aus PDF...")
            pdf_reader = PdfReader(self.pdf_path)
            ground_truth_text = ""

            for page in pdf_reader.pages:
                ground_truth_text += page.extract_text() or ""
            
            return ground_truth_text.strip()
        except Exception as e:
            print(f"Fehler beim Lesen des PDFs: {e}")
            return ""

    def run_ocr(self, ocr_engines):
        for engine_name, engine_instance in ocr_engines.items():
            print(f"Starte OCR mit {engine_name}...")
            start_time = time.time()  # Zeitmessung starten
            document = engine_instance.extract_text(Document(path=self.pdf_path))  # Aufruf von process
            processing_time = time.time() - start_time  # Verarbeitungszeit messen
            ocr_text = self._extract_text_from_document(document)
            self.ocr_results[engine_name] = {
                "text": ocr_text,
                "processing_time": processing_time
            }

    def _extract_text_from_document(self, document):
        # Extrahiert Text aus den Textchunks des Documents
        return "\n".join(chunk.text for chunk in document.textList).strip()

    def compare_results(self):
        print("\n=== Vergleich der OCR-Ergebnisse ===")
        results = {}
        for ocr_name, data in self.ocr_results.items():
            metrics = self._calculate_metrics(data['text'])
            metrics['processing_time'] = data['processing_time']
            results[ocr_name] = metrics

        for ocr_name, metrics in results.items():
            print(f"\n--- {ocr_name} ---")
            print(f"Textgenauigkeit: {metrics['char_accuracy']:.2f}%")
            print(f"Fehlerrate (CER): {metrics['char_error_rate']:.2f}%")
            print(f"Verarbeitungszeit: {metrics['processing_time']:.2f} Sekunden")
            print(f"Levenshtein-Distanz: {metrics['levenshtein_distance']}")
            print(f"Ähnlichkeitsrate: {metrics['similarity_ratio']:.2f}%")

    def _calculate_metrics(self, ocr_text):
        levenshtein_distance = Levenshtein.distance(self.ground_truth, ocr_text)
        char_accuracy = self._calculate_char_accuracy(self.ground_truth, ocr_text)
        similarity_ratio = SequenceMatcher(None, self.ground_truth, ocr_text).ratio() * 100
        char_error_rate = self._calculate_char_error_rate(self.ground_truth, ocr_text, levenshtein_distance)

        return {
            "levenshtein_distance": levenshtein_distance,
            "char_accuracy": char_accuracy,
            "char_error_rate": char_error_rate,
            "similarity_ratio": similarity_ratio,
        }

    @staticmethod
    def _calculate_char_accuracy(ground_truth, ocr_text):
        # Länge der Texte angleichen
        min_length = min(len(ground_truth), len(ocr_text))
        max_length = max(len(ground_truth), len(ocr_text))

        # Zähle korrekt übereinstimmende Zeichen
        correct_chars = sum(1 for i in range(min_length) if ground_truth[i] == ocr_text[i])

        # Genauigkeit berechnen
        return (correct_chars / max_length) * 100 if max_length > 0 else 0

    @staticmethod
    def _calculate_char_error_rate(ground_truth, ocr_text, levenshtein_distance):
        # CER: Anzahl der Edit-Operationen (Levenshtein-Distanz) geteilt durch die Länge der Ground Truth
        ground_truth_length = len(ground_truth)
        return (levenshtein_distance / ground_truth_length) * 100 if ground_truth_length > 0 else 0

    @staticmethod
    def main(pdf_path):
        # OCR-Engines initialisieren
        ocr_engines = {
            "Tesseract": OCRTesseract(),
            "PaddleOCR": OCRPaddle(),
            "Nougat": OCRNougat()
        }

        # DocumentOCRResults erstellen und OCRs ausführen
        ocr_comparator = DocumentOCRResults(pdf_path)
        ocr_comparator.run_ocr(ocr_engines)

        # Ergebnisse vergleichen
        ocr_comparator.compare_results()


# Wenn die Datei direkt ausgeführt wird
if __name__ == "__main__":
    # Pfad zum PDF angeben
    pdf_path = "C:\\Users\\ramaz\\Documents\\Paper.pdf"
    DocumentOCRResults.main(pdf_path)
