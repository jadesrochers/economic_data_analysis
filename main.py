from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from model.beadata import Beadata
from model.geojson import GeoData
from geojson import getgeojson
from typing import Dict, List, Union
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


@app.get("/beadata/county_timeseries/{table}/{linecode}")
async def get_county_timeseries(table: str, linecode: str) -> Dict[str, List[Dict[str, Union[int, float]]]]:
    print('Getting time series for table: {table}, linecode: {linecode}'.format(table=table, linecode=linecode))
    # Code to get the table data 
    data = {}
    try:
        data = beadata.get_time_series_data(table, linecode)
    except Exception as e:
        raise HTTPException(status_code=404, detail='Problem retrieving time series for table: {table} linecode: {linecode}'.format(table=table, linecode=linecode))
    return data


@app.get("/beadata/county_proportions/{table}/{linecode}")
async def get_county_proportion(table: str, linecode: str) -> Dict[str, List[Dict[str, Union[int, float]]]]:
    print('Getting county proportion for table: {table}, linecode: {linecode}'.format(table=table, linecode=linecode))
    # Code to get the table data 
    data = {}
    try:
        data = beadata.get_county_proportion(table, linecode)
    except Exception as e:
        raise HTTPException(status_code=404, detail='Problem retrieving time series for table: {table} linecode: {linecode}'.format(table=table, linecode=linecode))
    return data


@app.get("/beadata/state_proportions/{table}/{linecode}")
async def get_state_proportion(table: str, linecode: str) -> Dict[str, List[Dict[str, Union[int, float]]]]:
    print('Getting state proportion for table: {table}, linecode: {linecode}'.format(table=table, linecode=linecode))
    # Code to get the table data 
    data = {}
    try:
        data = beadata.get_state_proportion(table, linecode)
    except Exception as e:
        raise HTTPException(status_code=404, detail='Problem retrieving time series for table: {table} linecode: {linecode}'.format(table=table, linecode=linecode))
    return data


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


geojson_names = set(['us_state', 'us_county', 'us_county_combined'])
@app.get("/geojson/{name}")
async def get_geojson(name: str) -> GeoData:
    print('Geojson data endpoint hit')
    if name not in geojson_names:
        raise HTTPException(status_code=404, detail='GeoJson item: {name} not found'.format(name=name))
    return getgeojson(name)

