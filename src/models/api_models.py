from pydantic import BaseModel, Field

from models.camel_model import CamelModel


class Alcohol(CamelModel):
    category: str = Field(description='category of the alcohol')
    sub_category: str = Field(description='sub-category of the alcohol')
    brand: str = Field(description='brand name of the alcohol')
    name: str = Field(description='product name of the alcohol from the brand')
    decanting_time: float = Field(description='decanting time in minutes of the alcohol if it needs, otherwise output null')


class WinePreference(BaseModel):
    sweetness: str = Field(description='sweetness of the wine: dry, medium or high')
    acidity: str = Field(description='acidity of the wine: low, medium or high')
    body: str = Field(description='body of the wine: light, medium or bold')