from difflib import SequenceMatcher
from rapidfuzz.distance import Levenshtein
from PyPDF2 import PdfReader
import time
import os
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
            
            return self._normalize_text(ground_truth_text)
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
                "text": self._normalize_text(ocr_text),
                "processing_time": processing_time
            }

    def _extract_text_from_document(self, document):
        # Extrahiert Text aus den Textchunks des Documents
        return "\n".join(chunk.text for chunk in document.textList).strip()

    @staticmethod
    def _normalize_text(text):
        """Normalisiert den Text durch Entfernen von überflüssigen Leerzeichen, Zeilenumbrüchen und Vereinheitlichung."""
        import re
        text = text.lower()  # Kleinbuchstaben
        text = re.sub(r'\s+', ' ', text).strip()  # Mehrfache Leerzeichen entfernen
        text = text.replace("\n", " ").replace("\n\n", "")
        return text

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
            print(f"Fehlerrate (WER): {metrics['word_error_rate']:.2f}%")
            print(f"Verarbeitungszeit: {metrics['processing_time']:.2f} Sekunden")
            print(f"Levenshtein-Distanz: {metrics['levenshtein_distance']}")
            print(f"Ähnlichkeitsrate: {metrics['similarity_ratio']:.2f}%")

    def _calculate_metrics(self, ocr_text):
        levenshtein_distance = Levenshtein.distance(self.ground_truth, ocr_text)
        char_accuracy = self._calculate_char_accuracy(self.ground_truth, ocr_text)
        similarity_ratio = SequenceMatcher(None, self.ground_truth, ocr_text).ratio() * 100
        char_error_rate = self._calculate_char_error_rate(self.ground_truth, levenshtein_distance)
        word_error_rate = self._calculate_word_error_rate(self.ground_truth, ocr_text)

        return {
            "levenshtein_distance": levenshtein_distance,
            "char_accuracy": char_accuracy,
            "char_error_rate": char_error_rate,
            "word_error_rate": word_error_rate,
            "similarity_ratio": similarity_ratio,
        }

    @staticmethod
    def _calculate_char_accuracy(ground_truth, ocr_text):
        min_length = min(len(ground_truth), len(ocr_text))
        max_length = max(len(ground_truth), len(ocr_text))

        correct_chars = sum(1 for i in range(min_length) if ground_truth[i] == ocr_text[i])

        return (correct_chars / max_length) * 100 if max_length > 0 else 0

    @staticmethod
    def _calculate_char_error_rate(ground_truth, levenshtein_distance):
        ground_truth_length = len(ground_truth)
        return (levenshtein_distance / ground_truth_length) * 100 if ground_truth_length > 0 else 0

    @staticmethod
    def _calculate_word_error_rate(ground_truth, ocr_text):
        gt_words = ground_truth.split()
        ocr_words = ocr_text.split()

        levenshtein_distance = Levenshtein.distance(gt_words, ocr_words)
        return (levenshtein_distance / len(gt_words)) * 100 if len(gt_words) > 0 else 0

    @staticmethod
    def process_folder(folder_path):
        pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
        aggregated_results = {}

        for pdf_file in pdf_files:
            print(f"\nVerarbeite Datei: {pdf_file}")
            pdf_path = os.path.join(folder_path, pdf_file)
            ocr_comparator = DocumentOCRResults(pdf_path)

            ocr_engines = {
                "Tesseract": OCRTesseract(),
                "PaddleOCR": OCRPaddle(),
                "Nougat": OCRNougat()
            }

            ocr_comparator.run_ocr(ocr_engines)

            for ocr_name, data in ocr_comparator.ocr_results.items():
                if ocr_name not in aggregated_results:
                    aggregated_results[ocr_name] = {
                        "char_accuracy": [],
                        "char_error_rate": [],
                        "word_error_rate": [],
                        "similarity_ratio": [],
                        "processing_time": []
                    }

                metrics = ocr_comparator._calculate_metrics(data['text'])
                aggregated_results[ocr_name]["char_accuracy"].append(metrics['char_accuracy'])
                aggregated_results[ocr_name]["char_error_rate"].append(metrics['char_error_rate'])
                aggregated_results[ocr_name]["word_error_rate"].append(metrics['word_error_rate'])
                aggregated_results[ocr_name]["similarity_ratio"].append(metrics['similarity_ratio'])
                aggregated_results[ocr_name]["processing_time"].append(data['processing_time'])

        print("\n=== Durchschnittliche Ergebnisse ===")
        for ocr_name, metrics in aggregated_results.items():
            print(f"\n--- {ocr_name} ---")
            print(f"Durchschnittliche Textgenauigkeit: {sum(metrics['char_accuracy']) / len(metrics['char_accuracy']):.2f}%")
            print(f"Durchschnittliche Fehlerrate (CER): {sum(metrics['char_error_rate']) / len(metrics['char_error_rate']):.2f}%")
            print(f"Durchschnittliche Fehlerrate (WER): {sum(metrics['word_error_rate']) / len(metrics['word_error_rate']):.2f}%")
            print(f"Durchschnittliche Ähnlichkeitsrate: {sum(metrics['similarity_ratio']) / len(metrics['similarity_ratio']):.2f}%")
            print(f"Durchschnittliche Verarbeitungszeit: {sum(metrics['processing_time']) / len(metrics['processing_time']):.2f} Sekunden")

# Wenn die Datei direkt ausgeführt wird
if __name__ == "__main__":
    folder_path = "C:\\Users\\ramaz\\Documents\\PDF_Folder"
    DocumentOCRResults.process_folder(folder_path)
