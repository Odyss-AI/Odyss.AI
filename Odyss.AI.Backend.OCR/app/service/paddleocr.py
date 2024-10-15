from io import BytesIO
import zlib
from bson import ObjectId
import os
import PyPDF2
from pptxtopdf import convert as pptx_to_pdf
from docx2pdf import convert as docx_to_pdf
from app.user import TextChunk, Image
from PIL import Image as PilImage
from app.config import Config
from paddleocr import PaddleOCR  # PaddleOCR importieren

class OCRPaddle:
    def __init__(self):
        # PaddleOCR initialisieren (kann angepasst werden je nach Sprache)
        self.ocr = PaddleOCR(use_angle_cls=True, lang='de')  # Für deutsche Texte 'de' wählen

    def extract_text(self, doc, document_path):
        # Prüfe den Typ des Dokuments basierend auf dem Dateipfad
        file_extension = os.path.splitext(document_path)[1].lower()

        if file_extension == ".pdf":
            # Direkt PDF verarbeiten
            self.process_pdf(document_path, doc)
        elif file_extension in [".docx", ".pptx"]:
            # Konvertiere zu PDF und dann verarbeite das konvertierte PDF
            converted_pdf_path = self.convert_docx_or_pptx_to_pdf(document_path)
            self.process_pdf(converted_pdf_path, doc)
            os.remove(converted_pdf_path)  # Lösche das konvertierte PDF nach der Verarbeitung
        else:
            print("Unsupported file type")

        return doc

    def process_pdf(self, document_path, doc):
        with open(document_path, 'rb') as pdf_file:
            pdf_stream = BytesIO(pdf_file.read())
            page_texts = self.extract_text_from_pdf(pdf_stream)
            for page_text, page_num in page_texts:
                self.split_text_into_chunks(page_text, doc, page_num)

            self.extract_images_from_pdf(pdf_stream, doc)

    def convert_docx_or_pptx_to_pdf(self, document_path):
        try:
            if document_path.endswith(".docx"):
                docx_to_pdf(document_path)
            elif document_path.endswith(".pptx"):
                pptx_to_pdf(document_path, Config.LOCAL_DOC_PATH)
        except Exception as e:
            raise Exception(f"Error during conversion: {e}")

        # Rückgabe des Pfads zur neuen PDF-Datei
        return document_path.replace('.docx', '.pdf').replace('.pptx', '.pdf')

    def extract_text_from_pdf(self, pdf_stream):
        full_text = ""
        page_texts = []
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_stream)
            for page_num, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                if page_text:
                    full_text += f"{page_text.strip()}\n"
                    page_texts.append((page_text.strip(), page_num + 1))
                else:
                    page_texts.append(("", page_num + 1))
            
            if not full_text.strip():  # If no text was found
                full_text = ""  # Return empty string for image-only documents

        except Exception as e:
            print(f"Error extracting text from PDF: {e}")

        return page_texts

    def extract_images_from_pdf(self, pdf_stream, doc):
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_stream)
            
            for page_num, page in enumerate(pdf_reader.pages):
                resources = page.get("/Resources").get_object()
                xobjects = resources.get("/XObject")
                
                if xobjects:
                    xobjects = xobjects.get_object()
                    image_counter = 1
                    
                    for obj in xobjects:
                        xobject = xobjects[obj].get_object()
                        
                        if xobject["/Subtype"] == "/Image":
                            try:
                                width = xobject["/Width"]
                                height = xobject["/Height"]

                                # Daten extrahieren
                                data = xobject._data
                                file_extension = "png"

                                # Überprüfe auf vorhandene Filter und dekodiere entsprechend
                                if "/Filter" in xobject:
                                    if xobject["/Filter"] == "/FlateDecode":
                                        try:
                                            data = zlib.decompress(data)
                                            img = PilImage.frombytes("RGB", (width, height), data)
                                        except Exception as e:
                                            print(f"Fehler beim Dekomprimieren von Bild {image_counter} auf Seite {page_num + 1}: {e}")
                                            continue
                                    elif xobject["/Filter"] == "/DCTDecode":
                                        file_extension = "jpg"
                                        img = PilImage.open(BytesIO(data))
                                    elif xobject["/Filter"] == "/JPXDecode":
                                        file_extension = "jp2"
                                        img = PilImage.open(BytesIO(data))
                                    else:
                                        print(f"Unbekannter Filter {xobject['/Filter']} für Bild {image_counter} auf Seite {page_num + 1}")
                                        continue

                                # OCR auf dem Bild ausführen
                                print(f"Starte OCR für Bild {image_counter} auf Seite {page_num + 1}...")
                                img_text = self.ocr_image(img)  # PaddleOCR-Funktion

                                # Erstelle ein Image-Objekt
                                image_obj = Image(
                                    id=str(ObjectId()),
                                    link=f"extracted_image_{page_num + 1}_{image_counter}.{file_extension}",
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

    def split_text_into_chunks(self, full_text, doc, page_num):
        chunks = full_text.split('\n\n')
        for chunk in chunks:
            if chunk.strip():
                text_chunk = TextChunk(id=str(ObjectId()), text=chunk.strip(), page=page_num)
                doc.textList.append(text_chunk)

    def ocr_image(self, image):
        try:
            print(f"Starte PaddleOCR-Bildverarbeitung für OCR...")

            # Textextraktion mit PaddleOCR durchführen
            ocr_result = self.ocr.ocr(image)

            extracted_text = "\n".join([line[1][0] for line in ocr_result])

            if extracted_text.strip():
                print(f"OCR erfolgreich. Erkannt: {extracted_text}")
                return extracted_text
            else:
                print(f"Kein Text erkannt.")
                return ""

        except Exception as e:
            print(f"Fehler bei der PaddleOCR: {e}")
            return ""
        
