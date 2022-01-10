import datetime
import os

import yfinance as yf
import pandas as pd


def return_list_tickers_names():
    # TODO path to csv file has to be updated
    data = pd.read_csv("data/symbols.csv",
                       usecols=['Symbol', 'Name'])
    return data


def return_tickers_from_names(names):
    data = return_list_tickers_names()
    df = data[data.Name.isin(names)]
    return df['Symbol'].tolist()


def return_closed_prices_names(names, date):
    return return_closed_prices(return_tickers_from_names(names), date)

#can be deleted, because method is already implemented in controller
def return_closed_prices(tickers, date):
    return yf.download(tickers, date)['Adj Close']

#TODO delete main method. Only for testing purposes
if __name__ == '__main__':
    names = ['Amazon.com Inc. Common Stock','Aadi Bioscience Inc. Common Stock']
    start = datetime.datetime(2017, 6, 6)
    end = datetime.datetime(2018, 6, 6)
    print( return_closed_prices_names(names, start))

