from pydantic import BaseModel, Field
from typing import Optional, List, Union
from enum import Enum

from model.camel_model import CamelModel


class Message(CamelModel):
    role: str
    content: str

class QuantitativeRange(BaseModel):
    minimum: Optional[float] = Field(default=None, description="Minimum of the item, null if not specified.")
    around: Optional[float] = Field(default=None, description="Around the item range, null if not specified.")
    maximum: Optional[float] = Field(default=None, description="Maximum of the item, null if not specified.")

class WineType(str, Enum):
    RED = "Red wine"
    ROSE = "Rosé wine"
    WHITE = "White wine"
    SPARKLING = "Sparkling wine"
    DESSERT = "Dessert wine"
    FORTIFIED = "Fortified wine"
    
class Detail(BaseModel):
    types: Optional[List[WineType]] = Field(default=None, description="Types of wines: Red, Rosé, White, Sparkling, Dessert, or Fortified. Null if not specified.")
    grapes: Optional[List[Union[str, None]]] = Field(default=None, description="Grapes, null if not specified.")
    alcohol: Optional[QuantitativeRange] = Field(default=None, description="Alcohol content, null if user did not specify.")
    vintages: Optional[List[Optional[int]]] = Field(default=None, description="Vintages, null if user did not specify.")
    price: Optional[QuantitativeRange] = Field(default=None, description="Price in HKD currency, null if user did not specify in the query.")
    regions: Optional[List[Union[str, None]]] = Field(default=None, description="Regions, null if not specified.")
    wineries: Optional[List[Union[str, None]]] = Field(default=None, description="Wineries, null if not specified.")
    quantity: Optional[QuantitativeRange] = Field(default=None, description="Quantity, null if user did not specify.")
    description: Optional[str] = Field(default=None, description="Characteristics of the suggested wines, sweetness, acidity, tannin, alcohol and body.")

class WineProfile(BaseModel):
    condition: str = Field(description='Conditions that the wine suggestion profile is under.')
    requirements: str = Field(description="User's specific requirements on wines")
    analysis: str = Field(description="Analyze the findings from condition and requirements.")
    proposal: str = Field(description="Propose a suggestion as a solution to conditions and requirements.")
    detail: Detail = Field(description="Details of the suggested wines.")

class DetailQuery(BaseModel):
    detail_index: int = Field(description="Index of the detail to query.")
    query: str = Field(description="Query to query the detail.")

class DetailQueris(BaseModel):
    detail_queries: List[DetailQuery] = Field(description="Detail queries to query the details.")