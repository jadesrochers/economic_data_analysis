from pymongo import MongoClient

ATLAS_URI=mongodb+srv://<username>:<password>@sandbox.lqlql.mongodb.net/?retryWrites=true&w=majority
DB_NAME=pymongo_tutorial

mongodb_client = MongoClient(config["ATLAS_URI"])
database = mongodb_client[config["DB_NAME"]]

def get_geojson_data(boundaries: str):
    return database.query()
