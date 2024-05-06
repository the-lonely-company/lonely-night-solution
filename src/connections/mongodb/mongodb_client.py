from pymongo.mongo_client import MongoClient

db_client = MongoClient('mongodb+srv://lonelyltdcompany:20240424@alcoholic.whtr0ut.mongodb.net/?retryWrites=true&w=majority&appName=alcoholic')

db = db_client.

collection_beverage = db['beverage']
