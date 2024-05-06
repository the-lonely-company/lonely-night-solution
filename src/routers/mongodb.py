from typing import List

from fastapi import APIRouter
from models.database_models.alcoholic import Beverage
from connections.mongodb.mongodb_client import collection_beverage
from bson import ObjectId

from loguru import logger


mongodb_router = APIRouter(
    prefix='/mongo'
)


@mongodb_router.get('/get_alcohol', response_model=List[Beverage])
async def get_alcohols() -> List[Beverage]:
    beverages = collection_beverage.find()
    beverages = [Beverage.model_validate(beverage) for beverage in beverages]

    return beverages


@mongodb_router.post('/add_alcohol')
async def add_alcohol(beverage: Beverage) -> None:
    collection_beverage.insert_one(beverage.dict())


@mongodb_router.put('/update_alcohol/{id}')
async def update_alcohol(id: str, beverage: Beverage) -> None:
    collection_beverage.find_one_and_update({'_id': ObjectId(id)}, {'$set': dict(beverage)})


@mongodb_router.delete('/{id}')
async def delete_alcohol(id: str) -> None:
    collection_beverage.find_one_and_delete({'_id': ObjectId(id)})