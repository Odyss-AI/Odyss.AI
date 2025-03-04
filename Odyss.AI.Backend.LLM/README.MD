# Übersicht

Odyss.AI.Backend.LLM ist ein Backend-Projekt, das die Verarbeitung und Bereitstellung von Language Model (LLM) Diensten unterstützt. Dieses Projekt umfasst zwei Hauptkomponenten:

1. **ImageTagger**: Ein selbst trainierter Bilderkenner, der Bilder kategorisiert, um mehr Informationen an Pixtral zu senden. Diese Komponente war ursprünglich Teil des Projekts, wurde aber aufgrund von Performance Problemen wieder aus dem Workflow entfernt. Der Bilderkenner ermöglicht eine effiziente Bildklassifizierung.
2. **Mathematische Formelerkennung**: Ein Experiment, das darauf abzielt, mathematische Formeln mithilfe von Pixtral aus Dokumenten zu extrahieren. Diese Komponente untersucht die Möglichkeiten der automatisierten Erkennung und Verarbeitung mathematischer Inhalte.

# Dokumentation für den Image Tagger

## Übersicht

Der Image Tagger ist eine Komponente des Odyss.AI.Backend.LLM Projekts, die zur Bildklassifizierung entwickelt wurde. Ursprünglich war er in den Workflow integriert, um Bilder zu kategorisieren und zusätzliche Informationen an Pixtral zu senden. Aufgrund von Performance-Problemen und Fehlklassifikationen, die die Ergebnisse von Pixtral beeinträchtigten, wurde der Image Tagger jedoch deaktiviert. Trotz dieser Deaktivierung erzielte der Image Tagger sehr gute Ergebnisse auf den Train/Test-Split-Daten und bleibt ein wichtiger Bestandteil der Projektentwicklung.

## Dataset

Das Dataset stammt von Kaggle und ist zu finden unter https://www.kaggle.com/datasets/sunedition/graphs-dataset .

## Komponenten

1. **img_tagger.ipynb**: Das Notebook `img_tagger.ipynb` dient zur Erstellung des Klassifikators. Es analysiert den Datensatz und zeigt die Genauigkeit (accuracy) sowie die Konfusionsmatrix (confusion matrix) des Modells.
2. **ImageTagger.py**: Das Programm `ImageTagger.py` war ursprünglich in das Projekt integriert, um Bilder zu klassifizieren und die Informationen an Pixtral weiterzugeben, um die Analyse zu verbessern. Der Image Tagger erzielte sehr gute Ergebnisse auf den Train/Test-Split-Daten.

## Deaktivierung des Image Taggers

Der ImageTagger wurde deaktiviert, da Fehlklassifikationen die Ergebnisse von Pixtral erheblich verschlechterten. `ImageTagger.py` nimmt Bilddaten entgegen und klassifiziert diese mit dem Modell `diagram_classifier.h5`.

## Voraussetzungen

- **Python 3.7+**: Notwendig zur Ausführung der Skripte und Notebooks.
- **Jupyter Notebook**: Zum Anzeigen und Ausführen des Notebooks `img_tagger.ipynb`.
- **TensorFlow**: Zum Laden und Verwenden des Modells `diagram_classifier.h5`.
- **Keras**: Zum Erstellen und Trainieren des Modells.
- **Pandas**: Zum Verarbeiten des Datensatzes.
- **NumPy**: Für numerische Operationen.
- **Matplotlib**: Zum Visualisieren der Ergebnisse.

## Schritte zur Reproduktion

1. Klonen Sie das Git-Repository.
2. Installieren Sie die notwendigen Anforderungen mit `pip install -r requirements.txt`.
3. Laden Sie das Dataset von [Kaggle](https://www.kaggle.com/datasets/sunedition/graphs-dataset) herunter und speichern Sie es im entsprechenden Verzeichnis.
4. Öffnen und führen Sie das Notebook `img_tagger.ipynb` aus, um das Modell zu erstellen und zu trainieren.
5. Verwenden Sie `ImageTagger.py`, um Bilder mit dem trainierten Modell `diagram_classifier.h5` zu klassifizieren.

# Dokumentation für das Experiment der Formel Extraktion

## Übersicht

Das Experiment der Formel Extraktion besteht aus mehreren Jupyter Notebooks, die zur Extraktion und Analyse von Formeln aus wissenschaftlichen Papern verwendet werden. Die Hauptkomponenten des Experiments sind:

1. **pixtral_formula_extraction**: Dieses Jupyter Notebook ist für die eigentliche Extraktion der Formeln zuständig. Es installiert die notwendigen Anforderungen und führt die Extraktion durch. Poppler ist notwendig zum Ausführen des Notebooks und ist im Git-Repository enthalten. Zur Reproduktion der Ergebnisse kann dieses Notebook ausgeführt werden.
2. **Datensatz**: Der Datensatz, auf dem das Experiment basiert, ist unter dem Verzeichnis `Paper` zu finden.
3. **formula_analysis**: Dieses Jupyter Notebook enthält die Analyse der Ergebnisse des Experiments. Die Analyseergebnisse sind als Datensatz unter `output.xlsx` zu finden. Die Ergebnisse wurden per hand annotiert um einen Ground Truth zu erhalten. Dieser Ground Truth wurde in der Spalte "Vergleich Pixtral" und "Vergleich Nougat" mit dem extrahierten ergebnissen verglichen. Die Analyse der Ergebnisse sind in dem Jupyter Notebook `formula_analysis.ipynb` zu finden.

## Voraussetzungen

- **Poppler**: Notwendig zum Ausführen des Notebooks `pixtral_formula_extraction`.
- **Jupyter Notebook**: Zum Ausführen und Anzeigen der Notebooks.

## Schritte zur Reproduktion

1. Klonen Sie das Git-Repository.
2. Installieren Sie die notwendigen Anforderungen, die im Notebook `pixtral_formula_extraction` angegeben sind.
3. Installieren Sie poppler (https://github.com/oschwartz10612/poppler-windows).
4. Die SSH Verbindungsdetails sind in dem Jupyter Notebook zu finden, funktionieren allerdings nur mit einem Privaten SSH-Key des Autors. Passen Sie die SSH Verbindungsdetails auf Ihren SSH-Key an.
5. Führen Sie das Notebook `pixtral_formula_extraction` aus, um die Formeln zu extrahieren.
6. Die Ground Truth und der Vergleich in `output.xslx` wurden per Hand erstellt.
7. Die Ergebnisse von Nougat wurden mit dem Programm `nougat_txt.py` in Odyss.AI.Backend.OCR Erstellt und per hand an die `output.xslx` annotiert. Die Ausführung `nougat_txt.py` wird in der Readme von Odyss.AI.Backend.OCR erklärt.
8. Analysieren Sie die Ergebnisse mit dem Notebook `formula_analysis`.

## Ergebnisse

Die durchgeführte Analyse zeigt deutliche Unterschiede in der Leistung zwischen den beiden Systemen, insbesondere bei der Erkennung und Verarbeitung von Formeln.

### **Ergebnisse im Überblick**

* Nougat erzielt insgesamt deutlich bessere Ergebnisse als Pixtral.
* Die Kategorie *"richtig"* ist bei Nougat deutlich häufiger vertreten als bei Pixtral.
* Die Anzahl der falschen Zuordnungen (*"FALSCH"* und  *"falsche formel"* ) ist bei Pixtral höher als bei Nougat.

### **Fehlinterpretationen von Formeln**

Die fehlerhafte Erkennung von Formeln in der Spalte *"Vergleich Pixtral"* hat zwei Hauptursachen:

1. **Tabellenstruktur** : Vier der nicht erkannten Formeln befanden sich innerhalb einer Tabelle.
2. **Hintergrundtext** : Drei Formeln konnten aufgrund von Hintergrundtext im Dokument nicht korrekt erkannt werden. Dies führte zu fehlenden Erkennungen.

### **Vergleich Pixtral vs. Nougat**

Die Ergebnisse deuten darauf hin, dass Nougat in der Lage ist, Formeln in Standardkontexten zuverlässiger zu erkennen und zu interpretieren. Allerdings zeigt sich auch, dass Nougat strukturell eingebettete Formeln (z. B. in Tabellen) nicht verarbeitet.

Die grafische Darstellung verdeutlicht diese Unterschiede weiter: Während Nougat eine höhere Anzahl an korrekt erkannten Formeln aufweist, kämpft Pixtral mit einer größeren Anzahl an falsch erkannten oder nicht lesbaren Formeln.

### **Fazit**

* **Nougat ist in der Formelverarbeitung insgesamt präziser** , insbesondere in standardisierten Kontexten.
* **Hintergrundtext stellt für beide Systeme eine Herausforderung dar** , wobei Pixtral hier anfälliger für Fehlinterpretationen ist.

Eine Optimierung der Erkennung könnte durch eine Kombination der Stärken beider Systeme erfolgen – beispielsweise durch eine Vorfilterung von Tabelleninhalten oder eine gezielte Nachbearbeitung der Pixtral-Ergebnisse.
