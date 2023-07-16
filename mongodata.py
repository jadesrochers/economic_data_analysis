from pymongo import MongoClient
from urllib.parse import quote_plus
# For serializing the return from mongodb
from bson import json_util
import json
import pickle


mongouser='loony'
mongopass=quote_plus('eh6pnehlzqNlNBcfNKYa50pPRFkMxbOBgl86zu3iCECppapxIIg6v77TtJG12HbZx8FxXkRUbL3sJY28')

ATLAS_URI='mongodb+srv://{username}:{password}@cluster0.1cnhy.gcp.mongodb.net/?retryWrites=true&w=majority'.format(username=mongouser, password=mongopass)
DB_NAME='geojson_complete'

mongodb_client = MongoClient(ATLAS_URI)
database = mongodb_client[DB_NAME]

# Get the collections present
for coll in database.list_collections():
    print('Collection: ', coll)


def get_county_data(database):
    county_coll = database.get_collection('US_County_Outline')
    return county_coll.find_one()

def get_state_data(database):
    state_coll = database.get_collection('US_State_Outline')
    return state_coll.find_one()


# Check out a few of the keys
# print('County Data _id: {id}, name: {name}, and description: {description}'.format(id=all_county_data.get('_id'), name=all_county_data.get('name'), description=all_county_data.get('description')))
# print('State Data _id: {id}, name: {name}, and description: {description}'.format(id=all_state_data.get('_id'), name=all_state_data.get('name'), description=all_state_data.get('description')))

# Get the county and state geojson data here
def find_by_name(collection, name):
    blah = collection.find({ 'name': name})
    blahrslt = blah.next()
    return blahrslt.keys()

def pickle_data_binary(data, filename: str):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)

def save_formatted_text(data: json, filename: str):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# all_county_data = get_county_data(database)
all_state_data = get_state_data(database)
# This causes problems for everything, get rid of it
del all_state_data['_id']

# pickle_data_binary(all_county_data, 'us_county_outline_geojson.json')
# pickle_data_binary(all_state_data, 'us_state_outline_geojson.json')
save_formatted_text(all_state_data, 'us_state_outline_geojson.txt')

# county_coll = database.get_collection('US_County_Outline')
# state_coll = database.get_collection('US_State_Outline')
# find_by_name(county_coll, 'US_County_Outline')

