## OCR Vergleich: Tesseract vs. Paddle vs. Nougat

## Einleitung

In diesem Dokument vergleichen wir drei OCR-Technologien: Tesseract, Paddle und Nougat. Ziel ist es, ihre Leistungsfähigkeit hinsichtlich Textgenauigkeit, Verarbeitungszeit und Benutzerfreundlichkeit zu bewerten mit **PDFReader**. Wir testen verschiedene Dokumenttypen, darunter:

1. Normale Dokumente mit markierbarem Text und Bildern **(Fall 1)**
2. Dokumente, die nur aus Bildern bestehen **(Fall 2)**
3. Word- und PowerPoint-Dokumente, die in PDFs konvertiert wurden **(Fall 3)**

Die folgenden Kriterien werden zur Bewertung herangezogen.

## Allgemeine Informationen (Fall 1)

- **Dokument:** Paper (normales Dokument)
- **Anzahl Seiten:** 16 Seiten

## Vergleichskriterien (Fall 1)

| Kriterium                                              | Tesseract       | Paddle          | Nougat          |
| ------------------------------------------------------ | --------------- | --------------- | --------------- |
| **Textgenauigkeit (%)**                          | [Genauigkeit T] | [Genauigkeit P] | [Genauigkeit N] |
| **Verarbeitungszeit (min)**                      | 0:05            | 0:04            | 0:30            |
| **Formatierung (ja/nein)**                       | ?               | [Format P]      | ja              |
| **Bilderkennung (Anzahl)**                       | 5               | 5               | 5               |
| **Skalierbarkeit**                               | [Skalierung T]  | [Skalierung P]  | [Skalierung N]  |
| **Fehlerrate (%)**                               | [Fehler T]      | [Fehler P]      | [Fehler N]      |
| **Benutzerfreundlichkeit (gut/mittel/schlecht)** | gut             | gut/mittel      | schlecht        |
| **Sonderzeichen/Formeln (%)**                    | [Formeln T]     | [Formeln P]     | [Formeln N]     |

## Ergebnisse im Detail (Seite 1, Fall 1)

### Tesseract

- **Bilderkennung (1. Bild):** "1\nWho is the “Supplier”?\nneem ante 7 Analytic Insight Inc\nINFILL, What is the doc type?\nPurchase Order\np=\nB Is the year 1995?\nae 2,0 Yes\nOCRed Document LLM Extension Pre-training Instruction Tuning\n\nText tokens + Bounding boxes Disentangled Spatial Attention Blocks + Infilling Objective KIE + NLI + VQA + Classify\n"
- **Skalierbarkeit:** [Details]
- **Fehlerrate:** [Details]
- **Benutzerfreundlichkeit:** [Details]
- **Sonderzeichen/Formeln:** [Details]

### Paddle

- **Bilderkennung (1. Bild):** "Who is the \"Supplier\"?\n(DOMEST\n(Recommended Props\nAnalytic Insight Inc\nate\nMarch3.199\nescription\nLUCKY STRIKE QUALITATIVE ADV\nCITIES\n INFILL\nWhat is the doc type?\nequested byz\nA.A.Strobel\nResearch Req\nBudgeted:\nPurchase Order\nOriginal Budgeted\nwntract.\nIs the year 1995?\nYes\nOCRed Document\nLLM Extension\nPre-training\nInstruction Tuning\nText tokens + Bounding boxes\nDisentangled Spatial Attention\nBlocks + Infilling Objective\nKIE + NLI + VQA+ Classify"
- **Skalierbarkeit:** [Details]
- **Fehlerrate:** [Details]
- **Benutzerfreundlichkeit:** [Details]
- **Sonderzeichen/Formeln:** [Details]

"Who is the \"Supplier\"?\n(DOMEST\n(Recommended Props\nAnalytic Insight Inc\nate\nMarch3.199\nescription\nLUCKY STRIKE QUALITATIVE ADV\nCITIES\n INFILL\nWhat is the doc type?\nequested byz\nA.A.Strobel\nResearch Req\nBudgeted:\nPurchase Order\nOriginal Budgeted\nwntract.\nIs the year 1995?\nYes\nOCRed Document\nLLM Extension\nPre-training\nInstruction Tuning\nText tokens + Bounding boxes\nDisentangled Spatial Attention\nBlocks + Infilling Objective\nKIE + NLI + VQA+ Classify",

    "link":"C:\\Users\\ramaz\\Documents\\extracted_image_2_1.png"

### Nougat

- **Bilderkennung:** "\n\n**OCRed Document**\n\nText tokens + Bounding boxes\n\nDisentangled Spatial Attention\n\n**Pre-training**\n\n**Instruction Tuning**\n\n**Closing the number of tokens + Bounding boxes\n\n**OCRed Document**\n\n**Text tokens + Bounding boxes**\n\nDisentangled Spatial Attention\n\n**OCRed Document**\n"**Skalierbarkeit:** [Details]
- **Fehlerrate:** [Details]
- **Benutzerfreundlichkeit:** [Details]
- **Sonderzeichen/Formeln:** [Details]

## Allgemeine Informationen (Fall 2)

- **Dokument:** Paper als Images
- **Anzahl Seiten:** 16 Seiten als Images

## Vergleichskriterien (Fall 2)

| Kriterium                                              | Tesseract       | Paddle          | Nougat          |
| ------------------------------------------------------ | --------------- | --------------- | --------------- |
| **Textgenauigkeit (%)**                          | [Genauigkeit T] | [Genauigkeit P] | [Genauigkeit N] |
| **Verarbeitungszeit (min)**                      | 0:30            | 0:22            | 14:30           |
| **Formatierung (ja/nein)**                       | ja              | ?               | ja *            |
| **Bilderkennung (Anzahl)**                       | 16              | 16              | 16              |
| **Skalierbarkeit**                               | [Skalierung T]  | [Skalierung P]  | [Skalierung N]  |
| **Fehlerrate (%)**                               | [Fehler T]      | [Fehler P]      | [Fehler N]      |
| **Benutzerfreundlichkeit (gut/mittel/schlecht)** | gut             | gut/mittel      | schlecht        |
| **Sonderzeichen/Formeln (%)**                    | schlecht        | mittel          | [Formeln N]     |

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
- **Benutzerfreundlichkeit:** [Details]
- **Sonderzeichen/Formeln:** [Details]

## Allgemeine Informationen (Fall 3)

- **Dokument:** Paper als Word-Dokument als Images
- **Anzahl Seiten:** 16 Seiten als Images

## Vergleichskriterien (Fall 3)

| Kriterium                                              | Tesseract       | Paddle          | Nougat          |
| ------------------------------------------------------ | --------------- | --------------- | --------------- |
| **Textgenauigkeit (%)**                          | [Genauigkeit T] | [Genauigkeit P] | [Genauigkeit N] |
| **Verarbeitungszeit (min)**                      | 0:30            | 0:28            | 15:00           |
| **Formatierung (ja/nein)**                       | ja              | [Format P]      | ja*             |
| **Bilderkennung (Anzahl)**                       | 16              | 16              | 16              |
| **Skalierbarkeit**                               | [Skalierung T]  | [Skalierung P]  | [Skalierung N]  |
| **Fehlerrate (%)**                               | [Fehler T]      | [Fehler P]      | [Fehler N]      |
| **Benutzerfreundlichkeit (gut/mittel/schlecht)** | gut             | gut/mittel      | schlecht        |
| **Sonderzeichen/Formeln (%)**                    | [Formeln T]     | [Formeln P]     | [Formeln N]     |

## Ergebnisse im Detail (Seite 1, Fall 3)

### Tesseract

- **Bilderkennung:** "401.00908v1 [cs.CL] 31 Dec 2023\n\nDOCLLM: A LAYOUT-AWARE GENERATIVE LANGUAGE MODEL\nFOR MULTIMODAL DOCUMENT UNDERSTANDING\n\nDongsheng Wang”, Natraj Raman*, Mathieu Sibue*\nZhiqiang Ma, Petr Babkin, Simerjot Kaur, Yulong Pei, Armineh Nourbakhsh, Xiaomo Liu\nJPMorgan Al Research\n{first .last}@jpmchase.com\n\nABSTRACT\n\nEnterprise documents such as forms, invoices, receipts, reports, contracts, and other similar records,\noften carry rich semantics at the intersection of textual and spatial modalities. The visual cues offered\nby their complex layouts play a crucial role in comprehending these documents effectively. In this\nPaper, we present DocLLM, a lightweight extension to traditional large language models (LLMs) for\nreasoning over visual documents, taking into account both textual semantics and spatial layout. Our\nmodel differs from existing multimodal LLMs by avoiding expensive image encoders and focuses\nexclusively on bounding box information to incorporate the spatial layout structure. Specifically,\nthe cross-alignment between text and spatial modalities is captured by decomposing the attention\nmechanism in classical transformers to a set of disentangled matrices. Furthermore, we devise a\npre-training objective that learns to infill text segments. This approach allows us to address irregular\nlayouts and heterogeneous content frequently encountered in visual documents. The pre-trained\nmodel is fine-tuned using a large-scale instruction dataset, covering four core document intelligence\ntasks. We demonstrate that our solution outperforms SotA LLMs on 14 out of 16 datasets across all\ntasks, and generalizes well to 4 out of 5 previously unseen datasets.\n\nKeywords DocAl- VRDU - LLM - GPT - Spatial Attention\n\n1 Introduction\n\nDocuments with rich layouts, including invoices, receipts, contracts, orders, and forms, constitute a significant portion\nof enterprise corpora. The automatic interpretation and analysis of these documents offer considerable advantages [I],\nwhich has spurred the development of Al-driven solutions. These visually rich documents feature complex layouts,\nbespoke type-setting, and often exhibit variations in templates, formats and quality. Although Document AI (DocAl) has\nmade tremendous progress in various tasks including extraction, classification and question answering, there remains a\nsignificant performance gap in real-world applications. In particular, accuracy, reliability, contextual understanding and\ngeneralization to previously unseen domains continues to be a challenge\n\nDocument intelligence is inherently a multi-modal problem with both the text content and visual layout cues being\ncritical to understanding the documents. It requires solutions distinct from conventional large language models such as\nGPT-3.5 [3], Llama [4], Falcon [5]] or PaLM [6] that primarily accept text-only inputs and assume that the documents\nexhibit simple layouts and uniform formatting, which may not be suitable for handling visual documents. Numerous\nvision-language frameworks [[71|8]] that can process documents as images and capture the interactions between textual\nand visual modalities are available. However, these frameworks necessitate the use of complex vision backbone\narchitectures [9] to encode image information, and they often make use of spatial information as an auxiliary contextual\nsignal (70,(11).\n\nIn this paper we present DocLLM, a light-weight extension to standard LLMs that excels in several visually rich form\nunderstanding tasks. Unlike traditional LLMs, it models both spatial layouts and text semantics, and therefore is\n\n“These authors contributed equally to this work.\n"
- **Skalierbarkeit:** [Details]
- **Fehlerrate:** [Details]
- **Benutzerfreundlichkeit:** [Details]
- **Sonderzeichen/Formeln:** [Details]

### Paddle

- **Bilderkennung:** "DOCLLM: A LAYOUT-AWARE GENERATIVE LANGUAGE MODEL\nFOR MULTIMODAL DOCUMENT UNDERSTANDING\nDongsheng Wang*, Natraj Raman\", Mathieu Sibue\nZhiqiang Ma, Petr Babkin, Simerjot Kaur, Yulong Pei, Armineh Nourbakhsh, Xiaomo Liu\n JPMorgan AI Research\n 2023\n{first.last}@jpmchase.com\nDec '\nABSTRACT\nEnterprise documents such as forms, invoices, receipts, reports, contracts, and other similar records.\noften carry rich semantics at the intersection of textual and spatial modalities. The visual cues offered\nby their complex layouts play a crucial role in comprehending these documents effectively. In this\nreasoning over visual documents, taking into account both textual semantics and spatial layout. Our\nmodel differs from existing multimodal LLMs by avoiding expensive image encoders and focuses\nexclusively on bounding box information to incorporate the spatial layout structure. Specifically.\nthe cross-alignment between text and spatial modalities is captured by decomposing the attention\nmechanism in classical transformers to a set of disentangled matrices. Furthermore, we devise a\npre-training objective that learns to infill text segments. This approach allows us to address irregular\n00908v1\nlayouts and heterogeneous content frequently encountered in visual documents. The pre-trained\nmodel is fine-tuned using a large-scale instruction dataset, covering four core document intelligence\ntasks. We demonstrate that our solution outperforms SotA LLMs on 14 out of 16 datasets across all\ntasks, and generalizes well to 4 out of 5 previously unseen datasets.\nKeywords DocAI - VRDU - LLM - GPT - Spatial Attention\n1\n Introduction\nDocuments with rich layouts, including invoices, receipts, contracts, orders, and forms, constitute a significant portion\nof enterprise corpora. The automatic interpretation and analysis of these documents offer considerable advantages [].\nwhich has spurred the development of AI-driven solutions. These visually rich documents feature complex layouts,\nbespoke type-setting, and often exhibit variations in templates, formats and quality. Although Document AI (DocAIl) has\nmade tremendous progress in various tasks including extraction, classification and question answering, there remains a\nsignificant performance gap in real-world applications. In particular, accuracy, reliability, contextual understanding and\ngeneralization to previously unseen domains continues to be a challenge [2].\nDocument intelligence is inherently a multi-modal problem with both the text content and visual layout cues being\ncritical to understanding the documents. It requires solutions distinct from conventional large language models such as\nGPT-3.5 [l, Llama [41, Falcon [ll or PaLM [] that primarily accept text-only inputs and assume that the documents\nexhibit simple layouts and uniform formatting, which may not be suitable for handling visual documents. Numerous\nvision-language frameworks [7] that can process documents as images and capture the interactions between textual\nand visual modalities are available. However, these frameworks necessitate the use of complex vision backbone\narchitectures [] to encode image information, and they often make use of spatial information as an auxiliary contextual\nsignal [L0 I].\nIn this paper we present DocLLM, a light-weight extension to standard LLMs that excels in several visually rich form\nunderstanding tasks. Unlike traditional LLMs, it models both spatial layouts and text semantics, and therefore is\n* These authors contributed equally to this work"
- **Skalierbarkeit:** [Details]
- **Fehlerrate:** [Details]
- **Benutzerfreundlichkeit:** [Details]
- **Sonderzeichen/Formeln:** [Details]

### Nougat

- **Bilderkennung:** "\n\n# DocLLM: A layout-aware generative language model for multimodal document understanding\n\nDongsheng Wang\n\nThese authors contributed equally to this work.\n\nNatraj Raman\n\nThis work was supported by the National Science Foundation of China (No. 116731002) and the National Science Foundation of China (No. 116731002).\n\nMathieu Sibue1\n\nZhiqiang Ma\n\nPetr Babkin\n\nSmerjot Kaur\n\nYulong Pei\n\nArmineh Nourbakhsh\n\nXiaomo Liu\n\nJPMorgan AI Research\n\n{first.last}@jpmchase.com\n\nFootnote 1: footnotemark:\n\n###### Abstract\n\nEnterprise documents such as forms, invoices, receipts, reports, contracts, and other similar records, often carry rich semantics at the intersection of textual and spatial modalities. The visual cues offered by their complex layouts play a crucial role in comprehending these documents effectively. In this paper, we present DocLLM, a lightweight extension to traditional large language models (LLMs) for reasoning over visual documents, taking into account both textual semantics and spatial layout. Our model differs from existing multimodal LLMs by avoiding expensive image encoders and focuses exclusively on bounding box information to incorporate the spatial layout structure. Specifically, the cross-alignment between text and spatial modalities is captured by decomposing the attention mechanism in classical transformers to a set of disentangled matrices. Furthermore, we devise a pre-training objective that learns to infill text segments. This approach allows us to address irregular layouts and heterogeneous content frequently encountered in visual documents. The pre-trained model is fine-tuned using a large-scale instruction dataset, covering four core document intelligence tasks. We demonstrate that our solution outperforms SotA LLMs on 14 out of 16 datasets across all tasks, and generalizes well to 4 out of 5 previously unseen datasets.\n\nDocAI \\(\\cdot\\) VRDU \\(\\cdot\\) LLM \\(\\cdot\\) GPT \\(\\cdot\\) Spatial Attention\n\n## 1 Introduction\n\nDocuments with rich layouts, including invoices, receipts, contracts, orders, and forms, constitute a significant portion of enterprise corpora. The automatic interpretation and analysis of these documents offer considerable advantages [1], which has spurred the development of AI-driven solutions. These visually rich documents feature complex layouts, bespoke type-setting, and often exhibit variations in templates, formats and quality. Although Document AI (DocAI) has made tremendous progress in various tasks including extraction, classification and question answering, there remains a significant performance gap in real-world applications. In particular, accuracy, reliability, contextual understanding and generalization to previously unseen domains continues to be a challenge [2].\n\nDocument intelligence is inherently a multi-modal problem with both the text content and visual layout cues being critical to understanding the documents. It requires solutions distinct from conventional large language models such as GPT-3.5 [3], Llama [4], Falcon [5] or PaLM [6] that primarily accept text-only inputs and assume that the documents exhibit simple layouts and uniform formatting, which may not be suitable for handling visual documents. Numerous vision-language frameworks [7] that can process documents as images and capture the interactions between textual and visual modalities are available. However, these frameworks necessitate the use of complex vision backbone architectures [9] to encode image information, and they often make use of spatial information as an auxiliary contextual signal [10][11].\n\nIn this paper we present DocLLM, a light-weight extension to standard LLMs that excels in several visually rich form understanding tasks. Unlike traditional LLMs, it models both spatial layouts and text semantics, and therefore is"
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
