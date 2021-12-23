import streamlit as st
import controller.control as cl
import controller.plots as myPlots

from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt import plotting
from pypfopt import EfficientFrontier
from pypfopt import DiscreteAllocation

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

import plotly.graph_objects as go
import plotly.express as px

def mean_variance_setup():
    st.title('Mean Variance Optimization')

    c1, c2 = st.columns((2, 1))

    c2.header('About')
    c2.info('Mean-Variance Optimization helps investors understand the trade-off between expected returns and risk for a given portfolio. Here: ')

    c1.header('Setup')

    invest_cash = c1.number_input('Purchase Power', min_value = 10, max_value = 100000000, value = 10, step = 50)

    # Start Date
    start_date = c1.date_input('Start date', datetime.date(2020, 1, 1))

    # List of Stocks
    list_of_stocks = c1.multiselect("Selct all tickers you want to have in the portfolio", cl.return_list_tickers())

    # Select how to perform the MVO
    list_covariance_options = c1.selectbox("How should the covariance be calculated?", ["Sample Covariance", "Covariance Shrinkage: Ledoit Wolf", "Semi Covariance", "Exponential Covariance", "Ledoitn Wolf Constant Variance", "Ledoit Wolf Single Factor", "Ledoit Wolf Constant Correlation", "Oracle Approximatiion"])

    # Expected Return Method
    list_expected_returns = c1.selectbox("How should the expected return be calculated?", ["Mean Historical Return", "Exponential Moving Average", "CAPM Return"])

    st.markdown('---')

    if (len(list_of_stocks) > 0): 
        # Download price data from desired stocks
        st.markdown('### Data Retireved')
        df = cl.return_closed_prices(list_of_stocks, start_date).dropna(how="all")
        st.write(df)

        st.markdown('---')

        st.markdown('### Historical Adjusted Prices')
        st.line_chart(df)

        st.markdown('---')

        if (list_covariance_options == "Sample Covariance"):
            st.markdown("### Sample Covariance")
            sample_cov = risk_models.sample_cov(df, frequency=252)
            st.write(sample_cov)

            fig = go.Figure(data=go.Heatmap(
                   z= sample_cov,
                   x= list_of_stocks,
                   y= list_of_stocks,
                   hoverongaps = False, 
                   type = 'heatmap',
                   colorscale = 'Viridis'))

            st.plotly_chart(fig)
            # figOne, ax = plt.subplots()
            # sns.heatmap(sample_cov.corr(), ax=ax)
            # st.write(figOne)

        else:
            st.markdown("### Covariance Schrinkage")
            S = risk_models.CovarianceShrinkage(df).ledoit_wolf()
            fig = go.Figure(data=go.Heatmap(
                   z= S,
                   x= list_of_stocks,
                   y= list_of_stocks,
                   hoverongaps = False),
                   type = 'heatmap',
                   colorscale = 'Viridis')
            st.plotly_chart(fig)
            
        st.markdown('---')

        st.markdown('### Expected Returns')
        mu = expected_returns.capm_return(df)

        st.write(mu)
        st.bar_chart(mu)

        st.markdown('---')
        st.markdown('### Weight Distribution')
        S = risk_models.CovarianceShrinkage(df).ledoit_wolf()
        # You don't have to provide expected returns in this case
        ef = EfficientFrontier(None, S, weight_bounds=(None, None))
        ef.min_volatility()
        weights = ef.clean_weights()

        st.write(weights)
        st.bar_chart(pd.Series(weights))

        st.markdown('##### Annual Volatility')
        myPlots.plot_performance(ef.portfolio_performance(verbose=True))
        
        st.markdown('---')
        st.markdown('### Discrete Allocation')

        latest_prices = df.iloc[-1]  # prices as of the day you are allocating
        da = DiscreteAllocation(weights, latest_prices, total_portfolio_value = invest_cash, short_ratio = 0.3)
        alloc, leftover = da.lp_portfolio()
        st.write(f"Discrete allocation performed with ${leftover:.2f} leftover")
        st.bar_chart(pd.Series(alloc))

        st.markdown('---')
        st.markdown('### Efficient Frontier')

        n_samples = 1000
        w = np.random.dirichlet(np.ones(len(mu)), n_samples)
        rets = w.dot(mu)
        stds = np.sqrt((w.T * (S @ w.T)).sum(axis=0))
        sharpes = rets / stds

        print("Sample portfolio returns:", rets)
        print("Sample portfolio volatilities:", stds)

        # Plot efficient frontier with Monte Carlo sim
        ef = EfficientFrontier(mu, S)

        fig, ax = plt.subplots()
        plotting.plot_efficient_frontier(ef, ax=ax, show_assets=False)

        # Find and plot the tangency portfolio
        # ef.max_sharpe()
        ret_tangent, std_tangent, _ = ef.portfolio_performance()
        ax.scatter(std_tangent, ret_tangent, marker="*", s = 10, c="r", label="Max Sharpe")

        # Plot random portfolios
        ax.scatter(stds, rets, marker=".", c=sharpes, cmap="viridis_r")

        # Format
        ax.set_title("Efficient Frontier with random portfolios")
        ax.legend()
        plt.tight_layout()
        st.plotly_chart(fig)

        st.markdown('---')
        st.markdown('### Minimizing Risk & Target Return')
        ef = EfficientFrontier(mu, S, weight_bounds=(None, None))

        # TODO: Add objective which is some sort of constraint (e.g. sector)

        ef.efficient_return(target_return=0.07, market_neutral=True)
        weights = ef.clean_weights()
        st.write('New Weights')
        st.write(pd.Series(weights))
        st.bar_chart(pd.Series(weights))



