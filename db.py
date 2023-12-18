import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017")

db = myclient['alcoholic']
collection = db['alcohols']

cur = collection.find({})
for doc in cur:
    print(doc)