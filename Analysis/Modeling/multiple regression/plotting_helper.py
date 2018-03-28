"""Helper to use ggplot to plot multiple regression predictions."""

import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
from ggplot import *
from dplython import *


def plot_match(df, x_var, y_var, match_id, filename_out):
    """Plot and save based on specified variables."""
    pass


def plot_match_and_preds(df, x_var, y_var, match_id, filename_out):
    """Plot y as well as y-hat (actual vs. prediction) for a given match."""
    pass


def plot_match_range():
    """Plot multiple matches at once."""
    pass
