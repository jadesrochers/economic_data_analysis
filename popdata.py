from pathlib import Path
import pandas as pd
from pandas import DataFrame
import json 
import locale
import re
from typing import Dict, List, Union, Pattern, Tuple
import numpy as np

locale.setlocale(locale.LC_ALL, '')
default_value = 0.0

pop_counts_re = 'Resident_population_complete_count_(.*)'
data_path = Path('./POPdata')
always_use = ['geo_id']
rename_mappings = {'GEO_ID': 'geo_id', 'Area_name': 'area_name'}


def find_datafile(number: str):
    table_path = list(data_path.glob('POP{number}.csv.0'.format(number=number)))[0]
    return table_path



def find_data_cols(raw_data: DataFrame, pattern: Pattern) -> Tuple[DataFrame, List[str]]:
    colnames = raw_data.columns
    remove_columns = []
    use_columns = []
    for colname in colnames:
        if colname in always_use:
            use_columns.append(colname)
        elif not pattern.search(colname):
            remove_columns.append(colname)
        else:
            extract_year = pattern.search(colname).group(1)
            use_columns.append(extract_year)
            raw_data = raw_data.rename(columns={colname: extract_year}, errors='raise')
    return raw_data.drop(columns = remove_columns), use_columns


def get_years_from_names(raw_data: DataFrame, pattern: Pattern) -> List[int]:
    colnames = raw_data.columns
    years = []
    for colname in colnames:
        if pattern.search(colname):
            year = pattern.search(colname).group(1)
            years.append(locale.atof(year))
    return years


def get_all_years(number: str) -> List[int]:
    table_path = find_datafile(number)
    raw_data = pd.read_csv(table_path)
    data_series_pattern = re.compile(pop_counts_re)
    return get_years_from_names(raw_data, data_series_pattern)


def create_sub_dicts(use_columns, df):
    # Put this in a function because otherwise the lambda has no scope
    # to find the use_columns variable
    return df.groupby('geo_id').apply(lambda x: x[use_columns].to_dict(orient='records')).to_dict()


def get_time_series_data(number: str) -> Dict[str, List[Dict[str, Union[int, float]]]]:
    table_path = find_datafile(number)
    raw_data = pd.read_csv(table_path)
    raw_data = raw_data.rename(columns=rename_mappings, errors='raise')
    data_series_pattern = re.compile(pop_counts_re)
    df, use_columns = find_data_cols(raw_data, data_series_pattern)
    colname = 'value'
    df = df.melt(id_vars=['geo_id'], var_name='year', value_name='value')
    # Convert data if needed, and make column to manipulate
    if df.dtypes[colname] == np.dtype('str'):
        raw_data[colname] = raw_data[colname].map(lambda x: default_value if  x.startswith('(NA)') else locale.atof(x))
    return df.groupby('geo_id').apply(lambda x: x[['year', 'value']].to_dict(orient='records')).to_dict()


def drop_states(pattern: Pattern, df: DataFrame, colname: str):
    return df[colname].map(lambda x: bool(pattern.match(x)))


def get_county_proportion(number: str) -> Dict[str, List[Dict[str, Union[int, float]]]]:
    state_convert_regex = re.compile('^0500000US[0-9]{2}')
    state_raw_regex = re.compile('^0[04]00000US[0-9]{2}.*')
    table_path = find_datafile(number)
    raw_data = pd.read_csv(table_path)
    raw_data = raw_data.rename(columns=rename_mappings, errors='raise')
    raw_data['dropper'] = drop_states(state_raw_regex, raw_data, 'geo_id')
    raw_data = raw_data.drop(raw_data[raw_data.dropper].index)
    data_series_pattern = re.compile(pop_counts_re)
    df, use_columns = find_data_cols(raw_data, data_series_pattern)
    colname = 'value'
    df = df.melt(id_vars=['geo_id'], var_name='year', value_name='value')
    # Convert data if needed, and make column to manipulate
    if df.dtypes[colname] == np.dtype('str'):
        df[colname] = df[colname].map(lambda x: default_value if  x.startswith('(NA)') else locale.atof(x))
    df['state_geoid'] = df['geo_id'].map(lambda x: state_convert_regex.search(x).group(0));
    # Get sum for the state for each county/year to do proportion calc
    county_year_sum = df.groupby(['state_geoid', 'year'])['value'].transform('sum')
    county_year_pct = round(100 * (df['value'] / county_year_sum), 2)
    year_sum = df.groupby(['year'])['value'].transform('sum')
    df['county_pct'] = county_year_pct
    pivoted_county_proportion = pd.pivot_table(df, index='geo_id', columns='year', aggfunc='sum', values='county_pct', fill_value=0.0)
    pivot_melt = pd.melt(pivoted_county_proportion.reset_index(), id_vars='geo_id')
    return pivot_melt.groupby('geo_id').apply(lambda x: x[['year', 'value']].to_dict(orient='records')).to_dict()


def get_state_proportion(number: str) -> Dict[str, List[Dict[str, Union[int, float]]]]:
    state_convert_regex = re.compile('^0500000US[0-9]{2}')
    state_raw_regex = re.compile('^0[04]00000US[0-9]{2}.*')
    table_path = find_datafile(number)
    raw_data = pd.read_csv(table_path)
    raw_data = raw_data.rename(columns=rename_mappings, errors='raise')
    raw_data['dropper'] = drop_states(state_raw_regex, raw_data, 'geo_id')
    raw_data = raw_data.drop(raw_data[raw_data.dropper].index)
    data_series_pattern = re.compile(pop_counts_re)
    df, use_columns = find_data_cols(raw_data, data_series_pattern)
    colname = 'value'
    df = df.melt(id_vars=['geo_id'], var_name='year', value_name='value')
    # Convert data if needed, and make column to manipulate
    if df.dtypes[colname] == np.dtype('str'):
        df[colname] = df[colname].map(lambda x: default_value if  x.startswith('(NA)') else locale.atof(x))
    df['state_geoid'] = df['geo_id'].map(lambda x: state_convert_regex.search(x).group(0));
    pivoted_state_sum = pd.pivot_table(df, index='state_geoid', columns='year', aggfunc='sum', values='value', fill_value=0.0)
    state_proportions = pivoted_state_sum.div(pivoted_state_sum.sum(axis=0), axis=1)
    pivot_melt = pd.melt(state_proportions.reset_index(), id_vars='state_geoid')
    pivot_melt['value'] = round(pivot_melt['value'] * 100, 2)
    return pivot_melt.groupby('state_geoid').apply(lambda x: x[['year', 'value']].to_dict(orient='records')).to_dict()


