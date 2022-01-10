import streamlit as st
from inform import Descriptions

import models_dependencies.google_sheet as googleSheet

def plot_performance(tuple, ef, list_of_stock):

    columnA, columnB = st.columns((2, 1))

    columnA.header('Annual Performance Expectations')
    columnA.write("Expected annual return: {}%".format(round(tuple[0] * 100, 2)))
    columnA.write("Annual volatility: {}%".format(round(tuple[1] * 100, 2)))
    columnA.write("Sharpe Ratio: {}".format(round(tuple[2], 2)))

    columnB.header('Informer')
    columnB.info(Descriptions.ANNUAL_VOLATILITY)
    columnB.info(Descriptions.ANNUAL_EXPECTED_RETURN)
    columnB.info(Descriptions.SHARPE_RATIO)