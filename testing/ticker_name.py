import yfinance as yf


def ticker_name(list):
    name = []

    for ticker in list:
        name.append(yf.Ticker(ticker).info['longName'])

    return name


if __name__ == '__main__':
    tickers = ["MSFT", "FB", "AAPL", "TSLA"]
    result = ticker_name(tickers)
    print(result)
