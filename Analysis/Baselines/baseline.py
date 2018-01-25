"""Calculate baseline trends data for discrete stages of a matchday."""

import pandas as pd
import datetime

# Stage 0: Buildup (BLD)                        Stage 1 - 2.0 Hours
# Stage 1: Immediate Pre-Match (PRM)            Stage 2 - 2.0 Hours
# Stage 2: Match (MTC)                          Kickoff Time - (Est.) End Time
# Stage 3: Immediate Post-Match (POM)           Stage 2 + 2.0 Hours
# Stage 4: Aftermath (AFT)                      Stage 3 + 2.0 Hours

# Useful: http://www.theanalysisfactor.com/wide-and-long-data/


def calculate_baseline(club_in, match_df):
    """Calculate baseline (average search trend) given matchday stage."""
    # get relevant files as data frames
    match_info = pd.read_csv("../../Match Information/"
                             + club_in + "_matches_2016.csv")

    # get kickoff time
    kickoff_time = match_info.iloc["kickoff_time"]
    kickoff_time_dt = kickoff_time  # convert to datetime

    # estimated end time
    end_time_dt = kickoff_time_dt  # make additions

    # calculate stage interval

    # pull interval data as list

    # calculate average and return a list

    return 0


def get_baselines(final_df, club_in):
    """Run baseline calculations for a given club; wide form data out."""
    # get relevant files as data frames
    search_vol = pd.read_csv("../../Matchday Volumes/"
                             + club_in + "_matchday_2016.csv")
    search_vol['time'] = search_vol.apply(lambda row: row.date[-8:], axis=1)
    search_vol['date'] = search_vol.apply(lambda row: row.date[:-9], axis=1)

    # iterate through all 20 matches
    for match, match_df in search_vol.groupby('date'):

        # for each match, generate a unique identifer: club_match
        match_id = str(club_in) + str(match_df['date'].iloc[0])

        # for each match, calculate baseline for each stage, add to final df TODO
        baseline_results = calculate_baseline(club_in, match_df).append()


# EXECUTION
if __name__ == "__main__":
    # create data frame
    df = pd.DataFrame(columns=['match', 'stage0_base', 'stage1_base',
                               'stage2_base', 'stage3_base', 'stage4_base'])

    # open teams & iterate through all, filling data frame
    teams = []
    with open("../../teams.txt", 'r') as file:
        for c in file:
            names = c.split(', ')
            get_baselines(df, names[0])
