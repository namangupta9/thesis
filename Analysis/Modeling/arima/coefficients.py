"""Plotting distribution of feature coefficients for ARIMAX models."""

import json
import pandas as pd
from dplython import DplyFrame
import matplotlib
matplotlib.use('TkAgg')
from ggplot import (ggplot, geom_density, scale_color_brewer,
                    scale_x_continuous, facet_wrap, labs, ggtitle,
                    theme_gray, aes) # noqa: E402


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

# data
p = ggplot(aes(x='value', color='variable'), data=master_df)
p += geom_density(fill=True)
p += scale_x_continuous(limits=(-25, 25))
p += scale_color_brewer(type='qual', palette=3)
p += ggtitle("sarimax coefficient magnitude distributions")
p += facet_wrap("feature", ncol=3)

# visual
t = theme_gray()
t._rcParams['font.size'] = 10
t._rcParams['font.family'] = 'monospace'
p += t

p.save("arima_1/" + "faceted.png")

# TODO how to create faceted plot of each feature
