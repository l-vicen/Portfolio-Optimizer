import streamlit as st

import pandas as pd
from pypfopt import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt import risk_models, expected_returns, plotting
import matplotlib.pyplot as plt


# Read in price data
df = pd.read_csv("data/stock_prices.csv", parse_dates=True, index_col="date")
st.write(df)

st.write('MEAN HISTORUCAL RETURN')
mu = expected_returns.mean_historical_return(df)
st.write(mu)

st.write('SAMPLE COVARIANCE')
S = risk_models.sample_cov(df)
st.write(S)

# Optimize for maximal Sharpe ratio

st.write('EFFICIENT FRONTIER')
ef = EfficientFrontier(mu, S)
raw_weights = ef.max_sharpe()
cleaned_weights = ef.clean_weights()
ef.save_weights_to_file("weights.csv")  # saves to file
st.write("Weigth distribution")
st.write(cleaned_weights)
ef.portfolio_performance(verbose=True)

from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices

latest_prices = get_latest_prices(df)

weights = {'GOOG': 0.03835,
'AAPL': 0.0689,
'FB': 0.20603,
'BABA': 0.07315,
'AMZN': 0.04033,
'GE': 0.0,
'AMD': 0.0,
'WMT': 0.0,
'BAC': 0.0,
'GM': 0.0,
'T': 0.0,
'UAA': 0.0,
'SHLD': 0.0,
'XOM': 0.0,
'RRC': 0.0,
'BBY': 0.01324,
'MA': 0.35349,
'PFE': 0.1957,
'JPM': 0.0,
'SBUX': 0.01082}

da = DiscreteAllocation(weights, latest_prices, total_portfolio_value=10000)
allocation, leftover = da.greedy_portfolio()
st.write("Discrete allocation:", allocation)
st.write("Funds remaining: ${:.2f}".format(leftover))