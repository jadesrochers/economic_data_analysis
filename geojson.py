import json
import pickle
from model.geojson import GeoData

geojsonfiles = {
     'us_state': 'us_state_outline_geojson.json',
     'us_county': 'us_county_outline_geojson.json'
}

def getgeojson(name: str) -> GeoData:
    with open(geojsonfiles[name], 'rb') as file:
        return pickle.load(file) 

