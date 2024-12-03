from io import BytesIO
import zlib
from bson import ObjectId
from torch import device
import torch
from transformers import AutoProcessor, AutoModelForVision2Seq, StoppingCriteriaList 
import os
from PyPDF2 import PdfReader
from app.user import Document, TextChunk, Image
from PIL import Image as PilImage
from app.config import Config
from .StoppingCriteraScores import StoppingCriteriaScores
from pdf2image import convert_from_bytes

class OCRNougat:
    def __init__(self):
        self.device = device("cuda" if torch.cuda.is_available() else "cpu")
        # Nougat Modell und Prozessor laden
        self.processor = AutoProcessor.from_pretrained("facebook/nougat-base")
        self.model = AutoModelForVision2Seq.from_pretrained("facebook/nougat-base")

    def extract_text(self, doc: Document):
        self.process_pdf(doc.path, doc)
        # os.remove(doc.path)  # Lösche das konvertierte PDF nach der Verarbeitung

        return doc

# Process
    def process_pdf(self, document_path, doc):
        print(f"Öffne PDF für die Verarbeitung: {document_path}")
        with open(document_path, 'rb') as pdf_file:
            pdf_stream = BytesIO(pdf_file.read())
            page_texts = self.extract_text_from_pdf(pdf_stream)
            print(f"{len(page_texts)} Seiten im PDF erkannt")

            for page_text, page_num in page_texts:
                print(f"Verarbeite Seite {page_num}")
                
                # Wende `split_text_into_chunks` direkt auf den Text an
                self.split_text_into_chunks(page_text, doc, page_num)

            # Extrahiere Bilder
            self.extract_images_from_pdf(pdf_stream, doc)

# extraction
    def extract_text_from_pdf(self, pdf_stream):
        page_texts = []
        try:
            print("Extrahiere Text aus PDF mit Nougat OCR...")
            
            # Konvertiere PDF-Seiten in Bilder
            images = convert_from_bytes(pdf_stream.getvalue(), fmt='JPEG')
            print(f"{len(images)} Seiten in Bilder konvertiert.")

            for page_num, image in enumerate(images):
                print(f"Verarbeite Seite {page_num + 1} mit Nougat OCR...")
                
                # Wandle das Bild in einen Byte-Stream für die OCR-Methode um
                img_byte_stream = BytesIO()
                image.save(img_byte_stream, format='JPEG')
                img_byte_stream.seek(0)
                
                # Führe OCR auf dem Bild aus
                page_text = self.ocr_image(img_byte_stream)
                
                # Prüfe, ob Text erkannt wurde
                if page_text.strip():
                    print(f"Text auf Seite {page_num + 1} erkannt.")
                    page_texts.append((page_text.strip(), page_num + 1))
                else:
                    print(f"Kein Text auf Seite {page_num + 1} erkannt.")
                    page_texts.append(("", page_num + 1))
                
        except Exception as e:
            print(f"Fehler beim Extrahieren des Textes aus dem PDF: {e}")

        return page_texts

    def extract_images_from_pdf(self, pdf_stream, doc):
        try:
            pdf_reader = PdfReader(pdf_stream)

            for page_num, page in enumerate(pdf_reader.pages):
                resources = page.get("/Resources")
                if resources is None:
                    print(f"Keine Ressourcen auf Seite {page_num + 1}.")
                else:
                    xobjects = resources.get("/XObject")
                    if xobjects is None:
                        print(f"Keine XObjects auf Seite {page_num + 1}.")
                    else:
                        xobjects = xobjects.get_object()
                        image_counter = 1  # Zähler für die Bilder pro Seite

                        for obj in xobjects:
                            xobject = xobjects[obj].get_object()

                            if xobject["/Subtype"] == "/Image":
                                img = None
                                try:
                                    width = xobject["/Width"]
                                    height = xobject["/Height"]
                                    data = xobject._data
                                    file_extension = "png"

                                    # Filter prüfen und entsprechende Verarbeitung
                                    filter_type = xobject.get("/Filter", None)

                                    if filter_type == "/FlateDecode":
                                        try:
                                            data = zlib.decompress(data)
                                            img = PilImage.frombytes("RGB", (width, height), data)
                                        except Exception as e:
                                            print(f"Fehler beim Dekomprimieren von FlateDecode auf Seite {page_num + 1}: {e}")

                                    elif filter_type == "/DCTDecode":
                                        file_extension = "jpg"
                                        img_save_path = os.path.join(
                                            Config.LOCAL_IMG_PATH,
                                            f"extracted_image_{page_num+1}_{image_counter}.{file_extension}"
                                        )
                                        with open(img_save_path, "wb") as f:
                                            f.write(data)
                                        img = None

                                    elif filter_type == "/JPXDecode":
                                        file_extension = "jp2"
                                        img_save_path = os.path.join(
                                            Config.LOCAL_IMG_PATH,
                                            f"extracted_image_{page_num+1}_{image_counter}.{file_extension}"
                                        )
                                        with open(img_save_path, "wb") as f:
                                            f.write(data)
                                        img = None

                                    else:
                                        print(f"Unbekannter Filter {filter_type} auf Seite {page_num + 1}, Bild {image_counter}.")

                                    # Bild speichern, falls ein PIL-Image erstellt wurde
                                    if img is not None:
                                        img_save_path = os.path.join(
                                            Config.LOCAL_IMG_PATH,
                                            f"extracted_image_{page_num+1}_{image_counter}.{file_extension}"
                                        )
                                        img.save(img_save_path)
                                        print(f"Bild {image_counter} auf Seite {page_num + 1} erfolgreich gespeichert als {img_save_path}.")

                                    # OCR auf dem Bild ausführen
                                    if os.path.exists(img_save_path):
                                        print(f"Starte OCR für Bild {image_counter} auf Seite {page_num + 1}...")
                                        img_text = self.ocr_image(img_save_path)

                                        # Text verarbeiten und hinzufügen
                                        if img_text.strip():
                                            self.split_text_into_chunks(img_text, doc, page_num)

                                        # Image-Objekt erstellen und zur imgList hinzufügen
                                        image_obj = Image(
                                            id=str(ObjectId()),
                                            link=img_save_path,
                                            page=page_num + 1,
                                            type=file_extension,
                                            imgtext=img_text if isinstance(img_text, str) else "",
                                            llm_output=""
                                        )
                                        doc.imgList.append(image_obj)

                                    image_counter += 1

                                except Exception as e:
                                    print(f"Fehler beim Verarbeiten des Bildes auf Seite {page_num + 1}, Objekt {obj}: {e}")

        except Exception as e:
            print(f"Fehler beim Extrahieren der Bilder aus dem PDF: {e}")

        print(f"Bildextraktion abgeschlossen. Gefundene Bilder: {len(doc.imgList)}")


    def split_text_into_chunks(self, full_text, doc, page_num, max_chunk_size=512, enable_chunking=True):
        # Text in Abschnitte aufteilen, die durch doppelte Zeilenumbrüche getrennt sind
        sections = full_text.split('\n\n')

        for section in sections:
            if enable_chunking:
                # Teile den Abschnitt weiter auf, wenn er länger als max_chunk_size ist
                while len(section) > max_chunk_size:
                    # Füge einen TextChunk mit max_chunk_size hinzu
                    text_chunk = TextChunk(id=str(ObjectId()), text=section[:max_chunk_size].strip(), page=page_num)
                    doc.textList.append(text_chunk)
                    section = section[max_chunk_size:]  # Rest des Abschnitts
                
            # Füge den verbleibenden Abschnitt hinzu, wenn nicht leer
            if section.strip():
                text_chunk = TextChunk(id=str(ObjectId()), text=section.strip(), page=page_num)
                doc.textList.append(text_chunk)

    def ocr_image(self, image_stream):
        try:
            print(f"Starte Bildverarbeitung für OCR...")

            # Lade das Bild aus dem Stream
            image = PilImage.open(image_stream).convert("RGB")

            # Bild für das Modell vorbereiten
            pixel_values = self.processor(images=image, return_tensors="pt").pixel_values

            # Textextraktion durchführen mit benutzerdefinierter StoppingCriteria
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
                return ""  # Leeren String zurückgeben, wenn nichts erkannt wurde

            # Ergebnis dekodieren
            generated_text = self.processor.batch_decode(outputs[0], skip_special_tokens=True)[0]

            # Postprocess the generation (optional, je nach Anwendungsfall)
            generated_text = self.processor.post_process_generation(generated_text, fix_markdown=False)

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
    