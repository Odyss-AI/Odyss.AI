from difflib import SequenceMatcher
from typing import Counter
from rapidfuzz.distance import Levenshtein
from bs4 import BeautifulSoup
import time
import os
import re
from app.service.tesseractocr import OCRTesseract
from app.service.paddleocr import OCRPaddle
from app.service.nougatocr import OCRNougat
import jiwer
from app.user import Document
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import jaccard_score
from sklearn.metrics import precision_recall_fscore_support

def clean_text_ocr(text):
    """Bereinigt den Text für den OCR-Vergleich, behält Groß-/Kleinschreibung sowie mathematische Zeichen."""
    text = re.sub(r'[^\w\s\-\.\+\*\/\^]', '', text)  # Entfernt unerwünschte Zeichen, behält aber mathematische Operatoren
    text = re.sub(r'\s+', ' ', text).strip()  # Mehrfache Leerzeichen reduzieren
    return text

def calculate_jaccard_similarity(reference, hypothesis):
    """Berechnet die Jaccard-Ähnlichkeit mit Scikit-learn."""
    ref_words = set(reference.split())
    hyp_words = set(hypothesis.split())

    # Erstelle eine gemeinsame Wortliste
    all_words = list(ref_words | hyp_words)

    # Binärvektoren für beide Texte erstellen
    y_true = [1 if word in ref_words else 0 for word in all_words]
    y_pred = [1 if word in hyp_words else 0 for word in all_words]

    return jaccard_score(y_true, y_pred) * 100


def cosine_similarity_metric(text1, text2):
    """Berechnet die Cosine Similarity zwischen zwei Texten mit Bigrammen und Stopword-Filterung."""
    vectorizer = TfidfVectorizer(ngram_range=(1,2), stop_words="english").fit_transform([text1, text2])
    vectors = vectorizer.toarray()
    return cosine_similarity([vectors[0]], [vectors[1]])[0][0] * 100

def calculate_word_error_rate(reference, hypothesis):
    """Berechnet die Word Error Rate (WER) mit JiWER."""
    wer = jiwer.wer(reference, hypothesis) * 100  # Als Prozentwert
    return wer

def calculate_precision_recall_f1(reference, hypothesis):
    """Berechnet Precision, Recall und F1-Score über Wortfrequenzen mit Counter."""
    ref_word_counts = Counter(reference.split())
    hyp_word_counts = Counter(hypothesis.split())

    true_positive = sum(min(ref_word_counts[w], hyp_word_counts[w]) for w in ref_word_counts if w in hyp_word_counts)
    false_positive = sum(hyp_word_counts[w] for w in hyp_word_counts if w not in ref_word_counts)
    false_negative = sum(ref_word_counts[w] for w in ref_word_counts if w not in hyp_word_counts)

    precision = (true_positive / (true_positive + false_positive)) * 100 if (true_positive + false_positive) > 0 else 0
    recall = (true_positive / (true_positive + false_negative)) * 100 if (true_positive + false_negative) > 0 else 0
    f1_score = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    return precision, recall, f1_score

class DocumentOCRResults2:
    def __init__(self, pdf_path, html_path):
        self.pdf_path = pdf_path
        self.html_path = html_path
        self.ground_truth = self._extract_ground_truth()
        self.ocr_results = {}
        self._save_ground_truth()

    def _extract_ground_truth(self):
        """Extrahiert Ground Truth aus der HTML-Datei und speichert sie als Textdatei."""
        try:
            with open(self.html_path, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f, "html.parser")
            text = soup.get_text()
            return clean_text_ocr(text)
        except Exception as e:
            print(f"Fehler beim Extrahieren der Ground Truth: {e}")
            return ""
    
    def _save_ground_truth(self):
        """Speichert die Ground Truth als Textdatei."""
        gt_text_file = os.path.join("app", "service", "results5", os.path.basename(self.html_path).replace(".html", "_ground_truth.txt"))
        with open(gt_text_file, "w", encoding="utf-8") as f:
            f.write(self.ground_truth)

    def _extract_text_from_document(self, document):
        """Extrahiert den OCR-Text aus dem Dokument-Objekt."""
        return clean_text_ocr(" ".join(chunk.text for chunk in document.textList))
    
    def run_ocr(self, ocr_engines):
        """Führt OCR mit allen angegebenen Engines durch."""
        for engine_name, engine_instance in ocr_engines.items():
            print(f"Starte OCR mit {engine_name}...")
            start_time = time.time()
            document = engine_instance.extract_text(Document(
                id="dummy_id", doc_id="dummy_doc_id", mongo_file_id="dummy_mongo_id", name=os.path.basename(self.pdf_path), 
                timestamp=time.time(), summary="", imgList=[], textList=[], path=self.pdf_path
            ))
            processing_time = time.time() - start_time
            ocr_text = self._extract_text_from_document(document)
            self.ocr_results[engine_name] = {"text": ocr_text, "processing_time": processing_time}
            self._save_ocr_text(engine_name, ocr_text)

    def _save_ocr_text(self, engine_name, text):
        """Speichert den extrahierten OCR-Text als Datei."""
        ocr_text_file = os.path.join("app", "service", "results5", f"{os.path.basename(self.pdf_path).replace('.pdf', '')}_{engine_name}_text.txt")
        with open(ocr_text_file, "w", encoding="utf-8") as f:
            f.write(text)

    def compare_results(self):
        """Vergleicht die OCR-Ergebnisse mit der Ground Truth und speichert sie."""
        results = {}
        for ocr_name, data in self.ocr_results.items():
            metrics = self._calculate_metrics(data['text'])
            metrics['processing_time'] = data['processing_time']
            results[ocr_name] = metrics
        output_file = os.path.join("app", "service", "results5", os.path.basename(self.pdf_path).replace(".pdf", "_OCR_Ergebnisse.json"))
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4, ensure_ascii=False)
        print(f"\nErgebnisse gespeichert in: {output_file}")
    
    def _calculate_metrics(self, ocr_text):
        levenshtein_distance = Levenshtein.distance(self.ground_truth, ocr_text)
        similarity_ratio = SequenceMatcher(None, self.ground_truth, ocr_text).ratio() * 100
        jaccard_similarity_score = calculate_jaccard_similarity(self.ground_truth, ocr_text)
        cosine_sim = cosine_similarity_metric(self.ground_truth, ocr_text)
        char_error_rate = jiwer.cer(self.ground_truth, ocr_text) * 100
        word_error_rate = calculate_word_error_rate(self.ground_truth, ocr_text)
        precision, recall, f1_score = calculate_precision_recall_f1(self.ground_truth, ocr_text)
        return {
            "levenshtein_distance": levenshtein_distance,
            "normalized_levenshtein": levenshtein_distance / len(self.ground_truth) if len(self.ground_truth) > 0 else 0,
            "char_error_rate": char_error_rate,
            "word_error_rate": word_error_rate,
            "similarity_ratio": similarity_ratio,
            "jaccard_similarity": jaccard_similarity_score,
            "cosine_similarity": cosine_sim,
            "precision": precision,
            "recall": recall,
            "f1_score": f1_score
        }
    
    @staticmethod
    def process_folder(dataset_root):
        """Verarbeitet alle PDFs in `paper_pdfs/` und vergleicht sie mit `paper_htmls/`."""
        pdf_folder = os.path.join(dataset_root, "paper_pdfs")
        html_folder = os.path.join(dataset_root, "paper_htmls")
        results_folder = os.path.join("app", "service", "results5")

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

            ocr_comparator = DocumentOCRResults2(pdf_path, html_path)

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

if __name__ == "__main__":
    dataset_root = os.path.join("app", "service", "dataset_root")
    DocumentOCRResults2.process_folder(dataset_root)
