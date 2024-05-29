from typing import List

from fastapi import APIRouter
from models.database_models.alcoholic import Beverage
from connections.mongodb.mongodb_client import beverages_inventory
from bson import ObjectId

from loguru import logger


mongodb_router = APIRouter(
    prefix='/mongo'
)


@mongodb_router.get('/get_alcohol', response_model=List[Beverage])
async def get_alcohols() -> List[Beverage]:
    response = beverages_inventory.find()
    beverages = [Beverage.model_validate(res) for res in response]

    return beverages


@mongodb_router.post('/add_alcohol')
async def add_alcohol(beverage: Beverage) -> None:
    beverages_inventory.insert_one(beverage.dict())


@mongodb_router.put('/update_alcohol/{id}')
async def update_alcohol(id: str, beverage: Beverage) -> None:
    beverages_inventory.find_one_and_update({'_id': ObjectId(id)}, {'$set': dict(beverage)})


@mongodb_router.delete('/{id}')
async def delete_alcohol(id: str) -> None:
    beverages_inventory.find_one_and_delete({'_id': ObjectId(id)})