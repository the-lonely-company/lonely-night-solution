from typing import Optional, List, Dict, Any
from model.camel_model import CamelModel


class Grape(CamelModel):
    name: str

class Food(CamelModel):
    name: str

class Winery(CamelModel):
    name: str

class Vintage(CamelModel):
    name: str
    year: int

class Country(CamelModel):
    name: str

class Region(CamelModel):
    name: str
    country: Country

class Style(CamelModel):
    name: Optional[str] = None
    wine_type: Optional[str] = None
    varietal_name: Optional[str] = None
    blurb: Optional[str] = None
    body_description: Optional[str] = None
    acidity_description: Optional[str] = None

class Beverage(CamelModel):
    url_id: int
    name: str
    is_natural: Optional[bool] = None
    alcohol: float
    closure: Optional[str] = None
    grapes: List[Grape]
    foods: List[Food] = None
    winery: Optional[Winery] = None
    region: Region
    style: Optional[Style] = None
    description: Optional[str] = None
