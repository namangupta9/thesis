"""Helpers for ARIMA Modeling (Time Series Analysis)."""

import json
import pandas as pd
from dplython import sift, X
import matplotlib
matplotlib.use('TkAgg')

from ggplot import (ggplot, geom_line, labs, scale_x_date,
                    theme_gray, aes, date_format)  # noqa: E402


def export_coefficients(coefficients_dict, filename):
    """Write coefficients_dict to JSON in a specified outfile."""
    with open(filename, "w+") as outfile:
        json.dump(coefficients_dict, outfile)


def process_data(longform_df):
    """
    Process data before beginning analysis.

    Only going to focus on the actual match.

    Doesn't make sense to consider the buildup & post-match here, since
    we're focusing on the 'interruptions' that match events have that
    should theoretically cause movement in search volume levels.
    """
    stage_2_df = longform_df >> sift(X.stage_2_ind == 1)
    stage_2_df = stage_2_df.reset_index(drop=True)

    stage_2_df["date"] = stage_2_df.match_id.apply(lambda x:
                                                   "20" + x.split("20")[-1])

    stage_2_df['date_time'] = (stage_2_df['date'].astype(str)
                               + " "
                               + stage_2_df['time'].astype(str))

    stage_2_df['date_time'] = pd.to_datetime(stage_2_df['date_time'],
                                             errors="coerce",
                                             infer_datetime_format=True)
    return stage_2_df


def plot_predictions(date_times, actual_values, predictions,
                     match_id, feature_set_in, filename):
    """
    Plot y-var and save based on specified variables.

    Assumes that df has already been filtered using dplyr's sift mechanism.
    Also assumes that a date has been passed in.
    """
    actual_df = pd.DataFrame()
    actual_df['date_time'] = pd.to_datetime(date_times,
                                            errors="coerce",
                                            infer_datetime_format=True)
    actual_df['search_vol'] = actual_values
    actual_df['match_id'] = "actual" + match_id

    predict_df = pd.DataFrame()
    predict_df['date_time'] = pd.to_datetime(date_times,
                                             errors="coerce",
                                             infer_datetime_format=True)
    predict_df['search_vol'] = list(predictions)
    predict_df['match_id'] = "predictedby_" + str(feature_set_in) + match_id

    plotting_df = pd.concat([actual_df, predict_df], axis=0, ignore_index=True)

    # build layers for plot
    p = ggplot(aes(x='date_time',
                   y='search_vol',
                   group="match_id",
                   color="match_id"), data=plotting_df)
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
    p.save(filename, width=16, height=8)
