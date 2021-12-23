from pypfopt import expected_returns

def calculate_expected_return_according_to(prices, method):

    if (method == "Mean Historical Return"):
        return expected_returns.mean_historical_return(prices)
    
    elif (method == "Exponential Moving Average"):
        return expected_returns.ema_historical_return(prices)
    
    else:
        return expected_returns.capm_return(prices)
