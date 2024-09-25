from io import BytesIO
import zlib
from paddleocr import PaddleOCR
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
import os
import re
import PyPDF2
import pdfplumber
from pptxtopdf import convert as pptx_to_pdf
from docx2pdf import convert as docx_to_pdf
from app.models.user import TextChunk, Image
from docx import Document as DocxDocument
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


class OCRService:
    def __init__(self):
        self.ocr = PaddleOCR(use_angle_cls=True, use_gpu=False, lang="de")
        self.processor = TrOCRProcessor.from_pretrained("microsoft/trocr-small-handwritten")
        self.model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-small-handwritten")

    def extract_text(self, doc):
        file_extension = os.path.splitext(doc.name)[1].lower()

        if file_extension == ".pdf":
            self.process_pdf(doc)  # PDF-Verarbeitung aufrufen
        elif file_extension in [".docx", ".pptx"]:
            self.convert_docx_or_pptx_to_pdf(doc)  # Konvertiere DOCX/PPTX zu PDF
            self.process_pdf(doc)  # PDF-Verarbeitung aufrufen
        else:
            print("Unsupported file type")  # Überprüfen, ob der Dateityp nicht unterstützt wird

        return doc


# Convert
    def convert_docx_or_pptx_to_pdf(self, doc):
        try:
            if doc.name.endswith(".docx"):
                docx_to_pdf(doc.doclink)  # Convert DOCX to PDF
            elif doc.name.endswith(".pptx"):
                pptx_to_pdf(doc.doclink)  # Convert PPTX to PDF
        except Exception as e:
            raise Exception(f"Error during conversion: {e}")

        doc.name = doc.name.replace('.docx', '.pdf').replace('.pptx', '.pdf')
        return doc

    def convert_docx_to_pdf(self, doc):
        print(f"Starting DOCX to PDF conversion for: {doc.doclink}")
        
        try:
            doc_content = DocxDocument(doc.doclink)
            print(f"Number of paragraphs in DOCX: {len(doc_content.paragraphs)}")
            
            pdf_stream = BytesIO()
            pdf_canvas = canvas.Canvas(pdf_stream, pagesize=letter)

            for idx, paragraph in enumerate(doc_content.paragraphs):
                print(f"Writing Paragraph {idx + 1} to PDF: {paragraph.text}")
                pdf_canvas.drawString(100, 750, paragraph.text)
                pdf_canvas.showPage()

            pdf_canvas.save()
            pdf_stream.seek(0)

            pdf_length = pdf_stream.getbuffer().nbytes
            print(f"PDF Stream created with length: {pdf_length} bytes")

            doc.doclink = pdf_stream
            return pdf_stream

        except Exception as e:
            print(f"Error during DOCX to PDF conversion: {e}")
            raise



    def convert_pptx_to_pdf(self, doc):
        # Dateiinhalt in Bytes laden
        pptx_stream = BytesIO(doc.doclink.read())
        pdf_stream = BytesIO()  # Erstelle einen neuen BytesIO-Stream für die PDF

        try:
            # Konvertiere PPTX-Stream direkt zu PDF-Stream
            pptx_to_pdf(pptx_stream, pdf_stream)  # Anpassung hier
            pdf_stream.seek(0)  # Zurücksetzen des Streams auf den Anfang
        except Exception as e:
            raise Exception(f"Fehler bei der Konvertierung von PPTX zu PDF: {e}")

        return pdf_stream  # Gibt den PDF-Stream zurück

      
# handle formulas
    def extract_formulas_from_image(self, image_path):
        processor = TrOCRProcessor.from_pretrained("microsoft/trocr-small-handwritten")
        model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-small-handwritten")

        image = Image.open(image_path).convert("RGB")
        pixel_values = processor(image, return_tensors="pt").pixel_values
        generated_ids = model.generate(pixel_values)
        generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        
        # Example regex to identify LaTeX-like formulas from the recognized text
        formulas = re.findall(r'\$[^\$]+\$', generated_text)
        return formulas
    
    def save_formulas_to_file(self, formulas, output_path):
        with open(output_path, "w", encoding="utf-8") as f:
            for formula, page_num in formulas:
                f.write(f"Formula on Page {page_num}: {formula}\n")

    def extract_text_formulas_from_pdf(self, file_path):
        formulas = []
        with pdfplumber.open(file_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                text = page.extract_text()
                matches = re.findall(r'\$[^\$]+\$', text)  # Extract LaTeX-like formulas
                formulas.extend([(match, page_num + 1) for match in matches])
        return formulas

# extraction
    def extract_text_from_pdf(self, pdf_stream):
        full_text = ""
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_stream)
            for page_num, page in enumerate(pdf_reader.pages):
                print(f"Reading text from page {page_num + 1}")
                page_text = page.extract_text()
                if page_text:
                    full_text += f"{page_text.strip()} (Page {page_num + 1})\n"
                else:
                    print(f"No text found on page {page_num + 1}.")
                    full_text += f"No text detected on page {page_num + 1}\n"
            
            if not full_text.strip():  # If no text was found
                print("The document appears to contain only images.")
                full_text = ""  # Return empty string for image-only documents

        except Exception as e:
            print(f"Error extracting text from PDF: {e}")

        return full_text




    def extract_images_from_pdf(self, pdf_stream, doc):
        image_counter = 1

        # Öffne den PDF-Stream anstelle einer Datei
        pdf_reader = PyPDF2.PdfReader(pdf_stream)
        
        for page_num, page in enumerate(pdf_reader.pages):
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

                            # Statt die Datei zu speichern, verwende BytesIO
                            image_stream = BytesIO(data)

                            # Führe OCR auf dem Bild durch, ohne es zu speichern
                            self.ocr_image(image_stream, doc, page_num + 1, image_counter)
                            image_counter += 1
                        except Exception as e:
                            print(f"Error reading image data for object {obj} on page {page_num + 1}: {e}")

# OCR
    def ocr_image(self, image_stream, doc, page_num, image_counter):
        try:
            # Lade das Bild direkt aus dem BytesIO-Stream
            image_stream.seek(0)  # Setze den Stream auf den Anfang zurück
            ocr_result = self.ocr.ocr(image_stream)

            if ocr_result:
                img_text = "\n".join([line[1][0] for line in ocr_result[0]])
                image_obj = Image(
                    id=self.generate_id(),
                    link=f"page_{page_num}_image_{image_counter}.jpg",  # Link könnte für spätere Nutzung oder Referenz generiert werden
                    page=page_num,
                    type="OCR",
                    imgtext=img_text,
                    llm_output=""  # Kann später durch LLM-Ergebnisse gefüllt werden
                )
                doc.imgList.append(image_obj)
        except Exception as e:
            print(f"Error during OCR for image on page {page_num}, image {image_counter}: {e}")


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


# Sudo main
    def process_pdf(self, doc):
        print(f"Starting PDF processing for document: {doc.name}")
        
        try:
            # Attempt to extract text from PDF
            print("Attempting to extract text from PDF...")
            output_text = self.extract_text_from_pdf(doc.doclink)
            print(f"Extracted text from PDF: {output_text}")
            
            # Split extracted text into chunks if text is found
            if output_text:
                print("Splitting extracted text into chunks...")
                self.split_text_into_chunks(output_text, doc)
                print(f"Text chunks created: {len(doc.textList)}")
            else:
                print("No text detected in PDF, proceeding to image extraction...")

            # Always attempt image extraction regardless of text outcome
            print("Attempting to extract images from PDF...")
            self.extract_images_from_pdf(doc.doclink, doc)
            print(f"Image extraction complete. Images found: {len(doc.imgList)}")

        except Exception as e:
            print(f"Error during PDF processing: {e}")
