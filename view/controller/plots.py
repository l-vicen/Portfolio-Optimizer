import streamlit as st
from inform import Descriptions

import models_dependencies.google_sheet as googleSheet

def plot_performance(tuple, ef, list_of_stock):

    columnA, columnB = st.columns((2, 1))

    columnA.write("Expected annual return: {}%".format(round(tuple[0] * 100, 2)))
    columnA.write("Annual volatility: {}%".format(round(tuple[1] * 100, 2)))
    columnA.write("Sharpe Ratio: {}".format(round(tuple[2], 2)))

    columnB.info(Descriptions.ANNUAL_VOLATILITY)
    columnB.info(Descriptions.ANNUAL_EXPECTED_RETURN)
    columnB.info(Descriptions.SHARPE_RATIO)

    share = ['Dont Share', 'Share Portfolio']
    share_choice = columnA.radio('Let the world know about this Portfolio', share)

    if (share_choice == share[0]):
        columnA.error('Why not let the world benefit from your ideas ? :O')
    else:
        googleSheet.save_expected_performance(ef.portfolio_performance(), list_of_stocks, "MVO")
        columnA.success('Success!')
