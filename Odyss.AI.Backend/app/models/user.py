from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class Image(BaseModel):
    id: str
    link: str
    page: int
    type: str
    imgtext: str
    llm_output: str

class TextChunk(BaseModel):
    id: str
    text: str
    page: int

class Document(BaseModel):
    id: str
    name: str
    timestamp: datetime
    doclink: str
    summary: str
    imgList: List[Image]
    textList: List[TextChunk]

class User(BaseModel):
    id: str
    username: str
    documents: List[Document] = Field(default_factory=list)