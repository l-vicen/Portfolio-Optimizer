from pypfopt.expected_returns import mean_historical_return
from pypfopt.risk_models import CovarianceShrinkage
import pandas as pd

dataframe = pd.read_csv("data/tesla.csv")

def applyhistoricalReturn(dataframe):
    return mean_historical_return(dataframe)

def applyCovarianceSchrinkage(dataframe):
    return CovarianceShrinkage(dataframe).ledoit_wolf()


applyhistoricalReturn(dataframe)
applyCovarianceSchrinkage(dataframe)