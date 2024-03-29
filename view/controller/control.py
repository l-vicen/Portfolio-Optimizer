import yfinance as yf
import pandas as pd
import numpy as np

"""
This function reads in a Nasdaq csv file
containing information about stocks listed 
in this borse. This function removes everything
besides the list of symbols, and returns a list 
of tickers.
"""
def return_list_tickers():
    data = pd.read_csv("data/symbols.csv")
    df = data['Symbol']
    return df.values.tolist()

"""
This function reads in a Nasdaq csv file
containing information about stocks listed 
in this borse. This function removes everything
besides the list names, and returns 
a list of company names.
"""
def return_list_tickers_only_names():
    data = pd.read_csv("data/symbols.csv")
    df = data['Name']
    return df.values.tolist()

"""
This function reads in a Nasdaq csv file
containing information about stocks listed 
in this borse. This function removes everything
besides the list of symbols and names, and returns 
a list of tickers.
"""
def return_list_tickers_names():
    data = pd.read_csv("data/symbols.csv", usecols=['Symbol', 'Name'])
    return data

"""
This function reads the cleaned .csv
from return_list_tickers_names() and 
gives the respective tickers only. 
"""
def return_tickers_from_names(names):
    data = return_list_tickers_names()
    df = data[data['Name'].isin(names)]
    nestedArray = df['Symbol'].values.tolist()
    arr = np.array(nestedArray)

    return arr.flatten().tolist()

def return_tickers_from_names_david(names):
    data = return_list_tickers_names()
    df = data[data.Name.isin(names)]
    return df['Symbol'].tolist()


"""
This fuction downloads the adjusted closing price
of a list of stocks given since a respective date.
This method returns a dataframe. 
"""
def return_closed_prices(tickers, date):
    return yf.download(tickers, date)['Adj Close']

"""
This fuction downloads the adjusted closing price
of a list of company names given since a respective date.
This method returns a dataframe. 
"""
def return_closed_prices_names(names, date):
    return return_closed_prices(return_tickers_from_names(names), date) 

"""
This fuction downloads the market capitalization
values for given list of tickers.
"""
def return_market_capitalizations(tickers): 
    marketCaps = {} 

    for i in tickers:
        stock = yf.Ticker(i)
        marketCaps[i] = stock.info["marketCap"]

    return marketCaps

"""
This function is Andre's data query for the
backtesting feature.
"""
def return_closed_prices_time_interval(ticker, start, end):
   return yf.download(ticker, start=start, end=end)


