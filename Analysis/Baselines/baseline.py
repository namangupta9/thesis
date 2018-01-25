"""Calculate baseline trends data for discrete stages of a matchday."""

import pandas as pd
import datetime

# Stage 0: Buildup (BLD)                        Stage 1 - 2.0 Hours
# Stage 1: Immediate Pre-Match (PRM)            Stage 2 - 2.0 Hours
# Stage 2: Match (MTC)                          Kickoff Time - (Est.) End Time
# Stage 3: Immediate Post-Match (POM)           Stage 2 + 2.0 Hours
# Stage 4: Aftermath (AFT)                      Stage 3 + 2.0 Hours

# Useful: http://www.theanalysisfactor.com/wide-and-long-data/


def calculate_baseline(club_in, matchweek_in, stage_in):
    """Calculate baseline (average search trend) given matchday stage."""
    # get relevant files as data frames
    match_info = pd.read_csv("../../Match Information/"
                             + club_in + "_matches_2016.csv")

    search_vol = pd.read_csv("../../Matchday Volumes/"
                             + club_in + "_matchday_2016.csv")

    # get kickoff time
    kickoff_time = match_info.iloc[matchweek_in]["kickoff_time"]
    kickoff_time_dt = kickoff_time  # convert to datetime

    # estimated end time
    end_time_dt = kickoff_time_dt  # make additions

    # calculate stage interval

    # pull interval data as list

    # calculate average and return

    return 0


def get_baselines(club_in):
    """Run baseline calculations for all clubs."""


# execution
# wide & long-form data
if __name__ == "__main__":
    # open teams & iterate through all
    teams = []
    with open("../../teams.txt", 'r') as file:
        for c in file:
            names = c.split(', ')
            get_baselines(names[0])
