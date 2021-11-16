import yfinance as yf

"""
To understand the format of each function, 
read the function name based on the following
example:

def return_<format>_attribute():
...
end
"""

def return_closed_prices(tickers, date):
    return yf.download(tickers, date)['Adj Close']


