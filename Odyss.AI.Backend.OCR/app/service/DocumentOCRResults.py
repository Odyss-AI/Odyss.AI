from difflib import SequenceMatcher
from rapidfuzz.distance import Levenshtein
from bs4 import BeautifulSoup
import time
import os
import re
from jiwer import wer
from app.service.tesseractocr import OCRTesseract
from app.service.paddleocr import OCRPaddle
from app.service.nougatocr import OCRNougat
from app.user import Document
import json

class DocumentOCRResults:
    def __init__(self, pdf_path, html_path):
        self.pdf_path = pdf_path
        self.html_path = html_path
        self.ground_truth = self._extract_ground_truth()
        self.ocr_results = {}

    def _extract_ground_truth(self):
        """Extrahiert Ground Truth aus der HTML-Datei."""
        try:
            with open(self.html_path, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f, "html.parser")
            text = soup.get_text()
            return self._normalize_text(text)
        except Exception as e:
            print(f"Fehler beim Extrahieren der Ground Truth: {e}")
            return ""

    def run_ocr(self, ocr_engines):
        """Führt OCR mit allen angegebenen Engines durch."""
        for engine_name, engine_instance in ocr_engines.items():
            print(f"🔍 Starte OCR mit {engine_name}...")
            start_time = time.time()
            document = engine_instance.extract_text(Document(
            id="dummy_id",
            doc_id="dummy_doc_id",
            mongo_file_id="dummy_mongo_id",
            name=os.path.basename(self.pdf_path),  # Setze den Dateinamen als Dokumentnamen
            timestamp=time.time(),  # Setze aktuellen Zeitstempel
            summary="",
            imgList=[],
            textList=[],
            path=self.pdf_path
            ))
            processing_time = time.time() - start_time
            ocr_text = self._extract_text_from_document(document)
            self.ocr_results[engine_name] = {
                "text": self._normalize_text(ocr_text),
                "processing_time": processing_time
            }

    def _extract_text_from_document(self, document):
        """Extrahiert den OCR-Text aus dem Dokument-Objekt."""
        return "\n".join(chunk.text for chunk in document.textList).strip()

    @staticmethod
    def _normalize_text(text):
        """Bereinigt den Text durch Entfernen von Sonderzeichen und Normalisierung."""
        text = text.lower()
        text = re.sub(r'\s+', ' ', text).strip()
        text = text.replace("\n", " ").replace("\n\n", "")
        return text

    def compare_results(self):
        """Vergleicht die OCR-Ergebnisse mit der Ground Truth und speichert sie in 'results/'."""
        results = {}
        for ocr_name, data in self.ocr_results.items():
            metrics = self._calculate_metrics(data['text'])
            metrics['processing_time'] = data['processing_time']
            results[ocr_name] = metrics

        # Speichere die Ergebnisse im 'results/' Ordner
        results_folder = os.path.join(os.path.dirname(__file__), "results")
        os.makedirs(results_folder, exist_ok=True)  # Falls Ordner nicht existiert, erstelle ihn

        output_file = os.path.join(results_folder, os.path.basename(self.pdf_path).replace(".pdf", "_OCR_Ergebnisse.json"))
        
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4, ensure_ascii=False)

        print(f"\nErgebnisse gespeichert in: {output_file}")



    def _calculate_metrics(self, ocr_text):
        levenshtein_distance = Levenshtein.distance(self.ground_truth, ocr_text)
        similarity_ratio = SequenceMatcher(None, self.ground_truth, ocr_text).ratio() * 100
        char_error_rate = self._calculate_char_error_rate(self.ground_truth, levenshtein_distance)
        word_error_rate = wer(self.ground_truth, ocr_text) * 100
        precision, recall, f1_score = self._calculate_precision_recall_f1(self.ground_truth, ocr_text)

        return {
            "levenshtein_distance": levenshtein_distance,
            "normalized_levenshtein": levenshtein_distance / len(self.ground_truth) if len(self.ground_truth) > 0 else 0,
            "char_error_rate": char_error_rate,
            "word_error_rate": word_error_rate,
            "similarity_ratio": similarity_ratio,
            "precision": precision,
            "recall": recall,
            "f1_score": f1_score
        }


    @staticmethod
    def _calculate_char_error_rate(ground_truth, levenshtein_distance):
        return (levenshtein_distance / len(ground_truth)) * 100 if len(ground_truth) > 0 else 0

    @staticmethod
    def _calculate_precision_recall_f1(ground_truth, ocr_text):
        gt_words = set(ground_truth.split())
        ocr_words = set(ocr_text.split())

        true_positive = len(gt_words & ocr_words)
        false_positive = len(ocr_words - gt_words)
        false_negative = len(gt_words - ocr_words)

        precision = (true_positive / (true_positive + false_positive)) * 100 if (true_positive + false_positive) > 0 else 0
        recall = (true_positive / (true_positive + false_negative)) * 100 if (true_positive + false_negative) > 0 else 0
        f1_score = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

        return precision, recall, f1_score

    # @staticmethod
    # def process_folder(dataset_root):
    #     """Verarbeitet nur **ein** PDF in `paper_pdfs/` und vergleicht es mit `paper_htmls/`."""
    #     pdf_folder = os.path.join(dataset_root, "paper_pdfs")
    #     html_folder = os.path.join(dataset_root, "paper_htmls")

    #     # Wähle ein bestimmtes PDF zum Testen
    #     test_file = "2103.11879v2.pdf"

    #     if test_file not in os.listdir(pdf_folder):
    #         print(f"Datei {test_file} nicht gefunden!")
    #         return

    #     pdf_path = os.path.join(pdf_folder, test_file)
    #     html_path = os.path.join(html_folder, test_file.replace(".pdf", ".html"))

    #     if not os.path.exists(html_path):
    #         print(f"Keine HTML-Ground-Truth für {test_file} gefunden!")
    #         return

    #     print(f"\nTeste OCR mit Datei: {test_file}")

    #     ocr_comparator = DocumentOCRResults(pdf_path, html_path)

    #     ocr_engines = {
    #         "Tesseract": OCRTesseract(),
    #         "PaddleOCR": OCRPaddle(),
    #         "Nougat": OCRNougat()
    #     }

    #     ocr_comparator.run_ocr(ocr_engines)
    #     ocr_comparator.compare_results()  # Zeigt Ergebnisse für die einzelne Datei an

    @staticmethod
    def process_folder(dataset_root):
        """Verarbeitet alle PDFs in `paper_pdfs/` und vergleicht sie mit `paper_htmls/`."""
        pdf_folder = os.path.join(dataset_root, "paper_pdfs")
        html_folder = os.path.join(dataset_root, "paper_htmls")
        results_folder = os.path.join("app", "service", "results")

        os.makedirs(results_folder, exist_ok=True)  # Ordner erstellen, falls nicht vorhanden

        pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]
        aggregated_results = {}

        all_results = {}

        for pdf_file in pdf_files:
            print(f"\nVerarbeite Datei: {pdf_file}")
            pdf_path = os.path.join(pdf_folder, pdf_file)
            html_path = os.path.join(html_folder, pdf_file.replace(".pdf", ".html"))

            if not os.path.exists(html_path):
                print(f"Keine HTML-Ground-Truth für {pdf_file} gefunden!")
                continue

            ocr_comparator = DocumentOCRResults(pdf_path, html_path)

            ocr_engines = {
                "Tesseract": OCRTesseract(),
                "PaddleOCR": OCRPaddle(),
                "Nougat": OCRNougat()
            }

            ocr_comparator.run_ocr(ocr_engines)

            pdf_results = {}

            for ocr_name, data in ocr_comparator.ocr_results.items():
                if ocr_name not in aggregated_results:
                    aggregated_results[ocr_name] = {
                        "levenshtein_distance": [],
                        "normalized_levenshtein": [],
                        "char_error_rate": [],
                        "word_error_rate": [],
                        "similarity_ratio": [],
                        "precision": [],
                        "recall": [],
                        "f1_score": [],
                        "processing_time": []
                    }

                metrics = ocr_comparator._calculate_metrics(data['text'])

                # Speichere die Ergebnisse für dieses PDF
                pdf_results[ocr_name] = metrics

                # Füge Werte zur Aggregation hinzu
                aggregated_results[ocr_name]["levenshtein_distance"].append(metrics['levenshtein_distance'])
                aggregated_results[ocr_name]["normalized_levenshtein"].append(metrics['normalized_levenshtein'])
                aggregated_results[ocr_name]["char_error_rate"].append(metrics['char_error_rate'])
                aggregated_results[ocr_name]["word_error_rate"].append(metrics['word_error_rate'])
                aggregated_results[ocr_name]["similarity_ratio"].append(metrics['similarity_ratio'])
                aggregated_results[ocr_name]["precision"].append(metrics['precision'])
                aggregated_results[ocr_name]["recall"].append(metrics['recall'])
                aggregated_results[ocr_name]["f1_score"].append(metrics['f1_score'])
                aggregated_results[ocr_name]["processing_time"].append(data['processing_time'])

            # Speichere das Ergebnis für dieses einzelne PDF
            pdf_result_path = os.path.join(results_folder, f"{pdf_file.replace('.pdf', '')}_ocr_results.json")
            with open(pdf_result_path, "w", encoding="utf-8") as f:
                json.dump(pdf_results, f, indent=4)

            all_results[pdf_file] = pdf_results

            ocr_comparator.compare_results()  # Zeigt Ergebnisse pro Datei an

        # Berechne Durchschnittswerte über alle Dokumente
        avg_results = {}

        print("\n=== Durchschnittliche OCR-Ergebnisse ===")
        for ocr_name, metrics in aggregated_results.items():
            avg_results[ocr_name] = {
                "levenshtein_distance": sum(metrics['levenshtein_distance']) / len(metrics['levenshtein_distance']) if metrics['levenshtein_distance'] else 0,
                "normalized_levenshtein": sum(metrics['normalized_levenshtein']) / len(metrics['normalized_levenshtein']) if metrics['normalized_levenshtein'] else 0,
                "char_error_rate": sum(metrics['char_error_rate']) / len(metrics['char_error_rate']) if metrics['char_error_rate'] else 0,
                "word_error_rate": sum(metrics['word_error_rate']) / len(metrics['word_error_rate']) if metrics['word_error_rate'] else 0,
                "similarity_ratio": sum(metrics['similarity_ratio']) / len(metrics['similarity_ratio']) if metrics['similarity_ratio'] else 0,
                "precision": sum(metrics['precision']) / len(metrics['precision']) if metrics['precision'] else 0,
                "recall": sum(metrics['recall']) / len(metrics['recall']) if metrics['recall'] else 0,
                "f1_score": sum(metrics['f1_score']) / len(metrics['f1_score']) if metrics['f1_score'] else 0,
                "processing_time": sum(metrics['processing_time']) / len(metrics['processing_time']) if metrics['processing_time'] else 0
            }

            print(f"\n--- {ocr_name} ---")
            print(f"Levenshtein-Distanz: {avg_results[ocr_name]['levenshtein_distance']:.2f}")
            print(f"Normalisierte Levenshtein-Distanz: {avg_results[ocr_name]['normalized_levenshtein']:.4f}")
            print(f"Durchschnittliche Fehlerrate (CER): {avg_results[ocr_name]['char_error_rate']:.2f}%")
            print(f"Durchschnittliche Fehlerrate (WER): {avg_results[ocr_name]['word_error_rate']:.2f}%")
            print(f"Durchschnittliche Ähnlichkeitsrate: {avg_results[ocr_name]['similarity_ratio']:.2f}%")
            print(f"Durchschnittliche Precision: {avg_results[ocr_name]['precision']:.2f}%")
            print(f"Durchschnittliche Recall: {avg_results[ocr_name]['recall']:.2f}%")
            print(f"Durchschnittlicher F1-Score: {avg_results[ocr_name]['f1_score']:.2f}%")
            print(f"Durchschnittliche Verarbeitungszeit: {avg_results[ocr_name]['processing_time']:.2f} Sekunden")

        # Speichere Gesamtergebnisse für alle PDFs
        avg_results_path = os.path.join(results_folder, "ocr_results.json")
        with open(avg_results_path, "w", encoding="utf-8") as f:
            json.dump(avg_results, f, indent=4)

        print(f"\nAlle Ergebnisse wurden in `{results_folder}/ocr_results.json` gespeichert.")


# Wenn die Datei direkt ausgeführt wird
if __name__ == "__main__":
    dataset_root = os.path.join("app\\service\\dataset_root")
    DocumentOCRResults.process_folder(dataset_root)
