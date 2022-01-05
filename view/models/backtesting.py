import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import datetime
import controller.control as cl

def backtesting_setup():

    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.title('Backtesting')

    c1, c2 = st.columns((2, 1))

    c2.header('About')
    c2.info(' epjcnqej cqej ce[j q[c qjc[qe c[qjcqe[cj qejc dec qejc qjej cec')

    c1.header('Setup')

    # Dates
    start = c1.date_input('Start date', datetime.date(2020, 12, 1))
    end = c1.date_input('End date', datetime.date(2021, 12, 1))

    # Initial investment
    init_investment = c1.number_input('Initial Investment', min_value = 10, max_value = 100000000, value = 1000, step = 50)

    # Tickers of portfolio
    tickers = c1.multiselect("Selct all tickers you want to have in the portfolio", cl.return_list_tickers())

    # TODO: Figure out how to input
    # Allocation percentages
    allocations = [.2, .3, .5]

    if (len(tickers) > 0): 
        # Downloading asset prices
        d1 = {}
        for ticker in tickers:
            d1[ticker] = pd.DataFrame(cl.return_closed_prices_time_interval(ticker, start, end))

        # Calculating cumulative return
        d2 = {}
        for ticker, df in d1.items():
            df = df.dropna()
            df['Cum Return'] = df['Adj Close'] / df.iloc[0]['Adj Close']
            d2[ticker] = df

        # Download benchmark prices and calculating cumulative return
        SPY = yf.download('SPY', start=start, end=end)
        SPY = SPY.dropna()
        SPY['Cum Return'] = SPY['Adj Close'] / SPY.iloc[0]['Adj Close']

        # Calculate value of initial investment of the portfolio
        i = 0
        for ticker, df in d2.items():
            df['Value'] = allocations[i] * init_investment * df['Cum Return']
            i += 1

        # Calculate value of initial investment of SPY
        SPY['SPY Total'] = init_investment * SPY['Cum Return']
        SPY['SPY Total'] = round(SPY['SPY Total'])

        # Combine all dataframes
        all_vals = []
        for ticker, df in d2.items():
            all_vals.append(df['Value'])

        portfolio_val = pd.concat(all_vals, axis=1)
        portfolio_val.columns = tickers

        # Calculate cumulative return value and cumulative return in %
        portfolio_val['Portfolio Total'] = round(portfolio_val.sum(axis=1))
        portfolio_val['Cum Return'] = portfolio_val['Portfolio Total'] / portfolio_val.iloc[0]['Portfolio Total']
        portfolio_val['Cum Return %'] = (portfolio_val['Cum Return'] - 1) * 100
        SPY['Cum Return %'] = (SPY['Cum Return'] - 1) * 100

        # Visualize portfolio value and compare it to SPY benchmark
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=portfolio_val.index, y=portfolio_val['Portfolio Total'], name='Portfolio Total'))
        fig1.add_trace(go.Scatter(x=SPY.index, y=SPY['SPY Total'], name='Benchmark Total'))
        fig1.update_layout(title="Portfolio Value")

        st.plotly_chart(fig1)

        # Visualize return in %
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=portfolio_val.index, y=portfolio_val['Cum Return %'], name='Portfolio Cumulative Return %'))
        fig2.add_trace(go.Scatter(x=SPY.index, y=SPY['Cum Return %'], name='Benchmark Cumulative Return %'))
        fig2.update_layout(title="Cumulative Return % (Portfolio vs Benchmark)")

        st.plotly_chart(fig2)


