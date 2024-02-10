from program.workers.jsonbase import *
from program.streamlit_functions.etf_performance.compare_asset_performance import analyse_asset_performance
from program.streamlit_functions.portfolio_holdings.streamlit_portfolio_holdings import streamlit_portfolio_holdings
from program.streamlit_functions.manage_portfolio.streamlit_manage_portfolio import streamlit_manage_portfolio
from program.workers.jsonbase import JsonBaseUserPortfolio
import streamlit as st

import time

st. set_page_config(layout="wide", page_title='Portfolio',
                    page_icon=':moneybag:')

if 'loaded_portfolio' in st.session_state:
    # Show content based on selected radio button

    selected_tab = st.sidebar.radio(
        "Menu:",
        ["Portfolio visualisation", "Manage portfolio", "Analyse asset performance",], index=0
    )
    st.session_state.selected_tab = selected_tab

    print('gui', selected_tab)
    print('session state tab', st.session_state.selected_tab)

    if selected_tab == "Portfolio visualisation":
        streamlit_portfolio_holdings()
    elif selected_tab == "Manage portfolio":
        streamlit_manage_portfolio()
    elif selected_tab == "Analyse asset performance":
        analyse_asset_performance()
    st.sidebar.markdown('---')

    st.sidebar.write(
        'total value:', st.session_state.loaded_portfolio.user_portfolio['total value'])

    exchange_rate_expander = st.sidebar.expander('Exchange rates')
    exchange_rate_expander.write(
        st.session_state.loaded_portfolio.user_portfolio['exchange rates'])
else:
    st.sidebar.info('No portfolio loaded - load portfolio in side menu.')

st.sidebar.markdown('---')


loaded_portfolio_name = st.empty()
st.session_state.loaded_portfolio_name = loaded_portfolio_name

st.session_state.user_name = 'ruben'
portfolios = get_portfolio_names(user_name=st.session_state.user_name)

user_portfolio = st.sidebar.selectbox(
    "Select portfolio", options=portfolios)


if st.sidebar.button('Load portfolio'):
    with st.spinner('Loading user portfolio...'):
        st.session_state.loaded_portfolio = JsonBaseUserPortfolio(
            st.session_state.user_name, user_portfolio)
        st.session_state.loaded_portfolio_name = user_portfolio
        st.experimental_rerun()
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

    new_portfolio = JsonBaseUserPortfolio(
        st.session_state.user_name_name, new_portfolio_name)
    new_portfolio.create_new_portfolio()
    st.sidebar.success(
        f'Created new portfolio with name {new_portfolio_name}.')
    time.sleep(0.5)
    st.experimental_rerun()
