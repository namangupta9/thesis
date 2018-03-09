"""ARIMA Modeling (Time Series Analysis)."""

# What is ARMA, and ARIMA? Why ARIMA > Multiple Linear Regression?
# https://machinelearningmastery.com/arima-for-time-series-forecasting-with-python/

# An ARIMA model is a class of statistical models for analyzing and forecasting
# time series data. It explicitly caters to a suite of standard structures in
# time series data, and as such provides a simple yet powerful method for
# making skillful time series forecasts.

# ARIMA is an acronym that stands for AutoRegressive Integrated Moving Average.
# It is a generalization of the simpler AutoRegressive Moving Average and adds
# the notion of integration.

# This acronym is descriptive, capturing the key aspects of the model itself:

# AR: Autoregression.
#     A model that uses the dependent relationship between an observation
#     and some number of lagged observations.

# I: Integrated.
#    The use of differencing of raw observations (e.g. subtracting an
#    observation from an observation at the previous time step) in order to
#    make the time series stationary.

# MA: Moving Average.
#     A model that uses the dependency between an observation and a residual
#     error from a moving average model applied to lagged observations.

# Each component is explicitly specified in the model as a parameter.

# A standard notation is used of ARIMA(p,d,q) where the parameters are
# substituted with integer values to quickly indicate the specific ARIMA model
# being used.

# The parameters of the ARIMA model are defined as follows:

# p: # of lag observations included in the model (lag order)
# d: # of times that the raw observations are differenced (degree of differencing)
# q: The size of the moving average window, (order of moving average)

# A linear regression model is constructed including the specified number
# and type of terms, and the data is prepared by a degree of differencing in
# order to make it stationary, i.e. to remove trend and seasonal structures
# that negatively affect the regression model.

# A value of 0 can be used for a parameter, which indicates to not use that
# element of the model. This way, the ARIMA model can be configured to perform
# the function of an ARMA model, and even a simple AR, I, or MA model.

# Adopting an ARIMA model for a time series assumes that the underlying process
# that generated the observations is an ARIMA process. This may seem obvious,
# but helps to motivate the need to confirm the assumptions of the model in the
# raw observations and in the residual errors of forecasts from the model.

import pandas as pd
from dplython import *
import statsmodels.api as sm
# http://www.statsmodels.org/dev/generated/statsmodels.tsa.arima_model.ARIMA.html
