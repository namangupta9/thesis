"""Calculate baseline trends data for discrete stages of a matchday."""

import pandas as pd
import datetime
from datetime import time
import math

# Stage 0: Buildup (BLD)                        Stage 1 - 2.0 Hours
# Stage 1: Immediate Pre-Match (PRM)            Stage 2 - 2.0 Hours
# Stage 2: Match (MTC)                          Kickoff Time - (Est.) End Time
# Stage 3: Immediate Post-Match (POM)           Stage 2 + 2.0 Hours
# Stage 4: Aftermath (AFT)                      Stage 3 + 2.0 Hours

# Useful: http://www.theanalysisfactor.com/wide-and-long-data/

def get_competitive_index(match_info_df):
    """Return the 'competitive index' of a match."""
    # competitive index defined as |home win - away win|
    return math.fabs(float(match_info_df["avg_a_odds"].iloc[0]) -
                     float(match_info_df["avg_h_odds"].iloc[0]))


def calculate_baseline(club_in, match_df):
    """Calculate baseline (average search trend) for a given match."""
    # get relevant files as data frames; pick out individual match
    match_info = pd.read_csv("../../Match Information/"
                             + club_in + "_matches_2016.csv")
    match_info = match_info[match_info["date"] == match_df['date'].iloc[0]]

    # get kickoff time, convert to datetime to get stage timings
    kickoff_time = match_info["kickoff_time"].iloc[0]
    kickoff_time_dt = datetime.datetime.strptime(kickoff_time, '%H:%M:%S')

    # estimated end time
    # (kickoff + 90' + 6' est. total stoppage time + 15' Halftime)
    end_time_dt = kickoff_time_dt + datetime.timedelta(minutes=90)
    end_time_dt += datetime.timedelta(minutes=15)
    end_time_dt += datetime.timedelta(minutes=6)

    # calculate stage intervals
    stage_0_start = (kickoff_time_dt - datetime.timedelta(minutes=240)).time()
    stage_1_start = (kickoff_time_dt - datetime.timedelta(minutes=120)).time()
    stage_2_start = kickoff_time_dt.time()
    stage_3_start = end_time_dt.time()
    stage_4_start = (end_time_dt + datetime.timedelta(minutes=120)).time()
    stage_4_end = (end_time_dt + datetime.timedelta(minutes=240)).time()

    # a bit more data frame formatting to enable pulling by time intervals
    pd.options.mode.chained_assignment = None  # default='warn'
    match_df['time'] = match_df['time'].apply(lambda x: datetime.datetime.strptime(x, '%H:%M:%S').time())
    match_df = match_df.set_index(['time'])

    # remove fullname if necessary; we don't care about this
    if len(match_df.columns) == 4:
        match_df = match_df.drop(match_df.columns[1], axis=1)

    # finally, calculate baselines
    results = {}
    results["stage_0"] = stage_0_start
    results["stage_1"] = stage_1_start
    results["stage_2"] = stage_2_start
    results["stage_3"] = stage_3_start
    results["stage_4"] = stage_4_start
    results["stage_4_end"] = stage_4_end
    results["stage_0_base"] = match_df.loc[stage_0_start : stage_1_start].iloc[:, -2].mean()
    results["stage_1_base"] = match_df.loc[stage_1_start : stage_2_start].iloc[:, -2].mean()
    results["stage_2_base"] = match_df.loc[stage_2_start : stage_3_start].iloc[:, -2].mean()
    results["stage_3_base"] = match_df.loc[stage_3_start : stage_4_start].iloc[:, -2].mean()

    # format the precision of results
    results["stage_0_base"] = float(format(results["stage_0_base"], '.2f'))
    results["stage_1_base"] = float(format(results["stage_1_base"], '.2f'))
    results["stage_2_base"] = float(format(results["stage_2_base"], '.2f'))
    results["stage_3_base"] = float(format(results["stage_3_base"], '.2f'))

    # sometimes, the match is too late to collect stage 4 data (limitation)
    if len(match_df.loc[stage_4_start : stage_4_end].iloc[:, -2]) > 0:
        results["stage_4_base"] = match_df.loc[stage_4_start : stage_4_end].iloc[:, -2].mean()
        results["stage_4_base"] = float(format(results["stage_4_base"], '.2f'))
    else:
        results["stage_4_base"] = None

    # grab competitive index & format precision
    results["match_competitive_idx"] = get_competitive_index(match_info)
    results["match_competitive_idx"] = float(format(results["match_competitive_idx"], '.2f'))

    return results


def get_baselines(club_in):
    """Run baseline calculations for a given club; wide form data out."""
    # get relevant files as data frames
    search_vol = pd.read_csv("../../Matchday Volumes/"
                             + club_in + "_matchday_2016.csv")
    search_vol['time'] = search_vol.apply(lambda row: row.date[-8:], axis=1)
    search_vol['date'] = search_vol.apply(lambda row: row.date[:-9], axis=1)

    # empty container (to store final values at end)
    match_results = []

    # iterate through all 20 matches
    match_wk = 0
    for match, match_df in search_vol.groupby('date'):

        # for each match, generate a unique identifer: club_match
        match_id = str(club_in) + str(match_df['date'].iloc[0])

        # for each match, calculate baseline for each stage
        baseline_results = calculate_baseline(club_in, match_df)
        baseline_results["match"] = match_id
        baseline_results["matchweek"] = match_wk
        match_results.append(baseline_results)
        match_wk += 1

    # create & merge data frame from collection of individual dicts
    # with final dictionary referenced from main execution
    df = pd.DataFrame(match_results)
    print "Finished: " + club_in
    return df


# EXECUTION
if __name__ == "__main__":
    # open teams & iterate through all, collecting data frames
    teams = []
    with open("../../teams.txt", 'r') as file:
        for c in file:
            names = c.split(', ')
            teams.append(get_baselines(names[0]))

    # concatenate all data frames together and export
    df = pd.concat(teams)
    df.to_csv("baselines.csv")
    print "Exported: baselines.csv"
