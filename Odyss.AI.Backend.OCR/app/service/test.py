from pdf2image import convert_from_path
from pix2tex.cli import LatexOCR
from PIL import Image

# # PDF-Datei in Bild umwandeln
# images = convert_from_path('C:\\Users\\...\\Documents\\Form1.pdf', dpi=150)

# # Wenn mehrere Seiten vorhanden sind, wähle die erste Seite
# img = images[0]

# # Sicherstellen, dass das Bild im richtigen Format ist (PIL.Image)
# if img.mode != 'RGB':
#     img = img.convert('RGB')

# # Verkleinere das Bild auf eine maximale Größe, aber behalte das Seitenverhältnis
# # max_size = (1024, 1024)  # Maximale Breite und Höhe
# # images.thumbnail(max_size, Image.Resampling.LANCZOS)

# # LaTeX aus dem Bild extrahieren
# model = LatexOCR()
# print("Extracted LaTeX:")
# print(model(img))



# img = Image.open('C:\\Users\\...\\Documents\\Form1.png')
# model = LatexOCR()
# print(model(img))

# import cv2
# import numpy as np
# from pdf2image import convert_from_path
# from pix2tex.cli import LatexOCR

# PDF in Bild umwandeln
# images = convert_from_path('C:\\Users\\...\\Documents\\Paper.pdf', dpi=150)

# Wenn mehrere Seiten vorhanden sind, wähle die erste Seite
# img = np.array(images[0])

# Konvertiere das Bild in Graustufen
# gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

# Wende Schwellwertsetzung an, um die Formeln zu extrahieren
# _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

# Finde Konturen (möglicherweise Formeln)
# contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Extrahiere die gefundenen Konturen (Formeln)
# for i, contour in enumerate(contours):
#     x, y, w, h = cv2.boundingRect(contour)
#     formula_img = img[y:y+h, x:x+w]

#     Speichern des extrahierten Bereichs als Bild (optional)
#     cv2.imwrite(f'formula_{i}.png', formula_img)

#     LaTeX aus dem extrahierten Bild
#     model = LatexOCR()
#     print(f"Extracted LaTeX for formula {i}:")
#     print(model(formula_img))


# from pdf2image import convert_from_path
# from PIL import Image
# import pytesseract
# from pix2tex.cli import LatexOCR

# # PDF in Bild umwandeln
# images = convert_from_path('C:\\Users\\...\\Documents\\Paper.pdf', dpi=150)
# model = LatexOCR()

# for img in images:
#     # Sicherstellen, dass das Bild im richtigen Format vorliegt
#     if img.mode != 'RGB':
#         img = img.convert('RGB')

#     # Extrahiere Text mit Pytesseract und erhalte Bounding Boxen
#     boxes = pytesseract.image_to_boxes(img)

#     # Gehe alle Boxen durch und überprüfe, ob es sich um eine Formel handeln könnte
#     for b in boxes.splitlines():
#         b = b.split()
#         # Hier könntest du eine bessere Erkennungslogik einbauen, aber nehmen wir an,
#         # dass wir alle Boxen, die in der Nähe von Formeln sind, verwenden wollen
#         if "math" in b[0]:  # Überprüfe, ob der Text in der Box mathematisch ist
#             x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
            
#             # Extrahiere den Bereich mit der Formel
#             formula_img = img.crop((x, y, w, h))

#             # Formel mit LatexOCR extrahieren
#             formula = model(formula_img)
            
#             # Gebe die erkannte Formel aus
#             if formula:
#                 print("Erkannte Formel:", formula)
#             else:
#                 print("Keine Formel erkannt")

