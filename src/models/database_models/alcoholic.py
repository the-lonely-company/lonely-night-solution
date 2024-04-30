from typing import Optional
from pydantic import BaseModel


class Alcohol(BaseModel):
    winery: str
    label: str
    sweetness: str
    acidity: str
    body: str
    alcohol: str
    tannis: str
    rating: float
    first_classification: str
    second_classification: str
    third_classification: Optional[str]
    