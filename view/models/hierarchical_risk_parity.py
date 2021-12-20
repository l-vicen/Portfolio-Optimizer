# load needed packages
import streamlit as st
from pypfopt import expected_returns

import controller.plots as myPlots
import controller.control as cl

import plotly.figure_factory as ff
import plotly.express as px

import pandas as pd
import numpy as np

from pypfopt import expected_returns
from pypfopt import HRPOpt


def hrp_setup():
    st.title('Hierarchical Risk Parity Optimization')
    c1, c2 = st.columns((2, 1))
    c2.header('About')
    c2.info('the hierarchical risk parity have three major steps:' + '\n'
                + '1. TREE CLUSTERING' + ' \n'
                + 'Similar investments are grouped together based on their correlation matrix. This step breaks down the assets in our portfolio into different hierarchical clusters using the famous Hierarchical Tree Clustering algorithm' + '\n'
                + '2. QUASI DIAGONALIZATION' + '\n'
                + 'It is nothing more than a simple seriation algorithm, a statistical technique which is used to rearrange the data to show the inherent clusters clearly' + '\n'
                + '3. RECURSIVE BISECTION' + '\n'
                + 'The final step of the algorithm then calculates the weight for each of the assets using a recursive bi-sectioning procedure of the reordered covariance matrix')
    c1.header('Setup')

    invest_cash = c1.number_input('Purchase Power', min_value=10, max_value=100000000, value=10, step=50)

    # Start Date
    start_date = c1.date_input('Start date')

    # End Date
    end_date = c1.date_input('End date')

    # List of Stocks
    list_of_stocks = c1.multiselect("Selct all tickers you want to have in the portfolio", cl.return_list_tickers())
    st.markdown('---')

    if (len(list_of_stocks) > 0): 
        st.markdown('### Data Retrived')
        # Download price data from desired stocks
        df = cl.return_closed_prices(list_of_stocks, start_date).dropna(how="all")

        ## financial insights
        st.write(df)
        st.markdown('---')
        st.markdown('### Historical Adjusted Prices')
        st.line_chart(df)
        st.markdown('---')

        rets = expected_returns.returns_from_prices(df)

        hrp = HRPOpt(rets)
        hrp.optimize()
        weights = hrp.clean_weights()

        st.markdown('---')
        st.markdown('1. TREE CLUSTERING')

        st.write(hrp.tickers)
        st.write(len(hrp.tickers))
        st.write(hrp.clusters)
        st.write(hrp.weights)

        fig = ff.create_dendrogram(hrp.clusters, orientation='bottom')
        fig.update_layout(width=800, height=500)
        st.plotly_chart(fig)

        st.markdown('---')
        st.markdown('2. QUASI DIAGONALIZATION')

        st.write(hrp.cov_matrix)

        # fig = px.scatter_matrix( hrp.cov_matrix, dimensions=hrp.tickers, color="species")
        # fig.update_traces(diagonal_visible=False)
        # st.plotly_chart(fig)

        st.markdown('---')
        st.markdown('3. RECURSIVE BISECTION')
        st.write(weights)
        st.bar_chart(pd.Series(weights))

        st.markdown('---')
        st.markdown('4. EXPECTED PERFORMANCE')

        myPlots.plot_performance(hrp.portfolio_performance(verbose=True))


