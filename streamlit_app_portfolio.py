import streamlit as st

import time

st. set_page_config(layout="wide", page_title='Portfolio', page_icon=':moneybag:')

# import the PortfolioDefiner class from the portfolio module
from program.workers.jsonbase import JsonBaseUserPortfolio
from program.streamlit_functions.manage_portfolio.streamlit_manage_portfolio import streamlit_manage_portfolio
from program.streamlit_functions.portfolio_holdings.streamlit_portfolio_holdings import streamlit_portfolio_holdings
from program.workers.jsonbase import *

loaded_portfolio_name = st.empty()
st.session_state.loaded_portfolio_name = loaded_portfolio_name

user_name = 'ruben'
portfolios = get_portfolio_names(user_name=user_name)

user_portfolio = st.sidebar.selectbox(
    "Select portfolio", options=portfolios)


if st.sidebar.button('Load portfolio'):
    with st.spinner('Loading user portfolio...'):
        st.session_state.loaded_portfolio = JsonBaseUserPortfolio(user_name, user_portfolio)
        st.session_state.loaded_portfolio_name = user_portfolio
        st.experimental_rerun()
st.sidebar.markdown('---')


selected_tab = st.sidebar.radio(
    "Menu:",
    ["Show portfolio", "Manage portfolio"]
)

# Show content based on selected radio button
if selected_tab == "Show portfolio":
    streamlit_portfolio_holdings()
elif selected_tab == "Manage portfolio":
    streamlit_manage_portfolio()

st.sidebar.markdown('---')

st.sidebar.write('Create new portfolio')
new_portfolio_name = st.sidebar.text_input('New portfolio name', value='')
if st.sidebar.button('Create new portfolio'):
    if new_portfolio_name == '':
        st.sidebar.error('Please enter a name for the new portfolio.')
        st.stop()
    elif new_portfolio_name in portfolios:
        st.sidebar.error('Portfolio with that name already exists.')
        st.stop()
    

    new_portfolio = JsonBaseUserPortfolio(user_name, new_portfolio_name)
    new_portfolio.create_new_portfolio()
    st.sidebar.success(f'Created new portfolio with name {new_portfolio_name}.')
    time.sleep(0.5)
    st.experimental_rerun()
