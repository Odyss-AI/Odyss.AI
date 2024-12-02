from io import BytesIO
import zlib
from bson import ObjectId
import os
from PyPDF2 import PdfReader
import numpy as np
from app.user import TextChunk, Image, Document
from PIL import Image as PilImage
from app.config import Config
from paddleocr import PaddleOCR  # PaddleOCR importieren

class OCRPaddle:
    def __init__(self):
        # PaddleOCR initialisieren (kann angepasst werden je nach Sprache)
        print("Initialisiere PaddleOCR mit deutscher Sprache...")
        self.ocr = PaddleOCR(use_angle_cls=True, lang='de')  # Für deutsche Texte 'de' wählen

    def extract_text(self, doc: Document):
        self.process_pdf(doc.path, doc)
        # os.remove(doc.path)  # Lösche das konvertierte PDF nach der Verarbeitung
        return doc

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

    # def convert_docx_or_pptx_to_pdf(self, document_path):
    #     try:
    #         print(f"Konvertiere {document_path} zu PDF...")
    #         if document_path.endswith(".docx"):
    #             docx_to_pdf(document_path)
    #         elif document_path.endswith(".pptx"):
    #             pptx_to_pdf(document_path, Config.LOCAL_DOC_PATH)
    #     except Exception as e:
    #         raise Exception(f"Fehler während der Konvertierung: {e}")

        return document_path.replace('.docx', '.pdf').replace('.pptx', '.pdf')

    def extract_text_from_pdf(self, pdf_stream):
        full_text = ""
        page_texts = []
        try:
            print("Extrahiere Text aus PDF...")
            pdf_reader = PdfReader(pdf_stream)
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
                                            Config.LOCAL_DOC_PATH,
                                            f"extracted_image_{page_num+1}_{image_counter}.{file_extension}"
                                        )
                                        with open(img_save_path, "wb") as f:
                                            f.write(data)
                                        img = None

                                    elif filter_type == "/JPXDecode":
                                        file_extension = "jp2"
                                        img_save_path = os.path.join(
                                            Config.LOCAL_DOC_PATH,
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
                                            Config.LOCAL_DOC_PATH,
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

    def split_text_into_chunks(self, full_text, doc, page_num, max_chunk_size=512, enable_chunking=False):
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
            print("Starte PaddleOCR-Bildverarbeitung für OCR...")

            # Bild aus dem übergebenen BytesIO-Stream öffnen
            img = PilImage.open(image_stream)

            # Bild in ein NumPy-Array umwandeln
            img_array = np.array(img)

            # OCR auf dem Bild ausführen
            ocr_result = self.ocr.ocr(img_array)

            # Prüfen, ob OCR-Ergebnisse vorhanden sind, und extrahieren des Textes
            if ocr_result:
                # Extrahiere den Text aus der verschachtelten Struktur
                extracted_text = "\n".join([result[1][0] for result in ocr_result[0]])
                if extracted_text.strip():
                    # print(f"OCR erfolgreich. Erkannt: {extracted_text}")
                    return extracted_text
                else:
                    # print("Kein Text erkannt.")
                    return ""
            else:
                # print("Keine OCR-Ergebnisse.")
                return ""

        except Exception as e:
            print(f"Fehler bei der PaddleOCR: {e}")
            return ""


