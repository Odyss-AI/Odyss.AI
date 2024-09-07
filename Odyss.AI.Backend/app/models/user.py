from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class Image(BaseModel):
    ID: str
    URL_zu_Bild: str
    Seite: int
    Textinhalt_aus_OCR: str
    Output_von_Bilderkenner: str
    Ähnlichkeit: float

class TextObject(BaseModel):
    ID: str
    Ausgelesener_Text: str
    Seite: int
    Embeddings_zu_Textabschnitt: List[float]
    Ähnlichkeit: float

class Document(BaseModel):
    ID: str
    Timestamp: datetime
    URL_von_Dokument: str
    Hashwert_Doc: str
    Bilder: List[Image]
    Zusammenfassung: str
    TextObjekt: List[TextObject]

class User(BaseModel):
    id: str
    username: str
    documents: List[Document] = Field(default_factory=list)