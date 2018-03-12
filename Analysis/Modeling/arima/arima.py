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

# ARIMA MODEL #1: USING BASIC MATCH EVENTS
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


# ARIMA MODEL #2: USING ALL VARS
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


# ARIMA MODEL #3: STAGE 2, MATCH EVENTS ONLY
# LET'S ONLY FOCUS ON STAGE 2...makes more sense to consider match events in the context of the match itself,
#                               and not the buildup or post-match reaction time...
stage_2_df = longform_df >> sift(X.stage_2_ind == 1)
stage_2_df = stage_2_df.reset_index(drop=True)

# new, more thoughtful ARIMA model parameters
# d = 1 ("first difference"); let's predict the delta b/w volumes at consecutive intervals
# aka, "stationarizing" the time series
# q = 1 (a series displays moving average behavior if it apparently undergoes random
#        "shocks" whose effects are felt in 2+ consecutive periods. )
# TODO, diff b/w q = 1 & q = 2?

x_mat = stage_2_df >> select(stage_2_df.home_goal,
                             stage_2_df.away_goal,
                             stage_2_df.home_yellow,
                             stage_2_df.away_yellow,
                             stage_2_df.home_red,
                             stage_2_df.away_red,
                             stage_2_df.competitive_idx)

model = ARIMA(endog=stage_2_df.shorthand_search_vol,
              exog=x_mat,
              dates=stage_2_df.date_time,
              order=(0, 1, 1))

model_fit = model.fit(disp=0)   # disp=0 turns off debug information
with open('model3.txt', 'w') as f:
    # print summary
    print >> f, model_fit.summary()


# ARIMA MODEL #4: STAGE 2, ALL VARS
x_mat = stage_2_df >> select(stage_2_df.match_wk,
                             stage_2_df.home_goal,
                             stage_2_df.away_goal,
                             stage_2_df.home_yellow,
                             stage_2_df.away_yellow,
                             stage_2_df.home_red,
                             stage_2_df.away_red,
                             stage_2_df.cum_total_goals,
                             stage_2_df.cum_goal_diff,
                             stage_2_df.man_down,
                             stage_2_df.upset,
                             stage_2_df.competitive_idx)

model = ARIMA(endog=stage_2_df.shorthand_search_vol,
              exog=x_mat,
              dates=stage_2_df.date_time,
              order=(0, 1, 1))

model_fit = model.fit(disp=0)   # disp=0 turns off debug information
with open('model4.txt', 'w') as f:
    # print summary
    print >> f, model_fit.summary()


# ARIMA MODEL #5: STAGE 2, STATISTICAL INTERACTIONS

# we're really making two types of predictions here...
# predicting the impact (spikes) of individual match events (under certain conditions)
# and we're predicting "raw" scaled levels under certain conditions...
# -- like, we're not saying anything about the bump, but when there's a deadlock and upset,
#    we're seeing generally higher search activity levels!
# this later type of prediction should require a different model, right?
# we wouldn't need to first difference anymore, because we don't care about the "bump"

# TODO am i getting multiple collinearity problems here? idk what that fully means.
# interactions: what's the effect of a home or away goal when an upset's in progress?
# this new column will only be 1 when both home/away goal are 1, and upset is 1 (1*1=1)
# moving away from considering variables strictly in isolation, probably more accurate w/ interactions
stage_2_df['home_goal_AND_upset'] = stage_2_df['home_goal'].astype(int) * stage_2_df['upset'].astype(int)
stage_2_df['away_goal_AND_upset'] = stage_2_df['away_goal'].astype(int) * stage_2_df['upset'].astype(int)
stage_2_df['home_goal_AND_man_down'] = stage_2_df['home_goal'].astype(int) * stage_2_df['man_down'].astype(int)
stage_2_df['away_goal_AND_man_down'] = stage_2_df['away_goal'].astype(int) * stage_2_df['man_down'].astype(int)
stage_2_df['man_down_AND_upset'] = stage_2_df['man_down'].astype(int) * stage_2_df['upset'].astype(int)

# home / away goals when cum_goal_diff is 0? ("breaking deadlock")
stage_2_df["deadlock"] = (stage_2_df["cum_goal_diff"].astype(int) == 0).astype(int)
stage_2_df['home_goal_AND_deadlock'] = stage_2_df['home_goal'].astype(int) * stage_2_df['deadlock'].astype(int)
stage_2_df['away_goal_AND_deadlock'] = stage_2_df['away_goal'].astype(int) * stage_2_df['deadlock'].astype(int)

# other ideas
# when goal_diff of 0 and cum_total_goals > 2? really offensive but tight game
# when goal_diff of 0 and cum_total_goals < 2? really offensive but tight game

x_mat = stage_2_df >> select(stage_2_df.match_wk,
                             stage_2_df.home_goal,
                             stage_2_df.away_goal,
                             stage_2_df.home_yellow,
                             stage_2_df.away_yellow,
                             stage_2_df.home_red,
                             stage_2_df.away_red,
                             stage_2_df.home_goal_AND_upset,
                             stage_2_df.away_goal_AND_upset,
                             stage_2_df.home_goal_AND_man_down,
                             stage_2_df.away_goal_AND_man_down,
                             stage_2_df.man_down_AND_upset,
                             stage_2_df.home_goal_AND_deadlock,
                             stage_2_df.away_goal_AND_deadlock,
                             stage_2_df.competitive_idx)

model = ARIMA(endog=stage_2_df.shorthand_search_vol,
              exog=x_mat,
              dates=stage_2_df.date_time,
              order=(0, 1, 1))

model_fit = model.fit(disp=0)   # disp=0 turns off debug information
with open('model4.txt', 'w') as f:
    # print summary
    print >> f, model_fit.summary()

# ARIMA MODEL #5: STAGE 2, STRICTLY STATISTICAL INTERACTIONS
x_mat = stage_2_df >> select(stage_2_df.match_wk,
                             stage_2_df.home_goal_AND_upset,
                             stage_2_df.away_goal_AND_upset,
                             stage_2_df.home_goal_AND_man_down,
                             stage_2_df.away_goal_AND_man_down,
                             stage_2_df.man_down_AND_upset,
                             stage_2_df.home_goal_AND_deadlock,
                             stage_2_df.away_goal_AND_deadlock,
                             stage_2_df.competitive_idx)

model = ARIMA(endog=stage_2_df.shorthand_search_vol,
              exog=x_mat,
              dates=stage_2_df.date_time,
              order=(0, 1, 1))

model_fit = model.fit(disp=0)   # disp=0 turns off debug information
with open('model5.txt', 'w') as f:
    # print summary
    print >> f, model_fit.summary()


# ARIMA MODEL #6: STAGE 2, STRICTLY STATISTICAL INTERACTIONS (REMOVING SOME INSIGNIF. VARS)
# ALSO BUMPING UP TO 2 MA COEFFICIENTS..BOTH ARE STATISTICALLY SIGNIFICANT
x_mat = stage_2_df >> select(stage_2_df.away_goal_AND_upset,
                             stage_2_df.man_down_AND_upset,
                             stage_2_df.competitive_idx)

model = ARIMA(endog=stage_2_df.shorthand_search_vol,
              exog=x_mat,
              dates=stage_2_df.date_time,
              order=(0, 1, 2))

model_fit = model.fit(disp=0)   # disp=0 turns off debug information
with open('model6.txt', 'w') as f:
    # print summary
    print >> f, model_fit.summary()