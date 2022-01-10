import streamlit as st
from inform import Descriptions

def plot_performance(tuple, columnA, columnB):
    columnA.write("Expected annual return: {}%".format(round(tuple[0] * 100, 2)))
    columnA.write("Annual volatility: {}%".format(round(tuple[1] * 100, 2)))
    columnA.write("Sharpe Ratio: {}".format(round(tuple[2], 2)))

    columnB.info(Descriptions.ANNUAL_VOLATILITY)
    columnB.info(Descriptions.ANNUAL_EXPECTED_RETURN)
    columnB.info(Descriptions.SHARPE_RATIO)

