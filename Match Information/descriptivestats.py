"""Generate descriptive statistics for match events."""

import pandas as pd
import glob
from ast import literal_eval
from dplython import DplyFrame, sift, X


# process + load data frames for individual clubs' info into a container
csv_files = glob.glob("*.csv")
df_container = []
for club_csv in csv_files:
    df = pd.read_csv(club_csv)

    # get count of # occurrences
    home_goals = df.home_goals.apply(lambda x: len(literal_eval(x)))
    away_goals = df.away_goals.apply(lambda x: len(literal_eval(x)))
    home_yellows = df.home_yellows.apply(lambda x: len(literal_eval(x)))
    away_yellows = df.away_yellows.apply(lambda x: len(literal_eval(x)))
    home_reds = df.home_reds.apply(lambda x: len(literal_eval(x)))
    away_reds = df.away_reds.apply(lambda x: len(literal_eval(x)))

    data = pd.DataFrame({'home_goals': home_goals,
                         'away_goals': away_goals,
                         'home_yellows': home_yellows,
                         'away_yellows': away_yellows,
                         'home_reds': home_reds,
                         'away_reds': away_reds})

    df_container.append(data)

# concatenate all into one master data frames & generate descriptive stats
master_df = DplyFrame(pd.concat(df_container))
print("home goals", "\n", master_df.home_goals.describe())
print("away goals", "\n", master_df.away_goals.describe())
print("home yellows", "\n", master_df.home_yellows.describe())
print("away yellows", "\n", master_df.away_yellows.describe())
print("home reds", "\n", master_df.home_reds.describe())
print("away reds", "\n", master_df.away_reds.describe())

print("frequency of home goals", len(master_df >> sift(X.home_goals > 0)))
print("frequency of away goals", len(master_df >> sift(X.away_goals > 0)))
print("frequency of home yellows", len(master_df >> sift(X.home_yellows > 0)))
print("frequency of away yellows", len(master_df >> sift(X.away_yellows > 0)))
print("frequency of home reds", len(master_df >> sift(X.home_reds > 0)))
print("frequency of away reds", len(master_df >> sift(X.away_reds > 0)))

goals = master_df.apply(lambda row: row.home_goals + row.away_goals, axis=1)
print("goals", goals.describe())
print("freq", len(goals.nonzero()[0]))

yellows = master_df.apply(lambda row: row.home_yellows + row.away_yellows, axis=1)
print("yellows", yellows.describe())
print("yellows", len(yellows.nonzero()[0]))

reds = master_df.apply(lambda row: row.home_reds + row.away_reds, axis=1)
print("reds", reds.describe())
print("reds", len(reds.nonzero()[0]))
