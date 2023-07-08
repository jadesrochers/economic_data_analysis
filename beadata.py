import json 
import csv
from pathlib import Path
import pandas as pd
import re
import vaex

data_path = Path('./beadata')
geoid = 'GEO_ID'
timeperiod = 'TimePeriod'

def find_datafile(table: str):
    table_path = list(data_path.glob('BEA_{table}_complete.csv'.format(table=table)))[0]
    return table_path
     

# Use the built in csv, see if you can avoid doing vaex or pandas
def get_annual_data_csv(table: str, linecode: str, year: str):
    table_path = find_datafile(table)
    compiled_data = {}
    with open(table_path) as datafile:
        reader = csv.DictReader(datafile)
        n = True
        # Dictionary - want just the GEO_ID and the Value
        # in this, so clear all the other stuff out
        for row in reader:
            if n:
                keynames = row.keys()
                select_linecode = re.compile('[^\-]*-{linecode}+$'.format(linecode=linecode))
                filt = lambda name: bool(select_linecode.match(name))
                data_key = next(x for x in filter(filt, keynames))
                n = False
            if row[timeperiod] == year:
                import pdb; pdb.set_trace()
                compiled_data[row[geoid]] = row[data_key]
    return compiled_data



def get_annual_data(table: str, linecode: str, year: str):
    table_path = find_datafile(table)
    # data_df = pd.read_csv(table_path, index_col=0)
    vdf = vaex.from_csv(table_path)
    # Filter the data
    vdf[vdf.TimePeriod == year]
    has_linecode = re.compile("[^\-]*-[0-9]+$")
    for column in vdf.column_names:
        if bool(has_linecode.match(column)):
            if not column.endswith(str(linecode)):
                vdf.drop(column, inplace=True)
    # Dont see this in the docs anywhere, but try it
    rslt = vdf.export_json()
    # Otherwise, convert to pandas, then to json
    # vdf.to_pandas_df().to_json



# cat my.csv | python -c 'import csv, json, sys; print(json.dumps([dict(r) for r in csv.DictReader(sys.stdin)]))'
