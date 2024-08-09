import json
from pymongo.mongo_client import MongoClient
from loguru import logger

from model.database_model.beverage import Beverage


class BeverageResource:
    def __init__(self):
        self.db_client = MongoClient('mongodb+srv://lonelyltdcompany:20240424@olympus.vpwhx2s.mongodb.net/?retryWrites=true&w=majority&appName=olympus')
        self.beverage_db = self.db_client.beverage
        self.beverage_wine = self.beverage_db['wine']

    def get_beverage_by_id(self, id):
        result = self.beverage_wine.find_one({"url_id": id})
        if result:
            return Beverage(**result)
        else:
            return None
    
    def get_matched_beverages(self, query, description_embedding, quantity):
        matched_ids = []
        if query:
            matched_stocks = self.beverage_wine.find(query, {"_id": 1})
            matched_ids = [stock['_id'] for stock in matched_stocks]

        projection = {
            '_id': 0,
            'url_id': 1,
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
            'style.acidity_description': 1
        }

        logger.info(f"Number fo beverages by query - {len(matched_ids)}")

        if description_embedding:
            embedding_pipeline = [
                {
                    '$vectorSearch': {
                        'index': 'description_embedding_index', 
                        'path': 'description_embedding', 
                        'queryVector': description_embedding,
                        'exact': True,
                        'limit': quantity
                    }
                }, {
                    '$project': {
                        **projection,
                        'score': {
                            '$meta': 'vectorSearchScore'
                        }
                    }
                }
            ]

            if matched_ids:
                embedding_pipeline[0]['$vectorSearch']['filter'] = {'_id': {'$in': matched_ids[:10]}}

            result = self.beverage_wine.aggregate(embedding_pipeline)
            beverages = [Beverage(**item) for item in result]
        else:
            beverages = [Beverage(**item) for item in self.beverage_wine.find(query, projection).limit(quantity)]

        return beverages


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