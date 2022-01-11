# Dependencies
import streamlit as st
from gsheetsdb import connect
import pandas as pd

from inform import Descriptions
import plotly.express as px

def display_home():
    st.title('Multi-feature Portfolio Optimizer App (MPOA)')
    col1, col2 = st.columns([1,2])

    col1.header('About')
    col1.info(Descriptions.ABOUT)

    col2.header('Algorithmic Coverage')

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

    fig = px.histogram(df, x="Timestamp", color="Method")
    fig.show()

    col1.table(df)
    col2.plotly_chart(fig)  

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