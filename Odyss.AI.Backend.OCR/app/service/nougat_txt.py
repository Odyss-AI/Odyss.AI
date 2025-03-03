import os
import torch
from nougat import NougatModel
from nougat.utils.dataset import tokenize
from pathlib import Path
from pdf2image import convert_from_path
from nougat.utils.im2markup.data import extract_text

# Verzeichnisse definieren
PDF_DIR = './Odyss.AI.Backend.LLM/Paper'
OUTPUT_DIR = './nougat_txt_extraction'

# Sicherstellen, dass der Ausgabeordner existiert
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Modell laden
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
model = NougatModel.from_pretrained('facebook/nougat-small').to(DEVICE)
model.eval()

# Alle PDFs im Verzeichnis verarbeiten
for pdf_path in Path(PDF_DIR).glob("*.pdf"):
    images = convert_from_path(str(pdf_path))  # PDF in Bilder umwandeln
    pdf_name = pdf_path.stem  # Dokumentname ohne Endung
    
    for page_num, image in enumerate(images, start=1):
        input_tensor = tokenize([image]).to(DEVICE)
        with torch.no_grad():
            output = model.inference(input_tensor)[0]
        
        text_output = extract_text(output)
        
        # Datei speichern
        txt_filename = f"{pdf_name}_page{page_num}.txt"
        txt_path = os.path.join(OUTPUT_DIR, txt_filename)
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(text_output)

print("Extraktion abgeschlossen. Ergebnisse im Ordner 'nougat_txt_extraction'.")
