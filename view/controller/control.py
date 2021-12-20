import yfinance as yf
import pandas as pd

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
This fuction downloads the adjusted closing price
of a list of stocks given since a respective date.
This method returns a dataframe. 
"""
def return_closed_prices(tickers, date):
    return yf.download(tickers, date)['Adj Close']


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



