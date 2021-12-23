import streamlit as st
import controller.control as cl
import controller.plots as myPlots
import models_dependencies.expected_returns as expectedReturn
import models_dependencies.covariances as riskMatrix

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
    covariance_methods = ["Sample Covariance", "Semi Covariance", "Exponentially-weighted Covariance", "Covariance Schrinkage: Ledoit Wolf", "Covariance Schrinkage: Ledoit Wolf Costant Variance", "Covariance Schrinkage: Ledoit Wolf Single Factor", "Covariance Schrinkage: Ledoit Wolf Constant Correlation", "Covariance Schrinkage: Oracle Approximation"]
    covariance_method_choosen = c1.selectbox("How should the covariance be calculated?", covariance_methods)

    # Expected Return Method
    expected_returns_methods = ["Mean Historical Return", "Exponential Moving Average", "CAPM Return"]
    expected_return_method_choosen = c1.selectbox("How should the expected return be calculated?", expected_returns_methods)

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


        """[PART 1] In this part we calculate the 
        covariance matrix for given price dataframe
        and according to specific covariance method 
        selected. """

        st.markdown("### Covariance Mtrix")
        covarianceMatrixCalculated = riskMatrix.calculate_covariance_according_to(df, covariance_method_choosen)
        st.write(covarianceMatrixCalculated)

        fig = go.Figure(data=go.Heatmap(
                z= covarianceMatrixCalculated,
                x= list_of_stocks,
                y= list_of_stocks,
                hoverongaps = False, 
                type = 'heatmap',
                colorscale = 'Viridis'))

        st.plotly_chart(fig)            
        st.markdown('---')


        """[PART 2] In this part we calculate the 
        expected return for given price dataframe
        and according to specific expected return
        method selected. """

        st.markdown('### Expected Returns')
        expectedReturnCalculate = expectedReturn.calculate_expected_return_according_to(df, expected_return_method_choosen)
        st.write(expectedReturnCalculate)
        st.bar_chart(expectedReturnCalculate)
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



