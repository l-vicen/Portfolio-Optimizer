# TODO 5: Clean current code & and define client interface
import streamlit as st
import datetime

# Global configuration
st.set_page_config(layout="wide")

st.title("Portfolio Optimizer")

optimizers_strategies = ['Expected Returns', 'Risk Models', 'Mean-Variance Optimization (MPT)', 'Black-Litterman Allocation', 'Hierarchical Risk Parity (HRP)']
post_processing_weigths = ['Greedy algorithm', 'Integer programming']

c1, c2 = st.columns((2, 1))

c1.header('Simulation setup')
start_date = c1.date_input('Start date')
end_date = c1.date_input('End date')

c1.selectbox('Select one Optimizer Strategy', optimizers_strategies)
c1.selectbox('Select one Post-Processing Weight Algorithm', post_processing_weigths)

stocks = []
c1.multiselect('Select stocks you are interested in:', stocks)

c2.header('Help')


