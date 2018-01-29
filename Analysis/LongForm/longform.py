"""Aggregate long-form data table for all scraped matches."""

import pandas as pd
import datetime
from ast import literal_eval

# Useful: http://www.theanalysisfactor.com/wide-and-long-data/


def mark_events(home_goals, away_goals, home_yellows,
                away_yellows, home_reds, away_reds, df):
    """Mark events as they occur in a match in the long-form data table."""

    pd.options.mode.chained_assignment = None  # default='warn'

    # iterate through list of event type
    # for each event, pick out the row which contains the occurence of that match event
    # set that row's event value to be 1 instead of 0

    for goal in home_goals:
        idx = df["home_goal"].loc[df.index >= str(goal)].index[0]
        df["home_goal"].loc[idx] = 1

    for goal in away_goals:
        idx = df["away_goal"].loc[df.index >= str(goal)].index[0]
        df["away_goal"].loc[idx] = 1

    for card in home_yellows:
        idx = df["home_yellow"].loc[df.index >= str(card)].index[0]
        df["home_yellow"].loc[idx] = 1

    for card in away_yellows:
        idx = df["away_yellow"].loc[df.index >= str(card)].index[0]
        df["away_yellow"].loc[idx] = 1

    for card in home_reds:
        idx = df["home_red"].loc[df.index >= str(card)].index[0]
        df["home_red"].loc[idx] = 1

    for card in away_reds:
        idx = df["away_red"].loc[df.index >= str(card)].index[0]
        df["away_red"].loc[idx] = 1

    return df


def get_match_info(club_in, match_df, match_id):
    """Gather match information for every 4 mins (as per search data freq.)."""

    # get relevant match information
    match_info = pd.read_csv("../../Match Information/"
                             + club_in + "_matches_2016.csv")
    match_info = match_info[match_info["date"] == match_df['date'].iloc[0]]
    match_df = match_df.set_index(['time'])

    # remove fullname if necessary; we don't care about this
    if len(match_df.columns) == 4:
        match_df = match_df.drop(match_df.columns[1], axis=1)

    # delete the isPartial column, and the date can also go away (redundant once we have match id)
    del match_df["isPartial"]
    del match_df["date"]

    # rename the search volume column header to be non team-specific
    old_name = match_df.columns[-1]
    rename_dict = {old_name:"shorthand_search_vol"}
    match_df = match_df.rename(columns=rename_dict)

    # create column for match_id, fill with match_id parameter
    match_df["match_id"] = match_id

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
                 "home_yellow", "away_yellow", "home_red", "away_red"]
    match_df = match_df[col_order]
    return match_df


def get_club_info(club_in):
    """Run baseline calculations for a given club; wide form data out."""
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
        match_id = str(club_in) + str(match_df['date'].iloc[0])

        # for each match, gather and organize information
        result_df = get_match_info(club_in, match_df, match_id)
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

    # TODO
    # this file is so damn long...can we shorten it? maybe not get the entire day's data?
