class Descriptions:

    # HOME PAGE
    ABOUT = 'Our project allows you to query historical data from __yFinance API__ on different stocks based on their ticker, \
        with this information in hands you can run a multitude of different optimization strategies and see how they perform.'

    # SETUPS HELPERS

    ANNUAL_YEAR_TO_BE_CONSIDER_HELPER = 'Year to be considered (Annual unit measured)'

    LIST_PORTFOLIO_HELPER = 'Please add stocks from the S&P 500 to your portfolio. A portfolio is a collection on financial investments. '

    COVARIANCE_HELPER = 'Please choose a covariance method! The covariance is the risk model which will be used for the optimization.'

    EXP_RETURN_HELPER = 'Please choose an expected return method! The expected return is the anticipated profit or loss on the portfolio.'

    L2_REGULARIZATION_HELPER = 'Mean Variance Optimisation(MVO)  may only select a small number of assets out of a large portfolio. This can conflict with a well-diversified portfolio. The L2 regularization adds a “small weights penalty” to stop the optimizer from overfitting.'

    # COVARIANCES

    GEN_COVARIANCE = ' A covariance measures the strength and direction of a relationship between two assets. A positive covariance means that asset A and B move together. A negative covariance means that they move in opposite directions. ' \
        # @LUCAS should we use some more explaining? It could confuse the users because we would need to explain why cov. Is used as a risk model

    SAMPLE_COVARIANCE = 'The sample covariance matrix is an unbiased estimator of the covariance matrix, but in practice it can lead to misspecification error and lack of robustness.' \
                        ' This can cause false credence to erroneous values especially with MVO. Recommendation: Use a shrinkage estimator instead!'

    SEMI_COVARIANCE = 'Semi variance is a measure of downside risk below a certain benchmark.' #@LUCAS is the risk-free rate used as Benchmark B ? If so we should update it, for all methods… its quite close to zero, today it was 0,08% so 0,0008 not 0,02 anymore

    EXPONENTIAL_WEIGHTED_COVARIANCE = 'Covariance does not respect the order of observations and an assets performance often follows trends.  To compensate for this, the covariance of the days that have passed can be weighted. That works especially well with minimum variance portfolios!\
    Recommendation: Use exponential-weighted covariance on very well-diversified portfolios or portfolios that are optimized on minimum volatility!'

    LEDOIT_WOLF_SHRINKAGE = 'This covariance shrinkage improves the sample covariance by “shrinking” extreme values, bringing them closer to the centre. MVO is very sensitive to extreme errors which occur often with the sample covariance. Recommendation: Use Ledoit-Wolf as default covariance!'

    ORACLE_APPROXIMATION_SHRINKAGE = 'Oracle approximated shrinkage achieves a smaller mean-square error than Ledoit-Wolf when the samples are gaussian distributed.'



    # OBJECTIVE FUNCTIONS

    EFFICIENT_RISK = 'Efficient Risk maximizes return for a target risk (semideviation - downside standard deviation). \
        The resulting portfolio will have a semideviation less than the target (but not guaranteed to be equal).'

    EFFICIENT_RETURN = 'Efficient Return minimizes risk (semi deviation - downside standard deviation) for a given target return.'

    MAX_QUADRATIC_UTILITY = 'Maximize Quadratic Utility maximizes the quadratic utility using portfolio semivariance and your chosen \
        risk aversion parameter.'

    MIN_VOLATILITY = 'Minimize volatility optimizes the portfolio in relation to low risk. '

    MAX_SHARPE = 'Maximize Sharpe ratio optimizes the portfolio in relation to the highest Sharpe ratio.The Sharpe ratio is an index for the performance of the portfolio. '


    # OPTIMIZERS (MODELS)

    BLA = 'It is based on the concepts of Semi-Strong Form Efficiency, CAPM and Bayes’ theorem. The BL model is designed to combine' \
          'Modern portfolio theory (e.g. Mean-Variance-Optimization) with an investor´s views (insights, strategies, risks). '\
          'It makes use of Bayes’ theorem, integrating and converting a flexible number of views into explicit forecasts. ' \
          'If there is no “view” on a certain stock, BL retrieves the market equilibrium (CAPM ) which adds robustness to the model.'

    BLA_VIEW = 'Insert your view on how you believe your chosen stock will perform, eg. if you think Apple will perform +10%, type in “0,10”.'

    BLA_CONFIDENCE_VIEW = 'Insert your confidence in your view. If you are 20% confident of your view, type in 0,2. '

    HRP = 'The Hierarchical Risk Parity is novel portfolio optimization technique published by Lopez de Prado. It provides a more diversified, less risky portfolio than Black-Litterman and MVO. '

    HRP_TREE_CLUSTERING = 'Investments are split into two groups based on their correlation matrix. This step is repeated over and over again until every investment asset has its own branch. The algorithm breaks down the portfolio’s assets into different hierarchical clusters.'

    HRP_QUASI_DIAGNALIZATION = 'This step reorganizes the covariance so that similar investments are placed together and dissimilar investments are placed far apart.'

    HRP_RECURSIVE_BISECTION = 'The final step of the algorithm calculates the weight for each asset using a recursive bi-sectioning procedure of the reordered covariance matrix.'

    MVO = 'Mean-Variance Optimization derives from the modern portfolio theory (MPT), which was published by Harry Markowitz in 1952 \
        and for which he received the Nobel Prize in Economic Sciences.  The mean-variance-optimization helps the investor to compose a \
        portfolio that has a maximized expected return on a certain level of risk (portfolio variance). When you plot every (multiple) \
        possible combination of your portfolio in a graph with risk (standard deviation) on the x-axis and expected return on the y-axis, \
        the left-boundary of the plotted portfolios create parabola-like shape. The vertex-portfolio will be the closest point to the y-axis. \
        Every portfolio on the left-boundary from the vertex upwards has the highest expected return to a certain risk level thus is pareto efficient.'

    BACKTESTING = "Portfolio backtesting seeks to determine the effectiveness of a trading strategy using historical data. The method takes the \
                    portfolio with the selected assets and calculated allocation from the corresponding strategy and compares the performance to the benchmark \
                    S&P 500 regarding the given time period."

    # PERFORMANCE INDICATORS

    ANNUAL_VOLATILITY = 'Annual volatility is the variation in portfolio’s value over the course of a year. It measure indicates the level of risk associated with an investment.'

    ANNUAL_EXPECTED_RETURN = 'The annual expected return is the anticipated profit or loss on the portfolio. '

    SHARPE_RATIO = 'The Sharpe ratio is an index for the performance of the portfolio. A positive Sharpe ratio indicates the outperformance of the portfolio over the risk-free-return . ' \
                   'It is defined as the risk-free return subtracted from the expected return divided by the risk (standard deviation) of the returns.'

descriptions = Descriptions()
