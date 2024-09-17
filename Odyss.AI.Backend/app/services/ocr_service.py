from paddleocr import PaddleOCR
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
import os
import re
import PyPDF2
import pdfplumber
from pptxtopdf import convert as pptx_to_pdf
from docx2pdf import convert as docx_to_pdf
import hashlib
from datetime import datetime
from app.models.user import TextChunk, Image


class OCRService:
    def __init__(self):
        self.ocr = PaddleOCR(use_angle_cls=True, use_gpu=False, lang="de")
        self.processor = TrOCRProcessor.from_pretrained("microsoft/trocr-small-handwritten")
        self.model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-small-handwritten")

    def extract_text(self, doc):
        file_extension = os.path.splitext(doc.name)[1].lower()

        if file_extension == ".pdf":
            # self.process_pdf(doc) # PDF-Verarbeitung aufrufen
            print("pdf")
        elif file_extension in [".docx", ".pptx"]:
            self.convert_to_pdf(doc)  # PDF-Konvertierung aufrufen
            # self.process_pdf(doc)  # PDF-Verarbeitung aufrufen
        else:
            print("Unsupported file type. Please provide a .docx, .pptx, or .pdf file.")
        return doc
            
        # Emil tob dich aus, in doc bekommst du das Dokumentenobjekt übergeben 
        # Schau in user.py nach: Darin ist die URL, Name, usw.dwa
        # Du kannst dir ein Tool wie Insomnia holen, um direkt ein Dokument über den
        # Endpunkt zu senden und zu schauen, was du bekommst: 
        # document_routes.py -> document_manager.py --> OCRService
        # Falls du das so testen willst, frag mich einfach kurz für Einrichtung Insomnia,
        # musst auch den Pfad in document_routes.py anpassen, damit es funktioniert

        # Splitte den ausgelesenen Text in kleine Abschnitte und speichere
        # diese in doc.textlist als liste von TextChunk Objekten
        # Die TextChunks haben die Attribute ID, Text und Page
        # return das Dokumentenobjekt, daraus wird anschließend die Emebddings erstellt

        # Die erkannten Bilder werden in doc.imgList als Liste von Image Objekten gespeichert
        # Die Image Objekte haben die Attribute ID, Link, Page, Type, Imgtext und LLM_Output
        # Die Bilder sollen in OneDrie gespeichert werden, muss noch implementiert werden

        # Wichtig: Mach so viele Methoden darunter wie du brauchst für die OCR Logik, 
        # aber alle sollen hierin aufgerufen werden
        # So ist deine Logik abgekapselt und du kannst machen was du willst solange 
        # du das Dokumentenobjekt zurückgibst mit den entsprechenden Werten eingefügt

        # return doc
    
# Convert_to_PDF 
    def convert_docx_to_pdf(self, doc):
        docx_path = os.path.join(self.UPLOAD_FOLDER, doc.name)
        with open(docx_path, "wb") as f:
            f.write(doc.doclink.read())  # Speichert die Datei lokal aus dem Dokumentobjekt

        try:
            # Konvertierung von DOCX zu PDF
            docx_to_pdf(docx_path)
        except Exception as e:
            raise Exception(f"Fehler bei der Konvertierung von DOCX zu PDF: {e}")

        # Überprüfen, ob die PDF-Datei erstellt wurde
        pdf_path = docx_path.replace(".docx", ".pdf")
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"Die konvertierte PDF-Datei wurde nicht gefunden: {pdf_path}")

        return pdf_path

    def convert_pptx_to_pdf(self, doc):
        pptx_path = os.path.join(self.UPLOAD_FOLDER, doc.name)
        with open(pptx_path, "wb") as f:
            f.write(doc.doclink.read())  # Speichert die Datei lokal aus dem Dokumentobjekt

        try:
            # Konvertierung von PPTX zu PDF
            pptx_to_pdf(pptx_path, self.UPLOAD_FOLDER)
        except Exception as e:
            raise Exception(f"Fehler bei der Konvertierung von PPTX zu PDF: {e}")

        # Überprüfen, ob die PDF-Datei erstellt wurde
        pdf_path = pptx_path.replace(".pptx", ".pdf")
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"Die konvertierte PDF-Datei wurde nicht gefunden: {pdf_path}")

        return pdf_path
    
    
# handle formulas
    def extract_formulas_from_image(image_path):
        processor = TrOCRProcessor.from_pretrained("microsoft/trocr-small-handwritten")
        model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-small-handwritten")

        image = Image.open(image_path).convert("RGB")
        pixel_values = processor(image, return_tensors="pt").pixel_values
        generated_ids = model.generate(pixel_values)
        generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        
        # Example regex to identify LaTeX-like formulas from the recognized text
        formulas = re.findall(r'\$[^\$]+\$', generated_text)
        return formulas
    
    def save_formulas_to_file(formulas, output_path):
        with open(output_path, "w", encoding="utf-8") as f:
            for formula, page_num in formulas:
                f.write(f"Formula on Page {page_num}: {formula}\n")

    def extract_text_formulas_from_pdf(file_path):
        formulas = []
        with pdfplumber.open(file_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                text = page.extract_text()
                matches = re.findall(r'\$[^\$]+\$', text)  # Extract LaTeX-like formulas
                formulas.extend([(match, page_num + 1) for match in matches])
        return formulas

# extraction
    def extract_text_from_pdf(self, file_path):
        full_text = ""
        with open(file_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            for page_num, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                if page_text:
                    full_text += f"{page_text.strip()} (Page {page_num + 1})\n"
                else:
                    full_text += f"No text detected on page {page_num + 1}\n"
        return full_text

    def extract_images_from_pdf(self, file_path, doc):
        pdf_name = os.path.splitext(os.path.basename(file_path))[0]
        images_dir = "extracted_images"
        os.makedirs(images_dir, exist_ok=True)

        with open(file_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            for page_num, page in enumerate(pdf_reader.pages):
                image_counter = 1
                resources = page.get('/Resources').get_object()
                xobjects = resources.get('/XObject')

                if xobjects:
                    xobjects = xobjects.get_object()
                    for obj in xobjects:
                        xobject = xobjects[obj].get_object()
                        if xobject['/Subtype'] == '/Image':
                            try:
                                data = xobject._data
                                if '/Filter' in xobject:
                                    if xobject['/Filter'] == '/FlateDecode':
                                        data = zlib.decompress(data)

                                image_path = os.path.join(images_dir, f"{pdf_name}_page_{page_num + 1}_image_{image_counter}.jpg")
                                with open(image_path, "wb") as image_file:
                                    image_file.write(data)

                                # OCR on Image
                                self.ocr_image(image_path, doc, page_num + 1, image_counter)
                                image_counter += 1
                            except Exception as e:
                                print(f"Error reading image data for object {obj} on page {page_num + 1}: {e}")

# OCR
    def ocr_image(self, image_path, doc, page_num):
        try:
            ocr_result = self.ocr.ocr(image_path)
            if ocr_result:
                img_text = "\n".join([line[1][0] for line in ocr_result[0]])
                image_obj = Image(
                    id=self.generate_id(),
                    link=image_path,
                    page=page_num,
                    type="OCR",
                    imgtext=img_text,
                    llm_output=""  # You can fill this with LLM processing results if needed
                )
                doc.imgList.append(image_obj)
        except Exception as e:
            print(f"Error during OCR for {image_path}: {e}")

# Helper
    def save_image_data(self, xobject, data, pdf_name, page_num, image_counter, images_dir):
            if xobject.get('/Filter') == '/DCTDecode':
                image_path = os.path.join(images_dir, f"{pdf_name}_page_{page_num}_image_{image_counter}.jpg")
                with open(image_path, "wb") as image_file:
                    image_file.write(data)
            else:
                mode = "RGB" if xobject['/ColorSpace'] == '/DeviceRGB' else "P"
                img = Image.frombytes(mode, (xobject['/Width'], xobject['/Height']), data)
                image_path = os.path.join(images_dir, f"{pdf_name}_page_{page_num}_image_{image_counter}.png")
                img.save(image_path)
            return image_path

    def split_text_into_chunks(self, full_text, doc):
        chunks = full_text.split('\n')
        for idx, chunk in enumerate(chunks):
            if chunk.strip():
                text_chunk = TextChunk(id=self.generate_id(), text=chunk.strip(), page=idx + 1)
                doc.textList.append(text_chunk)

    def generate_id(self):
        # Generate a unique ID for chunks or images
        return hashlib.sha256(str(datetime.now().timestamp()).encode()).hexdigest()

# Sudo main
    def process_pdf(self, file_path, doc):
        output_text = self.extract_text_from_pdf(file_path)
        self.split_text_into_chunks(output_text, doc)
        self.extract_images_from_pdf(file_path, doc)
        formulas = self.extract_text_formulas_from_pdf(file_path)
        self.save_formulas_to_file(formulas, "math_formulas.txt")




    