from connections.mongodb.mongodb_client import collection_beverage
from models.database_models.alcoholic import Beverage
from chains.general_chain import general_chain
from chains.suggestion_chain import suggestion_chain


def route(info):
    if "suggestion" in info["topic"].lower():
        return suggestion_chain
    else:
        return general_chain
    
def get_beverage(wine_preference: dict):
    from loguru import logger; logger.debug(wine_preference)

    query = {
        'sweetness': wine_preference['sweetness'],
        'acidity': wine_preference['acidity'],
        'body': wine_preference['body']
    }

    response = collection_beverage.find(query)

    beverages = [Beverage.model_validate(res) for res in response]

    logger.debug(beverages)

    return beverages