"""Basic model."""

import pandas as pd
import datetime
from datetime import time
import math
import numpy as np
import scipy
import statsmodels.api as sm

# read df
longform_df = pd.read_csv("LongForm/longform.csv")
cols = longform_df.columns
relevant_cols = cols[2:]
y_var = longform_df[relevant_cols[0]]
x_vars = longform_df[relevant_cols[1:]]
# ones = np.ones()
# https://www.geeksforgeeks.org/numpy-ones-python/
# x_vars # add to columns

# Note the difference in argument order
lm = sm.OLS(y_var, x_vars).fit()
predictions = lm.predict(x_vars)  # make the predictions by the model

print predictions.iloc[110:120]    # this should give predictions, once we have the const stuff figured out.
# this was the goal time for chel / bournemouth

# also make an error column; y_var - prediciton
# for what games do you find a high level of error?
# is it systematic? maybe for all matchweek0 games? boxing day games?

# Print out the statistics
print(lm.summary())
print('Parameters: ', lm.params)
print('R2: ', lm.rsquared)


# reference
# http://www.statsmodels.org/dev/regression.html
# https://towardsdatascience.com/simple-and-multiple-linear-regression-in-python-c928425168f9
