## Übersicht

Odyss.AI.Backend.LLM ist ein Backend-Projekt, das die Verarbeitung und Bereitstellung von Language Model (LLM) Diensten unterstützt. Dieses Projekt umfasst zwei Hauptkomponenten:

1. **ImageTagger**: Ein selbst trainierter Bilderkenner, der Bilder kategorisiert, um mehr Informationen an Pixtral zu senden. Diese Komponente war ursprünglich Teil des Projekts, wurde aber aufgrund von Performance Problemen wieder aus dem Workflow entfernt. Der Bilderkenner ermöglicht eine effiziente Bildklassifizierung.

2. **Mathematische Formelerkennung**: Ein Experiment, das darauf abzielt, mathematische Formeln mithilfe von Pixtral aus Dokumenten zu extrahieren. Diese Komponente untersucht die Möglichkeiten der automatisierten Erkennung und Verarbeitung mathematischer Inhalte.

"""
ImageTagger.py

Dieses Modul greift auf das Modell 'diagramm_classifier.h5' zu, um Bilddaten zu klassifizieren. Damit die Funktionalität gewährleistet ist, müssen alle Abhängigkeiten, die in der Datei 'requirements.txt' aufgeführt sind, installiert werden.

Der ImageTagger übernimmt die Kommunikation der Bilddaten und klassifiziert die empfangenen Bilder.
"""

# Dokumentation für das Experiment der Formel Extraktion

## Übersicht
Das Experiment der Formel Extraktion besteht aus mehreren Jupyter Notebooks, die zur Extraktion und Analyse von Formeln aus wissenschaftlichen Papern verwendet werden. Die Hauptkomponenten des Experiments sind:

1. **pixtral_formula_extraction**: Dieses Jupyter Notebook ist für die eigentliche Extraktion der Formeln zuständig. Es installiert die notwendigen Anforderungen und führt die Extraktion durch. Poppler ist notwendig zum Ausführen des Notebooks und ist im Git-Repository enthalten. Zur Reproduktion der Ergebnisse kann dieses Notebook ausgeführt werden.

2. **Datensatz**: Der Datensatz, auf dem das Experiment basiert, ist unter dem Verzeichnis `Paper` zu finden.

3. **formula_analysis**: Dieses Jupyter Notebook enthält die Analyse der Ergebnisse des Experiments. Die Analyseergebnisse sind als Datensatz unter `output.xlsx` zu finden. Die Ergebnisse wurden per hand annotiert um einen Ground Truth zu erhalten. Dieser Ground Truth wurde in der Spalte "Vergleich" mit dem extrahierten ergebnissen verglichen. Die Analyse der Ergebnisse sind in dem Jupyter Notebook zu finden.

## Voraussetzungen
- **Poppler**: Notwendig zum Ausführen des Notebooks `pixtral_formula_extraction`. Poppler ist im Git-Repository enthalten.
- **Jupyter Notebook**: Zum Ausführen und Anzeigen der Notebooks.

## Schritte zur Reproduktion
1. Klonen Sie das Git-Repository.
2. Installieren Sie die notwendigen Anforderungen, die im Notebook `pixtral_formula_extraction` angegeben sind.
3. Die SSH Verbindungsdetails sind in dem Jupyter Notebook zu finden, funktionieren allerdings nur mit meinem SSH-Key. Passen Sie die SSH Verbindungsdetails auf Ihren SSH-Key an. 
4. Führen Sie das Notebook `pixtral_formula_extraction` aus, um die Formeln zu extrahieren.
5. Die Ground Truth und der Vergleich in "output.xslx" wurden per Hand erstellt.
6. Analysieren Sie die Ergebnisse mit dem Notebook `formula_analysis`.

## Ergebnisse
Die extrahierten und analysierten Formeln sind als Datensatz in der Datei `output.xlsx` gespeichert.
