from pydantic import BaseModel, Field
from typing import Optional, List

from model.camel_model import CamelModel


class Message(CamelModel):
    role: str
    content: str

class QuantitativeRange(BaseModel):
    minimum: Optional[float] = Field(description="Minimum of the item, null if not specified.")
    around: Optional[float] = Field(description="Around the item range, null if not specified.")
    maximum: Optional[float] = Field(description="Maximum of the item, null if not specified.")

class Detail(BaseModel):
    types: Optional[List[str]] = Field(description="Types of wines, red, white, sparkling, rose, dessert, null if not specificed.")
    grapes: Optional[List[str]] = Field(description="Grapes, null if not specified.")
    alcohol: Optional[QuantitativeRange] = Field(description="Alcohol content, null if user did not specify.")
    vintages: Optional[List[int]] = Field(description="Vintages, null if user did not specify.")
    price: Optional[QuantitativeRange] = Field(description="Price in HKD currency, null if user did not specify in the query.")
    region: Optional[List[str]] = Field(description="Regions, null if not specified.")
    winery: Optional[List[str]] = Field(description="Wineries, null if not specified.")
    quantity: Optional[QuantitativeRange] = Field(description="Quantity, null if user did not specify.")
    description: Optional[str] = Field(description="characteristics of the suggested wines, sweetness, acidity, tannin, alcohol and body.")

class WineProfile(BaseModel):
    condition: str = Field(description='Conditions that the wine suggestion profile is under.')
    requirements: str = Field(description="User's specific requirements on wines")
    analysis: str = Field(description="Analyze the findings from condition and requirements.")
    proposal: str = Field(description="Propose a suggestion as a solution to conditions and requirements.")
    detail: List[Detail] = Field(description="Details of the suggested wines.")
