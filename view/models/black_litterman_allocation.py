import numpy as np
from pandas.io.pytables import performance_doc
import streamlit as st
import controller.control as cl
import controller.plots as myPlots
import pandas as pd
import datetime

import models_dependencies.covariances as riskMatrix
from inform import Descriptions

from pypfopt import black_litterman, risk_models
from pypfopt import BlackLittermanModel
from pypfopt import EfficientFrontier, objective_functions
from pypfopt import DiscreteAllocation

import plotly.graph_objects as go
import plotly.express as px

def get_inputs(c1, c2):

    # Start Date
    start_date = c1.date_input('Start date', datetime.date(2020, 1, 1))

    # Initial investment
    init_investment = c1.number_input('Initial Investment', min_value = 10, max_value = 100000000, value = 1000, step = 50)

    # List of Stocks
    list_of_stocks = c1.multiselect("Selct all tickers you want to have in the portfolio", cl.return_list_tickers())

    market_prices = cl.return_closed_prices("SPY", start_date).dropna(how="all")
    
    risk_free_rate = 0.0163

    config_dictionary = dict(); 
    config_dictionary['start_date'] = start_date
    config_dictionary['init_investment'] = init_investment
    config_dictionary['list_of_stocks'] = list_of_stocks
    config_dictionary['market_prices'] = market_prices
    config_dictionary['risk_free_rate'] = risk_free_rate

    return config_dictionary


def model_executer_newbie(start_date, init_investment, list_of_stocks, market_prices, risk_free_rate,  c1, c2):

    if (len(list_of_stocks) > 0): 
        st.markdown('---')
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

        S = risk_models.CovarianceShrinkage(df, frequency=len(index)).ledoit_wolf()
        delta = black_litterman.market_implied_risk_aversion(market_prices, risk_free_rate = risk_free_rate)
  
        correlationMatrixCalculated = riskMatrix.map_cov_to_corr(S)

        market_prior = black_litterman.market_implied_prior_returns(marketCap, delta, S, risk_free_rate=risk_free_rate)

        st.markdown('### Absolute views / expectations')
        viewdict = {}
        for i in list_of_stocks:
            help = "Give your view on how you think your chosen stock will perform, eg. if you think " + i + " will perform +10%, type in “0,10”."
            viewdict[i] = st.number_input('view for ' + i, min_value=-10000.0, max_value=10000.0, value=0.00, step=0.1, help = help)
        data_items = viewdict. items()
        data_list = list(data_items)
        viewdictDF = pd. DataFrame(data_list, columns = ['Company', 'View'])
        bl = BlackLittermanModel(S, pi=market_prior, absolute_views=viewdict)
        st.markdown('---')

        st.markdown('### View confidences')
        confidences = {}
        for i in list_of_stocks:
            help = "Give your confidence in your view for " + i + " e.g. if you are 20% confident, type 0,2."
            confidences[i] = st.slider('confidence for the view ' + i, min_value=0.01, max_value=1.0, value=0.00, step=0.1, help = help)
        data_items = confidences. items()
        data_list = list(data_items)
        confidencesDF = pd. DataFrame(data_list, columns = ['Company', 'Confidence'])

        values_column = list(confidences.values()) # It is only the values list from the confidences dict, it is required like that by later methods from pyport.
        bl = BlackLittermanModel(S, pi=market_prior, absolute_views=viewdict, omega="idzorek", view_confidences=values_column)
        st.markdown('---')

        omegaSelf = np.diag(bl.omega)
        omega=bl.omega

        bl = BlackLittermanModel(S, pi="market", market_caps=marketCap, risk_aversion=delta, absolute_views=viewdict, omega=omega)
        ret_bl = bl.bl_returns()

        # Calculate the posterior estimate of the returns vector, given views on some assets
        rets_df = pd.DataFrame([market_prior, ret_bl, pd.Series(viewdict)],
                               index=["Prior", "Posterior", "Views"]).T
        st.write(rets_df)
        S_bl = bl.bl_cov()

        fig3 = px.histogram(rets_df, x=rets_df.index, y=["Prior", "Posterior", "Views"], barmode='group', labels=dict(x="Companies", y="Estimates", color="Estimates"))
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

        st.markdown('### Discrete allocation')
        da = DiscreteAllocation(weights, df.iloc[-1], total_portfolio_value=init_investment)
        alloc, leftover = da.lp_portfolio()
        data_items = alloc.items()
        data_list = list(data_items)
        allocDF = pd. DataFrame(data_list, columns = ['Company', 'Stocks in portfolio'])
        st.write(allocDF)
        st.write(f"Leftover: ${leftover:.2f}")
        st.markdown('---')

        st.markdown('### Portfolio performance')
        bl.bl_weights(risk_aversion=None)
        performance=bl.portfolio_performance(True, risk_free_rate=risk_free_rate)
        myPlots.plot_performance(performance)

def model_executer_pro(start_date, init_investment, list_of_stocks, market_prices, risk_free_rate,  c1, c2):
 
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

        st.markdown('### Market-implied risk premium') 
  
        st.info("Every asset in the market portfolio contributes a certain amount of risk to the portfolio. Standard theory suggests that investors must becompensated for the risk that they take, so we can attribute to each asset an expected compensation(i.e prior estimate of returns). This is quantified by the market-implied risk premium, which is the market’s excess return divided by its variance.")
        S = risk_models.CovarianceShrinkage(df, frequency=len(index)).ledoit_wolf()
        delta = black_litterman.market_implied_risk_aversion(market_prices, risk_free_rate = risk_free_rate)
        st.write(delta)
        st.markdown('---')

        st.markdown("### Covariance Matrix")
        help = "Calculated by using Covariance Shrinkage Ledoit Wolf"

        st.info(help)
        correlationMatrixCalculated = riskMatrix.map_cov_to_corr(S)
        st.write(S)
        st.markdown('---')

        st.markdown("### Correlation Matrix")
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

        st.info("Market prior is market’s estimate of the return, which is embedded into the market capitalisation of the asset. In this case it is calculated by using S&P 500 index for calculating the expected market return rate and FED risk-free rate (currently" + str(risk_free_rate) + ") for calculating the market risk premium. ")
        market_prior = black_litterman.market_implied_prior_returns(marketCap, delta, S, risk_free_rate=risk_free_rate)
        st.write(market_prior)

        fig2 = go.Figure(go.Bar(
            x=market_prior,
            y=list_of_stocks,
            orientation='h'))

        st.plotly_chart(fig2)
        st.markdown('---')

        st.markdown('### Absolute views / expectations')
        viewdict = {}
        for i in list_of_stocks:
            help = "Give your view on how you think your chosen stock will perform, eg. if you think " + i + " will perform +10%, type in “0,10”."
            viewdict[i] = st.number_input('view for ' + i, min_value=-10000.0, max_value=10000.0, value=0.00, step=0.1, help = help)
        data_items = viewdict. items()
        data_list = list(data_items)
        viewdictDF = pd. DataFrame(data_list, columns = ['Company', 'View'])
        # st.write(viewdictDF)
        bl = BlackLittermanModel(S, pi=market_prior, absolute_views=viewdict)
        st.markdown('---')

        st.markdown('### View confidences')
        confidences = {}
        for i in list_of_stocks:
            help = "Give your confidence in your view for " + i + " e.g. if you are 20% confident, type 0,2."
            confidences[i] = st.slider('confidence for the view ' + i, min_value=0.01, max_value=1.0, value=0.00, step=0.1, help = help)
        data_items = confidences. items()
        data_list = list(data_items)
        confidencesDF = pd. DataFrame(data_list, columns = ['Company', 'Confidence'])
        # st.write(confidencesDF)

        values_column = list(confidences.values()) # It is only the values list from the confidences dict, it is required like that by later methods from pyport.
        bl = BlackLittermanModel(S, pi=market_prior, absolute_views=viewdict, omega="idzorek", view_confidences=values_column)
        st.markdown('---')

        #st.markdown('### The covariance of the investor views (Omega)')
        omegaSelf = np.diag(bl.omega)
        # st.write(omegaSelf)
        omega=bl.omega

        fig4 = go.Figure(data=go.Heatmap(
            z=omega,
            x=list_of_stocks,
            y=list_of_stocks,
            hoverongaps=False,
            type='heatmap',
            colorscale='Viridis'))

        #st.plotly_chart(fig4)

        st.markdown('---')

        st.markdown('### Posterior estimates')
     
        st.info("The posterior estimates are the actual outputs of the Black-Litterman. They can be then used as an input for an optimizer  (Efficient Frontier in this case).")
        bl = BlackLittermanModel(S, pi="market", market_caps=marketCap, risk_aversion=delta, absolute_views=viewdict, omega=omega)
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

        st.markdown('### Discrete allocation')
        da = DiscreteAllocation(weights, df.iloc[-1], total_portfolio_value=init_investment)
        alloc, leftover = da.lp_portfolio()
        data_items = alloc.items()
        data_list = list(data_items)
        allocDF = pd. DataFrame(data_list, columns = ['Company', 'Stocks in portfolio'])
        st.write(allocDF)
        st.write(f"Leftover: ${leftover:.2f}")
        st.markdown('---')

        st.markdown('### Portfolio performance')
        bl.bl_weights(risk_aversion=None)
        performance=bl.portfolio_performance(True, risk_free_rate=risk_free_rate)
        myPlots.plot_performance(performance)


def share_portfolio(ef, list_of_stocks, c1, c2):
    share = ['Dont Share', 'Share Portfolio']
    share_choice = c1.radio('Let the world know about this Portfolio', share)

    if (share_choice == share[0]):
        c1.error('Why not let the world benefit from your ideas ? :O')
    else:
        googleSheet.save_expected_performance(ef.portfolio_performance(), list_of_stocks, "BLA")
        c1.success('Success!')

def identify_user_experience(c1, c2):

    users = ['I dont even know who I am', 'I am a newbie', 'Go ProInvestor Experience']
    experience = c1.radio('Pick User Experience', users)

    if (experience == users[0]):
        c1.warning('You have to know who you are before we can start ;)')

    elif (experience == users[1]):
        newbie_config = get_inputs(c1, c2)
        model_executer_newbie(newbie_config.get('start_date'), newbie_config.get('init_investment'), newbie_config.get('list_of_stocks'), newbie_config.get('market_prices'), newbie_config.get('risk_free_rate'),  c1, c2)
    else:
        pro_config = get_inputs(c1, c2)
        model_executer_pro(pro_config.get('start_date'), pro_config.get('init_investment'),pro_config.get('list_of_stocks'), pro_config.get('market_prices'), pro_config.get('risk_free_rate'),  c1, c2)

def bla_setup():

    st.title('Black-Litterman Allocation')

    c1, c2 = st.columns((2, 1))

    c1.header('Setup')
    identify_user_experience(c1, c2)

    c2.header('About')
    c2.info(Descriptions.BLA)

    st.markdown('---')