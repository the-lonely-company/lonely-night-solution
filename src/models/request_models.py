from typing import List, Optional
from pydantic import BaseModel

from models.camel_model import CamelModel


class Turn(BaseModel):
    party: str
    content: str    

class Message(CamelModel):
    content: str
    chat_history: Optional[List[Turn]]