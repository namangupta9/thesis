"""Helper to use ggplot to plot ARIMA predictions."""

import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
from ggplot import (ggplot, geom_line, labs, scale_x_date,
                    theme_gray, aes, date_format)


def plot_matches(df_in, date, filename_out, x_var='date_time',
                 y_var="shorthand_search_vol"):
    """
    Plot y-var and save based on specified variables.

    Assumes that df has already been filtered using dplyr's sift mechanism.
    Also assumes that a date has been passed in.
    """
    # basic data processing for viz
    df_in['date_time'] = date + " " + df_in['time'].astype(str)
    df_in['date_time'] = pd.to_datetime(df_in['date_time'],
                                        errors="coerce",
                                        infer_datetime_format=True)

    # build layers for plot
    p = ggplot(aes(x=x_var,
                   y=y_var,
                   group="match_id",
                   color="match_id"), data=df_in)
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
