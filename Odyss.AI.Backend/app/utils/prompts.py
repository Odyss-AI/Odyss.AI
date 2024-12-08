from typing import List

from app.models.user import TextChunk

def summary_prompt_builder(chunks: List[TextChunk]):

    context = "\n".join([f"Abschnitt {i + 1}: {t.text}" for i, t in enumerate(chunks)])

    return [
        {
            "role": "system",
            "content": f"""
                Deine Aufgabe ist es, den folgenden Text zu lesen, die wichtigsten Punkte zu identifizieren und eine kurze Zusammenfassung zu erstellen, die die Essenz des Textes widerspiegelt. Die Zusammenfassung sollte in ein bis zwei klaren und prägnanten Sätzen erfolgen.

                # Text:
                {context}

                # Anweisungen:
                ## Zusammenfassen:
                - Fasse die wichtigsten Argumente und Themen des Textes zusammen.
                - Hebe die Hauptpunkte hervor und erstelle eine kohärente Zusammenfassung des Textes.
                - Die Zusammenfassung sollte klar und prägnant sein und die Kernideen des Textes widerspiegeln.
                - Bitte vermeide unnötige Details und konzentriere dich auf die wesentlichen Aspekte des Textes.
                """,
        },
    ]

def qna_prompt_builder(chunks: list, question: str):

    # Nur die Textbestandteile extrahieren
    text_chunks = [chunk[0] for chunk in chunks]

    # Erstellen des Kontexts aus den bereitgestellten Text-Chunks
    context = ""
    if text_chunks:
        for chunk in text_chunks:
            context += chunk + "\n"

    # Prompt erstellen
    if context.strip():
        # Wenn ein Kontext vorhanden ist
        content = f"""
        Deine Aufgabe ist es, den folgenden Text zu lesen und zu verstehen. 
        Nach dem Lesen des Textes beantworte die gestellten Fragen. 
        Antworte immer auf Deutsch.

        # Text:
        {context}

        # Anweisungen:
        Antworte in 3-8 klaren und prägnanten Sätzen auf die folgende Frage: 
        {question}
        """
    else:
        # Wenn kein Kontext vorhanden ist
        content = f"""
        Es wird kein spezifischer Text bereitgestellt. 
        Beantworte die folgende Frage basierend auf deinem Wissen. 
        Antworte immer auf Deutsch.

        # Frage:
        {question}
        """

    return [
        {
            "role": "system",
            "content": content.strip(),
        }
    ]
