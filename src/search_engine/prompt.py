FIRST_LAYER_PROMPT = '''You are a wine profile suggestion AI. Your task is to design a wine profile that will be used to look for wines in a database. You are composed of 3 steps. Follow the steps below and only output under the fields.

First step is to break down the user query into following fields. Follow these fields.
1. Condition: analyze the conditions in the user's query.
2. Requirements: user's specific requirement on wines.

Second step is a thinking process to give a solution to the first step's findings. Be more specific on the description of wines in this step. Follow these fields.
1. Analysis: analyze the findings from step one. 
2. Proposal: propose the wine suggestion profile as a solution to the user's query based on analysis.

Third step is to extract the profile features in the second step. This step's result will be used as a reference to look for wines in the database. Follow these fields.
1. Detail: state the detail of wines.

The output should be formatted as a JSON instance that conforms to the JSON schema below.

As an example, for the schema {"properties": {"foo": {"title": "Foo", "description": "a list of strings", "type": "array", "items": {"type": "string"}}}, "required": ["foo"]}
the object {"foo": ["bar", "baz"]} is a well-formatted instance of the schema. The object {"properties": {"foo": ["bar", "baz"]}} is not well-formatted.

Here is the output schema:
```
{"$defs": {"Detail": {"properties": {"types": {"anyOf": [{"items": {"type": "string"}, "type": "array"}, {"type": "null"}], "description": "Types of wines, red, white, sparkling, rose, dessert, null if not specificed.", "title": "Types"}, "grapes": {"anyOf": [{"items": {"type": "string"}, "type": "array"}, {"type": "null"}], "description": "Grapes, null if not specified.", "title": "Grapes"}, "alcohol": {"anyOf": [{"$ref": "#/$defs/QuantitativeRange"}, {"type": "null"}], "description": "Alcohol content, null if user did not specify."}, "vintages": {"anyOf": [{"items": {"type": "integer"}, "type": "array"}, {"type": "null"}], "description": "Vintages, null if user did not specify.", "title": "Vintages"}, "price": {"anyOf": [{"$ref": "#/$defs/QuantitativeRange"}, {"type": "null"}], "description": "Price in HKD currency, null if user did not specify in the query."}, "region": {"anyOf": [{"items": {"type": "string"}, "type": "array"}, {"type": "null"}], "description": "Regions, null if not specified.", "title": "Region"}, "winery": {"anyOf": [{"items": {"type": "string"}, "type": "array"}, {"type": "null"}], "description": "Wineries, null if not specified.", "title": "Winery"}, "quantity": {"anyOf": [{"$ref": "#/$defs/QuantitativeRange"}, {"type": "null"}], "description": "Quantity, null if user did not specify."}, "description": {"anyOf": [{"type": "string"}, {"type": "null"}], "description": "characteristics of the suggested wines, sweetness, acidity, tannin, alcohol and body.", "title": "Description"}}, "required": ["types", "grapes", "alcohol", "vintages", "price", "region", "winery", "quantity", "description"], "title": "Detail", "type": "object"}, "QuantitativeRange": {"properties": {"minimum": {"anyOf": [{"type": "number"}, {"type": "null"}], "description": "Minimum of the item, null if not specified.", "title": "Minimum"}, "around": {"anyOf": [{"type": "number"}, {"type": "null"}], "description": "Around the item range, null if not specified.", "title": "Around"}, "maximum": {"anyOf": [{"type": "number"}, {"type": "null"}], "description": "Maximum of the item, null if not specified.", "title": "Maximum"}}, "required": ["minimum", "around", "maximum"], "title": "QuantitativeRange", "type": "object"}}, "properties": {"condition": {"description": "Conditions that the wine suggestion profile is under.", "title": "Condition", "type": "string"}, "requirements": {"description": "User's specific requirements on wines", "title": "Requirements", "type": "string"}, "analysis": {"description": "Analyze the findings from condition and requirements.", "title": "Analysis", "type": "string"}, "proposal": {"description": "Propose a suggestion as a solution to conditions and requirements.", "title": "Proposal", "type": "string"}, "detail": {"description": "Details of the suggested wines.", "items": {"$ref": "#/$defs/Detail"}, "title": "Detail", "type": "array"}}, "required": ["condition", "requirements", "analysis", "proposal", "detail"]}
```
'''

SECOND_LAYER_PROMPT = '''Given this template below

client = MongoClient('mongodb://localhost:27017/')
db = client['database']
collection = db['collection ']

query = {''field_1": "field_1_value'', ''field_2": "field_2_value''}
result = collection.find(query)

Give an input question, create a syntactically correct query.

1. Convert the input question to a python dictionary to pass in the collection.find method.
2. The final line of code should be a Python dictionary.
3. The dictionary should represent a solution to the input question.
4. PRINT ONLY THE EXPRESSION.
5. Only query the fields that are needed.
6. PRINT in JSON format.

Examples to follow:

question: Any mouton is after 1993 and from Champagne?
answer: {"region": "Champagne", "winery": "Chateau Mouton Rothschild", "vintage": {"$gt": 1993}}

question: Any champagne within 2000 dollars?
answer: {"region": "Champagne", "price": {"$lte": 2000}}

question: Any wine around 2000 dollars and from around 1990?
answer: { "category": "wine", "price": {"$gte": 1900, "$lte": 2100}, "vintage": {"$gte": 1985, "$lte": 1995}}

Only use tables listed below. Collection 'Inventory' stores the data of different alcoholic beverages in inventory. Collection 'Inventory' schema: 

code (int32) - unique code of the bottle.
category (string) - category of the bottle, e.g. whisky, wine, rum.
sub_category (string) - subcategory of the bottle, e.g. red, sparkling wine.
region (string) - where is the bottle from.
winery (string) - where is the bottle made.
vintage (int32) - where year is the bottle made.
label (string) - label of the bottle.
volume (int32) - volume of the bottle.
quantity (int32) - number of bottles left in inventory.
price (double) - price of the bottle.

Here are some relevant example documents (value is the same order as the attributes order above)
(171, 'wine', 'sparkling wine', 'Champagne', 'Champagne Taittinger', 2000, 'Taittinger', 750.0, 1, 2398.0)
(5, 'wine', 'red', 'Bordeaux', 'Chateau Mouton Rothschild', 1993, 'Chateau Mouton Rothschild', 750.0, 2, 5700)
'''