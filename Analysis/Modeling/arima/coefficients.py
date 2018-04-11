"""Plotting distribution of feature coefficients for ARIMAX models."""

import json
import pandas as pd
from dplython import DplyFrame
import matplotlib
matplotlib.use('TkAgg')
from ggplot import (ggplot, geom_histogram, labs, scale_x_continuous,
                    theme_gray, aes, date_format)  # noqa: E402


# data frame processing
json_filename = "arima_1.json"
coefficient_dict = json.load(open(json_filename))
coefficients = DplyFrame(pd.DataFrame.from_dict(coefficient_dict,
                                                orient='index'))
coefficients = coefficients.transpose()
folder_name = json_filename.split('.')[0]

for feature in ["home_goal", "away_goal", "home_yellow", "away_yellow",
                "home_red", "home_yellow"]:

    # data
    p = ggplot(aes(x=feature), data=coefficients)
    p += geom_histogram(binwidth=0.5)
    p += scale_x_continuous(limits=(-10, 10))

    # visual
    t = theme_gray()
    t._rcParams['font.size'] = 8
    t._rcParams['font.family'] = 'monospace'
    p += t

    p.save("arima_1/" + feature + ".png")

    # TODO how to create faceted plot of each feature
