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

name = 'Resident_population_complete_count_1930'
pop_counts = 'Resident_population_complete_count_.*'
data_path = Path('./POPdata')


def find_datafile(number: str):
    table_path = list(data_path.glob('POP{number}.csv.0'.format(table=table)))[0]
    return table_path


def find_data_cols(raw_data: DataFrame, pattern: Pattern) -> Tuple(DataFrame, List[str]):
    colnames = raw_data.columns
    remove_columns = []
    use_columns = []
    for colname in colnames:
        if not pattern.search(colname):
            remove_columns.append(colname)
        else:
            use_columns.append(colname)
    return raw_data.drop(columns = remove_columns), use_columns


def get_time_series_data(number: str) -> Dict[str, List[Dict[str, Union[int, float]]]]:
    table_path = find_datafile(number)
    raw_data = pd.read_csv(table_path)
    data_series_pattern = re.compile(pop_counts)
    df, use_columns = find_data_cols(raw_data, data_series_pattern)

    # Convert data if needed, and make column to manipulate
    if raw_data.dtypes[data_series] == np.dtype('str'):
        raw_data['Values'] = raw_data[data_series].map(lambda x: default_value if  x.startswith('(NA)') else locale.atof(x))
    else:
        raw_data['Values'] = raw_data[data_series]

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


