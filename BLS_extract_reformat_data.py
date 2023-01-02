#!/usr/bin/python3

# Shell was not going to cut it, bringing python in now
# Need to extract only desired traces from a large file, put that
# into dataframe as single or multiple cols, then re-arrange if needed

import pandas as pd
import numpy as np
from pandas import DataFrame

def print_data(df):
    print(df.loc[:,'LNS11300000'].to_string())
    df.loc[(2022, 'M01'),'LNS11300000']


def load_and_rearrange(filename):
    selected_series_df = pd.read_csv('SelectedSeries.txt', names=['series','year','month','value'])
    # Use pivot table method to re-arrange the data into series
    rearrange = pd.pivot_table(selected_series_df, values='value', index=['year', 'month'], columns=['series'])
    rearrange.to_csv('rearranged_selected_series.csv')


load_and_rearrange('SelectedSeries.txt')

def load_rearranged():
    series_df = pd.read_csv('rearranged_selected_series.txt')
    # You lose the indexes, but can still readily access the data
    print(series_df.loc[:,'LNS11300000'].to_string())
    series_df.loc[series_df.year == 2022,'LNS11300000']
    series_df.query('year == 2022 & month == \'M01\'').loc[:,'LNS11300000']

