## ------ START OF CREDENTIALS ------ ##
import requests

params = {
  'access_key': '7b4fbaf29d8b58f7657878cb5c42719f'
}

api_result = requests.get('https://api.marketstack.com/v1/tickers/aapl/eod', params)

api_response = api_result.json()


## ------ END OF CREDENTIALS ------ ##

## Tests
import pandas as pd

class Data:

  def compose(self):
    return pd.read_csv("data/tesla.csv")

data = Data()



