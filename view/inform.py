class Descriptions:

    # SETUPS HELPERS

    ANNUAL_YEAR_TO_BE_CONSIDER_HELPER = 'Year to be considered (Annual unit measured)'

    LIST_PORTFOLIO_HELPER = 'Here you can add stocks from the S&P 500 to your portfolio, that will be optimized. A portfolio is a \
        collection on financial investments. '

    COVARIANCE_HELPER = 'Choose the method how the covariance is computed! The covariance is the risk model for this optimization.'

    EXP_RETURN_HELPER = 'Choose the method how the expected return is computed! The expected return is the anticipated loss or profit \
        on the portfolio.'

    L2_REGULARIZATION_HELPER = 'MVO often selects only a few numbers of assets and omits many assets, which is expected when optimizing \
        a big set.But this can conflict with a well-diversified portfolio. The L2 regularization adds a “small weights penalty” to stop \
        the optimizer from overfitting.'

    # COVARIANCES

    SAMPLE_COVARIANCE = 'The sample covariance matrix is an unbiased estimator of the covariance matrix, but in practice it can lead to \
        misspecification error and lack of robustness, which can cause false credence to erroneous values especially with MVO. Recommendation: \
        Use a shrinkage estimator instead!'

    SEMI_COVARIANCE = 'The semi variance is a measure for downside risk below a certain benchmark.' #@LUCAS is the risk-free rate used as Benchmark B ? If so we should update it, for all methods… its quite close to zero, today it was 0,08% so 0,0008 not 0,02 anymore

    EXPONENTIAL_WEIGHTED_COVARIANCE = 'Covariance does not respect the order of observations and assets performance follows trends often.  A \
        tool to compensate for this issue is weighting the covariance by days that have passed since the data was collected. That works especially \
        well with minimum variance portfolios! Recommendation: Use exponential-weighted covariance on very well-diversified portfolios or \
        portfolios that are optimized on minimum volatility!'

    LEDOIT_WOLF_SHRINKAGE = 'This covariance shrinkage improves the sample covariance by “shrinking” extreme values closer to the center.\
        MVO is very sensitive to extreme errors which occur often with the sample covariance. Recommendation: Use Ledoit-Wolf as default \
        covariance!'

    ORACLE_APPROXIMATION_SHRINKAGE = 'When the samples are Gaussian distributed oracle approximated shrinkage achieves a smaller mean-square\
        error than Ledoit-Wolf.'



    # OBJECTIVE FUNCTIONS

    EFFICIENT_RISK = 'Efficient Risk maximizes return for a target risk (semideviation - downside standard deviation). \
        The resulting portfolio will have a semideviation less than the target (but not guaranteed to be equal).'

    EFFICIENT_RETURN = 'Efficient Return minimizes risk (semideviation - downside standard deviation) for a given target return.'

    MAX_QUADRATIC_UTILITY = 'Maximize Quadratic Utility maximizes the quadratic utility using portfolio semivariance and your chosen \
        risk aversion parameter.'

    MIN_VOLATILITY = 'Minimize volatility optimizes the portfolio in relation to low risk. '

    MAX_SHARPE = 'Maximize Sharpe ratio optimizes the portfolio in relation to the highest Sharpe ratio.The Sharpe ratio is an index \
        for the performance of the portfolio. '

    # OPTIMIZERS (MODELS)

    BLA = 'The Black-Litterman Allocation (BL) was developed by Fisher Black and Robert Litterman in the early 90s at Goldman-Sachs '\
          'and based on the concepts of  Semi-Strong Form Efficiency, CAPM, CAPM and Bayes’ theorem. It is designed to address ' \
          'the issue of personal view’s inclusion (private information as insights, strategies etc.), which occurs with eg. Mean-Variance-Optimization. '\
          'BL takes advantage of Bayes’ theorem to integrate a flexible number of views and converts them into explicit forecasts. ' \
          'If there is no “view” on a certain stock, BL retrieves the market equilibrium (CAPM ) alone which adds robustness to the model.'

    BLA_VIEW = 'Input your view on how you think your chosen stock will perform, eg. if you think Apple will perform +10%, type in \
        “0,10”.'

    BLA_CONFIDENCE_VIEW = 'Input your confidence in your view. If you are 20% confident of your view, type in 0,2. '

    HRP = 'The Hierarchical Risk Parity is novel portfolio optimization published by Lopez de Prado. It returns a diversified, less \
        risky portfolio than Black-Litterman and MVO. '

    HRP_TREE_CLUSTERING = 'TREE CLUSTERING Similar investments are grouped together into two branches based on their correlation matrix. \
        This step is repeated over and over again until every investment asset has its own branch. This algorithm breaks down the assets in our portfolio into different hierarchical clusters.'

    HRP_QUASI_DIAGNALIZATION = 'This step reorganizes the covariance so that similar investments are placed together and dissimilar \
        investments are placed far apart.'

    HRP_RECURSIVE_BISECTION = 'The final step of the algorithm then calculates the weight for each of the assets using a recursive \
        bi-sectioning procedure of the reordered covariance matrix.'

    MVO = 'Mean-Variance Optimization derives from the modern portfolio theory (MPT), which was published by Harry Markowitz in 1952 \
        and for which he received the Nobel Prize in Economic Sciences.  The mean-variance-optimization helps the investor to compose a \
        portfolio that has a maximized expected return on a certain level of risk (portfolio variance). When you plot every (multiple) \
        possible combination of your portfolio in a graph with risk (standard deviation) on the x-axis and expected return on the y-axis, \
        the left-boundary of the plotted portfolios create parabola-like shape. The vertex-portfolio will be the closest point to the y-axis. \
        Every portfolio on the left-boundary from the vertex upwards has the highest expected return to a certain risk level thus is pareto efficient.'

    BACKTESTING = "Portfolio backtesting seeks to determine the effectiveness of a trading strategy using historical data. The method \
        takes the portfolio with the selected assets and calculated allocation from the corresponding strategy and compares the \
        performance to the benchmark S&P 500 regarding the given time period."

    # PERFORMANCE INDICATORS

    ANNUAL_VOLATILITY = 'Annual volatility describes the variation in portfolio’s value over the course of a year. This measure indicates \
        the level of risk associated with an investment.'

    ANNUAL_EXPECTEd_RETURN = 'The annual expected return is the anticipated loss or profit on the portfolio. '

    SHARPE_RATIO = 'The Sharpe ratio is an index for the performance of the portfolio. A positive Sharpe ratio indicates the outperformance \
        of the portfolio over the risk-free-return . It is defined as the risk-free return subtracted from the expected return divided by the \
        risk (standard deviation) of the returns. '

descriptions = Descriptions()
