from pymongo.mongo_client import MongoClient
from loguru import logger

db_client = MongoClient('mongodb+srv://lonelyltdcompany:20240424@olympus.vpwhx2s.mongodb.net/?retryWrites=true&w=majority&appName=olympus')
db = db_client.beverages

beverages_inventory = db['inventory']


def vector_search(embedding):
    pipeline = [
        {
            '$vectorSearch': {
                'index': 'vector_index', 
                'path': 'EMBEDDING', 
                'queryVector': embedding,
                'numCandidates': 50, 
                'limit': 4
            }
        }, {
            '$project': {
                '_id': 0, 
                'CATEGORY': 1,
                'SUB_CATEGORY': 1,
                'REGION': 1,
                'WINERY': 1,
                'VINTAGE': 1,
                'LABEL': 1, 
                'VOLUME': 1,
                'QUANTITY': 1,
                'PRICE': 1,
                'DESCRIPTION': 1,
                'score': {
                    '$meta': 'vectorSearchScore'
                }
            }
        }
    ]

    result = beverages_inventory.aggregate(pipeline)
    labels = [dict(r) for r in result]

    logger.debug(result)

    logger.debug(labels)

    return labels