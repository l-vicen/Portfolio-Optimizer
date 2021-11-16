# TODO 5: Clean current code & and define client interface
import streamlit as st
from pypfopt import risk_models, expected_returns
from pypfopt import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt import risk_models, expected_returns, plotting
import control as cl
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

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

tickers = [ 'BAS.DE', 'BAYN.DE', 'BEI.DE', 'BMW.DE', 'BNR.DE', 'CON.DE', 'DAI.DE', 'DHER.DE', 'DB1.DE', 
            'DBK.DE', 'DPW.DE', 'DTE.DE', 'EOAN.DE', 'FME.GR', 'FRE.DE', 'HEI.DE', 'HFG.DE', 'HEN3.DE', 'IFX.DE',
            'LIN.DE', 'MRK.DE', 'MTX.DE', 'MUV2.DE', 'PAH3.DE', 'PUM.DE', 'QIA.DE', 'RWE.DE', 'SAP.DE', 'SRT3.DE', 
            'SIE.DE', 'ENR.DE', 'SHL.DE', 'SY1.DE', 'VNA.DE', 'VOW3.DE', 'ZAL.DE']
            
df = cl.return_closed_prices(tickers, '2020-1-1')

st.table(df)

st.write('MEAN HISTORUCAL RETURN')
mu = expected_returns.mean_historical_return(df)
st.write(mu)

st.write('SAMPLE COVARIANCE')
S = risk_models.sample_cov(df)
st.write(S)

st.write('EFFICIENT FRONTIER')
ef = EfficientFrontier(mu, S)
raw_weights = ef.max_sharpe()
cleaned_weights = ef.clean_weights()
ef.save_weights_to_file("weights.csv")  # saves to file
st.write("Weigth distribution")
st.write(cleaned_weights)
ef.portfolio_performance(verbose=True)

from pypfopt import CLA, plotting

cla = CLA(mu, S)
cla.max_sharpe()
cla.portfolio_performance(verbose=True)

ax = plotting.plot_efficient_frontier(cla, showfig=False)
ax.figure.savefig('output.png')