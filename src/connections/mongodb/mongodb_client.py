from pymongo.mongo_client import MongoClient

db_client = MongoClient('mongodb+srv://lonelyltdcompany:20240424@olympus.vpwhx2s.mongodb.net/?retryWrites=true&w=majority&appName=olympus')
db = db_client.beverage_industry

collection_beverage = db['beverage']
