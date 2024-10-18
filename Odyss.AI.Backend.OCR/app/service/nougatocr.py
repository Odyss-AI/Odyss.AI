from io import BytesIO
import zlib
from bson import ObjectId
from torch import device
import torch
from transformers import AutoProcessor, AutoModelForVision2Seq, StoppingCriteriaList 
import os
import PyPDF2
from pptxtopdf import convert as pptx_to_pdf
from docx2pdf import convert as docx_to_pdf
from app.user import Document, TextChunk, Image
from PIL import Image as PilImage
from app.config import Config
from .StoppingCriteraScores import StoppingCriteriaScores

class OCRNougat:
    def __init__(self):
        self.device = device("cuda" if torch.cuda.is_available() else "cpu")
        # Nougat Modell und Prozessor laden
        self.processor = AutoProcessor.from_pretrained("facebook/nougat-base")
        self.model = AutoModelForVision2Seq.from_pretrained("facebook/nougat-base")

    def extract_text(self, doc, document_path):
        print(f"Extrahiere Text aus Dokument: {document_path}")
        
        # Prüfe den Typ des Dokuments basierend auf dem Dateipfad
        file_extension = os.path.splitext(document_path)[1].lower()
        print(f"Dokumenttyp erkannt: {file_extension}")

        if file_extension == ".pdf":
            # Direkt PDF verarbeiten
            print(f"Starte Verarbeitung des PDF-Dokuments: {document_path}")
            self.process_pdf(document_path, doc)
        elif file_extension in [".docx", ".pptx"]:
            # Konvertiere zu PDF und dann verarbeite das konvertierte PDF
            print(f"Konvertiere {file_extension}-Dokument zu PDF...")
            converted_pdf_path = self.convert_docx_or_pptx_to_pdf(document_path)
            print(f"Verarbeite konvertiertes PDF: {converted_pdf_path}")
            self.process_pdf(converted_pdf_path, doc)
            os.remove(converted_pdf_path)  # Lösche das konvertierte PDF nach der Verarbeitung
            print(f"Lösche temporäre Datei: {converted_pdf_path}")
        else:
            print("Nicht unterstützter Dateityp")

        return doc

# Convert
    def process_pdf(self, document_path, doc):
        print(f"Öffne PDF für die Verarbeitung: {document_path}")
        with open(document_path, 'rb') as pdf_file:
            pdf_stream = BytesIO(pdf_file.read())
            page_texts = self.extract_text_from_pdf(pdf_stream)
            print(f"{len(page_texts)} Seiten im PDF erkannt")

            for page_text, page_num in page_texts:
                print(f"Verarbeite Seite {page_num}")
                self.split_text_into_chunks(page_text, doc, page_num)

            self.extract_images_from_pdf(pdf_stream, doc)

    def convert_docx_or_pptx_to_pdf(self, document_path):
        try:
            print(f"Konvertiere {document_path} zu PDF...")
            if document_path.endswith(".docx"):
                docx_to_pdf(document_path)
            elif document_path.endswith(".pptx"):
                pptx_to_pdf(document_path, Config.LOCAL_DOC_PATH)
        except Exception as e:
            raise Exception(f"Fehler während der Konvertierung: {e}")

        return document_path.replace('.docx', '.pdf').replace('.pptx', '.pdf')

# extraction
    def extract_text_from_pdf(self, pdf_stream):
        full_text = ""
        page_texts = []
        try:
            print("Extrahiere Text aus PDF...")
            pdf_reader = PyPDF2.PdfReader(pdf_stream)
            for page_num, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                if page_text:
                    print(f"Text auf Seite {page_num + 1} erkannt.")
                    full_text += f"{page_text.strip()}\n"
                    page_texts.append((page_text.strip(), page_num + 1))
                else:
                    print(f"Kein Text auf Seite {page_num + 1} erkannt.")
                    page_texts.append(("", page_num + 1))
            
            if not full_text.strip():  # If no text was found
                print("Kein Text im gesamten Dokument erkannt. Möglicherweise bildbasiertes PDF.")
                full_text = ""  # Return empty string for image-only documents

        except Exception as e:
            print(f"Fehler beim Extrahieren des Textes aus dem PDF: {e}")

        return page_texts


    def extract_images_from_pdf(self, pdf_stream, doc):
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_stream)
            
            for page_num, page in enumerate(pdf_reader.pages):
                resources = page.get("/Resources").get_object()
                xobjects = resources.get("/XObject")
                
                if xobjects:
                    xobjects = xobjects.get_object()
                    image_counter = 1  # Image counter für jede Seite zurücksetzen
                    
                    for obj in xobjects:
                        xobject = xobjects[obj].get_object()
                        
                        if xobject["/Subtype"] == "/Image":
                            try:
                                width = xobject["/Width"]
                                height = xobject["/Height"]

                                # Daten extrahieren
                                data = xobject._data
                                file_extension = "png"  # Standard PNG verwenden

                                # Überprüfe auf vorhandene Filter und dekodiere entsprechend
                                if "/Filter" in xobject:
                                    if xobject["/Filter"] == "/FlateDecode":
                                        try:
                                            data = zlib.decompress(data)  # Dekomprimiere die FlateDecode-Daten
                                            img = PilImage.frombytes("RGB", (width, height), data)
                                        except Exception as e:
                                            print(f"Fehler beim Dekomprimieren von Bild {image_counter} auf Seite {page_num + 1}: {e}")
                                            continue
                                    elif xobject["/Filter"] == "/DCTDecode":
                                        file_extension = "jpg"
                                    elif xobject["/Filter"] == "/JPXDecode":
                                        file_extension = "jp2"
                                    else:
                                        print(f"Unbekannter Filter {xobject['/Filter']} für Bild {image_counter} auf Seite {page_num + 1}")
                                        continue

                                # Speicherpfad für das Bild
                                img_save_path = os.path.join(Config.LOCAL_DOC_PATH, f"extracted_image_{page_num+1}_{image_counter}.{file_extension}")

                                # Speichere das Bild basierend auf dem Filtertyp
                                img.save(img_save_path)
                                print(f"Bild {image_counter} auf Seite {page_num + 1} erfolgreich gespeichert als {img_save_path}.")

                                # OCR auf dem Bild ausführen
                                print(f"Starte OCR für Bild {image_counter} auf Seite {page_num + 1}...")
                                img_text = self.ocr_image(img_save_path)  # Tesseract OCR-Funktion

                                # Erstelle ein TextChunk für den OCR-Text und füge es zur textList hinzu
                                if img_text.strip():  # Nur hinzufügen, wenn Text erkannt wurde
                                    self.split_text_into_chunks(img_text, doc, page_num)  # OCR-Text in Chunks speichern

                                # Erstelle ein Image-Objekt
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
                                print(f"Fehler beim Verarbeiten des Bildes für Objekt {obj} auf Seite {page_num + 1}: {e}")

        except Exception as e:
            print(f"Fehler beim Extrahieren der Bilder aus dem PDF: {e}")

        print(f"Image extraction complete. Images found: {len(doc.imgList)}")


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
    