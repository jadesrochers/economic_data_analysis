import json
import pickle
from model.geojson import GeoData

geojsonfiles = {
     'us_state': 'us_state_outline_geojson.json',
     'us_county': 'us_county_outline_geojson.json',
     'us_county_combined': 'us_county_binary_geojson_citycounty.json'
}


def pickle_data_binary(data, filename: str):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)


def getgeojson(name: str) -> GeoData:
    with open(geojsonfiles[name], 'rb') as file:
        return pickle.load(file) 


def write_text_geojson(file_content: str, file_name: str):
    with open(file_name, 'w') as file:
        json.dump(file_content, file, default=str)


def read_text_geojson(file_name: str):
    with open(file_name, 'r') as file:
        contents = file.read()
        # json.load() should work directly, but two step demo here
        return json.loads(contents)


def geojson_text_to_binary(infile: str, outfile: str):
    json = read_text_geojson(infile)
    pickle_data_binary(json, outfile)

