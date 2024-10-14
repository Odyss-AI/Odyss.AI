## OCR Vergleich: Tesseract vs. Paddle vs. Nougat

## Einleitung

In diesem Dokument vergleichen wir drei OCR-Technologien: Tesseract, Paddle und Nougat. Ziel ist es, ihre Leistungsfähigkeit hinsichtlich Textgenauigkeit, Verarbeitungszeit und Benutzerfreundlichkeit zu bewerten mit **PDFReader**. Wir testen verschiedene Dokumenttypen, darunter:

1. Normale Dokumente mit markierbarem Text und Bildern **(Fall 1)**
2. Dokumente, die nur aus Bildern bestehen **(Fall 2)**
3. Word- und PowerPoint-Dokumente, die in PDFs konvertiert wurden **(Fall 3)**

Die folgenden Kriterien werden zur Bewertung herangezogen.

## Allgemeine Informationen (Fall 2)

- **Dokument:** Paper als Images
- **Anzahl Seiten:** 16 Seiten als Images

## Vergleichskriterien (Fall 2)

| Kriterium                                              | Tesseract       | Paddle                     | Nougat                     |
| ------------------------------------------------------ | --------------- | -------------------------- | -------------------------- |
| **Textgenauigkeit (%)**                          | [Genauigkeit T] | [Genauigkeit P]            | [Genauigkeit N]            |
| **Verarbeitungszeit (min)**                      | 0:30            | [Zeit P]                   | [Zeit N]                   |
| **Formatierung (ja/nein)**                       | ja              | [Format P]                 | [Format N]                 |
| **Bilderkennung (Anzahl)**                       | 16              | [Anzahl P]                 | [Anzahl N]                 |
| **Skalierbarkeit**                               | [Skalierung T]  | [Skalierung P]             | [Skalierung N]             |
| **Fehlerrate (%)**                               | [Fehler T]      | [Fehler P]                 | [Fehler N]                 |
| **Benutzerfreundlichkeit (gut/mittel/schlecht)** | gut             | [Benutzerfreundlichkeit P] | [Benutzerfreundlichkeit N] |
| **Sonderzeichen/Formeln (%)**                    | [Formeln T]     | [Formeln P]                | [Formeln N]                |

## Ergebnisse im Detail (Seite 1, Fall 2)

### Tesseract 

- **Textgenauigkeit:** "401.00908v1 [cs.CL] 31 Dec 2023\n\nDOCLLM: A LAYOUT-AWARE GENERATIVE LANGUAGE MODEL\nFOR MULTIMODAL DOCUMENT UNDERSTANDING\n\nDongsheng Wang”, Natraj Raman*, Mathieu Sibue*\nZhiqiang Ma, Petr Babkin, Simerjot Kaur, Yulong Pei, Armineh Nourbakhsh, Xiaomo Liu\nJPMorgan Al Research\n{first .last}@jpmchase.com\n\nABSTRACT\n\nEnterprise documents such as forms, invoices, receipts, reports, contracts, and other similar records,\noften carry rich semantics at the intersection of textual and spatial modalities. The visual cues offered\nby their complex layouts play a crucial role in comprehending these documents effectively. In this\nPaper, we present DocLLM, a lightweight extension to traditional large language models (LLMs) for\nreasoning over visual documents, taking into account both textual semantics and spatial layout. Our\nmodel differs from existing multimodal LLMs by avoiding expensive image encoders and focuses\nexclusively on bounding box information to incorporate the spatial layout structure. Specifically,\nthe cross-alignment between text and spatial modalities is captured by decomposing the attention\nmechanism in classical transformers to a set of disentangled matrices. Furthermore, we devise a\npre-training objective that learns to infill text segments. This approach allows us to address irregular\nlayouts and heterogeneous content frequently encountered in visual documents. The pre-trained\nmodel is fine-tuned using a large-scale instruction dataset, covering four core document intelligence\ntasks. We demonstrate that our solution outperforms SotA LLMs on 14 out of 16 datasets across all\ntasks, and generalizes well to 4 out of 5 previously unseen datasets.\n\nKeywords DocAl- VRDU - LLM - GPT - Spatial Attention\n\n1 Introduction\n\nDocuments with rich layouts, including invoices, receipts, contracts, orders, and forms, constitute a significant portion\nof enterprise corpora. The automatic interpretation and analysis of these documents offer considerable advantages [I],\nwhich has spurred the development of Al-driven solutions. These visually rich documents feature complex layouts,\nbespoke type-setting, and often exhibit variations in templates, formats and quality. Although Document AI (DocAl) has\nmade tremendous progress in various tasks including extraction, classification and question answering, there remains a\nsignificant performance gap in real-world applications. In particular, accuracy, reliability, contextual understanding and\ngeneralization to previously unseen domains continues to be a challenge\n\nDocument intelligence is inherently a multi-modal problem with both the text content and visual layout cues being\ncritical to understanding the documents. It requires solutions distinct from conventional large language models such as\nGPT-3.5 [3], Llama [4], Falcon [5]] or PaLM [6] that primarily accept text-only inputs and assume that the documents\nexhibit simple layouts and uniform formatting, which may not be suitable for handling visual documents. Numerous\nvision-language frameworks [[71|8]] that can process documents as images and capture the interactions between textual\nand visual modalities are available. However, these frameworks necessitate the use of complex vision backbone\narchitectures [9] to encode image information, and they often make use of spatial information as an auxiliary contextual\nsignal (70,(11).\n\nIn this paper we present DocLLM, a light-weight extension to standard LLMs that excels in several visually rich form\nunderstanding tasks. Unlike traditional LLMs, it models both spatial layouts and text semantics, and therefore is\n\n“These authors contributed equally to this work.\n" 
- 
- **Verarbeitungszeit:** [Details]
- **Formatierung:** [Details]
- **Bilderkennung:** [Details]
- **Skalierbarkeit:** [Details]
- **Fehlerrate:** [Details]
- **Benutzerfreundlichkeit:** [Details]
- **Sonderzeichen/Formeln:** [Details]

### Paddle

- **Textgenauigkeit:** [Details]
- **Verarbeitungszeit:** [Details]
- **Formatierung:** [Details]
- **Bilderkennung:** [Details]
- **Skalierbarkeit:** [Details]
- **Fehlerrate:** [Details]
- **Benutzerfreundlichkeit:** [Details]
- **Sonderzeichen/Formeln:** [Details]

### Nougat

- **Textgenauigkeit:** [Details]
- **Verarbeitungszeit:** [Details]
- **Formatierung:** [Details]
- **Bilderkennung:** [Details]
- **Skalierbarkeit:** [Details]
- **Fehlerrate:** [Details]
- **Benutzerfreundlichkeit:** [Details]
- **Sonderzeichen/Formeln:** [Details]

## Zusammenfassung der Ergebnisse

- **Tesseract:** [Kurze Zusammenfassung, z.B. "Tesseract erzielte die höchste Textgenauigkeit, hatte jedoch eine längere Verarbeitungszeit."]
- **Paddle:** [Kurze Zusammenfassung, z.B. "Paddle bot eine gute Balance zwischen Genauigkeit und Geschwindigkeit."]
- **Nougat:** [Kurze Zusammenfassung, z.B. "Nougat war benutzerfreundlich, jedoch weniger genau."]

Diese Ergebnisse werden im Detail in den folgenden Abschnitten beschrieben.

## Fehleranalyse

### Häufigste Fehlerarten

- **Tesseract:** [Details zu häufigen Fehlern, z.B. "Häufige falsche Buchstabierungen bei speziellen Fachbegriffen."]
- **Paddle:** [Details zu häufigen Fehlern.]
- **Nougat:** [Details zu häufigen Fehlern.]

### Vergleich der Fehlerhäufigkeit

- [Hier kannst du eventuell eine Tabelle einfügen, die die Häufigkeit spezifischer Fehlerarten vergleicht.]

## Schlussfolgerung und Empfehlungen

Basierend auf den durchgeführten Tests lässt sich Folgendes feststellen:

- **Für Dokumente mit hohem Textanteil:** [Empfehlung z.B. "Tesseract hat sich als die beste Wahl erwiesen."]
- **Für Dokumente mit vielen Bildern:** [Empfehlung.]
- **Für Benutzerfreundlichkeit:** [Empfehlung, z.B. "Nougat bietet die intuitivste Benutzeroberfläche."]

Zusammenfassend kann gesagt werden, dass jede OCR-Technologie ihre Stärken und Schwächen hat, und die Wahl der besten Technologie hängt stark von den spezifischen Anforderungen des Anwendungsfalls ab.
