"""Plotting distribution of feature coefficients for ARIMAX models."""

import json
import pandas as pd
from dplython import DplyFrame
import matplotlib
matplotlib.use('TkAgg')
from ggplot import (ggplot, scale_color_brewer, geom_histogram,
                    scale_x_continuous, facet_wrap, labs, ggtitle,
                    scale_y_continuous, theme_gray,
                    aes, geom_boxplot) # noqa: E402


# data frame processing; creating a master df for faceting plots
json_filename = "arima_1.json"
coefficient_dict = json.load(open(json_filename))
coefficients = DplyFrame(pd.DataFrame.from_dict(coefficient_dict,
                                                orient='index'))
coefficients = coefficients.transpose()
folder_name = json_filename.split('.')[0]

dfs_to_concat = []
for feature in ["home_goal", "away_goal", "home_yellow", "away_yellow",
                "home_red", "away_red"]:

    # create a new long-form dataframe for clean plotting purposes
    values_dict = {"significant": coefficients[feature]["significant"],
                   "insignificant": coefficients[feature]["unsignificant"]}
    df = pd.DataFrame.from_dict(values_dict, orient='index')
    df = df.transpose()
    df = pd.melt(df)
    df['feature'] = feature
    dfs_to_concat.append(df)

master_df = pd.concat(dfs_to_concat)

# visuals
t = theme_gray()
t._rcParams['font.size'] = 10
t._rcParams['font.family'] = 'monospace'

# histogram
p = ggplot(aes(x='value', fill='variable', color='variable'),
           data=master_df)
p += geom_histogram(bins=25, alpha=0.5)
p += scale_x_continuous(limits=(-25, 25))
p += ggtitle("sarimax coefficient magnitude distribution")
p += facet_wrap("feature", ncol=3, scales="free")
p += labs(x=" ", y=" ")
p += t
p.save("arima_1/" + "histogram.png")

# boxplot
p = ggplot(aes(x='variable', y='value'), data=master_df)
p += geom_boxplot()
p += scale_y_continuous(limits=(-25, 25))
p += ggtitle("sarimax coefficient magnitudes")
p += facet_wrap("feature", ncol=3)
p += labs(x=" ", y=" ")
p += t
p.save("arima_1/" + "boxplot.png")
