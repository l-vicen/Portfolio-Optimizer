import streamlit as st
import control as cl
from pypfopt import risk_models
from pypfopt import expected_returns

import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt

from pypfopt import EfficientFrontier

def mean_variance_setup():
    st.title('Mean Variance Optimization')

    c1, c2 = st.columns((2, 1))
    c1.header('Setup')

    # Start Date
    start_date = c1.date_input('Start date')

    # End Date
    end_date = c1.date_input('End date')

    # List of Stocks
    list_of_stocks = c1.multiselect("Selct all tickers you want to have in the portfolio", cl.return_list_tickers())

    # Download price data from desired stocks
    df = cl.return_closed_prices(list_of_stocks, start_date)
    st.write(df)

    c2.markdown('blaaaaaaaaaaaaaaaaaaaaaaaa')

    st.markdown('---')

    st.markdown('### Historical Adjusted Prices')
    st.line_chart(df)

    st.markdown('---')

    st.markdown("### Covariance Matrix")
    sample_cov = risk_models.sample_cov(df, frequency=252)
    st.write(sample_cov)

    figOne, ax = plt.subplots()
    sns.heatmap(sample_cov.corr(), ax=ax)
    st.write(figOne)

    st.markdown('---')

    st.markdown('### Expected Returns')
    mu = expected_returns.capm_return(df)

    st.write(mu)
    st.bar_chart(mu)

    st.markdown('---')
    S = risk_models.CovarianceShrinkage(df).ledoit_wolf()
    # You don't have to provide expected returns in this case
    ef = EfficientFrontier(None, S, weight_bounds=(None, None))
    ef.min_volatility()
    weights = ef.clean_weights()
    st.write(weights)

