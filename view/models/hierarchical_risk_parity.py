# load needed packages
from pandas.core.frame import DataFrame
import streamlit as st
from scipy.linalg import block_diag 
import numpy as np

import controller.plots as myPlots
import controller.control as cl

import plotly.figure_factory as ff
import plotly.express as px

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
import scipy.cluster.hierarchy as sch

import seaborn as sns
from matplotlib import pyplot as plt

def hrp_setup():
    st.title('Hierarchical Risk Parity Optimization')
    c1, c2 = st.columns((2, 1))
    c2.header('About')
    c2.info(Descriptions.HRP)
    c1.header('Setup')

    invest_cash = c1.number_input('Purchase Power', min_value=10, max_value=100000000, value=10, step=50, help = "choose how much money you want to invest ")

    # Start Date
    start_date = c1.date_input('Start date', datetime.date(2020, 1, 1), help = "Please select the start date from which you want to download the data ")

    # List of Stocks
    list_of_stocks = c1.multiselect("Selct all tickers you want to have in the portfolio", cl.return_list_tickers())


    st.markdown('---')

    if (len(list_of_stocks) > 0): 

        st.markdown('### Data Retireved')
        df = cl.return_closed_prices(list_of_stocks, start_date).dropna(how="all")
        st.write(df)

        st.markdown('---')

        st.markdown('### Historical Adjusted Prices')
        st.line_chart(df)
        rets = expected_returns.returns_from_prices(df)

        hrp = HRPOpt(rets)
        hrp.optimize()
        weights = hrp.clean_weights()

        st.markdown('---')
        
        st.markdown('### 1. TREE CLUSTERING')
        st.markdown("In this part similar investments are grouped together based on their correlation matrix. This step breaks down the  assets in our portfolio into different hierarchical clusters using the famous Hierarchical Tree Clustering algorithm")

        fig, ax = plt.subplots() 
        ax = plotting.plot_dendrogram(hrp)
        st.pyplot(fig)

        """ Alternative way to plot the dendogram """
        # ax = plt.gca()
        # sch.dendrogram(hrp.clusters, labels=hrp.tickers, ax=ax, orientation="top")
        # ax.tick_params(axis="x", rotation=90)
        # plt.tight_layout()
        # st.pyplot(ax)

        st.markdown('---')
        st.markdown('### 2. QUASI DIAGONALIZATION')
        st.markdown("In this part it is nothing more than a simple seriation algorithm. A statistical technique which is used to rearrange the data to show the inherent clusters clearly")

        covarianceMatrixCalculated = riskMatrix.calculate_covariance_according_to(df, "Sample Covariance")
        correlationMatrixCalculated = riskMatrix.map_cov_to_corr(covarianceMatrixCalculated)
        st.write(correlationMatrixCalculated) 

        # Compute the correlation matrix
        corr = correlationMatrixCalculated 

        # Generate a mask for the upper triangle
        mask = np.triu(np.ones_like(corr, dtype=bool))

        # Set up the matplotlib figure
        f, ax2 = plt.subplots(figsize=(11, 9))

        #        Generate a custom diverging colormap
        cmap = sns.diverging_palette(230, 20, as_cmap=True)

        # Draw the heatmap with the mask and correct aspect ratio
        sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})
        
        st.pyplot(f)   

        #copyOfDf = df.iloc[:,1:] 
        #st.write(copyOfDf)
        #ax2 = sns.clustermap(copyOfDf, metric="euclidean", standard_scale=1, method="single")
            
        st.markdown('---')

        st.markdown('### 3. RECURSIVE BISECTION')
        st.markdown("The final step of the algorithm then calculates the weight for each of the assets using a recursive bi-sectioning procedure of the reordered covariance matrix")

        st.bar_chart(pd.Series(weights))
        st.write(weights)

        st.markdown('---')
        st.markdown('### 4. EXPECTED PERFORMANCE')

        myPlots.plot_performance(hrp.portfolio_performance(verbose=True))

        st.markdown('---')
        st.markdown('### 5. Backtesting')

        
        weightValues = weights.values()
        weightValuesList = list(weightValues)
        backTest.backtesting_setup(start_date, list_of_stocks, weightValuesList, c1, c2)



def hrp_setup_nubie():
    st.title('Hierarchical Risk Parity Optimization')
    c1, c2 = st.columns((2, 1))
    c2.header('About')
    c2.info(Descriptions.HRP)
    c1.header('Setup')

    invest_cash = c1.number_input('Purchase Power', min_value=10, max_value=100000000, value=10, step=50, help = "choose how much money you want to invest ")

    # Start Date
    start_date = c1.date_input('Start date', datetime.date(2020, 1, 1), help = "Please select the start date from which you want to download the data ")

    # List of Stocks
    list_of_stocks = c1.multiselect("Selct all tickers you want to have in the portfolio", cl.return_list_tickers())

    st.markdown('---')

    if (len(list_of_stocks) > 0): 

        st.markdown('### Data Retireved')
        df = cl.return_closed_prices(list_of_stocks, start_date).dropna(how="all")

        st.markdown('---')

        st.markdown('### Historical Adjusted Prices')
        st.line_chart(df)

        st.markdown('---')
        rets = expected_returns.returns_from_prices(df)

        hrp = HRPOpt(rets)
        hrp.optimize()
        weights = hrp.clean_weights()

        st.markdown('---')

        st.markdown('### EXPECTED PERFORMANCE')

        myPlots.plot_performance(hrp.portfolio_performance(verbose=True))

        st.markdown('---')

        st.markdown('### ASSET DISTRIBUTION')
        st.bar_chart(pd.Series(weights))
        st.write(weights) 
 
def identify_user_experience(c1, c2):

    users = ['I dont even know who I am', 'I am a newbie', 'Go ProInvestor Experience']
    experience = c1.radio('Pick User Experience', users)

    if (experience == users[0]):
        c1.warning('You have to know who you are before we can start ;)')
    
    if (experience == users[1]): 
        hrp_setup_nubie()
    
    else: 
        hrp_setup()


        

    
        

        


