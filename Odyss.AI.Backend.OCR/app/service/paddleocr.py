from io import BytesIO
import zlib
from bson import ObjectId
import os
import PyPDF2
import numpy as np
from app.user import TextChunk, Image, Document
from PIL import Image as PilImage
from app.config import Config
from paddleocr import PaddleOCR  # PaddleOCR importieren

class OCRPaddle:
    def __init__(self):
        # PaddleOCR initialisieren (kann angepasst werden je nach Sprache)
        print("Initialisiere PaddleOCR mit englischer Sprache...")
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en')  # Für deutsche Texte 'de' wählen

    def extract_text(self, doc: Document):
        self.process_pdf(doc.path, doc)
        # os.remove(doc.path)  # Lösche das konvertierte PDF nach der Verarbeitung
        return doc

    def process_pdf(self, document_path, doc):
        try:
            with open(document_path, 'rb') as pdf_file:
                pdf_stream = BytesIO(pdf_file.read())
                self.extract_text_from_pdf(pdf_stream, doc)
                self.extract_images_from_pdf(pdf_stream, doc)

        except Exception as e:
            print(f"Fehler bei der Verarbeitung des PDFs: {e}")

        return document_path.replace('.docx', '.pdf').replace('.pptx', '.pdf')

    def extract_text_from_pdf(self, pdf_stream, doc):
        try:
            print("Extrahiere Text aus PDF mit PaddleOCR...")

            # Konvertiere PDF-Seiten in Bilder
            from pdf2image import convert_from_bytes
            images = convert_from_bytes(pdf_stream.getvalue(), fmt='JPEG')

            for page_num, image in enumerate(images):
                print(f"Verarbeite Seite {page_num + 1} mit PaddleOCR...")

                # Wandle das Bild in einen Byte-Stream für die OCR-Methode um
                img_byte_stream = BytesIO()
                image.save(img_byte_stream, format='JPEG')
                img_byte_stream.seek(0)

                # Führe OCR auf dem Bild aus
                page_text = self.ocr_image(img_byte_stream)

                # Prüfe, ob Text erkannt wurde
                if page_text.strip():
                    print(f"Text auf Seite {page_num + 1} erkannt.")
                    # Text in Chunks aufteilen und hinzufügen
                    self.split_text_into_chunks(page_text.strip(), doc, page_num + 1)
                else:
                    print(f"Kein Text auf Seite {page_num + 1} erkannt.")
        except Exception as e:
            print(f"Fehler beim Extrahieren des Textes aus dem PDF: {e}")


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
                                print(f"Bild auf Seite {page_num + 1}: Breite={width}, Höhe={height}, Filter={xobject.get('/Filter')}, Datenlänge={len(data)}")

                                # Debugging und Analyse bei unbekanntem Filter
                                if "/Filter" not in xobject or xobject["/Filter"] not in ["/FlateDecode", "/DCTDecode", "/JPXDecode"]:
                                    raw_save_path = os.path.join(Config.LOCAL_IMG_PATH, f"raw_image_{page_num + 1}_{image_counter}.bin")
                                    with open(raw_save_path, "wb") as f:
                                        f.write(data)
                                    print(f"Rohdaten für Bild {image_counter} auf Seite {page_num + 1} gespeichert: {raw_save_path}")
                                    continue

                                file_extension = "png"  # Standard PNG verwenden
                                img_save_path = None

                                # Überprüfe auf vorhandene Filter und dekodiere entsprechend
                                if "/Filter" in xobject:
                                    if xobject["/Filter"] == "/FlateDecode":
                                        try:
                                            data = zlib.decompress(data)
                                            img = PilImage.frombytes("RGB", (width, height), data)
                                            img_save_path = os.path.join(
                                                Config.LOCAL_IMG_PATH,
                                                f"extracted_image_{page_num + 1}_{image_counter}.png"
                                            )
                                            img.save(img_save_path)
                                        except Exception as e:
                                            print(f"Fehler beim Verarbeiten von FlateDecode: {e}")
                                            continue
                                    elif xobject["/Filter"] == "/DCTDecode":
                                        file_extension = "jpg"
                                        img_save_path = os.path.join(
                                            Config.LOCAL_IMG_PATH,
                                            f"extracted_image_{page_num + 1}_{image_counter}.{file_extension}"
                                        )
                                        with open(img_save_path, "wb") as f:
                                            f.write(data)  # Speichere die Rohdaten direkt
                                    elif xobject["/Filter"] == "/JPXDecode":
                                        file_extension = "jp2"
                                        img_save_path = os.path.join(
                                            Config.LOCAL_IMG_PATH,
                                            f"extracted_image_{page_num + 1}_{image_counter}.{file_extension}"
                                        )
                                        with open(img_save_path, "wb") as f:
                                            f.write(data)  # Speichere die Rohdaten direkt
                                    else:
                                        print(f"Unbekannter Filter {xobject['/Filter']} für Bild {image_counter}")
                                        continue

                                if img_save_path:
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

    def split_text_into_chunks(self, full_text, doc, page_num, max_chunk_size=512):
        # Text in Wörter aufteilen
        words = full_text.split()

        # Temporäre Liste, um Wörter zwischenzuspeichern
        chunk_text = []
        
        # Schleife durch alle Wörter im Text
        for idx, word in enumerate(words):
            chunk_text.append(word)  # Füge das Wort dem aktuellen Chunk hinzu

            # Wenn der Chunk die maximale Anzahl von Wörtern erreicht, erstelle einen neuen TextChunk
            if len(chunk_text) >= max_chunk_size:
                text_chunk = TextChunk(id=str(ObjectId()), text=" ".join(chunk_text), page=page_num)
                doc.textList.append(text_chunk)
                chunk_text = []  # Leere den temporären Chunk, um mit dem nächsten zu starten

        # Wenn nach der Schleife noch ein nicht leerer Chunk übrig ist, füge ihn ebenfalls hinzu
        if chunk_text:
            text_chunk = TextChunk(id=str(ObjectId()), text=" ".join(chunk_text), page=page_num)
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


