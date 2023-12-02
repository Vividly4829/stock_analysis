import streamlit as st

import os
import sys

sys.path.insert(1, os.path.abspath('.'))

st. set_page_config(layout="wide", page_title='Portfolio', page_icon=':moneybag:')

# import the PortfolioDefiner class from the portfolio module


from program.workers.jsonbase import JsonBaseUserPortfolio
from program.streamlit_functions.manage_portfolio.streamlit_manage_portfolio import streamlit_manage_portfolio
from program.streamlit_functions.portfolio_holdings.streamlit_portfolio_holdings import streamlit_portfolio_holdings
from program.workers.jsonbase import *


user_name = 'ruben'
portfolios = get_portfolio_names(user_name=user_name)

user_portfolio = st.sidebar.selectbox(
    "Select portfolio", options=portfolios)


if st.sidebar.button('Load portfolio'):
    with st.spinner('Loading user portfolio...'):
        st.session_state.loaded_portfolio = JsonBaseUserPortfolio(user_name, user_portfolio)
        st.session_state.loaded_portfolio_name = user_portfolio
        trigger_rerun = True
st.sidebar.markdown('---')
    

selected_tab = st.sidebar.radio(
    "Menu:",
    ["Current holdings", "Manage portfolio"]
)

# Show content based on selected radio button
if selected_tab == "Current holdings":
    streamlit_portfolio_holdings()
elif selected_tab == "Manage portfolio":
    streamlit_manage_portfolio()