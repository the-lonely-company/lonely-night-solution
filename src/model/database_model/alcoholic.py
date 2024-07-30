from typing import Optional, List
from typing_extensions import Annotated

from pydantic import BaseModel
from pydantic.functional_validators import AfterValidator
from bson.objectid import ObjectId as _ObjectId


class Rating(BaseModel):
    rp: Optional[int] = None
    js: Optional[int] = None
    wa: Optional[int] = None


class Alcohol(BaseModel):
    degree: float
    level: str


class FoodPairing(BaseModel):
    ingredient: Optional[List[str]] = None
    dish: Optional[List[str]] = None


class Region(BaseModel):
    country: str
    city: str
    location: Optional[str] = None


class Beverage(BaseModel):
    winery: str
    label: str
    vintage: int
    price: float
    rating: Optional[Rating] = None
    region: Region
    sweetness: str
    acidity: str
    body: str
    alcohol: Alcohol
    tannis: str
    decanting_time: Optional[float] = None
    color: List[str]
    flavour: List[str]
    nose: List[str]
    drinking_temperature: float
    food_pairing: Optional[FoodPairing] = None
    grape: Optional[List[str]] = None
    first_classification: str
    second_classification: str
    third_classification: Optional[str] = None
    