import streamlit as st

def plot_performance(tuple):
    st.write("Expected annual return: {}%".format(round(tuple[0] * 100, 2)))
    st.write("Annual volatility: {}%".format(round(tuple[1] * 100, 2)))
    st.write("Sharpe Ratio: {}%".format(round(tuple[2] * 100, 2)))
