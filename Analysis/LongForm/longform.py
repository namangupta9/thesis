"""Aggregate long-form data table for all scraped matches."""

import pandas as pd
import datetime
from ast import literal_eval
from longform_helpers import mark_events, adjust_for_stages


def get_match_info(club_in, match_df, match_id, date):
    """
    Feature Engineering.

    What could explain search vol differences? Indicate them in df.

    Need to be backwards-looking features; when watching a football match,
    fans don't know what the future outcome or events will be. Hence, all
    these features need to be known to the fan at the time that the feature
    is indicated in the model.

    For example, can't include "Total Goals" since fans don't know that info
    as they're watching / searching the match live. A cumulative measure would
    be more appropriate - how many scored 'until this point'?

    Also important not to be too specific, to avoid overfitting risk.

    Selected Features:
    - Home & Away Goal Timing
    - Home & Away Booking Timing
    - Competitive Index of Match (|Away Win Odds - Home Win Odds|)
    - Cumulative Total Goals (Self explanatory)
    - Cumulative Goal Differential (How "close" is the match?)
    - Man down? (There's been at least 1 red card)
    - Match Week (Might affect buildup & match importance)
    - Upset In Progress? (Club w/ Lower Winning Odds is Actually Winning)

    """

    # get relevant match information
    match_info = pd.read_csv("../../Match Information/"
                             + club_in + "_matches_2016.csv")
    match_info = match_info[match_info["date"] == date]

    # rename the search volume column header to be non team-specific
    old_name = match_df.columns[-8]
    rename_dict = {old_name:"shorthand_search_vol"}
    match_df = match_df.rename(columns=rename_dict)

    # create a column for each type of match event; default value is 0
    match_df["home_goal"] = 0
    match_df["away_goal"] = 0
    match_df["home_yellow"] = 0
    match_df["away_yellow"] = 0
    match_df["home_red"] = 0
    match_df["away_red"] = 0

    # pull out the timings of bookings & goals
    home_goals_actual = match_info["home_goals"].apply(lambda x: literal_eval(x)).iloc[0]
    away_goals_actual = match_info["away_goals"].apply(lambda x: literal_eval(x)).iloc[0]
    home_yellows_actual = match_info["home_yellows"].apply(lambda x: literal_eval(x)).iloc[0]
    away_yellows_actual = match_info["away_yellows"].apply(lambda x: literal_eval(x)).iloc[0]
    home_reds_actual = match_info["home_reds"].apply(lambda x: literal_eval(x)).iloc[0]
    away_reds_actual = match_info["away_reds"].apply(lambda x: literal_eval(x)).iloc[0]

    # convert into datetime.time objects instead of strings
    home_goals_actual = [datetime.datetime.strptime(x, '%H:%M:%S').time() for x in home_goals_actual]
    away_goals_actual = [datetime.datetime.strptime(x, '%H:%M:%S').time() for x in away_goals_actual]
    home_yellows_actual = [datetime.datetime.strptime(x, '%H:%M:%S').time() for x in home_yellows_actual]
    away_yellows_actual = [datetime.datetime.strptime(x, '%H:%M:%S').time() for x in away_yellows_actual]
    home_reds_actual = [datetime.datetime.strptime(x, '%H:%M:%S').time() for x in home_reds_actual]
    away_reds_actual = [datetime.datetime.strptime(x, '%H:%M:%S').time() for x in away_reds_actual]

    # mark match events
    match_df = mark_events(home_goals_actual,
                           away_goals_actual,
                           home_yellows_actual,
                           away_yellows_actual,
                           home_reds_actual,
                           away_reds_actual,
                           match_df)

    # finalize the order of the columns & return
    col_order = ["match_id", "shorthand_search_vol", "home_goal", "away_goal",
                 "home_yellow", "away_yellow", "home_red", "away_red",
                 "stage_0_ind", "stage_1_ind", "stage_2_ind", "stage_3_ind",
                 "stage_4_ind", "competitive_idx"]

    match_df = match_df[col_order]
    return match_df


def get_club_info(club_in):
    # get relevant files as data frames
    search_vol = pd.read_csv("../../Matchday Volumes/"
                             + club_in + "_matchday_2016.csv")
    search_vol['time'] = search_vol.apply(lambda row: row.date[-8:], axis=1)
    search_vol['date'] = search_vol.apply(lambda row: row.date[:-9], axis=1)

    # empty container (to store final values at end)
    match_results = []

    # iterate through all 20 matches
    for match, match_df in search_vol.groupby('date'):

        # for each match, generate a unique identifer: club_match
        date = match_df['date'].iloc[0]
        match_id = str(club_in) + str(date)

        # use match_id to find appropriate time range for analysis
        # as well as indicate stages in data frame (dummy vars)
        match_df = adjust_for_stages(match_id, match_df)

        # for each match, gather and organize information
        result_df = get_match_info(club_in, match_df, match_id, date)
        match_results.append(result_df)


    # create & merge data frame from collection of individual data frames
    df = pd.concat(match_results)
    print "Finished: " + club_in
    return df


# EXECUTION
if __name__ == "__main__":
    # open teams & iterate through all, collecting data frames
    teams = []
    with open("../../teams.txt", 'r') as file:
        for c in file:
            names = c.split(', ')
            teams.append(get_club_info(names[0]))

    # concatenate all data frames together and export
    df = pd.concat(teams)
    df.to_csv("longform.csv")
    print "Exported: longform.csv"
