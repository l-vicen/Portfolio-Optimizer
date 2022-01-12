# Dependencies
import streamlit as st
from gsheetsdb import connect
import pandas as pd

from inform import Descriptions
import plotly.express as px

def display_home():
    st.title('Multi-feature Portfolio Optimizer App (MPOA)')
    col1, col2 = st.columns([1,1])

    col1.header('About')
    col1.markdown(Descriptions.ABOUT)

    col1.success( 
        """
        ##### Contribute
        Feel free to improve the current project at: \n
        https://github.com/l-vicen/-WIB06772-PortfolioOptimizer
        """
    )

    col2.header('App Features')
    col2.info(
        """
        * Real-Time query of financial data
        * Different UX & Model Configurations
        * Portfolio Optimization
            * Mean-Variance Optimization
            * Black-Litterman Allocation
            * Hierarchical Risk Parity
        * Different Expected Return Calculation Methods
        * Different Risk Model Calculation Methods
        * Optimal Portfolio Backtest (% SPY 500)
        * Optimization Log / Activity Track
        * Real time project review
        """
    )

    st.markdown('---')
    st.markdown("## Public Dashboard")

    conn = connect()

    sheet_url = st.secrets["feedback_gsheets_url"]
    df = pd.read_sql(f'SELECT * FROM "{sheet_url}"',
                     conn,
                     parse_dates=["timestamp"])

    df.rename(columns={"method": "Method",
                       "portfolio": "Portfolio",
                       "expected_annual_return": "Expected annual return",
                       "annual_volatility": "Annual volatility",
                       "sharpe_ratio": "Sharpe ratio",
                       "timestamp": "Timestamp"},
              inplace=True)

    df.index += 1

    col3, col4 = st.columns([1,1])

    fig = px.histogram(df, x="Timestamp", color="Method")
    fig.update_layout(title="User Activity over Time", width=850, height=500)

    fig.show()

    st.plotly_chart(fig) 
    col4.info(Descriptions.PUBLIC_DASHBOARD)
    st.table(df)

class Sidebar: 

    def sidebar_functionality(self):
        # Sidebar attribute Logo
        st.sidebar.image('view/assets/tum.png')
        st.sidebar.markdown('---')

    def sidebar_contact(self):
        st.sidebar.markdown('##### Contributors')
        st.sidebar.markdown('André Leibrant')
        st.sidebar.markdown('David Gewalt')
        st.sidebar.markdown('Hans Gottmann')
        st.sidebar.markdown('Kirill Molchanov')
        st.sidebar.markdown('Leon Linde')
        st.sidebar.markdown('Lucas Perasolo')
        st.sidebar.markdown('Zhiyan Chen')
        st.sidebar.markdown('---')

    def sidebar_inform_libs(self):
        st.sidebar.warning("This app builds upon PyPortfolioOpt library: portfolio optimization in Python, developed by Martin, R. A., (2021). Journal of Open Source Software, 6(61), 3066, https://doi.org/10.21105/joss.03066")
        st.sidebar.markdown('---')


sidebar = Sidebar()