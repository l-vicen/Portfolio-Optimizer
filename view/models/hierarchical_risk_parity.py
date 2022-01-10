# load needed packages
from pandas.core.frame import DataFrame
import streamlit as st
from scipy.linalg import block_diag 
import numpy as np

import controller.plots as myPlots
import controller.control as cl

import pandas as pd
import datetime

from pypfopt import expected_returns
from pypfopt import expected_returns
from pypfopt import HRPOpt
import models.backtesting as backTest
import models_dependencies.covariances as riskMatrix

from inform import Descriptions

from pypfopt import plotting
import matplotlib.pyplot as plt
import plotly.graph_objects as go

import seaborn as sns
from matplotlib import pyplot as plt
from inform import Descriptions

import models_dependencies.google_sheet as googleSheet

def hrp_setup_ex(c1, c2):
    
    #Amount of money that should be invested 
    invest_cash = c1.number_input('Purchase Power', min_value=10, max_value=100000000, value=10, step=50, help = Descriptions.LIST_PORTFOLIO_HELPER)

    # Start Date
    start_date = c1.date_input('Start date', datetime.date(2020, 1, 1), help = "Please select the start date from which you want to download the data ")

    # List of Stocks
    list_of_stocks = c1.multiselect("Selct all tickers you want to have in the portfolio", cl.return_list_tickers())

    if (len(list_of_stocks) > 0): 

        """Part[1]: We load the corresponding data for the selected tickers from yahoo finance and plot this data"""

        st.markdown('### Data Retireved')

        #Historical Adjusted Prices in table form 

        df = cl.return_closed_prices(list_of_stocks, start_date).dropna(how="all")
        st.write(np.log10(df))

        st.markdown('---')

        st.markdown('### Historical Adjusted Prices *')

        #Historical Adjusted Prices in graph form. Please note that a log scale is used 

        st.line_chart(np.log10(df))
        st.markdown('_*log scale is used_')

        st.markdown('---')

        """Part[2]: We perform the HRP using HROPT from pypfopt"""

        rets = expected_returns.returns_from_prices(df)
        hrp = HRPOpt(rets)
        hrp.optimize()
        weights = hrp.clean_weights()

        """Part[3]: Tree Clustering"""
        
        st.markdown('### 1. Tree Clustering')
        st.info(Descriptions.HRP_TREE_CLUSTERING)
        fig, ax = plt.subplots() 
        ax = plotting.plot_dendrogram(hrp)
        st.pyplot(fig)
        st.markdown('---')

        """Part[4]: QUASI DIAGONALIZATION"""

        st.markdown('### 2. Quasi Diagonalization')
        st.info(Descriptions.HRP_QUASI_DIAGNALIZATION)

        # Compute Correlation matrix 
        covarianceMatrixCalculated = riskMatrix.calculate_covariance_according_to(df, "Sample Covariance")
        correlationMatrixCalculated = riskMatrix.map_cov_to_corr(covarianceMatrixCalculated)
        st.write(correlationMatrixCalculated) 

        # Plot Heatmap
        fig = go.Figure(data=go.Heatmap(
                z= correlationMatrixCalculated,
                x= list_of_stocks,
                y= list_of_stocks,
                hoverongaps = False, 
                type = 'heatmap',
                colorscale = 'Viridis'))

        st.plotly_chart(fig)            
        st.markdown('---')

        # Generate a mask for the upper triangle
        mask = np.triu(np.ones_like(correlationMatrixCalculated , dtype=bool))

        cmap = sns.color_palette("viridis", as_cmap=True)

        # Set up the matplotlib figure
        f, ax2 = plt.subplots(figsize=(11, 9))

        # Draw the heatmap with the mask and correct aspect ratio
        sns.heatmap(correlationMatrixCalculated , cmap = cmap, mask=mask,  vmax=.3, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})
        st.pyplot(f)   
            
        st.markdown('---')

        """Part[5]: RECURSIVE BISECTION"""

        st.markdown('### 3. Recursive Bisection')
        st.info(Descriptions.HRP_RECURSIVE_BISECTION)

        # Plot weights 
        st.bar_chart(pd.Series(weights))

        # show weighs 
        st.write(weights)

        st.markdown('---')

        """Part[6]: Spare Porfolio Performance 
        Overview based on 3 KPIs: expected return, 
        annual volatility and sharpe ratio"""

        # Show calculated KPIs

        myPlots.plot_performance(hrp.portfolio_performance(verbose=True))

        st.markdown('---')

        """Part[7]: Backtesting Portfolio vs. SPY"""
        st.markdown('### 5. Backtesting')
        weightValues = weights.values()
        weightValuesList = list(weightValues)
        backTest.backtesting_setup(start_date, list_of_stocks, weightValuesList)

        # Decide whether or not to share
        share_portfolio(ef, list_of_stocks)


def hrp_setup_nubie(c1, c2):
    
    #Amount of money that should be invested 
    invest_cash = c1.number_input('Purchase Power', min_value=10, max_value=100000000, value=10, step=50, help = Descriptions.LIST_PORTFOLIO_HELPER)

    # Start Date
    start_date = c1.date_input('Start date', datetime.date(2020, 1, 1), help = "Please select the start date from which you want to download the data ")

    # List of Stocks
    list_of_stocks = c1.multiselect("Selct all tickers you want to have in the portfolio", cl.return_list_tickers())

    if (len(list_of_stocks) > 0): 

        """Part[1]: We load the corresponding data for the selected tickers from yahoo finance and plot this data"""

        st.markdown('### Data Retireved')

        #Historical Adjusted Prices in table form 

        df = cl.return_closed_prices(list_of_stocks, start_date).dropna(how="all")
        st.write(np.log10(df))

        st.markdown('---')

        st.markdown('### Historical Adjusted Prices *')

        #Historical Adjusted Prices in graph form. Please note that a log scale is used 

        st.line_chart(np.log10(df))
        st.markdown('_*log scale is used_')

        st.markdown('---')

        """Part[2]: We perform the HRP using HROPT from pypfopt"""

        rets = expected_returns.returns_from_prices(df)
        hrp = HRPOpt(rets)
        hrp.optimize()
        weights = hrp.clean_weights()

        """Part[3]: Spare Porfolio Performance 
        Overview based on 3 KPIs: expected return, 
        annual volatility and sharpe ratio"""

        # Show calculated KPIs

        myPlots.plot_performance(hrp.portfolio_performance(verbose=True))

        """Part[4]: Asset Distribution"""

        st.markdown('### Asset Distribution')

        # Plot weights 
        st.bar_chart(pd.Series(weights))

        # show weighs 
        st.write(weights)

        # Decide whether or not to share
        share_portfolio(hrp.portfolio_performance(), list_of_stocks)

def share_portfolio(hrp_performance, list_of_stocks):

    share = ['Dont Share', 'Share Portfolio']
    share_choice = st.radio('Let the world know about this Portfolio', share)

    if (share_choice == share[0]):
        st.error('Why not let the world benefit from your ideas ? :O')
    else:
        # Saving the expected performance from the current portfolio
        googleSheet.save_expected_performance(hrp_performance, list_of_stocks, "HRP")
        st.success('Success!')

def identify_user_experience(c1, c2):

    users = ['I dont even know who I am', 'I am a newbie', 'Go ProInvestor Experience']
    experience = c1.radio('Pick User Experience', users)

    if (experience == users[0]):
        c1.warning('You have to know who you are before we can start ;)')
    
    elif (experience == users[1]): 
        hrp_setup_nubie(c1, c2)
    
    else: 
        hrp_setup_ex(c1, c2)

def hrp_setup(): 

    st.title('Hierarchical Risk Parity Optimization')
    c1, c2 = st.columns((2, 1))

    c1.header('Setup')
    identify_user_experience(c1, c2)

    c2.header('About')
    c2.info(Descriptions.HRP)

    st.markdown('---')