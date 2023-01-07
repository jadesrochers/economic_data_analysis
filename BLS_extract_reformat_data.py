#!/usr/bin/env python3

# Use the local python interpreter
# Shell was not going to cut it, bringing python in now
# Need to extract only desired traces from a large file, put that
# into dataframe as single or multiple cols, then re-arrange if needed

import pandas as pd
import numpy as np
from pandas import DataFrame
import sys
import re

inputname=sys.argv[1]
outputname=sys.argv[2]


def print_data(df):
    print(df.loc[:,'LNS11300000'].to_string())
    df.loc[(2022, 'M01'),'LNS11300000']


def load_pivot_save(infile, outfile):
    selected_series_df = pd.read_csv(infile, names=['series','year','month','value'])
    patt = re.compile('^M0*', flags=0)
    selected_series_df['month'] = selected_series_df['month'].map(lambda x: patt.sub('', x, count=0))
    # Convert to correct type to get expected sorting
    selected_series_df['month'] = selected_series_df['month'].astype('int')
    # Use pivot table method to re-arrange the data into series
    pivoted = pd.pivot_table(selected_series_df, values='value', index=['year', 'month'], columns=['series'])
    ones = np.full(shape=(len(pivoted.index)), fill_value=1)
    pivoted['day'] = ones
    pivoted.to_csv(outfile)


load_pivot_save(inputname, outputname)

def load_output():
    series_df = pd.read_csv(outputname)
    # You lose the indexes, but can still readily access the data
    print(series_df.loc[:,'LNS11300000'].to_string())
    series_df.loc[series_df.year == 2022,'LNS11300000']
    series_df.query('year == 2022 & month == \'M01\'').loc[:,'LNS11300000']


