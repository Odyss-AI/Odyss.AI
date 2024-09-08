from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class Image(BaseModel):
    ID: str
    URL_zu_Bild: str
    Seite: int
    Type: str
    Textinhalt_aus_OCR: str
    Output_von_Bilderkenner: str

class TextObject(BaseModel):
    ID: str
    Ausgelesener_Text: str
    Seite: int

class Document(BaseModel):
    ID: str
    Timestamp: datetime
    URL_von_Dokument: str
    Zusammenfassung: str
    Bilder: List[Image]
    TextObjekt: List[TextObject]

class User(BaseModel):
    id: str
    username: str
    documents: List[Document] = Field(default_factory=list)