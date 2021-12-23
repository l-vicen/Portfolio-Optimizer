import streamlit as st
import controller.control as cl
import pandas as pd
import datetime

from pypfopt import black_litterman, risk_models
from pypfopt import BlackLittermanModel, plotting

def bla_setup():
    st.title('Black-Litterman Allocation')
    
    c1, c2 = st.columns((2, 1))

    c2.header('About')
    c2.info('::start:: Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industrys standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum')

    c1.header('Setup')

    invest_cash = c1.number_input('Purchase Power', min_value = 10, max_value = 100000000, value = 10, step = 50)

    # Start Date
    start_date = c1.date_input('Start date', datetime.date(2020, 1, 1))

    # List of Stocks
    list_of_stocks = c1.multiselect("Selct all tickers you want to have in the portfolio", cl.return_list_tickers())

    # Select how to perform the MVO
    covariance_methods = ["Sample Covariance", "Semi Covariance", "Exponentially-weighted Covariance", "Covariance Schrinkage: Ledoit Wolf", "Covariance Schrinkage: Ledoit Wolf Costant Variance", "Covariance Schrinkage: Ledoit Wolf Single Factor", "Covariance Schrinkage: Ledoit Wolf Constant Correlation", "Covariance Schrinkage: Oracle Approximation"]
    covariance_method_choosen = c1.selectbox("How should the covariance be calculated?", covariance_methods)

    # Expected Return Method
    expected_returns_methods = ["Mean Historical Return", "Exponential Moving Average", "CAPM Return"]
    expected_return_method_choosen = c1.selectbox("How should the expected return be calculated?", expected_returns_methods)

    st.markdown('---')

    if (len(list_of_stocks) > 0): 
        st.markdown('### Data Retrived')
        # Download price data from desired stocks
        df = cl.return_closed_prices(list_of_stocks, start_date).dropna(how="all")
        st.write(df)
        st.markdown('---')

        st.markdown('### Historical Adjusted Prices')
        st.line_chart(df)

        st.markdown('---')

        st.markdown('### Market Capitalization')
        marketCap = cl.return_market_capitalizations(list_of_stocks)
        # pd.DataFrame([marketCaps], list(marketCaps.keys()), ["Prices"])
        # st.write(marketCap)
        # st.bar_chart(marketCap)
        st.markdown('---')

        st.markdown('### Calculating Prior')
        S = risk_models.CovarianceShrinkage(pd.Series(df)).ledoit_wolf()
        delta = black_litterman.market_implied_risk_aversion(marketCap)
        st.write(delta)