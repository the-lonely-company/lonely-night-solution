from typing import List, Optional
from pydantic import BaseModel

from models.camel_model import CamelModel


class Message(BaseModel):
    role: str
    content: str    

class Messages(CamelModel):
    content: str
    chat_history: Optional[List[Message]]