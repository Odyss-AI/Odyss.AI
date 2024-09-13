from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class Message(BaseModel):
    id: str
    content: str
    timestamp: datetime
    is_user: bool

class Chat(BaseModel):
    id: str
    user_id: str
    messages: List[Message] = Field(default_factory=list)
    doc_ids: List[str] = Field(default_factory=list)