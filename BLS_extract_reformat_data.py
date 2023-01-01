#!/usr/bin/python3

# Shell was not going to cut it, bringing python in now
# Need to extract only desired traces from a large file, put that
# into dataframe as single or multiple cols, then re-arrange if needed

import pandas as pd
import numpy as np
from pandas import DataFrame

selected_series_df = pd.read_csv('SelectedSeries.txt', names=['series','year','month','value'])

# Use pivot table method to re-arrange the data into series
# pivot tables can do lots of analysis/aggregating, but here I just
# want to re-arrange.
rearrange = pd.pivot_table(selected_series_df, values='value', index=['year', 'month'], columns=['series'])

# Get data by the series, and then drill down to details
print(rearrange.loc[:,'LNS11300000'].to_string())
rearrange.loc[(2022, 'M01'),'LNS11300000']

# Save it to csv, then try reloading and see what we get
rearrange.to_csv('rearranged_selected_series.txt')

# Then load it to show that this is replicable - but that
# the way the loaded data is indexed is different
series_df = pd.read_csv('rearranged_selected_series.txt')
print(series_df.loc[:,'LNS11300000'].to_string())

# You lose the indexes, but can still readily access the data
series_df.loc[series_df.year == 2022,'LNS11300000']
# Using the query syntax, since I have not done this before
series_df.query('year == 2022 & month == \'M01\'').loc[:,'LNS11300000']


