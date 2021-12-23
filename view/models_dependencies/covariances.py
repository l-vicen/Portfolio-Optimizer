from pypfopt import risk_models

def calculate_covariance_according_to(prices, method):

    if (method == "Sample Covariance"):
        return risk_models.sample_cov(prices, frequency=252)
    
    elif (method == "Semi Covariance"):
        return risk_models.semicovariance(prices)

    elif (method == "Exponentially-weighted Covariance"):
        return risk_models.exp_cov(prices)

    elif (method == "Covariance Schrinkage: Ledoit Wolf"):
        return risk_models.risk_matrix(prices, "ledoit_wolf")

    elif (method == "Covariance Schrinkage: Ledoit Wolf Costant Variance"):
        return risk_models.risk_matrix(prices, "ledoit_wolf_constant_variance")
        
    elif (method == "Covariance Schrinkage: Ledoit Wolf Single Factor"):
        return risk_models.risk_matrix(prices, "ledoit_wolf_single_factor")

    elif (method == "Covariance Schrinkage: Ledoit Wolf Constant Correlation"):
        return risk_models.risk_matrix(prices, "ledoit_wolf_constant_correlation")

    else:
        return risk_models.risk_matrix(prices, "oracle_approximating")
