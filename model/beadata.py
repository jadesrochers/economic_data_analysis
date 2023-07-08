from pydantic import BaseModel

class BeaData(BaseModel):
    geoid_data: dict[str, float]

