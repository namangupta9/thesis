"""Time Series Modeling."""


import os
import pandas as pd
import numpy as np
from dplython import DplyFrame, select, sift, X
from statsmodels.tsa.statespace.sarimax import SARIMAX
from arima_helpers import process_data, plot_predictions, export_coefficients


def fit_arima_model(df_in, x_mat_in, order_in, coefficients_dict,
                    feature_set, match_id):
    """Fit an SARIMAX model to a match, given an x_matrix of features."""
    club_name = match_id.split("2")[0]
    path = "arima_" + str(feature_set) + "/" + club_name + "/"
    if not os.path.exists(path):
        os.makedirs(path)

    try:
        model = SARIMAX(endog=df_in.shorthand_search_vol.astype(int),
                        exog=x_mat_in,
                        dates=list(df_in.date_time),
                        order=(1, 1, 0),
                        enforce_stationarity=False)

        model_fit = model.fit(disp=0)   # disp=0 turns off debug information

        # write model summary & predictions plot to path
        filepath = path + match_id
        with open(filepath + ".txt", 'w') as f:
            print >> f, model_fit.summary()

        predictions = model_fit.predict()
        plot_predictions(date_times=df_in.date_time,
                         actual_values=df_in.shorthand_search_vol,
                         predictions=predictions,
                         match_id=match_id,
                         feature_set_in=feature_set,
                         filename=filepath)

        confidence_ints = model_fit.conf_int()
        for idx, feature in enumerate(x_mat_in.columns.values):
            coef = np.mean(confidence_ints.iloc[idx])
            upper = confidence_ints.iloc[idx][1]
            lower = confidence_ints.iloc[idx][0]

            # filter out 0's & distinguish by significance
            if coef != 0 and coef is not None:

                # both upper & lower bounds must be both (+), or both (-)
                prod = upper * lower
                if prod > 0:
                    coefficients_dict[feature]["significant"].append(coef)
                else:
                    coefficients_dict[feature]["unsignificant"].append(coef)

    except Exception:
        with open("errors.txt", "a+") as error_logfile:
            error_logfile.write("Error caused by " + match_id + '\n')


def run_arima_models(large_df_in, x_mat_in, feature_set_in):
    """Iterate through all individual time series, gathering coefficients."""
    coefficients = {}
    coefficients['home_goal'] = {"significant": [], "unsignificant": []}
    coefficients['away_goal'] = {"significant": [], "unsignificant": []}
    coefficients['home_yellow'] = {"significant": [], "unsignificant": []}
    coefficients['away_yellow'] = {"significant": [], "unsignificant": []}
    coefficients['home_red'] = {"significant": [], "unsignificant": []}
    coefficients['away_red'] = {"significant": [], "unsignificant": []}

    # two time series per match - one each for home & away
    for match_id, match_df in large_df_in.groupby(['match_id']):
        x_mat = x_mat_in >> sift(X.match_id == match_id)
        x_mat = x_mat.drop(columns=["match_id"])

        fit_arima_model(df_in=match_df,
                        x_mat_in=x_mat,
                        order_in=(1, 1, 0),
                        coefficients_dict=coefficients,
                        feature_set=feature_set_in,
                        match_id=str(match_id))

        print(match_id)

    json_filename = "arima_" + str(feature_set_in) + ".json"
    export_coefficients(coefficients, json_filename)


if __name__ == "__main__":
    longform_df = DplyFrame(pd.read_csv("../../LongForm/longform.csv",
                            dtype={'shorthand_search_vol': float}))

    stage_2_df = process_data(longform_df)
    x_mat = stage_2_df >> select(stage_2_df.match_id,
                                 stage_2_df.home_goal,
                                 stage_2_df.away_goal,
                                 stage_2_df.home_yellow,
                                 stage_2_df.away_yellow,
                                 stage_2_df.home_red,
                                 stage_2_df.away_red)

    # run model with 1st feature set
    run_arima_models(stage_2_df, x_mat, 1)
