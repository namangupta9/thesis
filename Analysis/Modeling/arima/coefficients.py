"""Plotting distribution of feature coefficients for ARIMAX models."""

import json
import pandas as pd
from dplython import DplyFrame
import matplotlib
matplotlib.use('TkAgg')
from ggplot import (ggplot, geom_density, scale_color_brewer,
                    scale_x_continuous,
                    theme_bw, aes) # noqa: E402


# data frame processing
json_filename = "arima_1.json"
coefficient_dict = json.load(open(json_filename))
coefficients = DplyFrame(pd.DataFrame.from_dict(coefficient_dict,
                                                orient='index'))
coefficients = coefficients.transpose()
folder_name = json_filename.split('.')[0]

for feature in ["home_goal", "away_goal", "home_yellow", "away_yellow",
                "home_red", "home_yellow"]:

    # create a new dataframe for clean plotting purposes
    values_dict = {"significant": coefficients[feature]["significant"],
                   "unsignificant": coefficients[feature]["unsignificant"]}

    df = pd.DataFrame.from_dict(values_dict, orient='index')
    df = df.transpose()
    df = pd.melt(df)    # convert to long-form
    # print(df)

    # data
    p = ggplot(aes(x='value', color='variable'), data=df)
    p += geom_density(fill=True)
    p += scale_x_continuous(limits=(-25, 25))

    # visual
    t = theme_bw()
    t._rcParams['font.size'] = 10
    t._rcParams['font.family'] = 'monospace'
    p += t

    p.save("arima_1/" + feature + ".png")

    # TODO how to create faceted plot of each feature
