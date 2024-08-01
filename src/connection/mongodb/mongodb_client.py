import json
from pymongo.mongo_client import MongoClient
from loguru import logger


class BeverageResource:
    def __init__(self):
        self.db_client = MongoClient('mongodb+srv://lonelyltdcompany:20240424@olympus.vpwhx2s.mongodb.net/?retryWrites=true&w=majority&appName=olympus')
        self.beverage_db = self.db_client.beverage
        self.beverage_wine = self.beverage_db['wine']

    def get_beverages_by_query(self, query):
        pipeline = [
            {
                '$match': query
            }, {
                '$project': {
                    '_id': 0, 
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
            }, {
                '$limit': 4
            }
        ]

        result = self.beverages_inventory.aggregate(pipeline)
        stocks = [dict(r) for r in result]

        logger.debug([stock.keys() for stock in stocks])

        return stocks
    
    def get_matched_beverages(self, query, description_embedding, quantity):
        matched_stocks = self.beverage_wine.find(query, {"_id": 1})
        matched_ids = [stock['_id'] for stock in matched_stocks]

        logger.info(matched_ids)

        embedding_pipeline = [
            {
                '$vectorSearch': {
                    'index': 'description_embedding_index', 
                    'path': 'description_embedding', 
                    'filter': {'_id': { '$in': matched_ids }},
                    'queryVector': description_embedding,
                    'exact': True,
                    'limit': quantity
                }
            }, {
                '$project': {
                    '_id': 0,
                    'name': 1,
                    'is_natural': 1,
                    'alcohol': 1, 
                    'grapes.name': 1,
                    'winery.name': 1, 
                    'region.name': 1,
                    'region.country.name': 1,
                    'style.wine_type': 1,
                    'style.varietal_name': 1,
                    'style.body_description': 1,
                    'style.acidity_description': 1,
                    'score': {
                        '$meta': 'vectorSearchScore'
                    }
                }
            }
        ]

        result = self.beverage_wine.aggregate(embedding_pipeline)
        final_stocks = [dict(r) for r in result]

        return final_stocks


    def meta_vector_search(self, embedding):
        pipeline = [
            {
                '$vectorSearch': {
                    'index': 'meta_embedding_index', 
                    'path': 'meta_embedding', 
                    'queryVector': embedding,
                    'exact': True,
                    'limit': 1
                }
            }, {
                '$project': {
                    '_id': 0,
                    'name': 1,
                    'is_natural': 1,
                    'alcohol': 1, 
                    'grapes.name': 1,
                    'winery.name': 1, 
                    'region.name': 1,
                    'region.country.name': 1,
                    'style.wine_type': 1,
                    'style.varietal_name': 1,
                    'style.body_description': 1,
                    'style.acidity_description': 1,
                     'vintages': {
                        '$let': {
                            'vars': {
                                'firstVintage': { '$arrayElemAt': ['$vintages', 0] }
                            },
                            'in': [
                                { 'year': '$$firstVintage.year' }
                            ]
                        }
                    }
                }
            }
        ]

        result = self.beverage_wine.aggregate(pipeline)
        stocks = [dict(r) for r in result]

        return stocks
    

beverage_resource = BeverageResource()