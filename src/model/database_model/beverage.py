from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from humps import camelize


class Grape(BaseModel):
    name: str

class Food(BaseModel):
    name: str

class Winery(BaseModel):
    name: str

class Vintage(BaseModel):
    name: str
    year: int

class Country(BaseModel):
    name: str

class Region(BaseModel):
    name: str
    country: Country

class Style(BaseModel):
    name: Optional[str] = None
    wine_type: Optional[str] = None
    varietal_name: Optional[str] = None
    blurb: Optional[str] = None
    body_description: Optional[str] = None
    acidity_description: Optional[str] = None

class Beverage(BaseModel):
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
    score: Optional[float] = None

    def to_camel_dict(self) -> Dict[str, Any]:
        beverage_dict = self.model_dump()
        camel_case_dict = camelize(beverage_dict)
        return camel_case_dict
