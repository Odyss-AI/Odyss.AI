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
    formula: List[str] = Field(default_factory=list)

class Document(BaseModel):
    id: str
    doc_id: str
    mongo_file_id: str
    name: str
    timestamp: datetime
    summary: str
    imgList: List[Image]
    textList: List[TextChunk]
    path: str
    
class User(BaseModel):
    id: str
    username: str
    documents: List[Document] = Field(default_factory=list)