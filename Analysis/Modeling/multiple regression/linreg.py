"""Multiple Linear Regression Modeling."""

import pandas as pd
from dplython import *
import statsmodels.api as sm

# read & dissect df
longform_df = DplyFrame(pd.read_csv("../../LongForm/longform.csv",
                        dtype={'shorthand_search_vol': int}))
cols = longform_df.columns
y_var = longform_df["shorthand_search_vol"]       # search volume


# MLR MODEL #1: USING ONLY MATCH STAGES TO PREDICT SEARCH VOLUME
# note the difference in argument order; y_var is dependent, x_vars independent
# using Stage 0 as "reference level"; only vars are stage_1-4_indicators
x_vars = longform_df[["stage_1_ind",
                      "stage_2_ind",
                      "stage_3_ind",
                      "stage_4_ind"]]
lm = sm.OLS(y_var, x_vars).fit()
with open('model1.txt', 'w') as f:
    # print summary
    print >> f, lm.summary()


# MLR MODEL #2: USING MATCH STAGES + COMPETITIVE INDEX TO PREDICT SEARCH VOL
x_vars = longform_df[["stage_1_ind",
                      "stage_2_ind",
                      "stage_3_ind",
                      "stage_4_ind",
                      "competitive_idx"]]
lm = sm.OLS(y_var, x_vars).fit()
with open('model2.txt', 'w') as f:
    # print summary
    print >> f, lm.summary()


# MLR MODEL #3: USING STAGES + COMPETITIVE INDEX + EVENTS TO PREDICT SEARCH VOL
x_vars = longform_df[["stage_1_ind",
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
    # print summary
    print >> f, lm.summary()


# MLR MODEL #4: USING STAGES + COMPETITIVE INDEX + MATCH STATE
x_vars = longform_df[["stage_1_ind",
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
    # print summary
    print >> f, lm.summary()


# MLR MODEL #5: USING ALL VARS
x_vars = longform_df[["stage_1_ind",
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
    # print summary
    print >> f, lm.summary()


# OTHER COMMENTS Schwartz Left

# print('Parameters: ', lm.params)
# print('R2: ', lm.rsquared)

# # make the predictions by the model
# predictions = lm.predict(x_vars)
# # this should give predictions, once we have the const stuff figured out.
# # this was the goal time for chel / bournemouth
# print predictions.iloc[110:120]

# ones = np.ones()
# https://www.geeksforgeeks.org/numpy-ones-python/
# x_vars # add to columns

# also make an error column; y_var - prediciton; the "residual"
# for what games do you find a high level of error?
# is it systematic? maybe for all matchweek0 games? boxing day games?

# REFERENCE
# http://www.statsmodels.org/dev/regression.html
# https://towardsdatascience.com/simple-and-multiple-linear-regression-in-python-c928425168f9
