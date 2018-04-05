"""Multiple Linear Regression Modeling."""

import pandas as pd
import numpy as np
from dplython import DplyFrame, sift, X
import statsmodels.api as sm
from plotting_helper import plot_matches


def predict_on_match_id(lm, longform_df, date, match_id, opponent_match_id,
                        model_no, filename_out, x_var_list):
    """Run prediction & plot / save on top of match search vol."""
    match_data = longform_df >> sift(X.match_id == match_id)
    candidate_data = match_data[x_var_list]
    preds = [(model_no, pred) for pred in lm.predict(candidate_data)]

    # turn predictions into data frame
    labels = ["match_id", "shorthand_search_vol"]
    temp_df = pd.DataFrame.from_records(preds, columns=labels)
    temp_df = temp_df.set_index(match_data.index)
    temp_df["time"] = match_data["time"]

    # append to long form df and plot
    preds_df = pd.concat([longform_df, temp_df], axis=0, ignore_index=True)
    sifted_df = preds_df >> sift((X.match_id == match_id) |
                                 (X.match_id == opponent_match_id) |
                                 (X.match_id == model_no))

    plot_matches(sifted_df, date, filename_out)


# read & dissect df
longform_df_og = pd.read_csv("../../LongForm/longform.csv",
                             dtype={'shorthand_search_vol': int})
longform_df = DplyFrame(longform_df_og)
cols = longform_df.columns
y_var = longform_df["shorthand_search_vol"]       # search volume
longform_df['ones'] = 1


# MLR MODEL #1: USING ONLY MATCH STAGES TO PREDICT SEARCH VOLUME
# note the difference in argument order; y_var is dependent, x_vars independent
# using Stage 0 as "reference level"; only vars are stage_1-4_indicators
x_var_list = ["ones", "stage_1_ind", "stage_2_ind",
              "stage_3_ind", "stage_4_ind"]
x_vars = longform_df[x_var_list]
lm = sm.OLS(y_var, x_vars).fit()
with open('model1.txt', 'w') as f:
    print >> f, lm.summary()
predict_on_match_id(lm=lm,
                    longform_df=longform_df,
                    date="2015-08-16",
                    match_id="chelsea2015-08-16",
                    opponent_match_id="manchester_city2015-08-16",
                    model_no="linreg_model1",
                    filename_out="model1.png",
                    x_var_list=x_var_list)


# MLR MODEL #2: USING MATCH STAGES + COMPETITIVE INDEX TO PREDICT SEARCH VOL
x_var_list += ["competitive_idx"]
x_vars = longform_df[x_var_list]
lm = sm.OLS(y_var, x_vars).fit()
with open('model2.txt', 'w') as f:
    print >> f, lm.summary()
predict_on_match_id(lm=lm,
                    longform_df=longform_df,
                    date="2015-08-16",
                    match_id="chelsea2015-08-16",
                    opponent_match_id="manchester_city2015-08-16",
                    model_no="linreg_model2",
                    filename_out="model2.png",
                    x_var_list=x_var_list)


# MLR MODEL #3: USING STAGES + COMPETITIVE INDEX + EVENTS TO PREDICT SEARCH VOL
x_var_list += ["home_goal", "away_goal", "home_yellow", "away_yellow",
               "home_red", "away_red"]
x_vars = longform_df[x_var_list]
lm = sm.OLS(y_var, x_vars).fit()
with open('model3.txt', 'w') as f:
    print >> f, lm.summary()
predict_on_match_id(lm=lm,
                    longform_df=longform_df,
                    date="2015-08-16",
                    match_id="chelsea2015-08-16",
                    opponent_match_id="manchester_city2015-08-16",
                    model_no="linreg_model3",
                    filename_out="model3.png",
                    x_var_list=x_var_list)


# MLR MODEL #4: USING STAGES + COMPETITIVE INDEX + MATCH STATE
x_var_list = ["ones", "stage_1_ind", "stage_2_ind",
              "stage_3_ind", "stage_4_ind", "competitive_idx",
              "cum_total_goals", "cum_goal_diff", "man_down", "upset"]
x_vars = longform_df[x_var_list]
lm = sm.OLS(y_var, x_vars).fit()
with open('model4.txt', 'w') as f:
    print >> f, lm.summary()
predict_on_match_id(lm=lm,
                    longform_df=longform_df,
                    date="2015-08-16",
                    match_id="chelsea2015-08-16",
                    opponent_match_id="manchester_city2015-08-16",
                    model_no="linreg_model4",
                    filename_out="model4.png",
                    x_var_list=x_var_list)


# MLR MODEL #5: USING ALL VARS
x_var_list = ["ones", "stage_1_ind", "stage_2_ind", "stage_3_ind",
              "stage_4_ind", "competitive_idx", "home_goal", "away_goal",
              "home_yellow", "away_yellow", "home_red", "away_red",
              "cum_total_goals", "cum_goal_diff", "man_down", "upset"]
x_vars = longform_df[x_var_list]
lm = sm.OLS(y_var, x_vars).fit()
with open('model5.txt', 'w') as f:
    print >> f, lm.summary()
predict_on_match_id(lm=lm,
                    longform_df=longform_df,
                    date="2015-08-16",
                    match_id="chelsea2015-08-16",
                    opponent_match_id="manchester_city2015-08-16",
                    model_no="linreg_model5",
                    filename_out="model5.png",
                    x_var_list=x_var_list)


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
x_var_list = ["ones", "stage_1_ind", "stage_2_ind", "stage_3_ind",
              "stage_4_ind", "competitive_idx", "home_goal", "away_goal",
              "home_yellow", "away_yellow", "home_red", "away_red",
              "cum_total_goals", "cum_goal_diff", "man_down", "upset",
              "home_goal_AND_upset", "away_goal_AND_upset",
              "home_goal_AND_man_down", "away_goal_AND_man_down",
              "man_down_AND_upset", "home_goal_AND_deadlock",
              "away_goal_AND_deadlock"]
x_vars = longform_df[x_var_list]
lm = sm.OLS(y_var, x_vars).fit()
with open('model6.txt', 'w') as f:
    print >> f, lm.summary()
predict_on_match_id(lm=lm,
                    longform_df=longform_df,
                    date="2015-08-16",
                    match_id="chelsea2015-08-16",
                    opponent_match_id="manchester_city2015-08-16",
                    model_no="linreg_model6",
                    filename_out="model6.png",
                    x_var_list=x_var_list)


# MLR MODEL #7: USING INTERACTIONS, ONLY STAGE 2
stage_2_df = longform_df >> sift(X.stage_2_ind == 1)
stage_2_df = stage_2_df.reset_index(drop=True)
y_var = stage_2_df["shorthand_search_vol"]
x_var_list = ["ones", "competitive_idx", "home_goal", "away_goal",
              "home_yellow", "away_yellow", "home_red", "away_red",
              "cum_total_goals", "cum_goal_diff", "man_down", "upset",
              "home_goal_AND_upset", "away_goal_AND_upset",
              "home_goal_AND_man_down", "away_goal_AND_man_down",
              "man_down_AND_upset", "home_goal_AND_deadlock",
              "away_goal_AND_deadlock"]
x_vars = stage_2_df[x_var_list]
lm = sm.OLS(y_var, x_vars).fit()
with open('model7.txt', 'w') as f:
    print >> f, lm.summary()
predict_on_match_id(lm=lm,
                    longform_df=stage_2_df,
                    date="2015-08-16",
                    match_id="chelsea2015-08-16",
                    opponent_match_id="manchester_city2015-08-16",
                    model_no="linreg_model7",
                    filename_out="model7.png",
                    x_var_list=x_var_list)


# MLR MODEL #8: REFINING MODEL 7, ONLY STAGE 2
# let's play with a few more features...
stage_2_df["cum_goal_diff < 2"] = (stage_2_df["cum_goal_diff"].astype(int) < 2).astype(int)
stage_2_df["goal"] = np.maximum(stage_2_df['home_goal'].astype(int), stage_2_df['away_goal'].astype(int))
stage_2_df["one_goal_scored"] = (stage_2_df["cum_total_goals"].astype(int) == 1).astype(int)
stage_2_df["first_goal"] = stage_2_df['goal'].astype(int) * stage_2_df['one_goal_scored'].astype(int)

# aren't many of these; maybe lack of occurence explaining poor significance?
stage_2_df["red"] = np.maximum(stage_2_df['home_red'].astype(int), stage_2_df['away_red'].astype(int))
stage_2_df["yellow"] = np.maximum(stage_2_df['home_yellow'].astype(int), stage_2_df['away_yellow'].astype(int))

# should be a difference b/w the thirds of the game, right?
pd.options.mode.chained_assignment = None  # default='warn'
stage_2_df["first_30"] = 0
stage_2_df["second_30"] = 0
stage_2_df["final_30"] = 0
first_thirty_end_idx = stage_2_df.shape[0] / 3
second_thirty_end_idx = first_thirty_end_idx * 2
stage_2_df["first_30"].iloc[0:first_thirty_end_idx] = 1
stage_2_df["second_30"].iloc[first_thirty_end_idx:second_thirty_end_idx] = 1
stage_2_df["final_30"].iloc[second_thirty_end_idx:] = 1
stage_2_df["goal_and_first_30"] = stage_2_df['goal'].astype(int) * stage_2_df['first_30'].astype(int)
stage_2_df["goal_and_second_30"] = stage_2_df['goal'].astype(int) * stage_2_df['second_30'].astype(int)
stage_2_df["goal_and_final_30"] = stage_2_df['goal'].astype(int) * stage_2_df['final_30'].astype(int)

# define some more features based on what part of the season it is
stage_2_df['first_3_wks'] = np.where(stage_2_df['match_wk'].astype(int) < 3, 1, 0)
stage_2_df['last_3_wks'] = np.where(stage_2_df['match_wk'].astype(int) > 34, 1, 0)
stage_2_df['holiday_wk'] = ((stage_2_df['match_wk'].astype(int) > 17) &
                            (stage_2_df['match_wk'].astype(int) < 21)).astype(int)

y_var = stage_2_df["shorthand_search_vol"]
x_var_list = ["ones", "first_3_wks", "last_3_wks", "holiday_wk",
              "competitive_idx", "first_30", "second_30", "final_30",
              "goal", "goal_and_first_30", "goal_and_second_30",
              "goal_and_final_30", "yellow", "red",
              "cum_total_goals", "man_down", "upset"]
x_vars = stage_2_df[x_var_list]
lm = sm.OLS(y_var, x_vars).fit()
with open('model8.txt', 'w') as f:
    print >> f, lm.summary()
predict_on_match_id(lm=lm,
                    longform_df=stage_2_df,
                    date="2015-08-16",
                    match_id="chelsea2015-08-16",
                    opponent_match_id="manchester_city2015-08-16",
                    model_no="linreg_model8",
                    filename_out="model8.png",
                    x_var_list=x_var_list)

# Useful: Best Matches of Season; How'd we do?
# http://metro.co.uk/2016/05/16/ranked-the-six-best-premier-league-matches-of-the-20162017-season-5881387/
predict_on_match_id(lm=lm,
                    longform_df=stage_2_df,
                    date="2015-12-28",
                    match_id="everton2015-12-28",
                    opponent_match_id="stoke_city2015-12-28",
                    model_no="linreg_model8",
                    filename_out="model8_1.png",
                    x_var_list=x_var_list)

predict_on_match_id(lm=lm,
                    longform_df=stage_2_df,
                    date="2016-01-23",
                    match_id="liverpool2016-01-23",
                    opponent_match_id="norwich_city2016-01-23",
                    model_no="linreg_model8",
                    filename_out="model8_2.png",
                    x_var_list=x_var_list)

predict_on_match_id(lm=lm,
                    longform_df=stage_2_df,
                    date="2016-02-14",
                    match_id="arsenal2016-02-14",
                    opponent_match_id="leicester_city2016-02-14",
                    model_no="linreg_model8",
                    filename_out="model8_3.png",
                    x_var_list=x_var_list)

predict_on_match_id(lm=lm,
                    longform_df=stage_2_df,
                    date="2016-03-05",
                    match_id="tottenham2016-03-05",
                    opponent_match_id="arsenal2016-03-05",
                    model_no="linreg_model8",
                    filename_out="model8_4.png",
                    x_var_list=x_var_list)

predict_on_match_id(lm=lm,
                    longform_df=stage_2_df,
                    date="2016-05-02",
                    match_id="chelsea2016-05-02",
                    opponent_match_id="tottenham2016-05-02",
                    model_no="linreg_model8",
                    filename_out="model8_5.png",
                    x_var_list=x_var_list)

# OTHER COMMENTS Schwartz Left

# also make an error column; y_var - prediction; the "residual"
# for what games do you find a high level of error?
# is it systematic? maybe for all matchweek0 games? boxing day games?

# REFERENCE
# http://www.statsmodels.org/dev/regression.html
# https://towardsdatascience.com/simple-and-multiple-linear-regression-in-python-c928425168f9
