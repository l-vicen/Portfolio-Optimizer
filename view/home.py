# Dependencies
import streamlit as st
import pandas as pd

def display_home():
    st.title('Data Science in Finance Seminar - WS21/22')
    col1, col2 = st.columns([1,1])

    col1.header('About')
    message = 'Our project allows you to query historical data from __yFinance API__ on different stocks based on their ticker, with this information in hands you can run a multitude of different optimization strategies and see how they perform.'
    col1.markdown(message, unsafe_allow_html = True)

    col2.header('Algorithmic Coverage')
    
class Sidebar: 
    def sidebar_functionality(self):
        # Sidebar attribute Logo
        st.sidebar.image('view/assets/tumSOM_logo.png')
        st.sidebar.markdown('---')

    def sidebar_contact(self):
        st.sidebar.markdown('##### Team')
        st.sidebar.markdown('Lucas Perasolo')
        st.sidebar.markdown('NAME 2')
        st.sidebar.markdown('NAME 3')
        st.sidebar.markdown('NAME 4')
        st.sidebar.markdown('.....')
        st.sidebar.markdown('---')

sidebar = Sidebar()