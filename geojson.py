import json

geojsonfiles = {
     'us_state': 'us_state_outline_geojson.json',
     'us_county': 'us_county_outline_geojson.json'
}

def getgeojson(name: str):
    with open(geojsonfiles[name]) as file:
        return json.loads(file.read()) 

