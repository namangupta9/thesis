"""ARIMA Modeling (Time Series Analysis)."""

import pandas as pd
from dplython import *
from statsmodels.tsa.arima_model import ARIMA
# http://www.statsmodels.org/dev/generated/statsmodels.tsa.arima_model.ARIMA.html

# read initial data
longform_df = DplyFrame(pd.read_csv("../../LongForm/longform.csv",
                        dtype={'shorthand_search_vol': float}))

# process data
longform_df["date"] = longform_df.match_id.apply(lambda x: "20" + x.split("20")[-1])
longform_df['date_time'] = longform_df['date'].astype(str) + " " + longform_df['time'].astype(str)
longform_df['date_time'] = pd.to_datetime(longform_df['date_time'], errors="coerce", infer_datetime_format=True)

# fit several ARIMA(2, 0, 2) models
# TODO: why did Schwartz use 2, 0, 2 as model parameters?
# TODO: why no Integration? why are we using ARMA?

# ARMA MODEL #1: USING BASIC MATCH EVENTS
x_mat = longform_df >> select(longform_df.home_goal,
                              longform_df.away_goal,
                              longform_df.home_yellow,
                              longform_df.away_yellow,
                              longform_df.home_red,
                              longform_df.away_red,
                              longform_df.stage_1_ind,
                              longform_df.stage_2_ind,
                              longform_df.stage_3_ind,
                              longform_df.stage_4_ind,
                              longform_df.competitive_idx)

model = ARIMA(endog=longform_df.shorthand_search_vol,
              exog=x_mat,
              dates=longform_df.date_time,
              order=(2, 0, 2))

model_fit = model.fit(disp=0)   # disp=0 turns off debug information
with open('model1.txt', 'w') as f:
    # print summary
    print >> f, model_fit.summary()


# ARMA MODEL #2: USING ALL VARS
x_mat = longform_df >> select(longform_df.match_wk,
                              longform_df.home_goal,
                              longform_df.away_goal,
                              longform_df.home_yellow,
                              longform_df.away_yellow,
                              longform_df.home_red,
                              longform_df.away_red,
                              longform_df.stage_1_ind,
                              longform_df.stage_2_ind,
                              longform_df.stage_3_ind,
                              longform_df.stage_4_ind,
                              longform_df.cum_total_goals,
                              longform_df.cum_goal_diff,
                              longform_df.man_down,
                              longform_df.upset,
                              longform_df.competitive_idx)

model = ARIMA(endog=longform_df.shorthand_search_vol,
              exog=x_mat,
              dates=longform_df.date_time,
              order=(2, 0, 2))

model_fit = model.fit(disp=0)   # disp=0 turns off debug information
with open('model2.txt', 'w') as f:
    # print summary
    print >> f, model_fit.summary()

# LET'S ONLY FOCUS ON STAGE 2
stage_2_df = longform_df >> sift(X.stage_2_ind == 1)

# LET'S START BUILDING IN SOME INTERACTIONS..
# multiply dummy variable values together
# for example, what's the effect of a home or away goal when an upset's in progress?
# this new column will only be 1 when both home/away goal are 1, and upset is 1 (1*1=1)
# moving away from considering variables strictly in isolation, probably more accurate w/ interactions

stage_2_df['home_goal_AND_upset'] = stage_2_df['home_goal'].astype(int) * stage_2_df['upset'].astype(int)
stage_2_df['away_goal_AND_upset'] = stage_2_df['away_goal'].astype(int) * stage_2_df['upset'].astype(int)
stage_2_df['man_down_AND_upset'] = stage_2_df['man_down'].astype(int) * stage_2_df['upset'].astype(int)

# other ideas for interactions
# goal diff of 0 and a goal?
# goal diff of 0 and cum goal diff > 5? really offensive but tight game
# goal diff of 0 and cum goal diff < 5? really defensive but tight game
