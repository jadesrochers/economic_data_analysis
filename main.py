from fastapi import FastAPI, HTTPException
from model.beadata import Beadata
from model.geojson import GeoJson
from geojson import getgeojson
from typing import Dict
import beadata

app = FastAPI()


@app.get("/health")
async def root():
    return {"message": "Server is operating"}


@app.get("/beadata/{table}/{linecode}/{year}")
async def get_table_annual_data(table: str, linecode: str, year: str) -> Dict[str, Beadata]:
    print('Getting table: {table}, linecode: {linecode}, year: {year}'.format(table=table, linecode=linecode, year=year))
    # Code to get the table data 
    data = {}
    try:
        data = beadata.get_annual_data(table, linecode, year)
    except Exception as e:
        raise HTTPException(status_code=404, detail='Problem retrieving data for table: {table} linecode: {linecode}, year: {year}'.format(table=table, linecode=linecode, year=year))
    return {'annual_data': data}


geojson_names = set(['us_state', 'us_county'])
@app.get("/geojson/{name}")
async def get_geojson(name: str) -> GeoJson:
    # store the geojson locally, access and return.
    # Get this from my mongodb database.
    if name not in geojson_names:
        raise HTTPException(status_code=404, detail='GeoJson item: {name} not found'.format(name=name))
    geojson = getgeojson(name)
    return {'geojson': geojson}

