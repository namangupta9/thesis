"""Multiple Linear Regression Modeling."""

import pandas as pd
import numpy as np
from dplython import *
import statsmodels.api as sm

# read & dissect df
longform_df = DplyFrame(pd.read_csv("../../LongForm/longform.csv",
                        dtype={'shorthand_search_vol': int}))
cols = longform_df.columns
y_var = longform_df["shorthand_search_vol"]       # search volume
longform_df['ones'] = 1


# TODO .predict(), and then plot the predicted values vs. actual values


# MLR MODEL #1: USING ONLY MATCH STAGES TO PREDICT SEARCH VOLUME
# note the difference in argument order; y_var is dependent, x_vars independent
# using Stage 0 as "reference level"; only vars are stage_1-4_indicators
x_vars = longform_df[["ones",
                      "stage_1_ind",
                      "stage_2_ind",
                      "stage_3_ind",
                      "stage_4_ind"]]
lm = sm.OLS(y_var, x_vars).fit()
with open('model1.txt', 'w') as f:
    print >> f, lm.summary()

# plot the predicted & the actual
# also have a column for the residual
longform_df["pred_1"] = lm.predict()

p = ggplot(aes(x='date_time',
               y='shorthand_search_vol',
               group="match_id",
               color="match_id"),
           data=longform_df >> sift((X.match_id == "chelsea2015-08-16") |
                                    (X.match_id == "manchester_city2015-08-16")))

p += geom_line(aes(y='pred_1'))

# MLR MODEL #2: USING MATCH STAGES + COMPETITIVE INDEX TO PREDICT SEARCH VOL
x_vars = longform_df[["ones",
                      "stage_1_ind",
                      "stage_2_ind",
                      "stage_3_ind",
                      "stage_4_ind",
                      "competitive_idx"]]
lm = sm.OLS(y_var, x_vars).fit()
with open('model2.txt', 'w') as f:
    print >> f, lm.summary()


# MLR MODEL #3: USING STAGES + COMPETITIVE INDEX + EVENTS TO PREDICT SEARCH VOL
x_vars = longform_df[["ones",
                      "stage_1_ind",
                      "stage_2_ind",
                      "stage_3_ind",
                      "stage_4_ind",
                      "competitive_idx",
                      "home_goal",
                      "away_goal",
                      "home_yellow",
                      "away_yellow",
                      "home_red",
                      "away_red"]]
lm = sm.OLS(y_var, x_vars).fit()
with open('model3.txt', 'w') as f:
    print >> f, lm.summary()


# MLR MODEL #4: USING STAGES + COMPETITIVE INDEX + MATCH STATE
x_vars = longform_df[["ones",
                      "stage_1_ind",
                      "stage_2_ind",
                      "stage_3_ind",
                      "stage_4_ind",
                      "competitive_idx",
                      "cum_total_goals",
                      "cum_goal_diff",
                      "man_down",
                      "upset"]]
lm = sm.OLS(y_var, x_vars).fit()
with open('model4.txt', 'w') as f:
    print >> f, lm.summary()


# MLR MODEL #5: USING ALL VARS
x_vars = longform_df[["ones",
                      "stage_1_ind",
                      "stage_2_ind",
                      "stage_3_ind",
                      "stage_4_ind",
                      "competitive_idx",
                      "home_goal",
                      "away_goal",
                      "home_yellow",
                      "away_yellow",
                      "home_red",
                      "away_red",
                      "cum_total_goals",
                      "cum_goal_diff",
                      "man_down",
                      "upset"]]
lm = sm.OLS(y_var, x_vars).fit()
with open('model5.txt', 'w') as f:
    print >> f, lm.summary()


# BUILDING IN STATISTICAL INTERACTIONS
longform_df['home_goal_AND_upset'] = longform_df['home_goal'].astype(int) * longform_df['upset'].astype(int)
longform_df['away_goal_AND_upset'] = longform_df['away_goal'].astype(int) * longform_df['upset'].astype(int)
longform_df['home_goal_AND_man_down'] = longform_df['home_goal'].astype(int) * longform_df['man_down'].astype(int)
longform_df['away_goal_AND_man_down'] = longform_df['away_goal'].astype(int) * longform_df['man_down'].astype(int)
longform_df['man_down_AND_upset'] = longform_df['man_down'].astype(int) * longform_df['upset'].astype(int)
longform_df["deadlock"] = (longform_df["cum_goal_diff"].astype(int) == 0).astype(int)
longform_df['home_goal_AND_deadlock'] = longform_df['home_goal'].astype(int) * longform_df['deadlock'].astype(int)
longform_df['away_goal_AND_deadlock'] = longform_df['away_goal'].astype(int) * longform_df['deadlock'].astype(int)

# MLR MODEL #6: USING INTERACTIONS
x_vars = longform_df[["ones",
                      "stage_1_ind",
                      "stage_2_ind",
                      "stage_3_ind",
                      "stage_4_ind",
                      "competitive_idx",
                      "home_goal",
                      "away_goal",
                      "home_yellow",
                      "away_yellow",
                      "home_red",
                      "away_red",
                      "man_down",
                      "upset",
                      "home_goal_AND_upset",
                      "away_goal_AND_upset",
                      "home_goal_AND_man_down",
                      "away_goal_AND_man_down",
                      "man_down_AND_upset",
                      "home_goal_AND_deadlock",
                      "away_goal_AND_deadlock"]]
lm = sm.OLS(y_var, x_vars).fit()
with open('model6.txt', 'w') as f:
    print >> f, lm.summary()


# MLR MODEL #7: USING INTERACTIONS, ONLY STAGE 2
stage_2_df = longform_df >> sift(X.stage_2_ind == 1)
stage_2_df = stage_2_df.reset_index(drop=True)
y_var = stage_2_df["shorthand_search_vol"]
x_vars = stage_2_df[["ones",
                     "competitive_idx",
                     "home_goal",
                     "away_goal",
                     "home_yellow",
                     "away_yellow",
                     "home_red",
                     "away_red",
                     "man_down",
                     "upset",
                     "home_goal_AND_upset",
                     "away_goal_AND_upset",
                     "home_goal_AND_man_down",
                     "away_goal_AND_man_down",
                     "man_down_AND_upset",
                     "home_goal_AND_deadlock",
                     "away_goal_AND_deadlock"]]
lm = sm.OLS(y_var, x_vars).fit()
with open('model7.txt', 'w') as f:
    print >> f, lm.summary()

# MLR MODEL #8: USING INTERACTIONS, ONLY STAGE 2
stage_2_df = longform_df >> sift(X.stage_2_ind == 1)
stage_2_df = stage_2_df.reset_index(drop=True)
y_var = stage_2_df["shorthand_search_vol"]
x_vars = stage_2_df[["ones",
                     "stage_2_ind",
                     "competitive_idx",
                     "home_goal",
                     "away_goal",
                     "home_yellow",
                     "away_yellow",
                     "home_red",
                     "away_red",
                     "man_down",
                     "upset",
                     "home_goal_AND_upset",
                     "away_goal_AND_upset",
                     "home_goal_AND_man_down",
                     "away_goal_AND_man_down",
                     "man_down_AND_upset",
                     "home_goal_AND_deadlock",
                     "away_goal_AND_deadlock"]]
lm = sm.OLS(y_var, x_vars).fit()
with open('model8.txt', 'w') as f:
    print >> f, lm.summary()


# OTHER COMMENTS Schwartz Left

# print('Parameters: ', lm.params)
# print('R2: ', lm.rsquared)

# # make the predictions by the model
# predictions = lm.predict(x_vars)
# # this should give predictions, once we have the const stuff figured out.
# # this was the goal time for chel / bournemouth
# print predictions.iloc[110:120]

# also make an error column; y_var - prediciton; the "residual"
# for what games do you find a high level of error?
# is it systematic? maybe for all matchweek0 games? boxing day games?

# REFERENCE
# http://www.statsmodels.org/dev/regression.html
# https://towardsdatascience.com/simple-and-multiple-linear-regression-in-python-c928425168f9
