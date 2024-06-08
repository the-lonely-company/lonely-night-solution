import json
from pymongo.mongo_client import MongoClient
from loguru import logger

db_client = MongoClient('mongodb+srv://lonelyltdcompany:20240424@olympus.vpwhx2s.mongodb.net/?retryWrites=true&w=majority&appName=olympus')
db = db_client.beverages

beverages_inventory = db['inventory']


def vector_search(embedding):
    pipeline = [
        {
            '$vectorSearch': {
                'index': 'description_embedding_vector_index', 
                'path': 'embedding', 
                'queryVector': embedding,
                'numCandidates': 50, 
                'limit': 4
            }
        }, {
            '$project': {
                '_id': 0, 
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
                'similarity_score': {
                    '$meta': 'vectorSearchScore'
                }
            }
        }
    ]

    result = beverages_inventory.aggregate(pipeline)
    stocks = [dict(r) for r in result]

    logger.debug(stocks)

    return stocks