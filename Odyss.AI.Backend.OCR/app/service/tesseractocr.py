from io import BytesIO
import re
import zlib
from bson import ObjectId
import os
from PyPDF2 import PdfReader
from app.user import TextChunk, Image, Document
from PIL import Image as PilImage
from app.config import Config
import pytesseract
from pix2tex.cli import LatexOCR

class OCRTesseract:

    def __init__(self):
        # Initialisiere LaTeX-OCR-Modell
        self.latex_ocr = LatexOCR()

    def extract_text(self, doc: Document):
        self.process_pdf(doc.path, doc)  # Verarbeite das konvertierte PDF
        # Lösche das konvertierte PDF nach der Verarbeitung (optional)
        # os.remove(doc.path)

        return doc

    def process_pdf(self, document_path, doc):
        with open(document_path, 'rb') as pdf_file:
            pdf_stream = BytesIO(pdf_file.read())
            self.extract_text_and_chunks_from_pdf(pdf_stream, doc)  # Direkte Verarbeitung
            self.extract_images_from_pdf(pdf_stream, doc)  # Bilder wie gehabt verarbeiten

    def extract_text_and_chunks_from_pdf(self, pdf_stream, doc, max_chunk_size=512, enable_chunking=True):
        try:
            pdf_reader = PdfReader(pdf_stream)
            for page_num, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                formulas_found = []

                if page_text:
                    # Text in Abschnitte teilen
                    sections = page_text.strip().split('\n\n')

                    for section in sections:
                        if enable_chunking:
                            # Längere Abschnitte weiter aufteilen
                            while len(section) > max_chunk_size:
                                text_chunk = TextChunk(
                                    id=str(ObjectId()),
                                    text=section[:max_chunk_size].strip(),
                                    page=page_num + 1,
                                )
                                doc.textList.append(text_chunk)
                                section = section[max_chunk_size:]  # Rest weiterverarbeiten

                        # Rest des Abschnitts als Chunk speichern
                        if section.strip():
                            text_chunk = TextChunk(
                                id=str(ObjectId()),
                                text=section.strip(),
                                page=page_num + 1,
                            )
                            doc.textList.append(text_chunk)

                    # Formeln extrahieren (Fall A)
                    formulas_found = self.extract_formulas(page_text.strip())
                    for formula in formulas_found:
                        formula_chunk = TextChunk(
                            id=str(ObjectId()),
                            text="",  # Kein Text, nur die Formel
                            page=page_num + 1,
                            formula=[formula],
                        )
                        doc.textList.append(formula_chunk)

                else:
                    print(f"No text detected on page {page_num + 1}")

                # Wenn keine Formeln aus dem Text extrahiert wurden, setze Flag für Fall B
                if not formulas_found:
                    print(f"Keine Formeln im markierbaren Text auf Seite {page_num + 1} gefunden. Fall B aktivieren.")

        except Exception as e:
            print(f"Error extracting text and chunks from PDF: {e}")

    def extract_images_from_pdf(self, pdf_stream, doc):
        try:
            pdf_reader = PdfReader(pdf_stream)

            for page_num, page in enumerate(pdf_reader.pages):
                resources = page.get("/Resources")
                if resources is None:
                    print(f"Keine Ressourcen auf Seite {page_num + 1}.")
                    continue

                xobjects = resources.get("/XObject")
                if xobjects is None:
                    print(f"Keine XObjects auf Seite {page_num + 1}.")
                    continue

                xobjects = xobjects.get_object()
                image_counter = 1  # Zähler für die Bilder pro Seite

                for obj in xobjects:
                    xobject = xobjects[obj].get_object()

                    if xobject["/Subtype"] == "/Image":
                        try:
                            # Bild extrahieren
                            width = xobject["/Width"]
                            height = xobject["/Height"]
                            data = xobject._data
                            file_extension = "png"

                            # Speichern des Bildes
                            img_save_path = os.path.join(
                                Config.LOCAL_DOC_PATH,
                                f"extracted_image_{page_num+1}_{image_counter}.{file_extension}"
                            )
                            with open(img_save_path, "wb") as f:
                                f.write(data)

                            # LaTeX-OCR auf dem Bild ausführen (Fall B)
                            latex_result = self.extract_latex_from_image(img_save_path)
                            if latex_result:
                                formula_chunk = TextChunk(
                                    id=str(ObjectId()),
                                    text="",  # Kein Text, nur die Formel
                                    page=page_num + 1,
                                    formula=[latex_result],
                                )
                                doc.textList.append(formula_chunk)
                                print(f"LaTeX-Formel erkannt: {latex_result}")

                            image_counter += 1

                        except Exception as e:
                            print(f"Fehler beim Verarbeiten des Bildes auf Seite {page_num + 1}, Objekt {obj}: {e}")

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
        # LaTeX-Formeln suchen (Inline und Block)
        formula_pattern = r'\$(.*?)\$|\\\[.*?\\\]|\\begin{.*?}.*?\\end{.*?}'
        matches = re.findall(formula_pattern, text, re.DOTALL)

        # Bereinigen und speichern
        formulas = [match.strip() for match in matches if match]
        return formulas


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
            print(f"Starte Tesseract-Bildverarbeitung für OCR...")

            # Lade das Bild aus dem Stream
            image = PilImage.open(image_stream)
            print(f"Bild erfolgreich geladen.")

            # Textextraktion mit Tesseract durchführen
            tesseract_text = pytesseract.image_to_string(image)

            if tesseract_text.strip():
                print(f"OCR erfolgreich. Erkannt: {tesseract_text}")
                return tesseract_text
            else:
                print(f"Kein Text erkannt.")
                return ""

        except Exception as e:
            print(f"Fehler bei der Tesseract OCR: {e}")
            return ""  
