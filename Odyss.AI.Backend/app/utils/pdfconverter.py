from pptxtopdf import convert as pptx_to_pdf
from docx2pdf import convert as docx_to_pdf
from app.config import Config

def convert_docx_or_pptx_to_pdf(self, document_path):
    try:
        if document_path.endswith(".docx"):
            # Konvertiere .docx zu PDF
            docx_to_pdf(document_path)
        elif document_path.endswith(".pptx"):
            # Konvertiere .pptx zu PDF
            pptx_to_pdf(document_path, Config.LOCAL_DOC_PATH)
    except Exception as e:
        raise Exception(f"Error during conversion: {e}")

    # Rückgabe des Pfads zur neuen PDF-Datei
    return document_path.replace('.docx', '.pdf').replace('.pptx', '.pdf')