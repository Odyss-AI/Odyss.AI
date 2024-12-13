## OCR Vergleich: Tesseract vs. Paddle vs. Nougat

## Einleitung

In diesem Dokument vergleichen wir drei OCR-Technologien: Tesseract, Paddle und Nougat. Ziel ist es, ihre Leistungsfähigkeit hinsichtlich Textgenauigkeit, Verarbeitungszeit und Benutzerfreundlichkeit zu bewerten im Vergleich zu einem **PDFReader**. Wir testen verschiedene Dokumenttypen, darunter:

1. Normale Dokumente mit markierbarem Text und Bildern **(Fall 1)**
2. Dokumente, die nur aus Bildern bestehen **(Fall 2)**

Die folgenden Kriterien werden zur Bewertung herangezogen.

## Allgemeine Informationen (Fall 1)

- **Dokument:** Paper (normales Dokument)
- **Anzahl Seiten:** 16 Seiten

## Vergleichskriterien (Fall 1)

| Kriterium                                              | Tesseract   | PaddleOCR   | Nougat      |
| :----------------------------------------------------- | ----------- | ----------- | ----------- |
| **Textgenauigkeit (%)**                          | 5.30        | 5.27        | 5.23        |
| **Verarbeitungszeit (min)**                      | 0:30        | 0:28        | 14:05       |
| **Formatierung *(*ja*****/ja/nein)**           | ja*         | ja          | ja*         |
| **Bilderkennung (Anzahl)**                       | 5           | 5           | 5           |
| **Fehlerrate (%)**                               | 6.26        | 9.24        | 23.04       |
| **Benutzerfreundlichkeit (gut/mittel/schlecht)** | gut         | mittel      | schlecht    |
| **Sonderzeichen/Formeln (%)**                    | [Formeln T] | [Formeln P] | [Formeln N] |
| **Ähnlichkeitsrate (%)**                        | 85.90       | 61.25       | 72.44       |

## Kriteriumserklärungen

- **Textgenauigkeit (%)** Gibt an, wie genau der von der OCR-Engine erkannte Text im Vergleich zum tatsächlichen Text (Ground Truth) ist. Berechnet durch die Anzahl korrekt erkannter Zeichen im Vergleich zur Gesamtzahl der Zeichen im tatsächlichen Text.
- **Verarbeitungszeit (min)** Misst, wie lange es dauert, ein Dokument mit der OCR-Engine zu verarbeiten. Die Zeit wird in Sekunden oder Minuten gemessen, abhängig von der Größe des Dokuments.
- **Formatierung (ja\*/ja/nein)** Gibt an, ob die OCR-Engine die ursprüngliche Formatierung des Dokuments beibehalten kann, wie Schriftarten, Absätze und Layout.

  - Ja* bedeutet, dass mehr Informationen zu der Formatierung des Dokumentes vorliegen
  - *Ja* bedeutet, dass die OCR-Engine die Formatierung größtenteils beibehalten kann
  - *Nein* bedeutet, dass die OCR-Engine die Formatierung entweder gar nicht beibehalten kann.
- **Bilderkennung (Anzahl)** Zeigt, wie viele Bilder oder Grafiken die OCR-Engine korrekt erkannt hat. Besonders relevant bei Dokumenten, die auch Bilder oder Grafiken enthalten.
- **Skalierbarkeit** Beschreibt, wie gut die OCR-Engine mit einer größeren Anzahl von Dokumenten oder mit Dokumenten unterschiedlicher Komplexität umgehen kann. Eine skalierbare Lösung arbeitet auch mit größeren Datenmengen effizient.
- **Fehlerrate (%)** Auch bekannt als **Char Error Rate (CER)**, misst die Anzahl der Fehler bei der Erkennung von Zeichen im Vergleich zur Ground Truth. Ein niedriger Wert bedeutet weniger Fehler bei der Texterkennung.
- **Benutzerfreundlichkeit (gut/mittel/schlecht)** Beschreibt, wie einfach es ist, mit der OCR-Engine zu arbeiten. Eine benutzerfreundliche Lösung ist einfach zu bedienen, gut dokumentiert und benötigt wenig Eingriff vom Benutzer.
- **Sonderzeichen/Formeln (%)** Misst die Fähigkeit der OCR-Engine, Sonderzeichen oder mathematische Formeln korrekt zu erkennen. Besonders wichtig für technische oder wissenschaftliche Dokumente, die solche Symbole enthalten.
- **Ähnlichkeitsrate (%)** Vergleicht den erkannten Text mit dem tatsächlichen Text (Ground Truth) und zeigt die Übereinstimmung als Prozentsatz.
  Die **Ähnlichkeitsrate** wird üblicherweise mit der **SequenceMatcher**-Methode berechnet, die die Ähnlichkeit zwischen zwei Texten misst. Sie vergleicht die Zeichenfolgen und bestimmt, wie viel von ihnen übereinstimmen, wobei das Ergebnis als Prozentsatz der Übereinstimmung ausgegeben wird. Eine hohe Ähnlichkeitsrate bedeutet, dass der erkannte Text dem tatsächlichen Text sehr ähnlich ist, was auf eine gute Erkennungsgenauigkeit hinweist.

## Ergebnisse im Detail (Seite 1, Fall 1)

### Tesseract

- **Texterkennung**: "401.00908v1 [cs.CL] 31 Dec 2023\n\nDOCLLM: A LAYOUT-AWARE GENERATIVE LANGUAGE MODEL\nFOR MULTIMODAL DOCUMENT UNDERSTANDING\n\nDongsheng Wang”, Natraj Raman*, Mathieu Sibue*\nZhiqiang Ma, Petr Babkin, Simerjot Kaur, Yulong Pei, Armineh Nourbakhsh, Xiaomo Liu\nJPMorgan Al Research\n{first .last}@jpmchase.com\n\nABSTRACT\n\nEnterprise documents such as forms, invoices, receipts, reports, contracts, and other similar records,\noften carry rich semantics at the intersection of textual and spatial modalities. The visual cues offered\nby their complex layouts play a crucial role in comprehending these documents effectively. In this\nPaper, we present DocLLM, a lightweight extension to traditional large language models (LLMs) for\nreasoning over visual documents, taking into account both textual semantics and spatial layout. Our\nmodel differs from existing multimodal LLMs by avoiding expensive image encoders and focuses\nexclusively on bounding box information to incorporate the spatial layout structure. Specifically,\nthe cross-alignment between text and spatial modalities is captured by decomposing the attention\nmechanism in classical transformers to a set of disentangled matrices. Furthermore, we devise a\npre-training objective that learns to infill text segments. This approach allows us to address irregular\nlayouts and heterogeneous content frequently encountered in visual documents. The pre-trained\nmodel is fine-tuned using a large-scale instruction dataset, covering four core document intelligence\ntasks. We demonstrate that our solution outperforms SotA LLMs on 14 out of 16 datasets across all\ntasks, and generalizes well to 4 out of 5 previously unseen datasets.\n\nKeywords DocAl- VRDU - LLM - GPT - Spatial Attention\n\n1 Introduction\n\nDocuments with rich layouts, including invoices, receipts, contracts, orders, and forms, constitute a significant portion\nof enterprise corpora. The automatic interpretation and analysis of these documents offer considerable advantages [I],\nwhich has spurred the development of Al-driven solutions. These visually rich documents feature complex layouts,\nbespoke type-setting, and often exhibit variations in templates, formats and quality. Although Document AI (DocAl) has\nmade tremendous progress in various tasks including extraction, classification and question answering, there remains a\nsignificant performance gap in real-world applications. In particular, accuracy, reliability, contextual understanding and\ngeneralization to previously unseen domains continues to be a challenge\n\nDocument intelligence is inherently a multi-modal problem with both the text content and visual layout cues being\ncritical to understanding the documents. It requires solutions distinct from conventional large language models such as\nGPT-3.5 [3], Llama [4], Falcon [5]] or PaLM [6] that primarily accept text-only inputs and assume that the documents\nexhibit simple layouts and uniform formatting, which may not be suitable for handling visual documents. Numerous\nvision-language frameworks [[71|8]] that can process documents as images and capture the interactions between textual\nand visual modalities are available. However, these frameworks necessitate the use of complex vision backbone\narchitectures [9] to encode image information, and they often make use of spatial information as an auxiliary contextual\nsignal (70,(11).\n\nIn this paper we present DocLLM, a light-weight extension to standard LLMs that excels in several visually rich form\nunderstanding tasks. Unlike traditional LLMs, it models both spatial layouts and text semantics, and therefore is\n\n“These authors contributed equally to this work.\n"
- **Bilderkennung (1. Bild):** "1\nWho is the “Supplier”?\nneem ante 7 Analytic Insight Inc\nINFILL, What is the doc type?\nPurchase Order\np=\nB Is the year 1995?\nae 2,0 Yes\nOCRed Document LLM Extension Pre-training Instruction Tuning\n\nText tokens + Bounding boxes Disentangled Spatial Attention Blocks + Infilling Objective KIE + NLI + VQA + Classify\n"
- **Skalierbarkeit:** [Details]
- **Fehlerrate:** [Details]
- **Sonderzeichen/Formeln:** [Details]
- **Ähnlichkeitsrate**: 85.90% – Tesseract hat den Text mit einer hohen Übereinstimmung zum tatsächlichen Text erkannt.

### Paddle

- **Texterkennung**: "DOCLLM: A LAYOUT-AWARE GENERATIVE LANGUAGE MODEL\nFOR MULTIMODAL DOCUMENT UNDERSTANDING\nDongsheng Wang*, Natraj Raman\", Mathieu Sibue\nZhiqiang Ma, Petr Babkin, Simerjot Kaur, Yulong Pei, Armineh Nourbakhsh, Xiaomo Liu\n JPMorgan AI Research\n 2023\n{first.last}@jpmchase.com\nDec '\nABSTRACT\nEnterprise documents such as forms, invoices, receipts, reports, contracts, and other similar records.\noften carry rich semantics at the intersection of textual and spatial modalities. The visual cues offered\nby their complex layouts play a crucial role in comprehending these documents effectively. In this\nreasoning over visual documents, taking into account both textual semantics and spatial layout. Our\nmodel differs from existing multimodal LLMs by avoiding expensive image encoders and focuses\nexclusively on bounding box information to incorporate the spatial layout structure. Specifically.\nthe cross-alignment between text and spatial modalities is captured by decomposing the attention\nmechanism in classical transformers to a set of disentangled matrices. Furthermore, we devise a\npre-training objective that learns to infill text segments. This approach allows us to address irregular\n00908v1\nlayouts and heterogeneous content frequently encountered in visual documents. The pre-trained\nmodel is fine-tuned using a large-scale instruction dataset, covering four core document intelligence\ntasks. We demonstrate that our solution outperforms SotA LLMs on 14 out of 16 datasets across all\ntasks, and generalizes well to 4 out of 5 previously unseen datasets.\nKeywords DocAI - VRDU - LLM - GPT - Spatial Attention\n1\n Introduction\nDocuments with rich layouts, including invoices, receipts, contracts, orders, and forms, constitute a significant portion\nof enterprise corpora. The automatic interpretation and analysis of these documents offer considerable advantages [].\nwhich has spurred the development of AI-driven solutions. These visually rich documents feature complex layouts,\nbespoke type-setting, and often exhibit variations in templates, formats and quality. Although Document AI (DocAIl) has\nmade tremendous progress in various tasks including extraction, classification and question answering, there remains a\nsignificant performance gap in real-world applications. In particular, accuracy, reliability, contextual understanding and\ngeneralization to previously unseen domains continues to be a challenge [2].\nDocument intelligence is inherently a multi-modal problem with both the text content and visual layout cues being\ncritical to understanding the documents. It requires solutions distinct from conventional large language models such as\nGPT-3.5 [l, Llama [41, Falcon [ll or PaLM [] that primarily accept text-only inputs and assume that the documents\nexhibit simple layouts and uniform formatting, which may not be suitable for handling visual documents. Numerous\nvision-language frameworks [7] that can process documents as images and capture the interactions between textual\nand visual modalities are available. However, these frameworks necessitate the use of complex vision backbone\narchitectures [] to encode image information, and they often make use of spatial information as an auxiliary contextual\nsignal [L0 I].\nIn this paper we present DocLLM, a light-weight extension to standard LLMs that excels in several visually rich form\nunderstanding tasks. Unlike traditional LLMs, it models both spatial layouts and text semantics, and therefore is\n* These authors contributed equally to this work"
- **Bilderkennung (1. Bild):** "Who is the \"Supplier\"?\n(DOMEST\n(Recommended Props\nAnalytic Insight Inc\nate\nMarch3.199\nescription\nLUCKY STRIKE QUALITATIVE ADV\nCITIES\n INFILL\nWhat is the doc type?\nequested byz\nA.A.Strobel\nResearch Req\nBudgeted:\nPurchase Order\nOriginal Budgeted\nwntract.\nIs the year 1995?\nYes\nOCRed Document\nLLM Extension\nPre-training\nInstruction Tuning\nText tokens + Bounding boxes\nDisentangled Spatial Attention\nBlocks + Infilling Objective\nKIE + NLI + VQA+ Classify"
- **Skalierbarkeit:** [Details]
- **Fehlerrate:** [Details]
- **Sonderzeichen/Formeln:** [Details]
- **Ähnlichkeitsrate**: 61.25% – PaddleOCR hat eine moderate Übereinstimmung mit dem tatsächlichen Text.

### Nougat

- **Texterkennung**: "\n\n# DocLLM: A layout-aware generative language model for multimodal document understanding\n\nDongsheng Wang\n\nThese authors contributed equally to this work.\n\nNatraj Raman\n\nThis work was supported by the National Science Foundation of China (No. 116731002) and the National Science Foundation of China (No. 116731002).\n\nMathieu Sibue1\n\nZhiqiang Ma\n\nPetr Babkin\n\nSmerjot Kaur\n\nYulong Pei\n\nArmineh Nourbakhsh\n\nXiaomo Liu\n\nJPMorgan AI Research\n\n{first.last}@jpmchase.com\n\nFootnote 1: footnotemark:\n\n###### Abstract\n\nEnterprise documents such as forms, invoices, receipts, reports, contracts, and other similar records, often carry rich semantics at the intersection of textual and spatial modalities. The visual cues offered by their complex layouts play a crucial role in comprehending these documents effectively. In this paper, we present DocLLM, a lightweight extension to traditional large language models (LLMs) for reasoning over visual documents, taking into account both textual semantics and spatial layout. Our model differs from existing multimodal LLMs by avoiding expensive image encoders and focuses exclusively on bounding box information to incorporate the spatial layout structure. Specifically, the cross-alignment between text and spatial modalities is captured by decomposing the attention mechanism in classical transformers to a set of disentangled matrices. Furthermore, we devise a pre-training objective that learns to infill text segments. This approach allows us to address irregular layouts and heterogeneous content frequently encountered in visual documents. The pre-trained model is fine-tuned using a large-scale instruction dataset, covering four core document intelligence tasks. We demonstrate that our solution outperforms SotA LLMs on 14 out of 16 datasets across all tasks, and generalizes well to 4 out of 5 previously unseen datasets.\n\nDocAI \\(\\cdot\\) VRDU \\(\\cdot\\) LLM \\(\\cdot\\) GPT \\(\\cdot\\) Spatial Attention\n\n## 1 Introduction\n\nDocuments with rich layouts, including invoices, receipts, contracts, orders, and forms, constitute a significant portion of enterprise corpora. The automatic interpretation and analysis of these documents offer considerable advantages [1], which has spurred the development of AI-driven solutions. These visually rich documents feature complex layouts, bespoke type-setting, and often exhibit variations in templates, formats and quality. Although Document AI (DocAI) has made tremendous progress in various tasks including extraction, classification and question answering, there remains a significant performance gap in real-world applications. In particular, accuracy, reliability, contextual understanding and generalization to previously unseen domains continues to be a challenge [2].\n\nDocument intelligence is inherently a multi-modal problem with both the text content and visual layout cues being critical to understanding the documents. It requires solutions distinct from conventional large language models such as GPT-3.5 [3], Llama [4], Falcon [5] or PaLM [6] that primarily accept text-only inputs and assume that the documents exhibit simple layouts and uniform formatting, which may not be suitable for handling visual documents. Numerous vision-language frameworks [7] that can process documents as images and capture the interactions between textual and visual modalities are available. However, these frameworks necessitate the use of complex vision backbone architectures [9] to encode image information, and they often make use of spatial information as an auxiliary contextual signal [10][11].\n\nIn this paper we present DocLLM, a light-weight extension to standard LLMs that excels in several visually rich form understanding tasks. Unlike traditional LLMs, it models both spatial layouts and text semantics, and therefore is"
- **Bilderkennung:** "\n\n**OCRed Document**\n\nText tokens + Bounding boxes\n\nDisentangled Spatial Attention\n\n**Pre-training**\n\n**Instruction Tuning**\n\n**Closing the number of tokens + Bounding boxes\n\n**OCRed Document**\n\n**Text tokens + Bounding boxes**\n\nDisentangled Spatial Attention\n\n**OCRed Document**\n"
- **Skalierbarkeit:** [Details]
- **Fehlerrate:** [Details]
- **Sonderzeichen/Formeln:** [Details]
- **Ähnlichkeitsrate**: 72.44% – Nougat liegt zwischen Tesseract und PaddleOCR, mit einer durchschnittlichen Übereinstimmung.

## Allgemeine Informationen (Fall 2)

- **Dokument:** Paper als Images
- **Anzahl Seiten:** 16 Seiten als Images

## Vergleichskriterien (Fall 2)

| Kriterium                                              | Tesseract       | Paddle          | Nougat          |
| ------------------------------------------------------ | --------------- | --------------- | --------------- |
| **Textgenauigkeit (%)**                          | [Genauigkeit T] | [Genauigkeit P] | [Genauigkeit N] |
| **Verarbeitungszeit (min)**                      | 0:30            | 0:22            | 14:30           |
| **Formatierung (ja/nein)**                       | ja              | nein            | ja              |
|                                                        |                 |                 |                 |
| **Skalierbarkeit**                               | [Skalierung T]  | [Skalierung P]  | [Skalierung N]  |
| **Fehlerrate (%)**                               | [Fehler T]      | [Fehler P]      | [Fehler N]      |
| **Benutzerfreundlichkeit (gut/mittel/schlecht)** | gut             | gut/mittel      | schlecht        |
| **Sonderzeichen/Formeln (%)**                    |                 |                 |                 |

## Ergebnisse im Detail (Seite 1, Fall 2)

### Tesseract

- **Textgenauigkeit:**
- **Bilderkennung**: "401.00908v1 [cs.CL] 31 Dec 2023\n\nDOCLLM: A LAYOUT-AWARE GENERATIVE LANGUAGE MODEL\nFOR MULTIMODAL DOCUMENT UNDERSTANDING\n\nDongsheng Wang”, Natraj Raman*, Mathieu Sibue*\nZhiqiang Ma, Petr Babkin, Simerjot Kaur, Yulong Pei, Armineh Nourbakhsh, Xiaomo Liu\nJPMorgan Al Research\n{first .last}@jpmchase.com\n\nABSTRACT\n\nEnterprise documents such as forms, invoices, receipts, reports, contracts, and other similar records,\noften carry rich semantics at the intersection of textual and spatial modalities. The visual cues offered\nby their complex layouts play a crucial role in comprehending these documents effectively. In this\nPaper, we present DocLLM, a lightweight extension to traditional large language models (LLMs) for\nreasoning over visual documents, taking into account both textual semantics and spatial layout. Our\nmodel differs from existing multimodal LLMs by avoiding expensive image encoders and focuses\nexclusively on bounding box information to incorporate the spatial layout structure. Specifically,\nthe cross-alignment between text and spatial modalities is captured by decomposing the attention\nmechanism in classical transformers to a set of disentangled matrices. Furthermore, we devise a\npre-training objective that learns to infill text segments. This approach allows us to address irregular\nlayouts and heterogeneous content frequently encountered in visual documents. The pre-trained\nmodel is fine-tuned using a large-scale instruction dataset, covering four core document intelligence\ntasks. We demonstrate that our solution outperforms SotA LLMs on 14 out of 16 datasets across all\ntasks, and generalizes well to 4 out of 5 previously unseen datasets.\n\nKeywords DocAl- VRDU - LLM - GPT - Spatial Attention\n\n1 Introduction\n\nDocuments with rich layouts, including invoices, receipts, contracts, orders, and forms, constitute a significant portion\nof enterprise corpora. The automatic interpretation and analysis of these documents offer considerable advantages [I],\nwhich has spurred the development of Al-driven solutions. These visually rich documents feature complex layouts,\nbespoke type-setting, and often exhibit variations in templates, formats and quality. Although Document AI (DocAl) has\nmade tremendous progress in various tasks including extraction, classification and question answering, there remains a\nsignificant performance gap in real-world applications. In particular, accuracy, reliability, contextual understanding and\ngeneralization to previously unseen domains continues to be a challenge\n\nDocument intelligence is inherently a multi-modal problem with both the text content and visual layout cues being\ncritical to understanding the documents. It requires solutions distinct from conventional large language models such as\nGPT-3.5 [3], Llama [4], Falcon [5]] or PaLM [6] that primarily accept text-only inputs and assume that the documents\nexhibit simple layouts and uniform formatting, which may not be suitable for handling visual documents. Numerous\nvision-language frameworks [[71|8]] that can process documents as images and capture the interactions between textual\nand visual modalities are available. However, these frameworks necessitate the use of complex vision backbone\narchitectures [9] to encode image information, and they often make use of spatial information as an auxiliary contextual\nsignal (70,(11).\n\nIn this paper we present DocLLM, a light-weight extension to standard LLMs that excels in several visually rich form\nunderstanding tasks. Unlike traditional LLMs, it models both spatial layouts and text semantics, and therefore is\n\n“These authors contributed equally to this work.\n"
- **Skalierbarkeit:** [Details]
- **Fehlerrate:** [Details]
- **Benutzerfreundlichkeit:** [Details]
- **Sonderzeichen/Formeln:** [Details]

### Paddle

- **Textgenauigkeit:**
- **Verarbeitungszeit:** [Details]
- **Formatierung:** [Details]
- **Bilderkennung:** "DOCLLM: A LAYOUT-AWARE GENERATIVE LANGUAGE MODEL\nFOR MULTIMODAL DOCUMENT UNDERSTANDING\nDongsheng Wang*, Natraj Raman\", Mathieu Sibue\nZhiqiang Ma, Petr Babkin, Simerjot Kaur, Yulong Pei, Armineh Nourbakhsh, Xiaomo Liu\n JPMorgan AI Research\n 2023\n{first.last}@jpmchase.com\nDec '\nABSTRACT\nEnterprise documents such as forms, invoices, receipts, reports, contracts, and other similar records.\noften carry rich semantics at the intersection of textual and spatial modalities. The visual cues offered\nby their complex layouts play a crucial role in comprehending these documents effectively. In this\nreasoning over visual documents, taking into account both textual semantics and spatial layout. Our\nmodel differs from existing multimodal LLMs by avoiding expensive image encoders and focuses\nexclusively on bounding box information to incorporate the spatial layout structure. Specifically.\nthe cross-alignment between text and spatial modalities is captured by decomposing the attention\nmechanism in classical transformers to a set of disentangled matrices. Furthermore, we devise a\npre-training objective that learns to infill text segments. This approach allows us to address irregular\n00908v1\nlayouts and heterogeneous content frequently encountered in visual documents. The pre-trained\nmodel is fine-tuned using a large-scale instruction dataset, covering four core document intelligence\ntasks. We demonstrate that our solution outperforms SotA LLMs on 14 out of 16 datasets across all\ntasks, and generalizes well to 4 out of 5 previously unseen datasets.\nKeywords DocAI - VRDU - LLM - GPT - Spatial Attention\n1\n Introduction\nDocuments with rich layouts, including invoices, receipts, contracts, orders, and forms, constitute a significant portion\nof enterprise corpora. The automatic interpretation and analysis of these documents offer considerable advantages [].\nwhich has spurred the development of AI-driven solutions. These visually rich documents feature complex layouts,\nbespoke type-setting, and often exhibit variations in templates, formats and quality. Although Document AI (DocAIl) has\nmade tremendous progress in various tasks including extraction, classification and question answering, there remains a\nsignificant performance gap in real-world applications. In particular, accuracy, reliability, contextual understanding and\ngeneralization to previously unseen domains continues to be a challenge [2].\nDocument intelligence is inherently a multi-modal problem with both the text content and visual layout cues being\ncritical to understanding the documents. It requires solutions distinct from conventional large language models such as\nGPT-3.5 [l, Llama [41, Falcon [ll or PaLM [] that primarily accept text-only inputs and assume that the documents\nexhibit simple layouts and uniform formatting, which may not be suitable for handling visual documents. Numerous\nvision-language frameworks [7] that can process documents as images and capture the interactions between textual\nand visual modalities are available. However, these frameworks necessitate the use of complex vision backbone\narchitectures [] to encode image information, and they often make use of spatial information as an auxiliary contextual\nsignal [L0 I].\nIn this paper we present DocLLM, a light-weight extension to standard LLMs that excels in several visually rich form\nunderstanding tasks. Unlike traditional LLMs, it models both spatial layouts and text semantics, and therefore is\n* These authors contributed equally to this work"
- **Skalierbarkeit:** [Details]
- **Fehlerrate:** [Details]
- **Benutzerfreundlichkeit:** [Details]
- **Sonderzeichen/Formeln:** [Details]

### Nougat

- **Textgenauigkeit:** [Details]
- **Verarbeitungszeit:** [Details]
- **Formatierung:** [Details]
- **Bilderkennung:** "\n\n# DocLLM: A layout-aware generative language model for multimodal document understanding\n\nDongsheng Wang\n\nThese authors contributed equally to this work.\n\nNatraj Raman\n\nThis work was supported by the National Science Foundation of China (No. 116731002) and the National Science Foundation of China (No. 116731002).\n\nMathieu Sibue1\n\nZhiqiang Ma\n\nPetr Babkin\n\nSmerjot Kaur\n\nYulong Pei\n\nArmineh Nourbakhsh\n\nXiaomo Liu\n\nJPMorgan AI Research\n\n{first.last}@jpmchase.com\n\nFootnote 1: footnotemark:\n\n###### Abstract\n\nEnterprise documents such as forms, invoices, receipts, reports, contracts, and other similar records, often carry rich semantics at the intersection of textual and spatial modalities. The visual cues offered by their complex layouts play a crucial role in comprehending these documents effectively. In this paper, we present DocLLM, a lightweight extension to traditional large language models (LLMs) for reasoning over visual documents, taking into account both textual semantics and spatial layout. Our model differs from existing multimodal LLMs by avoiding expensive image encoders and focuses exclusively on bounding box information to incorporate the spatial layout structure. Specifically, the cross-alignment between text and spatial modalities is captured by decomposing the attention mechanism in classical transformers to a set of disentangled matrices. Furthermore, we devise a pre-training objective that learns to infill text segments. This approach allows us to address irregular layouts and heterogeneous content frequently encountered in visual documents. The pre-trained model is fine-tuned using a large-scale instruction dataset, covering four core document intelligence tasks. We demonstrate that our solution outperforms SotA LLMs on 14 out of 16 datasets across all tasks, and generalizes well to 4 out of 5 previously unseen datasets.\n\nDocAI \\(\\cdot\\) VRDU \\(\\cdot\\) LLM \\(\\cdot\\) GPT \\(\\cdot\\) Spatial Attention\n\n## 1 Introduction\n\nDocuments with rich layouts, including invoices, receipts, contracts, orders, and forms, constitute a significant portion of enterprise corpora. The automatic interpretation and analysis of these documents offer considerable advantages [1], which has spurred the development of AI-driven solutions. These visually rich documents feature complex layouts, bespoke type-setting, and often exhibit variations in templates, formats and quality. Although Document AI (DocAI) has made tremendous progress in various tasks including extraction, classification and question answering, there remains a significant performance gap in real-world applications. In particular, accuracy, reliability, contextual understanding and generalization to previously unseen domains continues to be a challenge [2].\n\nDocument intelligence is inherently a multi-modal problem with both the text content and visual layout cues being critical to understanding the documents. It requires solutions distinct from conventional large language models such as GPT-3.5 [3], Llama [4], Falcon [5] or PaLM [6] that primarily accept text-only inputs and assume that the documents exhibit simple layouts and uniform formatting, which may not be suitable for handling visual documents. Numerous vision-language frameworks [7] that can process documents as images and capture the interactions between textual and visual modalities are available. However, these frameworks necessitate the use of complex vision backbone architectures [9] to encode image information, and they often make use of spatial information as an auxiliary contextual signal [10][11].\n\nIn this paper we present DocLLM, a light-weight extension to standard LLMs that excels in several visually rich form understanding tasks. Unlike traditional LLMs, it models both spatial layouts and text semantics, and therefore is"
- **Skalierbarkeit:** [Details]
- **Fehlerrate:** [Details]
- **Benutzerfreundlichkeit:** mittel
- **Sonderzeichen/Formeln:** [Details]

## Zusammenfassung der Ergebnisse

- **Tesseract:** Sehr gut für Standard-Textextraktion, unterstützt viele Sprachen, jedoch probleme bei komplexeren Layouts oder Dokumenten mi tspeziellenFormatierungen und Handwriting
- **Paddle:** Bietet herausragende Performance bei der Erkennung von Text aus Bildern mit komplexen Layouts und liefert gute Ergebnisse bei handschriftlichen und gemischten Dokumenten, jedoch etwas ressourcenintensiv und benötigt mehr Rechenleistung
- **Nougat:** Sehr gut bei der Erkennung von Texten aus schwer lesbaren Quellen und Dokumenten mitungewöhnlichen Layouts. Fokussiert auf unstrukturierte Textdaten und Bildverarbeitung, jedoch Noch in der Entwicklung, sodass es weniger dokumentierte Funktionen und eine kleinere Nutzerbasis gibt und sehr ressourcenintensiv und benötigt viel mehr Rechenleistung

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

# Ausführen der DocumentOCRResults-Klasse

Um die `DocumentOCRResults`-Klasse auszuführen, folge diesen Schritten:

### Wechsle zum richtigen Verzeichnis:

Wechsle in das Verzeichnis, in dem sich die Datei `DocumentOCRResults.py` befindet. In diesem Fall ist das Verzeichnis:

Du kannst dies im Terminal mit folgendem Befehl tun:

```bash
cd Odyss.AI.Backend.OCR

python -m app.service.DocumentOCRResults
```
