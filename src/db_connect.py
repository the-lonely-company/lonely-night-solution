from pymongo.mongo_client import MongoClient
import os
from dotenv import load_dotenv

def connect_to_db():

    load_dotenv()

    DB_PASSWORD = os.getenv('DB_PASSWORD')

    uri = "mongodb+srv://whiskey:{DB_PASSWORD}@wine-data.neklle0.mongodb.net/?retryWrites=true&w=majority".format(
        DB_PASSWORD=DB_PASSWORD
    )
    # Create a new client and connect to the server
    client = MongoClient(uri)

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    
    # return a client
    return client
