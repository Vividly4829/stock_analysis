import yfinance as yf
from datetime import datetime, timedelta
import time
import pandas as pd
from matplotlib import pyplot as plt
import streamlit as st

# Get input from users
start_date = st.sidebar.date_input("Start Date", datetime(2010, 11, 1))
end_date = st.sidebar.date_input("End Date", datetime(2023, 4, 30))
initial_capital = st.sidebar.slider("Initial Capital", min_value=1, max_value=1000, value=100, step=1)
transaction_cost = st.sidebar.slider("Transaction Cost (%)", min_value=0.0, max_value=1.0, value=0.35, step=0.01)
rebalance_variance = st.sidebar.slider("Rebalance Variance (%)", min_value=0.0, max_value=1.0, value=0.05, step=0.01)
rebalance_treshold = st.sidebar.slider("Rebalance Threshold (days)", min_value=1, max_value=365, value=30, step=1)

# Converting date objects to string format for further processing
start_date = start_date.strftime("%Y-%m-%d")
end_date = end_date.strftime("%Y-%m-%d")

# Convert percentage to actual fraction
transaction_cost /= 100
rebalance_variance /= 100



benchmarks = ['SPY', 'IAU', 'TQQQ', 'QQQ']
etf_portfolio = {'IAU': 0.5, 'TQQQ': 0.5}


st.sidebar.write("Current Benchmarks:", benchmarks)
st.sidebar.write("Current ETF Portfolio:", etf_portfolio)