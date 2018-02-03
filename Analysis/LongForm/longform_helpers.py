"""(Helpers) Aggregate long-form data table for all scraped matches."""

import pandas as pd
import datetime


def get_stages(match_id):
    """Return list of stage times based on match id."""
    stages = []
    with open("../Baselines/baselines.csv", "r") as file:
        baselines_df = pd.read_csv(file)
        match_row = baselines_df.loc[baselines_df["match"] == match_id]
        stages.append(match_row["stage_0"].iloc[0])
        stages.append(match_row["stage_1"].iloc[0])
        stages.append(match_row["stage_2"].iloc[0])
        stages.append(match_row["stage_3"].iloc[0])
        stages.append(match_row["stage_4"].iloc[0])
        stages.append(match_row["stage_4_end"].iloc[0])

    return stages


def get_comp_idx(match_id):
    """Return competitive index based on match id."""
    with open("../Baselines/baselines.csv", "r") as file:
        baselines_df = pd.read_csv(file)
        match_row = baselines_df.loc[baselines_df["match"] == match_id]
        return match_row["match_competitive_idx"].iloc[0]


def adjust_for_stages(match_id, match_df):
    """
    Return search vol df based on [Stage 0 : Stage 4] for a given match.

    Also includes other match-level information. Basically, this
    is the feature engineering.
    """

    # remove fullname if necessary; we don't care about this
    if len(match_df.columns) == 4:
        match_df = match_df.drop(match_df.columns[1], axis=1)

    # delete the isPartial column
    # the date can also go away (redundant once we have match id)
    del match_df["isPartial"]

    # create column for match_id, fill with match_id parameter
    pd.options.mode.chained_assignment = None  # default='warn'
    match_df["match_id"] = match_id

    # retrieve list of stage times from baselines.csv
    stages = get_stages(match_id)
    stages = [datetime.datetime.strptime(stage, '%H:%M:%S').time() for stage in stages]

    # a bit of formatting to enable pulling by time intervals
    match_df['time'] = match_df['time'].apply(lambda x: datetime.datetime.strptime(x, '%H:%M:%S').time())
    match_df = match_df.set_index(['time'])

    # preemptively create some indicator columns
    match_df["stage_0_ind"] = 0
    match_df["stage_1_ind"] = 0
    match_df["stage_2_ind"] = 0
    match_df["stage_3_ind"] = 0
    match_df["stage_4_ind"] = 0

    # chop all rows not between stages 0-4
    if len(match_df.loc[stages[0]:stages[5]]) != 0:
        match_df = match_df.loc[stages[0]:stages[5]]
    else:
        # sometimes, we won't have a full stage 4 (limitation of data)
        # in that case, make the 'end' of stage 4 11:59
        stages[5] = datetime.time(23, 59)
        match_df = match_df.loc[stages[0]:stages[5]]

    # mark indicators for individual stages
    match_df["stage_0_ind"].loc[stages[0]:stages[1]] = 1
    match_df["stage_1_ind"].loc[stages[1]:stages[2]] = 1
    match_df["stage_2_ind"].loc[stages[2]:stages[3]] = 1
    match_df["stage_3_ind"].loc[stages[3]:stages[4]] = 1
    match_df["stage_4_ind"].loc[stages[4]:stages[5]] = 1

    # also grab competitive index
    match_df["competitive_idx"] = get_comp_idx(match_id)

    return match_df


def mark_events(home_goals, away_goals, home_yellows,
                away_yellows, home_reds, away_reds, df):
    """Mark events as they occur in a match in the long-form data table."""
    pd.options.mode.chained_assignment = None  # default='warn'

    # iterate through list of event type
    # for each event, pick out the row which contains the occurence of event
    # set that row's event value to be 1 instead of 0
    for goal in home_goals:
        idx = df["home_goal"].loc[df.index >= goal].index[0]
        df["home_goal"].loc[idx] = 1

    for goal in away_goals:
        idx = df["away_goal"].loc[df.index >= goal].index[0]
        df["away_goal"].loc[idx] = 1

    for card in home_yellows:
        idx = df["home_yellow"].loc[df.index >= card].index[0]
        df["home_yellow"].loc[idx] = 1

    for card in away_yellows:
        idx = df["away_yellow"].loc[df.index >= card].index[0]
        df["away_yellow"].loc[idx] = 1

    for card in home_reds:
        idx = df["home_red"].loc[df.index >= card].index[0]
        df["home_red"].loc[idx] = 1

    for card in away_reds:
        idx = df["away_red"].loc[df.index >= card].index[0]
        df["away_red"].loc[idx] = 1

    return df
