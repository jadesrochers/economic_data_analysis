import json 
import csv
from pathlib import Path
import pandas as pd
import re
from typing import Dict, List
import locale

# Will use the system locale to determine the locale to set
# relevant for str -> numeric conversions and other stuff (what else?) 
locale.setlocale(locale.LC_ALL, '')
default_value = 0.0

data_path = Path('./beadata')
geoid = 'GEO_ID'
timeperiod = 'TimePeriod'

def find_datafile(table: str):
    table_path = list(data_path.glob('BEA_{table}_complete.csv'.format(table=table)))[0]
    return table_path

def find_metadata(table: str):
    table_path = list(data_path.glob('BEA_{table}_metadata.json'.format(table=table)))[0]
    return table_path
     

# Use the built in csv, see if you can avoid doing vaex or pandas
def get_annual_data(table: str, linecode: str, year: str) -> Dict[str, float]:
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
                compiled_data[row[geoid]] = default_value if row[data_key].startswith('(NA)') else locale.atof(row[data_key])
    return compiled_data


def get_time_series_data(table: str, linecode: str) -> Dict[str, List[float]]:
    table_path = find_datafile(table)
    raw_data = pd.read_csv(table_path)

    # This should work and replace missing with 0.0: 
    pivoted_table = pd.pivot_table(raw_data, index='GEO_ID', columns='TimePeriod', values='Values', fill_value=0.0)
    pivot_melt = pd.melt(pivoted_table.reset_index(), id_vars='GEO_ID')
    pivot_grouped = pivot_melt.groupby('GEO_ID')['value'].apply(list)


    # This assumes no missing data but is very simple
    grouped = raw_data.groupby('GEO_ID')['Values'].apply(list)
    geoid_tovalue = grouped.to_dict()

    return geoid_tovalue


def get_years(table: str) -> List[int]:
    metadata_path = find_metadata(table)
    with open(metadata_path) as metafile:
        data = json.load(metafile)
        return data['years']


# cat my.csv | python -c 'import csv, json, sys; print(json.dumps([dict(r) for r in csv.DictReader(sys.stdin)]))'
