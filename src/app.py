from flask import Flask, request
from src.db_connect import connect_to_db
import pprint


app = Flask(__name__)

# write a API end-point that gets list of wines by grapes(4 in prototyping stage) 

@app.route('/')
def get4wines():
    client = connect_to_db()
    red_wine_db = client["red_wine"]
    alko_db = red_wine_db["alko"]

    # GET Request Parameters into query
    args = request.args
    grape = args['grape']
    query = {"grapes" : grape}
    result = alko_db.find(query)

    # get first 4 wines
    returned_wines = {"wines" : []}
    for grapes_wine in result[:4]:
        pprint.pprint(grapes_wine)
        returned_wines["wines"].append(grapes_wine)

    # return as JSON
    return returned_wines