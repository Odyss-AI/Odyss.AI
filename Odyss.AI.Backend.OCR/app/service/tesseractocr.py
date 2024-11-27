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

class OCRTesseract:
    def extract_text(self, doc: Document):
        self.process_pdf(doc.path, doc)  # Verarbeite das konvertierte PDF
        # Lösche das konvertierte PDF nach der Verarbeitung (optional)
        os.remove(doc.path)

        return doc

    def process_pdf(self, document_path, doc):
        with open(document_path, 'rb') as pdf_file:
            pdf_stream = BytesIO(pdf_file.read())
            page_texts = self.extract_text_from_pdf(pdf_stream, doc)
            for page_text, page_num in page_texts:
                self.split_text_into_chunks(page_text, doc, page_num) 

            self.extract_images_from_pdf(pdf_stream, doc)

    def extract_text_from_pdf(self, pdf_stream, doc):
        full_text = ""
        page_texts = []
        formulas = []  # Liste für gefundene Formeln
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_stream)
            for page_num, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                if page_text:
                    full_text += f"{page_text.strip()}\n"
                    page_texts.append((page_text.strip(), page_num + 1))  # Seitenzahl hinzufügen
                    
                    # Suche nach mathematischen Formeln im Text
                    formulas_found = self.extract_formulas(page_text.strip())
                    formulas.append((formulas_found, page_num + 1))  # Formeln und Seitenzahl speichern
                else:
                    full_text += f"No text detected on page {page_num + 1}\n"
                    page_texts.append(("", page_num + 1))  # Leeren Text hinzufügen
                
                if not full_text.strip():  # If no text was found
                    full_text = ""  # Return empty string for image-only documents

        except Exception as e:
            print(f"Error extracting text from PDF: {e}")

        # Füge die gefundenen Formeln zur textList des Dokuments hinzu
        for formulas_on_page, page_num in formulas:
            for formula in formulas_on_page:
                text_chunk = TextChunk(id=str(ObjectId()), text="", page=page_num, formula=[formula])
                doc.textList.append(text_chunk)

        return page_texts  # Gib die Liste von Seiten zurück
    
    def extract_formulas(self, text):
        # Regex-Muster für einfache LaTeX-Formeln (z.B. $...$ oder \[...\])
        formula_pattern = r'\$(.*?)\$|\\\[(.*?)\\\]'  # Erlaube sowohl Inline- als auch Blockformeln
        matches = re.findall(formula_pattern, text)

        # Extrahiere die gefundenen Formeln
        formulas = []
        for match in matches:
            formula = match[0] if match[0] else match[1]  # Wähle den nicht leeren Teil aus
            formulas.append(formula.strip())

        return formulas

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


    def split_text_into_chunks(self, full_text, doc, page_num, max_chunk_size=512, enable_chunking=False):
        # Text in Wörter aufteilen
        words = full_text.split()

        # Variable für den aktuellen Chunk
        current_chunk = []
        word_count = 0

        for word in words:
            current_chunk.append(word)
            word_count += 1
            
            # Wenn die maximale Anzahl an Wörtern erreicht ist, speichere den Chunk und starte einen neuen
            if word_count >= max_chunk_size:
                text_chunk = TextChunk(id=str(ObjectId()), text=' '.join(current_chunk), page=page_num)
                doc.textList.append(text_chunk)
                current_chunk = []  # Leere den aktuellen Chunk
                word_count = 0  # Setze die Wortanzahl zurück

        # Falls nach der Schleife noch Wörter übrig sind, die weniger als max_chunk_size sind, füge sie als letzten Chunk hinzu
        if current_chunk:
            text_chunk = TextChunk(id=str(ObjectId()), text=' '.join(current_chunk), page=page_num)
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
