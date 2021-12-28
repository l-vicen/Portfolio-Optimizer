from pypfopt import EfficientFrontier
from pypfopt import objective_functions

def calculate_asset_distribution_according_to(method, regularization, tunning_factor,expected_returns, covariance_matrix):

    if (method == "Minimize Volatility"):
        efficientFrontier = EfficientFrontier(expected_returns, covariance_matrix)

        if (regularization == "Yes"): 
            efficientFrontier.add_objective(objective_functions.L2_reg, gamma = tunning_factor)
        else:
            pass

        efficientFrontier.min_volatility()
        return efficientFrontier
    
    elif (method == "Maximize Sharpe Ratio"):
        efficientFrontier = EfficientFrontier(expected_returns, covariance_matrix)

        if (regularization == "Yes"): 
            efficientFrontier.add_objective(objective_functions.L2_reg, gamma = tunning_factor)
        else:
            pass

        efficientFrontier.max_sharpe()
        return efficientFrontier

    elif (method == "Maximize Quadratic Utility"):
        efficientFrontier = EfficientFrontier(expected_returns, covariance_matrix)

        if (regularization == "Yes"): 
            efficientFrontier.add_objective(objective_functions.L2_reg, gamma = tunning_factor)
        else:
            pass

        efficientFrontier.max_quadratic_utility()
        return efficientFrontier

    elif (method == "Efficient Risk"):
        efficientFrontier = EfficientFrontier(expected_returns, covariance_matrix)

        if (regularization == "Yes"): 
            efficientFrontier.add_objective(objective_functions.L2_reg, gamma = tunning_factor)
        else:
            pass

        efficientFrontier.efficient_risk()
        return efficientFrontier

    else:
        efficientFrontier = EfficientFrontier(expected_returns, covariance_matrix)

        if (regularization == "Yes"): 
            efficientFrontier.add_objective(objective_functions.L2_reg, gamma = tunning_factor)
        else:
            pass

        efficientFrontier.efficient_return()
        return efficientFrontier
