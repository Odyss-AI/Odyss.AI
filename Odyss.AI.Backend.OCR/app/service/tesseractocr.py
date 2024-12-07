from io import BytesIO
import re
import zlib
from bson import ObjectId
import os
import PyPDF2
from app.user import TextChunk, Image, Document
from PIL import Image as PilImage
from app.config import Config
import pytesseract
from pix2tex.cli import LatexOCR
from pdf2image import convert_from_bytes

class OCRTesseract:
    def __init__(self):
        # Initialisiere LaTeX-OCR-Modell
        self.latex_ocr = LatexOCR()

    def extract_text(self, doc: Document):
        self.process_pdf(doc.path, doc)  # Verarbeite das konvertierte PDF
        # os.remove(doc.path)

        return doc

    def process_pdf(self, document_path, doc):
        try:
            with open(document_path, 'rb') as pdf_file:
                pdf_stream = BytesIO(pdf_file.read())
                self.extract_text_from_pdf(pdf_stream, doc)
                self.extract_images_from_pdf(pdf_stream, doc)

        except Exception as e:
            print(f"Fehler bei der Verarbeitung des PDFs: {e}")

# extraction
    def extract_text_from_pdf(self, pdf_stream, doc):
        try:
            print("Extrahiere Text aus PDF mit Tesseract OCR...")
            
            # Konvertiere PDF-Seiten in Bilder
            images = convert_from_bytes(pdf_stream.getvalue(), fmt='JPEG', poppler_path="/usr/bin/pdftoppm")

            for page_num, image in enumerate(images):
                print(f"Verarbeite Seite {page_num + 1} mit Tesseract OCR...")
                
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

    def extract_latex_from_image(self, image_path):
        try:
            print(f"Starte LaTeX-OCR für Bild {image_path}...")
            result = self.latex_ocr(image_path)
            return result if result else None
        except Exception as e:
            print(f"Fehler bei der LaTeX-OCR: {e}")
            return None
        
    def extract_formulas(self, text):
        # LaTeX-Formeln suchen (unverändert)
        formula_pattern = r'\$(.*?)\$|\\\[.*?\\\]|\\begin{.*?}.*?\\end{.*?}'
        matches = re.findall(formula_pattern, text, re.DOTALL)
        return [match.strip() for match in matches if match]


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


    def ocr_image(self, image):
        try:
            print(f"Starte Tesseract-Bildverarbeitung für OCR...")

            # Lade das Bild aus dem Stream
            image = PilImage.open(image)
            print(f"Bild erfolgreich geladen.")

            # Textextraktion mit Tesseract durchführen
            tesseract_text = pytesseract.image_to_string(image)

            if tesseract_text.strip():
                return tesseract_text
            else:
                print(f"Kein Text erkannt.")
                return ""

        except Exception as e:
            print(f"Fehler bei der Tesseract OCR: {e}")
            return ""  
