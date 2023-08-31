import streamlit as st

import os
import sys

sys.path.insert(1, os.path.abspath('.'))

# import the PortfolioDefiner class from the portfolio module

from program.workers.firebase import firebaseUserPortfolio
from program.streamlit_functions.manage_portfolio.streamlit_manage_portfolio import streamlit_manage_portfolio

st.title('TOTAL PORTFOLIO ANALYSIS')

manage_portfolio, portfolio_performance, portfolio_analysis = st.tabs(["Manage portfolio", "Performance", "Analysis"])

# crate a streamlit tab called *Manage portfolio*
with manage_portfolio:
    streamlit_manage_portfolio()
