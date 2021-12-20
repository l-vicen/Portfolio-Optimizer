import streamlit as st

def plot_performance(tuple):
    st.write("Expected annual return: {}%".format(tuple[0] * 100))
    st.write("Annual volatility: {}%".format(tuple[1] * 100))
    st.write("Sharpe Ratio: {}%".format(tuple[2] * 100))
