from contextlib import nullcontext
from urllib.parse import uses_relative
import streamlit as st


import controller.control as cl
import controller.plots as myPlots

import models_dependencies.expected_returns as expectedReturn
import models_dependencies.covariances as riskMatrix
import models_dependencies.objectives as objective
import models_dependencies.google_sheet as googleSheet

import models.backtesting as backTest

from pypfopt import DiscreteAllocation

import pandas as pd
import numpy as np
import datetime

import plotly.graph_objects as go

from inform import Descriptions

def stock_search(c1, c2):

    # List of Stocks
    search = ['Create Portfolio Using Company Name', 'Create Portfolio Using Tickers']
    search_choice = c1.radio('Search stock data based on Ticker or Company Name', search)

    if (search_choice == search[0]):

        list_of_stocks = c1.multiselect("Selct all companies you want to have in the portfolio",
                                    cl.return_list_tickers_only_names(),
                                    default=googleSheet.load_tickers(),
                                    on_change=googleSheet.change())

    
        return cl.mutter(list_of_stocks)

    else:
        list_of_stocks = c1.multiselect("Selct all tickers you want to have in the portfolio",
                                    cl.return_list_tickers(),
                                    default=googleSheet.load_tickers(),
                                    on_change=googleSheet.change())

        
        st.write(list_of_stocks)
        return list_of_stocks

def get_inputs_newbie(c1, c2):
    
    # Start Date
    start_date = c1.date_input('Start date', datetime.date(2020, 1, 1), help="deine mutter")

    # List of Stocks
    list_of_stocks = stock_search(c1, c2)
    
    c1.warning('Default Methods used: Mean Historical Return & Sample Covariance')

    # Pick Objective Functions
    objective_functions = ["Minimize Volatility", "Maximize Sharpe Ratio", "Maximize Quadratic Utility", "Efficient Risk", "Efficient Return"]
    objective_function_choosen = c1.selectbox("What is your optimization objective?", objective_functions)

    config_dictionary = dict(); 
    config_dictionary['start_date'] = start_date
    config_dictionary['list_of_stocks'] = list_of_stocks
    config_dictionary['covariance_method_choosen'] = 'Sample Covariance'
    config_dictionary['expected_return_method_choosen'] = 'Mean Historical Return'
    config_dictionary['objective_function_choosen'] = objective_function_choosen
    config_dictionary['add_regularization'] = "No"
    config_dictionary['tunning_factor_choosen'] = 0

    return config_dictionary


def get_inputs_pro(c1, c2):
    
    # Start Date
    start_date = c1.date_input('Start date', datetime.date(2020, 1, 1), help="deine mutter")

    # List of Stocks
    list_of_stocks = stock_search(c1, c2)

    # Select how to perform the MVO
    covariance_methods = ["Sample Covariance", "Semi Covariance", "Exponentially-weighted Covariance", "Covariance Schrinkage: Ledoit Wolf", "Covariance Schrinkage: Ledoit Wolf Costant Variance", "Covariance Schrinkage: Ledoit Wolf Single Factor", "Covariance Schrinkage: Ledoit Wolf Constant Correlation", "Covariance Schrinkage: Oracle Approximation"]
    covariance_method_choosen = c1.selectbox("How should the covariance be calculated?", covariance_methods, help = "e.g. AAPL for Apple Inc.")

    # Expected Return Method
    expected_returns_methods = ["Mean Historical Return", "Exponential Moving Average", "CAPM Return"]
    expected_return_method_choosen = c1.selectbox("How should the expected return be calculated?", expected_returns_methods, help = "")

    # Pick Objective Functions
    objective_functions = ["Minimize Volatility", "Maximize Sharpe Ratio", "Maximize Quadratic Utility", "Efficient Risk", "Efficient Return"]
    objective_function_choosen = c1.selectbox("What is your optimization objective?", objective_functions)

    regularization_options = ["Yes", "No"]
    add_regularization = c1.select_slider("Shoult the optimization have L2 Regularization?", regularization_options, value = "No")

    if (add_regularization == "Yes"):
        tunning_factor_choosen = c1.slider("Choose L2 Tunning Factor", min_value=0.1, max_value=1.0)
    else:
        tunning_factor_choosen = 0

    config_dictionary = dict(); 
    config_dictionary['start_date'] = start_date
    config_dictionary['list_of_stocks'] = list_of_stocks
    config_dictionary['covariance_method_choosen'] = covariance_method_choosen
    config_dictionary['expected_return_method_choosen'] = expected_return_method_choosen
    config_dictionary['objective_function_choosen'] = objective_function_choosen
    config_dictionary['add_regularization'] = add_regularization
    config_dictionary['tunning_factor_choosen'] = tunning_factor_choosen

    return config_dictionary


def model_executer(start_date, list_of_stocks, covariance_method_choosen, expected_return_method_choosen, objective_function_choosen, add_regularization, tunning_factor_choosen, c1, c2):
    
    if len(list_of_stocks) > 0:

        # Save current portfolio
        googleSheet.save_tickers(list_of_stocks)

        """[PART 0] In this part we retrieve 
        and plot data from yahooFinanace. The
        data is on the adjusted closed prices."""

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

        st.markdown("### Correlation Matrix")
        covarianceMatrixCalculated = riskMatrix.calculate_covariance_according_to(df, covariance_method_choosen)
        correlationMatrixCalculated = riskMatrix.map_cov_to_corr(covarianceMatrixCalculated)
        st.write(correlationMatrixCalculated)

        fig = go.Figure(data=go.Heatmap(
                z= correlationMatrixCalculated,
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
        expectedReturnCalculated = expectedReturn.calculate_expected_return_according_to(df, expected_return_method_choosen)
        st.write(expectedReturnCalculated)
        st.bar_chart(expectedReturnCalculated)
        st.markdown('---')

        """[PART 3] In this part we run the optimization
        setup selected in setup. """

        st.markdown('### Asset Distribution')

        ef = objective.calculate_asset_distribution_according_to(objective_function_choosen, add_regularization, tunning_factor_choosen ,expected_returns = expectedReturnCalculated, covariance_matrix = covarianceMatrixCalculated)

        asset_distribution = ef.clean_weights()
        st.write(asset_distribution)
        st.bar_chart(pd.Series(asset_distribution))
        st.markdown('---')

        """[PART 4] Spare Porfolio Performance 
        Overview based on 3 KPIs: expected return, 
        annual volatility and sharpe ratio."""

        st.markdown('##### Annual Performance Expectations')
        myPlots.plot_performance(ef.portfolio_performance(verbose=True))
        st.info(Descriptions.SHARPE_RATIO)
        st.markdown('---')
        
        """[PART 5] Discretionizing asset distribution
        such that in case brokeragge does not allow
        partial shares."""

        st.markdown('### Discrete Allocation')

        latest_prices = df.iloc[-1]  # prices as of the day you are allocating
        discreteAllocation = DiscreteAllocation(asset_distribution, latest_prices, total_portfolio_value=20000, short_ratio=0.3)
        allocation, leftover = discreteAllocation.lp_portfolio()
        st.write(f"Discrete allocation performed with ${leftover:.2f} leftover")
        st.write(allocation)

         
        """[PART 6] Plotting simulated portfolios"""

        st.markdown('---')
        st.markdown('### Efficient Frontier')

        n_samples = 1000

        weight = np.random.dirichlet(np.ones(len(expectedReturnCalculated)), n_samples).round(2)

        weigths_df = pd.DataFrame(weight)
        weigths_df['String Weight'] = weigths_df[weigths_df.columns[0:]].apply( lambda x: ', '.join(x.dropna().astype(str)), axis=1)
        #st.write("Weights:", weigths_df)

        rets = weight.dot(expectedReturnCalculated)
        stds = np.sqrt((weight.T * (covarianceMatrixCalculated @ weight.T)).sum(axis=0))
        sharpes = rets / stds

        # st.write("Sample portfolio returns:", rets)
        # st.write("Sample portfolio volatilities:", stds)
        # st.write(sharpes)

        #-- Plot the risk vs. return of randomly generated portfolios
        #-- Convert the list from before into an array for easy plotting
        ef_df = pd.DataFrame(list(zip(stds, rets, sharpes)), columns=['Volatility','Returns', 'Sharpes'])
        #st.write(ef_df)

        df_result = pd.concat([ef_df, weigths_df], axis=1)

        #st.write(df_result)
        tickesString = '[' + ', '.join(list_of_stocks) + ']'
        df_result['Portfolio'] = tickesString

        fig = go.Figure()
        fig.add_trace(go.Scatter(x = ef_df['Volatility'], y = ef_df['Returns'], 
                            marker = dict(color = ef_df['Sharpes'], 
                                        showscale=True, 
                                        size=7,
                                        line=dict(width=1),
                                        colorscale="RdBu",
                                        colorbar=dict(title="Sharpe<br>Ratio")
                                        ), 
                            mode='markers',
                            showlegend=False,
                            text=[df_result['Portfolio'][i] + "<br>" + '[' + df_result['String Weight'][i] + ']'  for i in range(n_samples)]))

        optimal = ef.portfolio_performance(verbose=True)
        optimalList = list(optimal)

        for t in range(len(optimalList)):
            optimalList[t] = optimalList[t].round(2)

        fig.add_trace(go.Scatter(x = [optimalList[1]], y = [optimalList[0]],   
                             mode = 'markers',
                             marker = dict(color='gold', size = 10, symbol = 'diamond'), 
                             name = 'Optimal Portfolio'))

        fig.update_layout(template='plotly_white',
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                        xaxis=dict(title='Annualised Risk (Volatility)'),
                        yaxis=dict(title='Annualised Return'),
                        title='Sample of Random Portfolios',
                        width=850,
                        height=500)
        fig.update_layout(coloraxis_colorbar=dict(title="Sharpe Ratio"))
        st.plotly_chart(fig)

        st.markdown('---')

        weightValues = asset_distribution.values()
        weightValuesList = list(weightValues)

        """[PART 7] Backtesting Portfolio vs. SPY"""
        backTest.backtesting_setup(start_date, list_of_stocks, weightValuesList, c1, c2)

        # Saving the expected performance from the current portfolio
        share_portfolio(ef, list_of_stocks, c1, c2)


def share_portfolio(ef, list_of_stocks, c1, c2):
    share = ['Dont Share', 'Share Portfolio']
    share_choice = c1.radio('Let the world know about this Portfolio', share)

    if (share_choice == share[0]):
        c1.error('Why not let the world benefit from your ideas ? :O')
    else:
        googleSheet.save_expected_performance(ef.portfolio_performance(), list_of_stocks, "MVO")
        c1.success('Success!')
        


def identify_user_experience(c1, c2):

    users = ['I dont even know who I am', 'I am a newbie', 'Go ProInvestor Experience']
    experience = c1.radio('Pick User Experience', users)

    if (experience == users[0]):
        c1.warning('You have to know who you are before we can start ;)')

    elif (experience == users[1]):
        newbie_config = get_inputs_newbie(c1, c2)
        model_executer(newbie_config.get('start_date'), newbie_config.get('list_of_stocks'), newbie_config.get('covariance_method_choosen'), newbie_config.get('expected_return_method_choosen'), newbie_config.get('objective_function_choosen'), newbie_config.get('add_regularization'), newbie_config.get('tunning_factor_choosen'), c1, c2)

    else:
        pro_config = get_inputs_pro(c1, c2)
        model_executer(pro_config.get('start_date'), pro_config.get('list_of_stocks'), pro_config.get('covariance_method_choosen'), pro_config.get('expected_return_method_choosen'), pro_config.get('objective_function_choosen'), pro_config.get('add_regularization') ,pro_config.get('tunning_factor_choosen'), c1, c2)
        
def mean_variance_setup():

    st.title('Mean Variance Optimization')

    c1, c2 = st.columns((2, 1))

    c1.header('Setup')
    identify_user_experience(c1, c2)

    c2.header('About')
    c2.info(Descriptions.MVO)

    st.markdown('---')




