from typing import List

from fastapi import APIRouter
from models.database_models.alcoholic import Alcohol
from connections.mongodb.mongodb_client import collection_alcohol
from bson import ObjectId


mongodb_router = APIRouter(
    prefix='/mongo'
)


@mongodb_router.get('/get_alcohol', response_model=List[Alcohol])
async def get_alcohols() -> List[Alcohol]:
    alcohols = collection_alcohol.find()
    alcohols = [Alcohol.model_validate(al) for al in alcohols]

    return alcohols


@mongodb_router.post('/add_alcohol')
async def add_alcohol(alcohol: Alcohol) -> None:
    collection_alcohol.insert_one(dict(alcohol))


@mongodb_router.put('/update_alcohol/{id}')
async def update_alcohol(id: str, alcohol: Alcohol) -> None:
    collection_alcohol.find_one_and_update({'_id': ObjectId(id)}, {'$set': dict(alcohol)})


@mongodb_router.delete('/{id}')
async def delete_alcohol(id: str) -> None:
    collection_alcohol.find_one_and_delete({'_id': ObjectId(id)})