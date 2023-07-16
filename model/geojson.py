from pydantic import BaseModel
from typing import List, Union

class GeoProperties(BaseModel):
    GEO_ID: str
    NAME: str
    LSAD: str
    CENSUSAREA: float

class Geometry(BaseModel):
    type: str
    # This may be deeply nested, but just calling it a float array
    coordinates: List[List[List[Union[float, List[float]]]]]

class Feature(BaseModel):
    type: str
    properties: GeoProperties
    geometry: Geometry

class GeoJson(BaseModel):
    type: str
    features: List[Feature]

class GeoData(BaseModel):
    geojson: GeoJson
    name: str
    source: str
    description: str
    website: str
