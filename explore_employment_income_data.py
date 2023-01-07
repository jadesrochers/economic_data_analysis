#!/usr/bin/python3

import pandas as pd
from bokeh.models import Tooltip
import bokeh.palettes as bpalettes
from bokeh.plotting import figure, show
import bokeh.palettes as bpalettes
from PIL import Image,ImageDraw
from collections import defaultdict

income_df = pd.read_csv("BEA_CAINC1_converted.csv")
employment_rate_df = pd.read_csv("BLS_LN_Rate_Series.csv")
employment_level_df = pd.read_csv("BLS_LN_Level_Series.csv")

# Test out your color palette by doing a simple plot of it.
def plot_palette(palette):
    pal_len = len(palette)
    width_px = 1000
    test = Image.new(mode="RGBA", size=(width_px, 120))
    for i, hex_col in enumerate(palette):
        newt = Image.new(mode="RGBA", size=(width_px // pal_len, 100), color=hex_col)
        test.paste(newt, (i * width_px // pal_len, 10))
    test.show()

# Use built in pandas plotting methods to show the series
# rearrange_medincome.set_index('TimePeriod').plot(figsize=(16,12), grid=True)


# Median income data, re-arrange to prepare for plot
rearrange_medincome = pd.pivot_table(income_df, values='CAINC1-3', index=['TimePeriod'], columns=['GeoName'])
cols_inc = rearrange_medincome.columns
palette_inc = bpalettes.viridis(len(cols_inc))


# Employment rate dataframe; format is already pretty much as needed
cols_emp_rate = employment_rate_df.drop(columns = ['year', 'month', 'day']).columns
# Generate a palette from a single color specified in RGBA HEX
palette_emp_grn = bpalettes.varying_alpha_palette('#1B6C1F', len(cols_emp_rate), 30, 255)


# Employment level data
cols_emp_level = employment_level_df.drop(columns = ['year', 'month', 'day']).columns
palette_emp_spec = bpalettes.varying_alpha_palette(bpalettes.Spectral11[0], len(cols_emp_level), 30, 255)


def tabulate_income_data(df, cols_inc, palette):
    data=defaultdict(list)
    data['color'] = palette
    for (col, color) in zip(cols_inc, palette):
        data['xdata'].append(df.index)
        data['lines'].append(df[col])
        data['county_name'].append(col)
        # fg.line(df.index, df[col], legend_label=col, color=color)
    return data

def options_income_data(data_source):
    fig_options = dict(
        tooltips=[('County', '@county_name')]
    )
    # A dict data source, the names in this dict then are used to get data
    line_options=dict(
        source=data_source,
        line_color='color',
        legend_field='county_name'
    )
    return fig_options, line_options


def tabulate_employment_data(df, cols_emp_rate, palette):
    data=defaultdict(list)
    data['color'] = palette
    # Need to convert the month, otherwise should work
    date_input = df.loc[:,('year','month','day')]
    for (col, color) in zip(cols_emp_rate, palette):
        data['xdata'].append(pd.to_datetime(date_input))
        data['lines'].append(df[col])
        data['series_id'].append(col)
        # fg.line(df.index, df[col], legend_label=col, color=color)
    return data

def options_employment_data(data_source):
    fig_options = dict(
        tooltips=[('Series', '@series_id')],
        x_axis_type='datetime'
    )
    # A dict data source, the names in this dict then are used to get data
    line_options=dict(
        source=data_source,
        line_color='color',
        legend_field='series_id'
    )
    return fig_options, line_options


def plot_many_cols(title, xlabel, ylabel, fig_options, line_options):
    fg = figure(title=title, width = 1000, height = 768, tools="pan, zoom_in, zoom_out, reset, save", **fig_options)
    fg.xaxis.axis_label = xlabel
    fg.yaxis.axis_label = ylabel
    fg.multi_line(xs='xdata', ys='lines', **line_options)
    show(fg)


income_data = tabulate_income_data(rearrange_medincome, cols_inc, palette_inc)
fig_opts_inc, line_opts_inc = options_income_data(income_data)
# You specify pairs of ('Display Name', '@data_source') for tooltip

emp_rate_data = tabulate_employment_data(employment_rate_df, cols_emp_rate, palette_emp_grn)
fig_opts_rate, line_opts_rate = options_employment_data(emp_rate_data)

emp_level_data = tabulate_employment_data(employment_level_df, cols_emp_level, palette_emp_spec)
fig_opts_level, line_opts_level = options_employment_data(emp_level_data)

import time
plot_many_cols('Median Income', 'Year', 'Income, $', fig_opts_inc, line_opts_inc)
time.sleep(0.5)
plot_many_cols('Participation and Unemployment Rates %', 'Year, Month', 'Pct, %', fig_opts_rate, line_opts_rate)
time.sleep(0.5)
plot_many_cols('Unemployment Levels', 'Year, Month', 'Number of', fig_opts_level, line_opts_level)

