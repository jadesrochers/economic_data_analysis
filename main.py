from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
async def root():
    return {"message": "Server is operating"}


@app.get("/beadata/{table}/{linecode}")
async def get_table_data(table: str, linecode: int):
    # Code to get the table data 
    return ()


@app.get("/geojson/{boundaries}/{scale}")
async def get_table_data(boundaries: str, scale: str):
    # store the geojson locally, access and return.
    # Get this from my mongodb database.
    return ()
