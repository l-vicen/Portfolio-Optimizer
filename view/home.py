# Dependencies
import streamlit as st
import pandas as pd

def display_home():
    st.title('Multi-feature Portfolio Optimizer App (MPOA)')
    col1, col2 = st.columns([1,1])

    col1.header('About')
    message = 'Our project allows you to query historical data from __yFinance API__ on different stocks based on their ticker, with this information in hands you can run a multitude of different optimization strategies and see how they perform.'
    col1.markdown(message, unsafe_allow_html = True)

    col2.header('Algorithmic Coverage')


    st.title("Public Dashboard")
    # Create a connection object.
    st.secrets["public_gsheets_url"]
    
class Sidebar: 

    def sidebar_functionality(self):
        # Sidebar attribute Logo
        st.sidebar.image('view/assets/tumSOM_logo.png')
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