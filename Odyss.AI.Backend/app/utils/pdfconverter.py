from io import BytesIO
from pptxtopdf import convert as pptx_to_pdf
from docx2pdf import convert as docx_to_pdf
from app.config import Config


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
