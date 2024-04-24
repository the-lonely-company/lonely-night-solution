from typing import List, Optional
from humps import camelize

from pydantic import BaseModel

def to_camel(string):
    return camelize(string)

class CamelModel(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True

class Turn(BaseModel):
    party: str
    content: str    

class Message(CamelModel):
    content: str
    chat_history: Optional[List[Turn]]