#!/usr/bin/python3

import pandas as pd
from bokeh.models import Tooltip
import bokeh.palettes as bpalettes
from bokeh.plotting import figure, show
import bokeh.palettes as bpalettes
from PIL import Image,ImageDraw
from collections import defaultdict

income_df = pd.read_csv("BEA_CAINC1_converted.csv")
labor_force_df = pd.read_csv("rearranged_selected_series.csv")

def plot_palette(palette):
    pal_len = len(palette)
    width_px = 1000
    test = Image.new(mode="RGBA", size=(width_px, 120))
    for i, hex_col in enumerate(palette):
        newt = Image.new(mode="RGBA", size=(width_px // pal_len, 100), color=hex_col)
        test.paste(newt, (i * width_px // pal_len, 10))
    test.show()


rearrange_medincome = pd.pivot_table(income_df, values='CAINC1-3', index=['TimePeriod'], columns=['GeoName'])

# Use built in pandas plotting methods to show the series
# rearrange_medincome.set_index('TimePeriod').plot(figsize=(16,12), grid=True)

cols = rearrange_medincome.columns
palette = bpalettes.Spectral11
palette_big = bpalettes.viridis(len(cols))
# Generate a palette from a single color specified in RGBA HEX
palette_grn = bpalettes.varying_alpha_palette('#1B6C1F', len(cols), 30, 255)
palette_spec = bpalettes.varying_alpha_palette(bpalettes.Spectral11[0], len(cols), 50, 255)


def plot_many_cols(title, xlabel, ylabel, df, cols, palette):
    data=defaultdict(list)
    # You specify pairs of ('Display Name', '@data_source') for tooltip
    fig_options = dict(
        tooltips=[('County', '@county_name')]
    )
    # A dict data source, the names in this dict then are used to get data
    line_options=dict(
        source=data,
        line_color='color'
    )
    fg = figure(title=title, width = 1000, height = 768, tools="pan, zoom_in, zoom_out, reset, save", **fig_options)
    fg.xaxis.axis_label = xlabel
    fg.yaxis.axis_label = ylabel
    palette = bpalettes.viridis(len(cols))
    data['color'] = palette
    for (col, color) in zip(cols, palette):
        data['xdata'].append(df.index)
        data['lines'].append(df[col])
        data['county_name'].append(col)
        # fg.line(df.index, df[col], legend_label=col, color=color)
    fg.multi_line(xs='xdata', ys='lines', legend_field='county_name', **line_options)
    show(fg)


plot_many_cols('Median Income', 'Year', 'Income, $', rearrange_medincome, cols, palette_grn)
import pdb; pdb.set_trace()
# fg = figure(title="ROC curves", width=800, height=600, tools="pan, reset, save")
# Plot two lines (you can plot as many as you want), these were ROCurves
# fg.line(model_fpr, model_tpr, line_width=1.5, legend_label='model', line_color="blue")
# fg.line(train_fpr, train_tpr, line_width=1.5, legend_label='training', line_color="red")


