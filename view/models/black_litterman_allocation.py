import numpy as np
import streamlit as st
import controller.control as cl
import pandas as pd
import datetime
import models_dependencies.covariances as riskMatrix

from pypfopt import black_litterman, risk_models
from pypfopt import BlackLittermanModel
from pypfopt import EfficientFrontier, objective_functions

import plotly.graph_objects as go
import plotly.express as px

def bla_setup():
    st.title('Black-Litterman Allocation')
    
    c1, c2 = st.columns((2, 1))

    c2.header('About')
    c2.info('::start:: Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industrys standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum')

    c1.header('Setup')

    # Start Date
    start_date = c1.date_input('Start date', datetime.date(2020, 1, 1))

    # List of Stocks
    list_of_stocks = c1.multiselect("Selct all tickers you want to have in the portfolio", cl.return_list_tickers())

    # Select how to perform the MVO
    covariance_methods = ["Sample Covariance", "Semi Covariance", "Exponentially-weighted Covariance", "Covariance Schrinkage: Ledoit Wolf", "Covariance Schrinkage: Ledoit Wolf Costant Variance", "Covariance Schrinkage: Ledoit Wolf Single Factor", "Covariance Schrinkage: Ledoit Wolf Constant Correlation", "Covariance Schrinkage: Oracle Approximation"]
    covariance_method_choosen = c1.selectbox("How should the covariance be calculated?", covariance_methods)
    
    st.markdown('---')

    if (len(list_of_stocks) > 0): 
        st.markdown('### Data Retrived')
        # Download price data from desired stocks
        df = cl.return_closed_prices(list_of_stocks, start_date).dropna(how="all")
        index = df. index
        st.write(df)
        st.markdown('---')

        st.markdown('### Historical Adjusted Prices')
        st.line_chart(df)

        st.markdown('---')

        st.markdown('### Market Capitalization')
        marketCap = cl.return_market_capitalizations(list_of_stocks)
        data_items = marketCap.items()
        data_list = list(data_items)
        dfMarketCap = pd.DataFrame(data_list, columns = ['Company', 'Capitalization'])
        st.write(dfMarketCap)
        st.markdown('---')

        st.markdown('### Calculating Prior')
        S = risk_models.CovarianceShrinkage(df, frequency=len(index)).ledoit_wolf()
        delta = black_litterman.market_implied_risk_aversion(df)
        st.write(delta)
        st.markdown('---')

        st.markdown("### Covariance Mtrix")
        correlationMatrixCalculated = riskMatrix.map_cov_to_corr(S)
        st.write(S)

        fig1 = go.Figure(data=go.Heatmap(
            z=correlationMatrixCalculated,
            x=list_of_stocks,
            y=list_of_stocks,
            hoverongaps=False,
            type='heatmap',
            colorscale='Viridis'))

        st.plotly_chart(fig1)
        st.markdown('---')

        st.markdown('### Market prior')
        market_prior = black_litterman.market_implied_prior_returns(marketCap, delta, S)
        st.write(market_prior)

        fig2 = go.Figure(go.Bar(
            x=market_prior,
            y=list_of_stocks,
            orientation='h'))
        st.plotly_chart(fig2)
        st.markdown('---')

        st.markdown('### Absolute views / expectations')
        # TODO: Can we move the input buttons here???
        viewdict = {}
        for i in list_of_stocks:
            viewdict[i] = st.number_input('view for ' + i, min_value=-0.001, max_value=10000.0, value=0.01, step=0.1)
        data_items = viewdict. items()
        data_list = list(data_items)
        viewdictDF = pd. DataFrame(data_list, columns = ['Company', 'View'])
        st.write(viewdictDF)
        bl = BlackLittermanModel(S, pi=market_prior, absolute_views=viewdict)
        st.markdown('---')

        st.markdown('### View confidences')
        # TODO: Can we move the input buttons here???
        confidences = {}
        for i in list_of_stocks:
            confidences[i] = st.slider('confidence for the view ' + i, min_value=0.01, max_value=1.0, value=0.01, step=0.1)
        data_items = confidences. items()
        data_list = list(data_items)
        confidencesDF = pd.DataFrame(data_list, columns = ['Company', 'Confidence'])
        st.write(confidencesDF)

        values_column = list(confidences.values()) # It is only the values list from the confidences dict, it is required like that by later methods from pyport.
        bl = BlackLittermanModel(S, pi=market_prior, absolute_views=viewdict, omega="idzorek", view_confidences=values_column)
        st.markdown('---')

        # TODO: Add variance of the view to the view DF
        st.markdown('### Variance of the views')
        omega = np.diag(bl.omega)
        st.write(omega)
        st.markdown('---')

        st.markdown('### Posterior estimates')
        # TODO: solve the issue with: ValueError: The truth value of a Series is ambiguous. Use a.empty, a.bool(), a.item(), a.any() or a.all().
        # We are using the shortcut to automatically compute market-implied prior
        #bl = BlackLittermanModel(S, pi="market", market_caps=marketCap, risk_aversion=delta, absolute_views=viewdict, omega=omega)
        #bl = BlackLittermanModel(S, pi="market", market_caps=marketCap, risk_aversion=delta, absolute_views=viewdict, omega=omega)
        # Posterior estimate of returns
        ret_bl = bl.bl_returns()
        #st.write(ret_bl)

        # Calculate the posterior estimate of the returns vector, given views on some assets
        rets_df = pd.DataFrame([market_prior, ret_bl, pd.Series(viewdict)],
                               index=["Prior", "Posterior", "Views"]).T
        st.write(rets_df)
        S_bl = bl.bl_cov()

        fig3 = px.histogram(rets_df, x=rets_df.index, y=["Prior", "Posterior", "Views"], barmode='group', labels=dict(x="Companies", y="Estimates", color="Estimates"))
        st.plotly_chart(fig3)
        st.markdown('---')

        st.markdown('### Portfolio allocation')
        ef = EfficientFrontier(ret_bl, S_bl)
        ef.add_objective(objective_functions.L2_reg)
        ef.max_sharpe()
        weights = ef.clean_weights()
        data_items = weights.items()
        data_list = list(data_items)
        weightsDF = pd. DataFrame(data_list, columns = ['Company', 'Weight in portfolio'])
        st.write(weightsDF)
        st.markdown('---')