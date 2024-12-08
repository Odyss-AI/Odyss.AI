# document_ocr_results.py

from difflib import SequenceMatcher
from rapidfuzz.distance import Levenshtein
from PyPDF2 import PdfReader
from tesseractocr import OCRTesseract  # Importiere TesseractOCR
from paddleocr import OCRPaddle        # Importiere PaddleOCR
from nougatocr import OCRNougat        # Importiere NougatOCR

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
            document = engine_instance.extract_text(Document(path=self.pdf_path))
            self.ocr_results[engine_name] = self._extract_text_from_document(document)

    def _extract_text_from_document(self, document):
        # Extrahiert Text aus den Textchunks des Documents
        return "\n".join(chunk.text for chunk in document.textList).strip()

    def compare_results(self):
        print("\n=== Vergleich der OCR-Ergebnisse ===")
        results = {
            ocr_name: self._calculate_metrics(ocr_text)
            for ocr_name, ocr_text in self.ocr_results.items()
        }

        for ocr_name, metrics in results.items():
            print(f"\n--- {ocr_name} ---")
            print(f"Levenshtein-Distanz: {metrics['levenshtein_distance']}")
            print(f"Zeichen-genaue Genauigkeit: {metrics['char_accuracy']:.2f}%")
            print(f"Ähnlichkeitsrate: {metrics['similarity_ratio']:.2f}%")

    def _calculate_metrics(self, ocr_text):
        levenshtein_distance = Levenshtein.distance(self.ground_truth, ocr_text)
        char_accuracy = self._calculate_char_accuracy(self.ground_truth, ocr_text)
        similarity_ratio = SequenceMatcher(None, self.ground_truth, ocr_text).ratio() * 100

        return {
            "levenshtein_distance": levenshtein_distance,
            "char_accuracy": char_accuracy,
            "similarity_ratio": similarity_ratio,
        }

    @staticmethod
    def _calculate_char_accuracy(ground_truth, ocr_text):
        correct_chars = sum(1 for gt, oc in zip(ground_truth, ocr_text) if gt == oc)
        total_chars = max(len(ground_truth), len(ocr_text))
        return (correct_chars / total_chars) * 100

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
    pdf_path = "path/to/document.pdf"
    DocumentOCRResults.main(pdf_path)
