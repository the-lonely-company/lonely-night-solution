from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://admin:lonelyltdcompany@alcohol.dzabi1t.mongodb.net/?retryWrites=true&w=majority&appName=Alcohol"

db_client = MongoClient(uri)

db = db_client.alcoholic

collection_alcohol = db['alcohol']
