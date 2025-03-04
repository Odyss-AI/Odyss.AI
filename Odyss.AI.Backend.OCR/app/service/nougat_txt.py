import os
import torch
from transformers import AutoProcessor, AutoModelForVision2Seq, StoppingCriteriaList
from pathlib import Path
from pdf2image import convert_from_path
from PIL import Image as PilImage
from StoppingCriteraScores import StoppingCriteriaScores
from io import BytesIO

class OCRNougat:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.processor = AutoProcessor.from_pretrained("facebook/nougat-base")
        self.model = AutoModelForVision2Seq.from_pretrained("facebook/nougat-base").to(self.device)
        self.model.config.max_position_embeddings = 8192  # Falls Text abgeschnitten wird
        self.model.eval()

    def extract_text(self, image_stream):
        try:
            print(f"Starte Bildverarbeitung für OCR...")

            # Umwandlung des Bilds in BytesIO-Stream
            with BytesIO() as img_byte_arr:
                image_stream.save(img_byte_arr, format='PNG')  # Speichern als PNG
                img_byte_arr.seek(0)  # Zurück zum Anfang des Streams

                # Bild aus dem Byte-Stream laden
                image = PilImage.open(img_byte_arr).convert("RGB")

            # Bild für das Modell vorbereiten
            pixel_values = self.processor(images=image, return_tensors="pt").pixel_values

            # Textextraktion durchführen ohne benutzerdefinierte StoppingCriteria
            outputs = self.model.generate(
                pixel_values.to(self.device),
                min_length=1,
                max_length=3584,
                bad_words_ids=[[self.processor.tokenizer.unk_token_id]],  # Filter für unbekannte Tokens
                return_dict_in_generate=True,
                output_scores=True,
                stopping_criteria=StoppingCriteriaList([StoppingCriteriaScores()])
            )

            # Überprüfen, ob Ausgabe generiert wurde
            if not outputs or len(outputs[0]) == 0:
                print("Kein Text generiert.")
                return ""  # Leeren String zurückgeben, wenn nichts erkannt wurde

            # Ergebnis dekodieren
            generated_text = self.processor.batch_decode(outputs[0], skip_special_tokens=True)[0]

            # Gebe den erkannten Text zurück, wenn vorhanden, ansonsten leeren String
            if generated_text.strip():
                print(f"Texterkennung abgeschlossen. Erkannt: {generated_text}")
                return generated_text
            else:
                print(f"Kein Text erkannt.")
                return ""

        except Exception as e:
            print(f"Fehler bei der OCR für Bild: {e}")
            return ""  # Stelle sicher, dass "" zurückgegeben wird, falls ein Fehler auftritt


# Verzeichnisse definieren
PDF_DIR = './Odyss.AI.Backend.LLM/Paper'
OUTPUT_DIR = './nougat_txt_extraction'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# OCR-Modell instanziieren
ocr_nougat = OCRNougat()

# Alle PDFs im Verzeichnis verarbeiten
for pdf_path in Path(PDF_DIR).glob("*.pdf"):
    images = convert_from_path(str(pdf_path))  # PDF in Bilder umwandeln
    pdf_name = pdf_path.stem  # Dokumentname ohne Endung
    
    for page_num, image in enumerate(images, start=1):
        text_output = ocr_nougat.extract_text(image)
        
        # Datei speichern
        if text_output.strip():  # Nur speichern, wenn Text extrahiert wurde
            txt_filename = f"{pdf_name}_page_{page_num}.txt"
            txt_path = os.path.join(OUTPUT_DIR, txt_filename)
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(text_output)
            print(f"Textextraktion für Seite {page_num} abgeschlossen.")
        else:
            print(f"Kein Text für Seite {page_num} extrahiert.")

print("Extraktion abgeschlossen. Ergebnisse im Ordner 'nougat_txt_extraction'.")
