import json 
import csv
from pathlib import Path
import pandas as pd
import re
from typing import Dict, List, Union
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


# Get all years of data for each geoid (county in this case)
def get_time_series_data(table: str, linecode: str) -> Dict[str, List[Dict[str, Union[int, float]]]]:
    table_path = find_datafile(table)
    raw_data = pd.read_csv(table_path)
    data_series = '{table}-{linecode}'.format(table=table, linecode=linecode)
    raw_data['Values'] = raw_data[data_series].map(lambda x: default_value if  x.startswith('(NA)') else round(locale.atof(x), 2))
    # This should work and replace missing with 0.0: 
    pivoted_table = pd.pivot_table(raw_data, index='GEO_ID', columns='TimePeriod', values='Values', fill_value=0.0)

    ## This gets nice series for each GEO_ID, but that is not the
    # format that the plotting libraries want
    # return pivoted_table.T.to_dict(orient='list')

    ## This gets each GEO_ID: a dict with TimePeriod/value as keys and
    # the respective time/value as the values, which should work for format.
    pivot_melt = pd.melt(pivoted_table.reset_index(), id_vars='GEO_ID')
    return pivot_melt.groupby('GEO_ID').apply(lambda x: x[['TimePeriod', 'value']].to_dict(orient='records')).to_dict()
    # pivot_grouped = pivot_melt.groupby('GEO_ID')['value'].apply(list)
    # This assumes no missing data but is very simple
    # grouped = raw_data.groupby('GEO_ID')['Values'].apply(list)
    # geoid_tovalue = grouped.to_dict()


# Get the mean of each state, country proportions
def get_county_proportion(table: str, linecode: str) -> Dict[str, List[Dict[str, Union[int, float]]]]:
    state_regex = re.compile('^[0-9]*US[0-9]{2}')
    table_path = find_datafile(table)
    raw_data = pd.read_csv(table_path)
    data_series = '{table}-{linecode}'.format(table=table, linecode=linecode)
    raw_data['Values'] = raw_data[data_series].map(lambda x: default_value if  x.startswith('(NA)') else locale.atof(x))
    raw_data['State_Geoid'] = raw_data['GEO_ID'].map(lambda x: state_regex.search(x).group(0));
    # Get sum for the state for each county/year to do proportion calc
    county_year_sum = raw_data.groupby(['State_Geoid', 'TimePeriod'])['Values'].transform('sum')
    county_year_pct = round(100 * (raw_data['Values'] / county_year_sum), 2)
    year_sum = raw_data.groupby(['TimePeriod'])['Values'].transform('sum')
    raw_data['county_pct'] = county_year_pct
    pivoted_county_proportion = pd.pivot_table(raw_data, index='GEO_ID', columns='TimePeriod', aggfunc='sum', values='county_pct', fill_value=0.0)
    pivot_melt = pd.melt(pivoted_county_proportion.reset_index(), id_vars='GEO_ID')
    return pivot_melt.groupby('GEO_ID').apply(lambda x: x[['TimePeriod', 'value']].to_dict(orient='records')).to_dict()


def get_state_proportion(table: str, linecode: str) -> Dict[str, List[Dict[str, Union[int, float]]]]:
    state_regex = re.compile('^[0-9]*US[0-9]{2}')
    table_path = find_datafile(table)
    raw_data = pd.read_csv(table_path)
    data_series = '{table}-{linecode}'.format(table=table, linecode=linecode)
    raw_data['Values'] = raw_data[data_series].map(lambda x: default_value if  x.startswith('(NA)') else locale.atof(x))
    raw_data['State_Geoid'] = raw_data['GEO_ID'].map(lambda x: state_regex.search(x).group(0));
    pivoted_state_sum = pd.pivot_table(raw_data, index='State_Geoid', columns='TimePeriod', aggfunc='sum', values='Values', fill_value=0.0)
    state_proportions = pivoted_state_sum.div(pivoted_state_sum.sum(axis=0), axis=1)
    pivot_melt = pd.melt(state_proportions.reset_index(), id_vars='State_Geoid')
    pivot_melt['value'] = round(pivot_melt['value'] * 100, 2)
    return pivot_melt.groupby('State_Geoid').apply(lambda x: x[['TimePeriod', 'value']].to_dict(orient='records')).to_dict()


def get_years(table: str) -> List[int]:
    metadata_path = find_metadata(table)
    with open(metadata_path) as metafile:
        data = json.load(metafile)
        return data['years']


# cat my.csv | python -c 'import csv, json, sys; print(json.dumps([dict(r) for r in csv.DictReader(sys.stdin)]))'
