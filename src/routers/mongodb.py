from fastapi import APIRouter
from models.api_models import Stock
from connections.mongodb.mongodb_client import beverages_inventory


mongodb_router = APIRouter(
    prefix='/mongo',
    tags=['Database']
)


@mongodb_router.get('/get_alcohol', response_model=Stock)
async def get_alcohols(category: str, code: int) -> Stock:
    query = {'category': category, 'code': code}

    projection = {
        'code': 1,
        'category': 1,
        'sub_category': 1,
        'region': 1,
        'winery': 1,
        'vintage': 1,
        'label': 1,
        'volume': 1,
        'quantity': 1,
        'price': 1,
        'description': 1,
        'image': 1
    }

    item = beverages_inventory.find_one(query, projection)

    if item:
        return Stock(**item)
    else:
        return f'No stock with category {category} and code {code} found'
