from app.models.user import User, Document, TextChunk, Image
from bson.objectid import ObjectId

def get_test_user():
    return User(
        id="5f2b6b3b4f3d453e2f6e1c7c",
        username="testuser",
        documents=[]
    )

def get_test_document(path: str):
    return Document(
        id=str(ObjectId()),
        doc_id=path,
        name="testdocument",
        timestamp="2020-08-05T12:00:00",
        doclink="",
        summary="This is a test document",
        imgList=[],
        textList=[
            TextChunk(
                id=str(ObjectId()), 
                text="Large Language Models (LLMs) sind eine Klasse von künstlichen neuronalen Netzwerken, die darauf trainiert sind, menschenähnlichen Text zu generieren und zu verstehen. Sie basieren auf tiefen Lernarchitekturen, wie beispielsweise dem Transformer-Modell, das große Mengen an Textdaten verarbeitet, um Sprachmuster zu lernen. Diese Modelle sind in der Lage, Texte fortzuführen, zu übersetzen, zusammenzufassen und sogar spezifische Aufgaben wie das Beantworten von Fragen oder das Verfassen von Code zu übernehmen. Bekannte LLMs sind GPT-4, BERT und T5, die von Organisationen wie OpenAI und Google entwickelt wurden.", 
                page=1,
                formula=["f(x) = x^2 + 2x + 1"]),
            TextChunk(
                id=str(ObjectId()),
                text="Das Training von Large Language Models erfordert gewaltige Mengen an Daten und Rechenleistung. Millionen bis Milliarden von Textdokumenten werden gesammelt, um die Modelle auf verschiedenen Aspekten der menschlichen Sprache zu schulen. Während des Trainings lernen die Modelle durch optimierte Algorithmen, die Beziehungen zwischen Wörtern, Sätzen und Kontexten zu verstehen. Durch den Einsatz von Selbstüberwachungsmechanismen können sie komplexe Muster erfassen. Dies führt dazu, dass LLMs in der Lage sind, kontextabhängige Antworten zu generieren, die auf eine Vielzahl von Eingaben reagieren können.",
                page=2,
                formula=["f(x) = x^3 + 3x^2 + 3x + 1"]),
            TextChunk(
                id=str(ObjectId()),
                text="Large Language Models finden Anwendung in zahlreichen Bereichen, von alltäglichen Sprachassistenzsystemen bis hin zur medizinischen Forschung. In der Kundenbetreuung werden sie eingesetzt, um automatisch Anfragen zu bearbeiten und Antworten zu generieren. In der Wissenschaft und im Bildungsbereich helfen sie beim Verfassen von Berichten und der Zusammenfassung wissenschaftlicher Studien. Sie spielen auch eine wichtige Rolle in der Entwicklung von Textgenerierungstools für kreative Aufgaben wie das Schreiben von Geschichten, Gedichten und sogar Drehbüchern. Darüber hinaus unterstützen LLMs die Analyse großer Datenmengen in Feldern wie Marketing, Recht und Finanzen.",
                page=3,
                formula=["f(x) = x^4 + 4x^3 + 6x^2 + 4x + 1"])
            ]
        )