import os
import json
import time
import re
from difflib import SequenceMatcher
from collections import Counter
from bs4 import BeautifulSoup
from rapidfuzz.distance import Levenshtein
import jiwer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import jaccard_score
from app.service.tesseractocr import OCRTesseract
from app.service.paddleocr import OCRPaddle
from app.user import Document

def clean_text_ocr(text):
    """Bereinigt den Text für den OCR-Vergleich, behält Groß-/Kleinschreibung sowie mathematische Zeichen."""
    text = re.sub(r'[^\w\s\-\.\+\*\/\^]', '', text)  # Entfernt unerwünschte Zeichen, behält aber mathematische Operatoren
    text = re.sub(r'\s+', ' ', text).strip()  # Mehrfache Leerzeichen reduzieren
    return text

def calculate_jaccard_similarity(reference, hypothesis):
    """Berechnet die Jaccard-Ähnlichkeit mit Scikit-learn."""
    ref_words = set(reference.split())
    hyp_words = set(hypothesis.split())

    all_words = list(ref_words | hyp_words)
    y_true = [1 if word in ref_words else 0 for word in all_words]
    y_pred = [1 if word in hyp_words else 0 for word in all_words]

    return jaccard_score(y_true, y_pred) * 100

def cosine_similarity_metric(text1, text2):
    """Berechnet die Cosine Similarity zwischen zwei Texten."""
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english").fit_transform([text1, text2])
    vectors = vectorizer.toarray()
    return cosine_similarity([vectors[0]], [vectors[1]])[0][0] * 100

def calculate_word_error_rate(reference, hypothesis):
    """Berechnet die Word Error Rate (WER) mit JiWER."""
    return jiwer.wer(reference, hypothesis) * 100  # Prozentwert

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

class DocumentOCRResults3:
    def __init__(self, pdf_path, html_path, nougat_txt_folder):
        self.pdf_path = pdf_path
        self.html_path = html_path
        self.nougat_txt_folder = nougat_txt_folder
        self.ground_truth = self._extract_ground_truth()
        self.ocr_results = {}
        self._save_ground_truth()

    def _extract_ground_truth(self):
        """Extrahiert Ground Truth aus der HTML-Datei."""
        try:
            with open(self.html_path, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f, "html.parser")
            text = soup.get_text()
            return clean_text_ocr(text)  # Bereinigung auskommentiert
        except Exception as e:
            print(f"Fehler beim Extrahieren der Ground Truth: {e}")
            return ""

    def _save_ground_truth(self):
        """Speichert die Ground Truth als Textdatei."""
        output_folder = os.path.join("app", "service", "results3_clean_text")
        os.makedirs(output_folder, exist_ok=True)
        gt_text_file = os.path.join(output_folder, os.path.basename(self.html_path).replace(".html", "_ground_truth.txt"))
        with open(gt_text_file, "w", encoding="utf-8") as f:
            f.write(self.ground_truth)

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

    def compare_results(self):
        """Vergleicht die OCR-Ergebnisse mit der Ground Truth und speichert sie."""
        results = {}
        for ocr_name, data in self.ocr_results.items():
            metrics = self._calculate_metrics(data['text'])
            metrics['processing_time'] = data['processing_time']
            results[ocr_name] = metrics
        output_file = os.path.join("app", "service", "results3_clean_text", os.path.basename(self.pdf_path).replace(".pdf", "_OCR_Ergebnisse.json"))
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4, ensure_ascii=False)
        print(f"\nErgebnisse gespeichert in: {output_file}")

    def _extract_nougat_text(self):
        """Liest und kombiniert die TXT-Dateien für Nougat."""
        base_name = os.path.basename(self.pdf_path).replace(".pdf", "")
        text_pages = []

        print(f"Suche nach Nougat-TXT-Dateien für: {base_name}")

        txt_files = sorted(
            [f for f in os.listdir(self.nougat_txt_folder) if f.startswith(base_name) and f.endswith(".txt")],
            key=lambda x: int(x.split("_page_")[-1].split(".")[0])
        )

        if not txt_files:
            print(f"Keine Nougat-TXT-Dateien für {base_name} gefunden!")
        else:
            print(f"{len(txt_files)} Nougat-TXT-Dateien gefunden für {base_name}.")

        for txt_file in txt_files:
            file_path = os.path.join(self.nougat_txt_folder, txt_file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    page_text = f.read()
                    text_pages.append(page_text)
                    print(f"✔ Gelesen: {txt_file} ({len(page_text)} Zeichen)")
            except Exception as e:
                print(f"Fehler beim Lesen von {txt_file}: {e}")

        full_text = " ".join(text_pages)
        print(f"Vollständiger Nougat-Text hat {len(full_text)} Zeichen.")
        return clean_text_ocr(full_text)  # Bereinigung aktiv

    def run_ocr(self, ocr_engines):
        """Führt OCR mit Tesseract und PaddleOCR durch und verwendet Nougat-TXT-Daten."""
        for engine_name, engine_instance in ocr_engines.items():
            print(f"Starte OCR mit {engine_name}...")
            start_time = time.time()
            document = engine_instance.extract_text(Document(
                id="dummy_id", doc_id="dummy_doc_id", mongo_file_id="dummy_mongo_id", name=os.path.basename(self.pdf_path),
                timestamp=time.time(), summary="", imgList=[], textList=[], path=self.pdf_path
            ))
            processing_time = time.time() - start_time
            ocr_text = clean_text_ocr(" ".join(chunk.text for chunk in document.textList))  # Bereinigung aktiv
            self.ocr_results[engine_name] = {"text": ocr_text, "processing_time": processing_time}
            self._save_ocr_text(engine_name, ocr_text)

        # Füge die Nougat-TXT-Extraktion als OCR-Ergebnis hinzu
        nougat_text = self._extract_nougat_text()
        self.ocr_results["Nougat-TXT"] = {
            "text": nougat_text,
            "processing_time": 0  # Kein Laufzeitbedarf
        }
        self._save_ocr_text("Nougat-TXT", nougat_text)

    def _save_ocr_text(self, engine_name, text):
        """Speichert den extrahierten OCR-Text als Datei."""
        output_folder = os.path.join("app", "service", "results3_clean_text")
        os.makedirs(output_folder, exist_ok=True)
        ocr_text_file = os.path.join(output_folder, f"{os.path.basename(self.pdf_path).replace('.pdf', '')}_{engine_name}_text.txt")
        with open(ocr_text_file, "w", encoding="utf-8") as f:
            f.write(text)

    @staticmethod
    def process_folder(dataset_root):
        """Verarbeitet alle PDFs in `paper_pdfs/` und vergleicht sie mit `paper_htmls/`."""
        pdf_folder = os.path.join(dataset_root, "paper_pdfs")
        html_folder = os.path.join(dataset_root, "paper_htmls")
        nougat_txt_folder = os.path.join(dataset_root, "nougat_txt_extraction")

        pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]

        for pdf_file in pdf_files:
            print(f"\nVerarbeite Datei: {pdf_file}")
            pdf_path = os.path.join(pdf_folder, pdf_file)
            html_path = os.path.join(html_folder, pdf_file.replace(".pdf", ".html"))

            if not os.path.exists(html_path):
                print(f"Keine HTML-Ground-Truth für {pdf_file} gefunden!")
                continue

            ocr_comparator = DocumentOCRResults3(pdf_path, html_path, nougat_txt_folder)

            ocr_engines = {
                "Tesseract": OCRTesseract(),
                "PaddleOCR": OCRPaddle()
            }

            ocr_comparator.run_ocr(ocr_engines)
            ocr_comparator.compare_results()

if __name__ == "__main__":
    dataset_root = os.path.join("app", "service", "dataset_root")
    DocumentOCRResults3.process_folder(dataset_root)
