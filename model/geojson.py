from pydantic import BaseModel
from typing import List

class GeoProperties(BaseModel):
    GEO_ID: str
    NAME: str

class Geometry(BaseModel):
    type: str
    # This may be deeply nested, but just calling it a float array
    coordinates: List[float]

class Feature(BaseModel):
    type: str
    properties: GeoProperties
    geometry: Geometry

class GeoJson(BaseModel):
    type: str
    name: str
    source: str
    description: str
    website: str
    features: List[Feature]
