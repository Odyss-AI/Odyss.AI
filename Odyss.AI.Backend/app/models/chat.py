from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from app.models.enum import AvailibleModels

class Message(BaseModel):
    id: str
    content: str
    timestamp: datetime
    is_user: bool
    selected_model: str = AvailibleModels.MISTRAL.value

class Chat(BaseModel):
    id: str
    user_id: str
    messages: List[Message] = Field(default_factory=list)
    chat_name: str
    doc_ids: List[str] = Field(default_factory=list)