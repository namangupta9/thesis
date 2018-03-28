"""Helper to use ggplot to plot multiple regression predictions."""

import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
from ggplot import (ggplot, geom_line, labs, scale_x_date,
                    theme_gray, aes, date_format)


def plot_matches(df, filename_out, x_var='date_time',
                 y_var="shorthand_search_vol"):
    """
    Plot y-var and save based on specified variables.

    Assumes that df has already been filtered using dplyr's sift mechanism.
    """
    # basic data processing for viz
    df["date"] = df.match_id.apply(lambda x: "20" + x.split("20")[-1])
    df['date_time'] = df['date'].astype(str) + " " + df['time'].astype(str)
    df['date_time'] = pd.to_datetime(df['date_time'],
                                     errors="coerce",
                                     infer_datetime_format=True)

    # build layers for plot
    p = ggplot(aes(x=x_var,
                   y=y_var,
                   group="match_id",
                   color="match_id"), data=df)
    p += geom_line()

    # informative
    p += labs(x="time (gmt)", y="search volume (scaled to 100)")
    # p += ggtitle("man. city (h) vs. chelsea (a)\naug. 8 '16, etihad stadium")
    p += scale_x_date(labels=date_format("%H:%M:%S"), date_breaks="30 minutes")

    # visual
    t = theme_gray()
    t._rcParams['font.size'] = 8
    t._rcParams['font.family'] = 'monospace'
    p += t

    # done
    p.save(filename_out, width=16, height=8)
