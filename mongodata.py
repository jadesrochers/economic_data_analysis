from pymongo import MongoClient
from urllib.parse import quote_plus
# For serializing the return from mongodb
from bson import json_util
import json


mongouser='loony'
mongopass=quote_plus('eh6pnehlzqNlNBcfNKYa50pPRFkMxbOBgl86zu3iCECppapxIIg6v77TtJG12HbZx8FxXkRUbL3sJY28')

ATLAS_URI='mongodb+srv://{username}:{password}@cluster0.1cnhy.gcp.mongodb.net/?retryWrites=true&w=majority'.format(username=mongouser, password=mongopass)
DB_NAME='geojson_complete'

mongodb_client = MongoClient(ATLAS_URI)
database = mongodb_client[DB_NAME]

# Get the collections present
for coll in database.list_collections():
    print('Collection: ', coll)

county_coll = database.get_collection('US_County_Outline')
state_coll = database.get_collection('US_State_Outline')
all_county_data = county_coll.find_one()
all_state_data = state_coll.find_one()

# See how you actually set up the data
all_county_data.keys()
all_state_data.keys()

# Check out a few of the keys
print('County Data _id: {id}, name: {name}, and description: {description}'.format(id=all_county_data.get('_id'), name=all_county_data.get('name'), description=all_county_data.get('description')))
print('State Data _id: {id}, name: {name}, and description: {description}'.format(id=all_state_data.get('_id'), name=all_state_data.get('name'), description=all_state_data.get('description')))
import pdb; pdb.set_trace()

# Get the county and state geojson data here

with open('us_county_outline_geojson.json', 'w') as f:
    json.dump(json_util.dumps(all_county_data), f, ensure_ascii=False)

with open('us_state_outline_geojson.json', 'w') as f:
    json.dump(json_util.dumps(all_state_data), f, ensure_ascii=False)


# Test out a find operation - worked knowing the name of the data
blah = county_coll.find({ 'name': 'US_County_Outline'})
blahrslt = blah.next()
blahrslt.keys()
blahrslt.get('name')
