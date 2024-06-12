from typing import Optional, List, Any
import math

from pydantic import BaseModel, Field, field_validator

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


class AssistantResponse(BaseModel):
    preference: Optional[str] = Field(description="user's preference on alcoholic beverages or favourite brands, null if user preference is open or cannot be identified")
    needs: Optional[str] = Field(description="user's needs on alcoholic beverages, null if no specifc needs")
    characteristic: Optional[str] = Field(description='characteristic, brands or names of drinks that matches user preference and needs')
    budget: Optional[float] = Field(description="user's budget in hkd, null if budget cannot be guessed")
    price_negotiating: Optional[bool] = Field(description='is user negotiating price or not')
    content : str = Field(description='content to respond to user query after analysis')
    recommend_status: bool = Field(description='did you choose to recommend drinks or not')


class Stock(BaseModel):
    code: int
    category: str
    sub_category: str
    region: str
    winery: str
    vintage: Optional[int] = None
    label: str
    volume: float
    quantity: int
    price: Optional[float] = None
    description: str
    image: str = None

    @field_validator('*', mode='before')
    def split_str(cls, v):
        if isinstance(v, float):
            if math.isnan(v):
                return None
            return v
        return v   

class StockWithSimilarityScore(Stock):
    similarity_score: float


class InvokeResponse(BaseModel):
    assistant_response: AssistantResponse
    recommendation: List[Optional[StockWithSimilarityScore]]
