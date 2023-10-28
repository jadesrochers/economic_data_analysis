import json 
import csv
from pathlib import Path
import pandas as pd
import re
from typing import Dict, List
import locale
import beadata
import numpy as np

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
 

def test_get_time_series_data(table: str, linecode: str) -> Dict[str, List[float]]:
    import pdb; pdb.set_trace()
    table_path = find_datafile(table)
    raw_data = pd.read_csv(table_path)
    raw_data['Values'] = raw_data['CAINC1-1'].map(lambda x: default_value if  x.startswith('(NA)') else locale.atof(x))
    # The index=GEO_ID indicates to group by that, the columns that Will
    # be created are laid out by columns='TimePeriod', and the values to
    # populate those columnes are specified by values='Values'
    pivoted_table = pd.pivot_table(raw_data, index='GEO_ID', columns='TimePeriod', values='Values', fill_value=0.0)
    pivot_melt = pd.melt(pivoted_table.reset_index(), id_vars='GEO_ID')
    pivot_grouped = pivot_melt.groupby('GEO_ID')['value'].apply(list)
    # Need to take the csv/pandas table and turn it into a storage object
    # for the return, perhaps having metadata about the values 
    # Such as what years, the varname, missing proportion,
    # and then the dict with GEO_ID and List of values to keep things 
    # as effecient as possible
    testpd = pivoted_table.stack()
    testrdl = raw_data.groupby('GEO_ID')['Values'].apply(list)
    testrd = raw_data.groupby(['GEO_ID', 'TimePeriod'])['Values'].apply(lambda x: x.fillna(0.0))
    testrd_reform = pd.melt(testrd.reset_index(), id_vars='GEO_ID')
    reform_list = testrd_reform.groupby('GEO_ID')['value'].apply(list)
    geoid_tovalue = reform_list.to_dict()


def get_time_series_data(table: str, linecode: str) -> Dict[str, List[float]]:
    table_path = find_datafile(table)
    raw_data = pd.read_csv(table_path)
    data_series = '{table}-{linecode}'.format(table=table, linecode=linecode)
    if raw_data.dtypes[data_series] == np.dtype('str'):
        raw_data['Values'] = raw_data[data_series].map(lambda x: default_value if  x.startswith('(NA)') else locale.atof(x))
    else:
        raw_data['Values'] = raw_data[data_series]

    # This might be broken - it is very slow and a pain
    # group_values = raw_data.groupby(['GEO_ID', 'TimePeriod'])['Values'].fillna(value=0.0)
    # Melt is useful, but trying to avoid the built in na fill
    # group_values = pd.melt(group_values.reset_index(), id_vars='GEO_ID')
    # group_values = group_values.groupby('GEO_ID')['value'].apply(list)

    # This should work and replace missing with 0.0: 
    pivoted_table = pd.pivot_table(raw_data, index='GEO_ID', columns='TimePeriod', values='Values', fill_value=0.0)
    # The .T is the transpose
    geoid_to_timeseries = pivoted_table.T.to_dict(orient='list')
    pivot_melt = pd.melt(pivoted_table.reset_index(), id_vars='GEO_ID')
    # pivot_grouped_dict = pivot_melt.groupby('GEO_ID')['value'].apply(list)
    pivot_grouped_dict = pivot_melt.groupby('GEO_ID').apply(lambda x: x[['TimePeriod', 'value']].to_dict(orient='records')).to_dict()


    # This assumes no missing data but is very simple
    # grouped = raw_data.groupby('GEO_ID')['Values'].apply(list)
    # geoid_tovalue = grouped.to_dict()
    return geoid_to_timeseries


# blah = get_time_series_data('CAINC1', 1)

def get_county_proportion_test(table: str, linecode: str) -> Dict[str, float]:
    state_regex = re.compile('^[0-9]*US[0-9]{2}')
    table_path = find_datafile(table)
    raw_data = pd.read_csv(table_path)
    data_series = '{table}-{linecode}'.format(table=table, linecode=linecode)
    import pdb; pdb.set_trace()
    if raw_data.dtypes[data_series] == np.dtype('str'):
        raw_data['Values'] = raw_data[data_series].map(lambda x: default_value if  x.startswith('(NA)') else locale.atof(x))
    else:
        raw_data['Values'] = raw_data[data_series]
    raw_data['State_Geoid'] = raw_data['GEO_ID'].map(lambda x: state_regex.search(x).group(0));
    # and some country summations
    county_year_sum = raw_data.groupby(['State_Geoid', 'TimePeriod'])['Values'].transform('sum')
    county_year_pct = 100 * (raw_data['Values'] / county_year_sum)
    raw_data['county_pct'] = county_year_pct
    pivoted_county_proportion = pd.pivot_table(raw_data, index='GEO_ID', columns='TimePeriod', aggfunc='sum', values='county_pct', fill_value=0.0)
    pivot_melt = pd.melt(pivoted_county_proportion.reset_index(), id_vars='GEO_ID')
    pivot_grouped_dict = pivot_melt.groupby('GEO_ID').apply(lambda x: x[['TimePeriod', 'value']].to_dict(orient='records')).to_dict()
    county_proportions_dict = pivoted_county_proportion.T.to_dict(orient='list')


def get_state_proportion_test(table: str, linecode: str) -> Dict[str, List[float]]:
    state_regex = re.compile('^[0-9]*US[0-9]{2}')
    table_path = find_datafile(table)
    raw_data = pd.read_csv(table_path)
    data_series = '{table}-{linecode}'.format(table=table, linecode=linecode)
    if raw_data.dtypes[data_series] == np.dtype('str'):
        raw_data['Values'] = raw_data[data_series].map(lambda x: default_value if  x.startswith('(NA)') else locale.atof(x))
    else:
        raw_data['Values'] = raw_data[data_series]
    raw_data['State_Geoid'] = raw_data['GEO_ID'].map(lambda x: state_regex.search(x).group(0));
    pivoted_state_sum = pd.pivot_table(raw_data, index='State_Geoid', columns='TimePeriod', aggfunc='sum', values='Values', fill_value=0.0)
    state_proportions = pivoted_state_sum.div(pivoted_state_sum.sum(axis=0), axis=1)

    pivot_melt = pd.melt(state_proportions.reset_index(), id_vars='State_Geoid')
    pivot_grouped_dict = pivot_melt.groupby('State_Geoid').apply(lambda x: x[['TimePeriod', 'value']].to_dict(orient='records')).to_dict()
    # The quick way; if you have a pivot table, index may already be set fine
    state_proportions_dict = state_proportions.T.to_dict(orient='list')
    # Otherwise examples of how to get list, dict other ways
    state_proportions_list = state_proportions.values.tolist()
    # proportion_melt = pd.melt(state_proportions.reset_index(), id_vars='State_Geoid')
    # state_proportion_timeseries = proportion_melt.groupby('State_Geoid')['value'].apply(list)


import geojson
def write_geojson_to_text_json(name: str, file_name: str):
    data = geojson.getgeojson(name)
    geojson.write_text_geojson(data, file_name)


def geojson_text_to_binary(infile: str, outfile: str):
    json = geojson.read_text_geojson(infile)
    geojson.pickle_data_binary(json, outfile)



#### TODO: Other values to calculate: 
## Percent change from the previous year could be neat to see
## as a rate of change graph. Will not be defined for most recent year.  


# blah = get_time_series_data('CAINC1', 1)
# blah = get_county_proportion_test('CAINC1', 1)
# blah = get_state_proportion_test('CAINC1', 1)
# write_geojson_to_text_json('us_county', 'us_county_text_geojson.json')
# geojson_text_to_binary('us_county_text_geojson_citycounty.json', 'us_county_binary_geojson_citycounty.json') 
# blah = geojson.getgeojson('us_county_combined')

table = 'CAGDP1'
# table = 'CAINC1'
linecode = '3'
data = get_time_series_data(table, linecode)
import pdb; pdb.set_trace()
data = get_county_proportion_test(table, linecode)
import pdb; pdb.set_trace()
data = get_state_proportion_test(table, linecode)
import pdb; pdb.set_trace()
