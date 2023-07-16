from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from model.beadata import Beadata
from model.geojson import GeoData
from geojson import getgeojson
from typing import Dict, List
import beadata

app = FastAPI()

origins = [
    "*",
    "http://localhost",
    "http://127.0.0.1",
] 

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


@app.get("/beadata/{table}/years")
async def get_years_for_table(table: str) -> Dict[str, List[int]]:
    try:
        years = beadata.get_years(table)
    except Exception as e:
        raise HTTPException(status_code=404, detail='Problem retrieving years for table: {table}'.format(table=table))
    return {'years': years}


geojson_names = set(['us_state', 'us_county'])
@app.get("/geojson/{name}")
async def get_geojson(name: str) -> GeoData:
    print('Geojson data endpoint hit')
    if name not in geojson_names:
        raise HTTPException(status_code=404, detail='GeoJson item: {name} not found'.format(name=name))
    return getgeojson(name)

