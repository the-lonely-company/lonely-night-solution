from fastapi import APIRouter, HTTPException
from connection.mongodb.mongodb_client import beverage_resource
from model.api_model.beverage import Beverage


db_router = APIRouter(
    prefix='/beverage',
    tags=['Beverage']
)


@db_router.get('/get-beverage', response_model=Beverage)
async def get_alcohols(id: int) -> Beverage:
    item = beverage_resource.get_beverage_by_id(id)

    if item:
        return Beverage(**item.to_camel_dict())
    else:
        return HTTPException(status_code=404, detail="Item not found")
