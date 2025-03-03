## Odyss.AI Backend OCR

Dieses Projekt implementiert den OCR-Teil eines Systems, bei dem Nutzer Dokumente hochladen können, um anschließend Fragen zu den Inhalten zu stellen oder „über das Dokument zu schreiben“. Im Kern wird das hochgeladene Dokument verarbeitet und in strukturierte JSON-Daten umgewandelt, sodass das Backend die extrahierten Inhalte (Text, Bilder und ggf. LaTeX-Formeln) weiterverwenden kann.

Das Besondere an diesem System ist, dass **drei verschiedene OCR-Implementierungen** angeboten werden:

* **Tesseract**
* **Nougat**
* **PaddleOCR**

Die einzelnen Implementierungen extrahieren sowohl Fließtext als auch eingebettete Bilder aus PDF-Dokumenten. Zusätzlich werden Texte in kleinere „Chunks“ aufgeteilt, um sie später besser verarbeiten zu können.

---

## Inhaltsverzeichnis

* [Überblick](#Überblick)
* [Projektstruktur](#projektstruktur)
* [Dataset](#dataset)
* [Funktionsweise und Ablauf](#funktionsweise-und-ablauf)

  * [OCR-Engines](#ocr-engines)
  * [PDF-Verarbeitung und Datenextraktion](#pdf-verarbeitung-und-datenextraktion)
  * [Textextraktion &amp; Chunking](#textextraktion--chunking)
* [Installation und Setup](#installation-und-setup)
* [Ausführung und Nutzung](#ausführung-und-nutzung)
* [Hinweise und Erweiterungsmöglichkeiten](#hinweise-und-erweiterungsmöglichkeiten)
* [OCR Vergleich: Tesseract vs. Paddle vs. Nougat](#ocr-vergleich-tesseract-vs-paddle-vs-nougat)

- [Einleitung](#einleitung)
- [Allgemeine Informationen (Fall 1)](#allgemeine-informationen-fall-1)
- [Vergleichskriterien (Fall 1)](#vergleichskriterien-fall-1)
- [Kriteriumserklärungen](#kriteriumserklarungen)
- [Ergebnisse im Detail (Seite 1, Fall 1)](#ergebnisse-im-detail-seite-1-fall-1)

  - [Tesseract](#tesseract)
  - [Paddle](#paddle)
  - [Nougat](#nougat)
- [Allgemeine Informationen (Fall 2)](#allgemeine-informationen-fall-2)
- [Vergleichskriterien (Fall 2)](#vergleichskriterien-fall-2)
- [Ergebnisse im Detail (Seite 1, Fall 2)](#ergebnisse-im-detail-seite-1-fall-2)

  - [Tesseract](#tesseract-1)
  - [Paddle](#paddle-1)
  - [Nougat](#nougat-1)
- [Zusammenfassung der Ergebnisse](#zusammenfassung-der-ergebnisse)
- [Fehleranalyse](#fehleranalyse)

  - [Häufigste Fehlerarten](#haeufigste-fehlerarten)
  - [Vergleich der Fehlerhäufigkeit](#vergleich-der-fehlerhaeufigkeit)
- [Ausführen der DocumentOCRResults-Klasse](#ausfuehren-der-documentocrresults-klasse)

  - [Wechsle zum richtigen Verzeichnis:](#wechsle-zum-richtigen-verzeichnis)
- [To Do](#To-Do)

---

## Überblick

Das OCR-Modul übernimmt folgende Aufgaben:

1. **Empfang eines Dokuments:**

   Das System erhält ein Dokument (z. B. PDF, docx, pptx) zusammen mit einer Anfrage. Dieses Dokument wird an den OCR-Service weitergeleitet.
2. **Datenextraktion:**

   Anhand der gewählten OCR-Engine wird das Dokument in einzelne Seiten/Bilder umgewandelt. Anschließend werden:

   * **Textinhalte** extrahiert,
   * **Bilder** aus dem Dokument identifiziert und gespeichert,
3. **Aufbereitung als JSON:**

   Die extrahierten Informationen (Text-„Chunks“ und Bildinformationen) werden in einer strukturierten Form (JSON) an das Backend zurückgegeben.

---

## Projektstruktur

Die Ordnerstruktur des Projekts sieht wie folgt aus:

```

Odyss.AI.Backend.OCR/         # Hauptordner
│
├── app/                      # Enthält den gesamten Anwendungscode
│   ├── routes/               # API-Routen
│   │   ├── __init__.py
│   │   └── routes.py
│   │
│   ├── service/              # OCR-Services und Hilfsklassen
|   |   ├── dataset_root      # test-dataset ist im git-ignore
│   │   ├── results	      # Ergebnis von DocumentOCRResults abgespeichert
│   │   ├── results2	      # Ergebnis von DocumentOCRResults2 abgespeichert, mit txts der OCRs und Ground_truth
│   │   ├── DocumentOCRResults.py # Veralteter Code zum Vergleichen (Initial)
│   │   ├── DocumentOCRResults2.py # Neuer Code zum Vergleichen
│   │   ├── nougatocr.py
│   │   ├── paddleocr.py
│   │   ├── StoppingCriteriaScores.py  # Hilfsklasse für Nougat (custom stopping criteria)
│   │   └── tesseractocr.py
│   │
│   ├── __init__.py
│   ├── config.py             # Konfigurationsdatei (z. B. Pfade, Umgebungsvariablen)
│   └── user.py               # Definition der Datenmodelle (z. B. Document, TextChunk, Image)
│
├── venv/                     # Virtuelle Umgebung (abhängig von Deiner Installation)
├── .env                      # Umgebungsvariablen
├── Dockerfile                # Docker-Setup für Containerisierung
├── OCR.md                    # OCR-Dokumentation 
├── requirements.txt          # Python-Abhängigkeiten
├── run.py                    # Haupteinstiegspunkt zum Starten des Backends
└── setup.py                  # Setup-Skript (zur Installation und Erstellung der venvs)
```

---


## Dataset

Für die OCR-Analyse wird ein Datensatz aus wissenschaftlichen Papern generiert. Die Paper stammen aus **arXiv** und werden mit Hilfe des bereitgestellten Resource-Codes heruntergeladen. Die Besonderheit dabei ist, dass arXiv neben der PDF-Datei auch die **LaTeX-Quellen (.tex)** bereitstellt, wodurch eine strukturierte Umwandlung in HTML möglich ist.

### **1. Herunterladen der Paper von arXiv**

Zunächst müssen Paper-PDFs von arXiv bezogen werden. Dies kann über den **Resource-Code** erfolgen, der in diesem Repository bereitgestellt wird. Der Code lädt die LaTeX-Quellen der Paper zusammen mit den zugehörigen PDF-Dateien.

### **2. Umwandlung von LaTeX in HTML**

Um die Paper für die OCR-Verarbeitung besser nutzbar zu machen, wird die `.tex`-Datei mit **LaTeXML** in XML und anschließend in HTML konvertiert:

1. **Konvertierung in XML:**
   ```bash
   latexml paper.tex --dest=paper.xml
   ```
2. **Konvertierung in HTML:**
   ```bash
   latexmlpost --format=html paper.xml --dest=paper.html
   ```

Nach diesem Prozess liegen die Paper in einer strukturierten HTML-Form vor.

### **3. Ordnerstruktur des Datasets**

Das Dataset wird in folgendem Verzeichnis innerhalb des Projekts abgelegt wie oben im Projektstruktur dargestellt:

```
service/dataset-root/
│── paper_htmls/   # Enthält die konvertierten HTML-Versionen der Paper
│── paper_pdfs/    # Enthält die originalen PDF-Dateien der Paper
```

Jede Datei wird in den entsprechenden Ordner eingefügt:

* **HTML-Dateien** (`.html`) in `paper_htmls/`
* **PDF-Dateien** (`.pdf`) in `paper_pdfs/`

### **4. Nutzung des Datasets**

Der generierte Datensatz kann für Tests, Trainingszwecke oder Vergleiche zwischen OCR-Engines verwendet werden. Die strukturierte HTML-Variante erleichtert insbesondere den Vergleich mit den extrahierten Texten aus den PDFs.

---


## Funktionsweise und Ablauf

### OCR-Engines

Die drei implementierten OCR-Engines haben jeweils ihre eigene Klasse und Logik:

1. **Tesseract (tesseractocr.py)**
   * **PDF-Verarbeitung:**

     Öffnet das PDF und wandelt die Seiten in Bilder um (mittels `pdf2image`).
   * **Textextraktion:**

     Führt mittels [pytesseract](https://pypi.org/project/pytesseract/) eine OCR auf den Seitenbildern aus.

     Zusätzlich wird die [LatexOCR-Funktionalität](https://github.com/lukas-blecher/LaTeX-OCR) eingebunden, um LaTeX-Formeln zu erkennen (Geht jedoch zur Zeit nicht).
   * **Bildextraktion:**

     Mit Hilfe von `PyPDF2` werden eingebettete Bilder aus dem PDF extrahiert, gespeichert und auch erneut einer OCR unterzogen.
   * **Chunking:**

     Der erkannte Text wird in kleinere „Chunks“ (z. B. 100 Wörter pro Chunk) aufgeteilt und als `TextChunk`-Objekte im `Document`-Objekt gespeichert.
2. **Nougat (nougatocr.py)**
   * **Modellbasiert:**

     Nutzt das [facebook/nougat-base](https://huggingface.co/facebook/nougat-base) Modell aus der Transformers-Bibliothek zur Texterkennung.
   * **Custom Stopping Criteria:**

     Mithilfe der Hilfsklasse `StoppingCriteriaScores` (in  *StoppingCriteriaScores.py* ) wird das Stoppen der Texterzeugung dynamisch gesteuert.
   * **Verarbeitung:**

     PDF-Seiten werden in Bilder konvertiert, worauf das Modell OCR durchführt. Der extrahierte Text wird wieder in Chunks (z. B. 512 Wörter pro Chunk) aufgeteilt.
   * **Bildextraktion:**

     Auch hier werden eingebettete Bilder im PDF erkannt, gespeichert und per OCR weiter verarbeitet.
3. **PaddleOCR (paddleocr.py)**
   * **PaddleOCR-Integration:**

     Nutzt die [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) Bibliothek, die speziell für die Erkennung von Text in Bildern (hier konfiguriert für Deutsch) optimiert ist.
   * **Prozess:**

     Wie bei den anderen Engines wird das PDF in Seitenbilder umgewandelt, und es erfolgt die Textextraktion.

     Eingebettete Bilder werden ebenfalls identifiziert, gespeichert und mittels PaddleOCR ausgewertet.
   * **Chunking:**

     Der erkannte Text wird in Chunks (hier z. B. 512 Wörter pro Chunk) aufgeteilt und im `Document`-Objekt abgelegt.

### PDF-Verarbeitung und Datenextraktion

Unabhängig von der verwendeten OCR-Engine erfolgt die grundlegende Verarbeitung eines PDFs in mehreren Schritten:

1. **PDF-Öffnen und Umwandeln:**

   Das PDF wird mittels `BytesIO` gelesen. Mittels der Bibliothek `pdf2image` werden alle Seiten als Bilder (JPEG) konvertiert.
2. **Texterkennung pro Seite:**

   Für jede Seite wird die OCR-Methode der jeweiligen Engine aufgerufen. Hierbei wird neben reinem Text auch versucht, LaTeX-Formeln (bei Tesseract) zu erkennen.
3. **Extraktion eingebetteter Bilder:**

   Mithilfe von `PyPDF2` wird über die Ressourcen einer PDF-Seite iteriert. Werden Objekte vom Typ „Image“ gefunden, so werden diese extrahiert, gespeichert und zusätzlich per OCR verarbeitet, um eventuellen Bildtext zu extrahieren.
4. **Speicherung in Datenmodellen:**

   Alle erkannten Texte werden in Objekten vom Typ `TextChunk` gespeichert, während extrahierte Bilder als `Image`-Objekte abgelegt werden. Diese werden beide im übergeordneten `Document`-Objekt zusammengefasst und letztlich als JSON an das Backend zurückgegeben.

### Textextraktion & Chunking

Um lange Texte handhabbar zu machen, wird der gesamte extrahierte Text in kleinere „Chunks“ aufgeteilt. Dies erfolgt folgendermaßen:

* **Wortweise Aufteilung:**

  Der erkannte Text wird zunächst in einzelne Wörter zerlegt.
* **Chunking-Logik:**

  Sobald eine vorgegebene Wortanzahl (z. B. 100 oder 512 Wörter, je nach Implementierung) erreicht ist, wird ein neuer `TextChunk` erstellt und dem Dokument hinzugefügt.
* **Integration von LaTeX:**

  Bei der Tesseract-Implementierung sollte zusätzlich das LaTeX-Ergebnis (falls erkannt) an den entsprechenden TextChunk angehängt.

---

## Ausführung und Nutzung

* **Starten der Anwendung:**

  Über `run.py` wird der Hauptserver gestartet. Innerhalb der `app/routes/routes.py` findest Du die API-Endpunkte, die die Dokumente entgegennehmen und an den entsprechenden OCR-Service weiterleiten.
* **OCR-Anfrage:**

  Ein Dokument (z. B. PDF) wird an den entsprechenden API-Endpunkt geschickt. Der Service:

  * Liest das Dokument
  * Führt die Texterkennung (und Bildverarbeitung) mittels der gewählten OCR-Engine aus
  * Teilt den extrahierten Text in Chunks auf
  * Gibt das Ergebnis als JSON an das Backend zurück.
* **Ausgabe:**

  Das finale JSON beinhaltet:

  * Eine Liste von `TextChunk`-Objekten (mit Text, Seitenangabe und ggf. LaTeX-Ergebnissen)
  * Eine Liste von `Image`-Objekten (mit Pfad, Seitennummer, Dateityp und extrahiertem Bildtext)

---

## Hinweise

* **Performance und GPU-Unterstützung:**

  Insbesondere das Nougat-Modul unterstützt die Ausführung auf einer GPU (falls verfügbar). Dies verbessert die OCR-Performance bei großen oder komplexen Dokumenten.
* **Logging und Debugging:**

  In den einzelnen Modulen sind diverse `print`-Anweisungen implementiert, um den Fortschritt und mögliche Fehler anzuzeigen. Für den Produktionseinsatz empfiehlt sich ein Umstieg auf ein professionelles Logging-Framework.

## OCR Vergleich: Tesseract vs. Paddle vs. Nougat

## Einleitung

In diesem Dokument vergleichen wir drei OCR-Technologien: Tesseract, Paddle und Nougat. Ziel ist es, ihre Leistungsfähigkeit hinsichtlich Textgenauigkeit, Verarbeitungszeit, Benutzerfreundlichkeit und weitere Kriterien zu bewerten. Wir testen mit diesem Dokument [arXiv:2401.00908](https://arxiv.org/abs/2401.00908) :

1. (Allgemeiner Vergleich)
2. (Intensiver Vergleich)

Die folgenden Kriterien werden zur Bewertung herangezogen.

## Allgemeine Informationen (Fall 1: Allgemeiner Vergleich)

- **Dokument:** Paper (normales Dokument)
- **Anzahl Seiten:** 16 Seiten

## Vergleichskriterien (Fall 1)

| Kriterium                                              | Tesseract   | PaddleOCR   | Nougat      |
| :----------------------------------------------------- | ----------- | ----------- | ----------- |
| **Verarbeitungszeit (min)**                      | 0:30        | 0:28        | 14:05       |
| **Formatierung *(*ja*****/ja/nein)**         | ja*         | ja          | ja*         |
| **Bilderkennung (Anzahl)**                       | 5           | 5           | 5           |
| **Benutzerfreundlichkeit (gut/mittel/schlecht)** | gut         | mittel      | schlecht    |
| **Sonderzeichen/Formeln (%)**                    | [Formeln T] | [Formeln P] | [Formeln N] |

## Kriteriumserklärungen

- **Verarbeitungszeit (min)** Misst, wie lange es dauert, ein Dokument mit der OCR-Engine zu verarbeiten. Die Zeit wird in Sekunden oder Minuten gemessen, abhängig von der Größe des Dokuments.
- **Formatierung (ja\*/ja/nein)** Gibt an, ob die OCR-Engine die ursprüngliche Formatierung des Dokuments beibehalten kann, wie Schriftarten, Absätze und Layout.

  - Ja* bedeutet, dass mehr Informationen zu der Formatierung des Dokumentes vorliegen
  - *Ja* bedeutet, dass die OCR-Engine die Formatierung größtenteils beibehalten kann
  - *Nein* bedeutet, dass die OCR-Engine die Formatierung entweder gar nicht beibehalten kann.
- **Bilderkennung (Anzahl)** Zeigt, wie viele Bilder oder Grafiken die OCR-Engine korrekt erkannt hat. Besonders relevant bei Dokumenten, die auch Bilder oder Grafiken enthalten.
- **Benutzerfreundlichkeit (gut/mittel/schlecht)** Beschreibt, wie einfach es ist, mit der OCR-Engine zu arbeiten. Eine benutzerfreundliche Lösung ist einfach zu bedienen, gut dokumentiert und benötigt wenig Eingriff vom Benutzer.
- **Sonderzeichen/Formeln (%)** Misst die Fähigkeit der OCR-Engine, Sonderzeichen oder mathematische Formeln korrekt zu erkennen. Besonders wichtig für technische oder wissenschaftliche Dokumente, die solche Symbole enthalten.

## Ergebnisse im Detail (Seite 1, Fall 1)

### Tesseract

- **Texterkennung**: "401.00908v1 [cs.CL] 31 Dec 2023\n\nDOCLLM: A LAYOUT-AWARE GENERATIVE LANGUAGE MODEL\nFOR MULTIMODAL DOCUMENT UNDERSTANDING\n\nDongsheng Wang”, Natraj Raman*, Mathieu Sibue*\nZhiqiang Ma, Petr Babkin, Simerjot Kaur, Yulong Pei, Armineh Nourbakhsh, Xiaomo Liu\nJPMorgan Al Research\n{first .last}@jpmchase.com\n\nABSTRACT\n\nEnterprise documents such as forms, invoices, receipts, reports, contracts, and other similar records,\noften carry rich semantics at the intersection of textual and spatial modalities. The visual cues offered\nby their complex layouts play a crucial role in comprehending these documents effectively. In this\nPaper, we present DocLLM, a lightweight extension to traditional large language models (LLMs) for\nreasoning over visual documents, taking into account both textual semantics and spatial layout. Our\nmodel differs from existing multimodal LLMs by avoiding expensive image encoders and focuses\nexclusively on bounding box information to incorporate the spatial layout structure. Specifically,\nthe cross-alignment between text and spatial modalities is captured by decomposing the attention\nmechanism in classical transformers to a set of disentangled matrices. Furthermore, we devise a\npre-training objective that learns to infill text segments. This approach allows us to address irregular\nlayouts and heterogeneous content frequently encountered in visual documents. The pre-trained\nmodel is fine-tuned using a large-scale instruction dataset, covering four core document intelligence\ntasks. We demonstrate that our solution outperforms SotA LLMs on 14 out of 16 datasets across all\ntasks, and generalizes well to 4 out of 5 previously unseen datasets.\n\nKeywords DocAl- VRDU - LLM - GPT - Spatial Attention\n\n1 Introduction\n\nDocuments with rich layouts, including invoices, receipts, contracts, orders, and forms, constitute a significant portion\nof enterprise corpora. The automatic interpretation and analysis of these documents offer considerable advantages [I],\nwhich has spurred the development of Al-driven solutions. These visually rich documents feature complex layouts,\nbespoke type-setting, and often exhibit variations in templates, formats and quality. Although Document AI (DocAl) has\nmade tremendous progress in various tasks including extraction, classification and question answering, there remains a\nsignificant performance gap in real-world applications. In particular, accuracy, reliability, contextual understanding and\ngeneralization to previously unseen domains continues to be a challenge\n\nDocument intelligence is inherently a multi-modal problem with both the text content and visual layout cues being\ncritical to understanding the documents. It requires solutions distinct from conventional large language models such as\nGPT-3.5 [3], Llama [4], Falcon [5]] or PaLM [6] that primarily accept text-only inputs and assume that the documents\nexhibit simple layouts and uniform formatting, which may not be suitable for handling visual documents. Numerous\nvision-language frameworks [[71|8]] that can process documents as images and capture the interactions between textual\nand visual modalities are available. However, these frameworks necessitate the use of complex vision backbone\narchitectures [9] to encode image information, and they often make use of spatial information as an auxiliary contextual\nsignal (70,(11).\n\nIn this paper we present DocLLM, a light-weight extension to standard LLMs that excels in several visually rich form\nunderstanding tasks. Unlike traditional LLMs, it models both spatial layouts and text semantics, and therefore is\n\n“These authors contributed equally to this work.\n"
- **Bilderkennung (1. Bild):** "1\nWho is the “Supplier”?\nneem ante 7 Analytic Insight Inc\nINFILL, What is the doc type?\nPurchase Order\np=\nB Is the year 1995?\nae 2,0 Yes\nOCRed Document LLM Extension Pre-training Instruction Tuning\n\nText tokens + Bounding boxes Disentangled Spatial Attention Blocks + Infilling Objective KIE + NLI + VQA + Classify\n"

### Paddle

- **Texterkennung**: "DOCLLM: A LAYOUT-AWARE GENERATIVE LANGUAGE MODEL\nFOR MULTIMODAL DOCUMENT UNDERSTANDING\nDongsheng Wang*, Natraj Raman\", Mathieu Sibue\nZhiqiang Ma, Petr Babkin, Simerjot Kaur, Yulong Pei, Armineh Nourbakhsh, Xiaomo Liu\n JPMorgan AI Research\n 2023\n{first.last}@jpmchase.com\nDec '\nABSTRACT\nEnterprise documents such as forms, invoices, receipts, reports, contracts, and other similar records.\noften carry rich semantics at the intersection of textual and spatial modalities. The visual cues offered\nby their complex layouts play a crucial role in comprehending these documents effectively. In this\nreasoning over visual documents, taking into account both textual semantics and spatial layout. Our\nmodel differs from existing multimodal LLMs by avoiding expensive image encoders and focuses\nexclusively on bounding box information to incorporate the spatial layout structure. Specifically.\nthe cross-alignment between text and spatial modalities is captured by decomposing the attention\nmechanism in classical transformers to a set of disentangled matrices. Furthermore, we devise a\npre-training objective that learns to infill text segments. This approach allows us to address irregular\n00908v1\nlayouts and heterogeneous content frequently encountered in visual documents. The pre-trained\nmodel is fine-tuned using a large-scale instruction dataset, covering four core document intelligence\ntasks. We demonstrate that our solution outperforms SotA LLMs on 14 out of 16 datasets across all\ntasks, and generalizes well to 4 out of 5 previously unseen datasets.\nKeywords DocAI - VRDU - LLM - GPT - Spatial Attention\n1\n Introduction\nDocuments with rich layouts, including invoices, receipts, contracts, orders, and forms, constitute a significant portion\nof enterprise corpora. The automatic interpretation and analysis of these documents offer considerable advantages [].\nwhich has spurred the development of AI-driven solutions. These visually rich documents feature complex layouts,\nbespoke type-setting, and often exhibit variations in templates, formats and quality. Although Document AI (DocAIl) has\nmade tremendous progress in various tasks including extraction, classification and question answering, there remains a\nsignificant performance gap in real-world applications. In particular, accuracy, reliability, contextual understanding and\ngeneralization to previously unseen domains continues to be a challenge [2].\nDocument intelligence is inherently a multi-modal problem with both the text content and visual layout cues being\ncritical to understanding the documents. It requires solutions distinct from conventional large language models such as\nGPT-3.5 [l, Llama [41, Falcon [ll or PaLM [] that primarily accept text-only inputs and assume that the documents\nexhibit simple layouts and uniform formatting, which may not be suitable for handling visual documents. Numerous\nvision-language frameworks [7] that can process documents as images and capture the interactions between textual\nand visual modalities are available. However, these frameworks necessitate the use of complex vision backbone\narchitectures [] to encode image information, and they often make use of spatial information as an auxiliary contextual\nsignal [L0 I].\nIn this paper we present DocLLM, a light-weight extension to standard LLMs that excels in several visually rich form\nunderstanding tasks. Unlike traditional LLMs, it models both spatial layouts and text semantics, and therefore is\n* These authors contributed equally to this work"
- **Bilderkennung (1. Bild):** "Who is the \"Supplier\"?\n(DOMEST\n(Recommended Props\nAnalytic Insight Inc\nate\nMarch3.199\nescription\nLUCKY STRIKE QUALITATIVE ADV\nCITIES\n INFILL\nWhat is the doc type?\nequested byz\nA.A.Strobel\nResearch Req\nBudgeted:\nPurchase Order\nOriginal Budgeted\nwntract.\nIs the year 1995?\nYes\nOCRed Document\nLLM Extension\nPre-training\nInstruction Tuning\nText tokens + Bounding boxes\nDisentangled Spatial Attention\nBlocks + Infilling Objective\nKIE + NLI + VQA+ Classify"

### Nougat

- **Texterkennung**: "\n\n# DocLLM: A layout-aware generative language model for multimodal document understanding\n\nDongsheng Wang\n\nThese authors contributed equally to this work.\n\nNatraj Raman\n\nThis work was supported by the National Science Foundation of China (No. 116731002) and the National Science Foundation of China (No. 116731002).\n\nMathieu Sibue1\n\nZhiqiang Ma\n\nPetr Babkin\n\nSmerjot Kaur\n\nYulong Pei\n\nArmineh Nourbakhsh\n\nXiaomo Liu\n\nJPMorgan AI Research\n\n{first.last}@jpmchase.com\n\nFootnote 1: footnotemark:\n\n###### Abstract\n\nEnterprise documents such as forms, invoices, receipts, reports, contracts, and other similar records, often carry rich semantics at the intersection of textual and spatial modalities. The visual cues offered by their complex layouts play a crucial role in comprehending these documents effectively. In this paper, we present DocLLM, a lightweight extension to traditional large language models (LLMs) for reasoning over visual documents, taking into account both textual semantics and spatial layout. Our model differs from existing multimodal LLMs by avoiding expensive image encoders and focuses exclusively on bounding box information to incorporate the spatial layout structure. Specifically, the cross-alignment between text and spatial modalities is captured by decomposing the attention mechanism in classical transformers to a set of disentangled matrices. Furthermore, we devise a pre-training objective that learns to infill text segments. This approach allows us to address irregular layouts and heterogeneous content frequently encountered in visual documents. The pre-trained model is fine-tuned using a large-scale instruction dataset, covering four core document intelligence tasks. We demonstrate that our solution outperforms SotA LLMs on 14 out of 16 datasets across all tasks, and generalizes well to 4 out of 5 previously unseen datasets.\n\nDocAI \\(\\cdot\\) VRDU \\(\\cdot\\) LLM \\(\\cdot\\) GPT \\(\\cdot\\) Spatial Attention\n\n## 1 Introduction\n\nDocuments with rich layouts, including invoices, receipts, contracts, orders, and forms, constitute a significant portion of enterprise corpora. The automatic interpretation and analysis of these documents offer considerable advantages [1], which has spurred the development of AI-driven solutions. These visually rich documents feature complex layouts, bespoke type-setting, and often exhibit variations in templates, formats and quality. Although Document AI (DocAI) has made tremendous progress in various tasks including extraction, classification and question answering, there remains a significant performance gap in real-world applications. In particular, accuracy, reliability, contextual understanding and generalization to previously unseen domains continues to be a challenge [2].\n\nDocument intelligence is inherently a multi-modal problem with both the text content and visual layout cues being critical to understanding the documents. It requires solutions distinct from conventional large language models such as GPT-3.5 [3], Llama [4], Falcon [5] or PaLM [6] that primarily accept text-only inputs and assume that the documents exhibit simple layouts and uniform formatting, which may not be suitable for handling visual documents. Numerous vision-language frameworks [7] that can process documents as images and capture the interactions between textual and visual modalities are available. However, these frameworks necessitate the use of complex vision backbone architectures [9] to encode image information, and they often make use of spatial information as an auxiliary contextual signal [10][11].\n\nIn this paper we present DocLLM, a light-weight extension to standard LLMs that excels in several visually rich form understanding tasks. Unlike traditional LLMs, it models both spatial layouts and text semantics, and therefore is"
- **Bilderkennung:** "\n\n**OCRed Document**\n\nText tokens + Bounding boxes\n\nDisentangled Spatial Attention\n\n**Pre-training**\n\n**Instruction Tuning**\n\n**Closing the number of tokens + Bounding boxes\n\n**OCRed Document**\n\n**Text tokens + Bounding boxes**\n\nDisentangled Spatial Attention\n\n**OCRed Document**\n"

## Allgemeine Informationen (Fall 2: Intensiver Vergleich)

- **Dokumente:** Paper-PDFs aus ArXiv (Abgelegt in **Odyss.AI.Backend.LLM/Paper**)
- **Anzahl Dokumente:** 19
- **Themen der Dokumente**: Mathematik, Informatik (Machine Learning)

## Vergleichskriterien (Fall 2)

| Kriterium                                              | Tesseract | Paddle     | Nougat   |
| ------------------------------------------------------ | --------- | ---------- | -------- |
| **Verarbeitungszeit (min)**                      | 0:30      | 0:22       | 14:30    |
| **Formatierung (ja/nein)**                       | ja        | nein       | ja       |
| **Benutzerfreundlichkeit (gut/mittel/schlecht)** | gut       | gut/mittel | schlecht |
| **Sonderzeichen/Formeln (%)**                    |           |            |          |

## Ergebnisse im Detail (Seite 1, Fall 2)

### Tesseract

- **Bilderkennung**: "401.00908v1 [cs.CL] 31 Dec 2023\n\nDOCLLM: A LAYOUT-AWARE GENERATIVE LANGUAGE MODEL\nFOR MULTIMODAL DOCUMENT UNDERSTANDING\n\nDongsheng Wang”, Natraj Raman*, Mathieu Sibue*\nZhiqiang Ma, Petr Babkin, Simerjot Kaur, Yulong Pei, Armineh Nourbakhsh, Xiaomo Liu\nJPMorgan Al Research\n{first .last}@jpmchase.com\n\nABSTRACT\n\nEnterprise documents such as forms, invoices, receipts, reports, contracts, and other similar records,\noften carry rich semantics at the intersection of textual and spatial modalities. The visual cues offered\nby their complex layouts play a crucial role in comprehending these documents effectively. In this\nPaper, we present DocLLM, a lightweight extension to traditional large language models (LLMs) for\nreasoning over visual documents, taking into account both textual semantics and spatial layout. Our\nmodel differs from existing multimodal LLMs by avoiding expensive image encoders and focuses\nexclusively on bounding box information to incorporate the spatial layout structure. Specifically,\nthe cross-alignment between text and spatial modalities is captured by decomposing the attention\nmechanism in classical transformers to a set of disentangled matrices. Furthermore, we devise a\npre-training objective that learns to infill text segments. This approach allows us to address irregular\nlayouts and heterogeneous content frequently encountered in visual documents. The pre-trained\nmodel is fine-tuned using a large-scale instruction dataset, covering four core document intelligence\ntasks. We demonstrate that our solution outperforms SotA LLMs on 14 out of 16 datasets across all\ntasks, and generalizes well to 4 out of 5 previously unseen datasets.\n\nKeywords DocAl- VRDU - LLM - GPT - Spatial Attention\n\n1 Introduction\n\nDocuments with rich layouts, including invoices, receipts, contracts, orders, and forms, constitute a significant portion\nof enterprise corpora. The automatic interpretation and analysis of these documents offer considerable advantages [I],\nwhich has spurred the development of Al-driven solutions. These visually rich documents feature complex layouts,\nbespoke type-setting, and often exhibit variations in templates, formats and quality. Although Document AI (DocAl) has\nmade tremendous progress in various tasks including extraction, classification and question answering, there remains a\nsignificant performance gap in real-world applications. In particular, accuracy, reliability, contextual understanding and\ngeneralization to previously unseen domains continues to be a challenge\n\nDocument intelligence is inherently a multi-modal problem with both the text content and visual layout cues being\ncritical to understanding the documents. It requires solutions distinct from conventional large language models such as\nGPT-3.5 [3], Llama [4], Falcon [5]] or PaLM [6] that primarily accept text-only inputs and assume that the documents\nexhibit simple layouts and uniform formatting, which may not be suitable for handling visual documents. Numerous\nvision-language frameworks [[71|8]] that can process documents as images and capture the interactions between textual\nand visual modalities are available. However, these frameworks necessitate the use of complex vision backbone\narchitectures [9] to encode image information, and they often make use of spatial information as an auxiliary contextual\nsignal (70,(11).\n\nIn this paper we present DocLLM, a light-weight extension to standard LLMs that excels in several visually rich form\nunderstanding tasks. Unlike traditional LLMs, it models both spatial layouts and text semantics, and therefore is\n\n“These authors contributed equally to this work.\n"

### Paddle

- **Bilderkennung:** "DOCLLM: A LAYOUT-AWARE GENERATIVE LANGUAGE MODEL\nFOR MULTIMODAL DOCUMENT UNDERSTANDING\nDongsheng Wang*, Natraj Raman\", Mathieu Sibue\nZhiqiang Ma, Petr Babkin, Simerjot Kaur, Yulong Pei, Armineh Nourbakhsh, Xiaomo Liu\n JPMorgan AI Research\n 2023\n{first.last}@jpmchase.com\nDec '\nABSTRACT\nEnterprise documents such as forms, invoices, receipts, reports, contracts, and other similar records.\noften carry rich semantics at the intersection of textual and spatial modalities. The visual cues offered\nby their complex layouts play a crucial role in comprehending these documents effectively. In this\nreasoning over visual documents, taking into account both textual semantics and spatial layout. Our\nmodel differs from existing multimodal LLMs by avoiding expensive image encoders and focuses\nexclusively on bounding box information to incorporate the spatial layout structure. Specifically.\nthe cross-alignment between text and spatial modalities is captured by decomposing the attention\nmechanism in classical transformers to a set of disentangled matrices. Furthermore, we devise a\npre-training objective that learns to infill text segments. This approach allows us to address irregular\n00908v1\nlayouts and heterogeneous content frequently encountered in visual documents. The pre-trained\nmodel is fine-tuned using a large-scale instruction dataset, covering four core document intelligence\ntasks. We demonstrate that our solution outperforms SotA LLMs on 14 out of 16 datasets across all\ntasks, and generalizes well to 4 out of 5 previously unseen datasets.\nKeywords DocAI - VRDU - LLM - GPT - Spatial Attention\n1\n Introduction\nDocuments with rich layouts, including invoices, receipts, contracts, orders, and forms, constitute a significant portion\nof enterprise corpora. The automatic interpretation and analysis of these documents offer considerable advantages [].\nwhich has spurred the development of AI-driven solutions. These visually rich documents feature complex layouts,\nbespoke type-setting, and often exhibit variations in templates, formats and quality. Although Document AI (DocAIl) has\nmade tremendous progress in various tasks including extraction, classification and question answering, there remains a\nsignificant performance gap in real-world applications. In particular, accuracy, reliability, contextual understanding and\ngeneralization to previously unseen domains continues to be a challenge [2].\nDocument intelligence is inherently a multi-modal problem with both the text content and visual layout cues being\ncritical to understanding the documents. It requires solutions distinct from conventional large language models such as\nGPT-3.5 [l, Llama [41, Falcon [ll or PaLM [] that primarily accept text-only inputs and assume that the documents\nexhibit simple layouts and uniform formatting, which may not be suitable for handling visual documents. Numerous\nvision-language frameworks [7] that can process documents as images and capture the interactions between textual\nand visual modalities are available. However, these frameworks necessitate the use of complex vision backbone\narchitectures [] to encode image information, and they often make use of spatial information as an auxiliary contextual\nsignal [L0 I].\nIn this paper we present DocLLM, a light-weight extension to standard LLMs that excels in several visually rich form\nunderstanding tasks. Unlike traditional LLMs, it models both spatial layouts and text semantics, and therefore is\n* These authors contributed equally to this work"

### Nougat

- **Bilderkennung:** "\n\n# DocLLM: A layout-aware generative language model for multimodal document understanding\n\nDongsheng Wang\n\nThese authors contributed equally to this work.\n\nNatraj Raman\n\nThis work was supported by the National Science Foundation of China (No. 116731002) and the National Science Foundation of China (No. 116731002).\n\nMathieu Sibue1\n\nZhiqiang Ma\n\nPetr Babkin\n\nSmerjot Kaur\n\nYulong Pei\n\nArmineh Nourbakhsh\n\nXiaomo Liu\n\nJPMorgan AI Research\n\n{first.last}@jpmchase.com\n\nFootnote 1: footnotemark:\n\n###### Abstract\n\nEnterprise documents such as forms, invoices, receipts, reports, contracts, and other similar records, often carry rich semantics at the intersection of textual and spatial modalities. The visual cues offered by their complex layouts play a crucial role in comprehending these documents effectively. In this paper, we present DocLLM, a lightweight extension to traditional large language models (LLMs) for reasoning over visual documents, taking into account both textual semantics and spatial layout. Our model differs from existing multimodal LLMs by avoiding expensive image encoders and focuses exclusively on bounding box information to incorporate the spatial layout structure. Specifically, the cross-alignment between text and spatial modalities is captured by decomposing the attention mechanism in classical transformers to a set of disentangled matrices. Furthermore, we devise a pre-training objective that learns to infill text segments. This approach allows us to address irregular layouts and heterogeneous content frequently encountered in visual documents. The pre-trained model is fine-tuned using a large-scale instruction dataset, covering four core document intelligence tasks. We demonstrate that our solution outperforms SotA LLMs on 14 out of 16 datasets across all tasks, and generalizes well to 4 out of 5 previously unseen datasets.\n\nDocAI \\(\\cdot\\) VRDU \\(\\cdot\\) LLM \\(\\cdot\\) GPT \\(\\cdot\\) Spatial Attention\n\n## 1 Introduction\n\nDocuments with rich layouts, including invoices, receipts, contracts, orders, and forms, constitute a significant portion of enterprise corpora. The automatic interpretation and analysis of these documents offer considerable advantages [1], which has spurred the development of AI-driven solutions. These visually rich documents feature complex layouts, bespoke type-setting, and often exhibit variations in templates, formats and quality. Although Document AI (DocAI) has made tremendous progress in various tasks including extraction, classification and question answering, there remains a significant performance gap in real-world applications. In particular, accuracy, reliability, contextual understanding and generalization to previously unseen domains continues to be a challenge [2].\n\nDocument intelligence is inherently a multi-modal problem with both the text content and visual layout cues being critical to understanding the documents. It requires solutions distinct from conventional large language models such as GPT-3.5 [3], Llama [4], Falcon [5] or PaLM [6] that primarily accept text-only inputs and assume that the documents exhibit simple layouts and uniform formatting, which may not be suitable for handling visual documents. Numerous vision-language frameworks [7] that can process documents as images and capture the interactions between textual and visual modalities are available. However, these frameworks necessitate the use of complex vision backbone architectures [9] to encode image information, and they often make use of spatial information as an auxiliary contextual signal [10][11].\n\nIn this paper we present DocLLM, a light-weight extension to standard LLMs that excels in several visually rich form understanding tasks. Unlike traditional LLMs, it models both spatial layouts and text semantics, and therefore is"

## Zusammenfassung der Ergebnisse

- **Tesseract:** Sehr gut für Standard-Textextraktion, unterstützt viele Sprachen, jedoch probleme bei komplexeren Layouts oder Dokumenten mi tspeziellenFormatierungen und Handwriting
- **Paddle:** Bietet herausragende Performance bei der Erkennung von Text aus Bildern mit komplexen Layouts und liefert gute Ergebnisse bei handschriftlichen und gemischten Dokumenten, jedoch etwas ressourcenintensiv und benötigt mehr Rechenleistung
- **Nougat:** Sehr gut bei der Erkennung von Texten aus schwer lesbaren Quellen und Dokumenten mitungewöhnlichen Layouts. Fokussiert auf unstrukturierte Textdaten und Bildverarbeitung, jedoch Noch in der Entwicklung, sodass es weniger dokumentierte Funktionen und eine kleinere Nutzerbasis gibt und sehr ressourcenintensiv und benötigt viel mehr Rechenleistung

## Fehleranalyse

### Häufigste Fehlerarten

- **Tesseract:**

  - **Zeichenfehler:**
    - Falsche Erkennung von Zeichen, z. B. wird „JPMorgan AI Research“ teilweise als „JPMorgan Al Research“ ausgegeben.
    - Verwechslungen bei Sonderzeichen wie Anführungszeichen (z. B. „Dongsheng Wang”“).
  - **Interpunktions- und Formatierungsfehler:**
    - Unregelmäßigkeiten bei Klammer- und Zitationszeichen (z. B. fehlerhafte Erkennung von eckigen Klammern, wie in „Falcon [5]]“).
  - **Layout-Inkonsistenzen:**
    - Teilweise fehlerhafte Trennung und Anordnung von Textabschnitten.
- **PaddleOCR:**

  - **Zeilenumbruch- und Einfügefehler:**
    - Fehlende oder überflüssige Zeilenumbrüche, was zu fragmentierten Sätzen führt (Beispiel: „Dec '“ oder das Einfügen von „00908v1“ mitten im Text).
  - **Zeichenersetzung:**
    - Fehlerhafte Erkennung von Sonderzeichen, wie das Verwechseln von „DocAI“ mit „DocAIl“.
  - **Unklare Segmentierung bei Zitaten:**
    - Probleme bei der korrekten Erkennung von Zitations- und Referenzelementen (z. B. fehlerhafte eckige Klammern und inkonsistente Zitatnummern).
- **Nougat:**

  - **Kleine Namens- und Fußnotenfehler:**
    - Zusätzliche Zeichen in Namen, z. B. „Mathieu Sibue1“ statt „Mathieu Sibue“.
    - Unvollständige oder unsauber formatierte Fußnoten („Footnote 1: footnotemark:“).
  - **Numerische Artefakte:**
    - Seltenes Einfügen von Zahlen oder Zeichen, die nicht zum Originaltext gehören.
  - **Allgemeine Sauberkeit:**
    - Insgesamt klarere Struktur und bessere Trennung von Titeln, Abstract und Fließtext, wenngleich kleinere Fehler auftreten.

### Vergleich der Fehlerhäufigkeit

- **Struktur und Sauberkeit:**

  - **Nougat** liefert im Allgemeinen die sauberste und am besten strukturierte Ausgabe, mit klar abgegrenzten Abschnitten und wenigen Fehlern.
  - **Tesseract** weist ähnliche Fehler auf, die typischerweise in der Zeichen- und Interpunktionswiedergabe liegen, jedoch ist die Grundstruktur weitgehend erkennbar.
- **Zeichen- und Formatierungsfehler:**

  - **Tesseract** tendiert zu typischen OCR-Zeichenfehlern (z. B. „Al“ statt „AI“, doppelte oder fehlende Klammern).
  - **PaddleOCR** hat häufiger Probleme mit falschen Zeilenumbrüchen und unerwünschten Einfügungen, was zu einer inkonsistenteren Textausgabe führt.
- **Spezifische Detailgenauigkeit:**

  - Während **Nougat** auch kleinere Fehler (wie Namenszusätze) aufweist, scheinen diese im Vergleich zur insgesamt besseren Formatierung unbedeutend.
  - **PDFReader** liefert Ergebnisse, die in vielen Aspekten mit denen von Tesseract vergleichbar sind, enthält jedoch zusätzliche Metadaten (z. B. Versionsangaben), die nicht immer zum eigentlichen Text gehören.

### Zusammenfassung

- **Nougat** ist hinsichtlich der Struktur und Klarheit der Ausgabe am besten geeignet, mit nur marginalen Fehlern bei Namen und Fußnoten.
- **Tesseract**  liefert vergleichbare Ergebnisse, bei denen jedoch typische OCR-Fehler wie falsche Zeichen und inkonsistente Interpunktion auftreten.
- **PaddleOCR** zeigt die häufigsten Probleme bei Zeilenumbrüchen und der falschen Erkennung von Sonderzeichen, was zu einer insgesamt weniger konsistenten Textausgabe führt.

Diese Analyse hilft, die Stärken und Schwächen der einzelnen OCR-Technologien zu bewerten und zeigt, dass die Wahl der passenden Lösung vom spezifischen Anwendungsfall abhängt.

## Ausführen der DocumentOCRResults2-Klasse

Um die `DocumentOCRResults2`-Klasse auszuführen, folge diesen Schritten:

### Wechsle zum richtigen Verzeichnis:

Wechsle in das Verzeichnis, in dem sich die Datei `DocumentOCRResults2.py` befindet. In diesem Fall ist das Verzeichnis:

Du kannst dies im Terminal mit folgendem Befehl tun:

```bash
cd Odyss.AI.Backend.OCR

python -m app.service.DocumentOCRResults2
```

---

## To Do

* **Datensatz-Erweiterung:**

  * Die OCRs wurden anhand von 19 Dokumenten verglichen. Erste Ergebnisse liegen vor, jedoch noch nicht detailliert. Optional kann die Analyse erweitert und umfassender getestet werden.
* **Formelerkennung:** Ziel: Formeln sollen direkt aus vollständigen Dokumenten extrahiert werden können.
* Aktueller Stand:

  * Die einzige bisher getestete Open-Source-Lösung (LaTeX-OCR – [GitHub-Link](https://github.com/lukas-blecher/LaTeX-OCR)) funktioniert nur, wenn die Formel isoliert vorliegt.
  * Es gibt weitere Programme zur Formelerkennung aus Dokumenten, diese sind jedoch nicht Open Source.
  * Nougat bietet ebenfalls eine Möglichkeit zur Extraktion von Formeln aus vollständigen Dokumenten. Dies befindet sich jedoch noch in der **Initial-Phase** und muss getestet werden.
* Nächste Schritte:

  * Nougat auf seine Fähigkeit zur Formelerkennung testen und evaluieren.
  * Eine eigene Lösung zur Extraktion von Formeln aus vollständigen Dokumenten entwickeln oder bestehende Ansätze erweitern.
  * Erfolgreiche Methoden in das bestehende System integrieren.
