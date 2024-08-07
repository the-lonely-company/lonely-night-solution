from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel
from typing import Optional, List, Union, Dict, Any
from enum import Enum
from humps import camelize
from bson import ObjectId


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
    types: Optional[List[WineType]] = Field(default=None, description="Types of wines.")
    grapes: Optional[List[str]] = Field(default=None, description="Grapes.")
    alcohol: Optional[QuantitativeRange] = Field(default=None, description="Alcohol content.")
    vintages: Optional[List[int]] = Field(default=None, description="Vintages.")
    price: Optional[QuantitativeRange] = Field(default=None, description="Price in HKD currency.")
    countries: Optional[List[str]] = Field(default=None, description="Countries.")
    regions: Optional[List[str]] = Field(default=None, description="Regions.")
    wineries: Optional[List[str]] = Field(default=None, description="Wineries.")
    quantity: Optional[QuantitativeRange] = Field(default=None, description="Number of bottles.")
    description: Optional[str] = Field(default=None, description="Characteristics of the suggested wines, sweetness, acidity, tannin, alcohol and body.")

class WineProfile(BaseModel):
    condition: str = Field(description='Conditions that the wine suggestion profile is under.')
    requirements: str = Field(description="User's specific requirements on wines")
    analysis: str = Field(description="Analyze the findings from condition and requirements.")
    profile: str = Field(description="Profile of the wines.")
    detail: Detail = Field(description="Details of the suggested wines.")

class DetailQuery(BaseModel):
    detail_index: int = Field(description="Index of the detail to query.")
    query: str = Field(description="Query to query the detail.")

class DetailQueris(BaseModel):
    detail_queries: List[DetailQuery] = Field(description="Detail queries to query the details.")

class Grape(CamelModel):
    name: str

class Winery(CamelModel):
    name: str

class Country(CamelModel):
    name: str

class Region(CamelModel):
    name: str
    country: Country

class Style(CamelModel):
    wine_type: Optional[str] = None
    varietal_name: Optional[str] = None
    body_description: Optional[str] = None
    acidity_description: Optional[str] = None

class Beverage(CamelModel):
    url_id: int
    name: str
    is_natural: Optional[bool] = None
    alcohol: float
    grapes: List[Grape]
    winery: Optional[Winery] = None
    region: Region
    style: Optional[Style] = None
    score: float

class SearchEngineResponse(CamelModel):
    explanation: str
    beverages: List[Beverage]