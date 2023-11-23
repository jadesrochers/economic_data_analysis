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
always_use = ['geo_id', 'area_name']
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


def create_sub_dicts(use_columns, df):
    # Put this in a function because otherwise the lambda has no scope
    # to find the use_columns variable
    return df.groupby('geo_id').apply(lambda x: x[use_columns].to_dict(orient='records')).to_dict()


def get_time_series_data(number: str) -> Dict[str, List[Dict[str, Union[int, float]]]]:
    import pdb; pdb.set_trace()
    table_path = find_datafile(number)
    raw_data = pd.read_csv(table_path)
    raw_data = raw_data.rename(columns=rename_mappings, errors='raise')
    data_series_pattern = re.compile(pop_counts_re)
    df, use_columns = find_data_cols(raw_data, data_series_pattern)

    # Convert data if needed, and make column to manipulate
    for col in use_columns:
        if df.dtypes[col] == np.dtype('str'):
            raw_data[col] = raw_data[col].map(lambda x: default_value if  x.startswith('(NA)') else locale.atof(x))

    return create_sub_dicts(use_columns, df)

