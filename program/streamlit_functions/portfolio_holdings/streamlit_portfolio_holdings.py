from program.workers.portfolio_parser import *
import streamlit as st
st.write('Current holdings')
   

def streamlit_portfolio_holdings():

    if 'loaded_portfolio' in st.session_state:
        st.dataframe(st.session_state.loaded_portfolio.holdings, width=2000, height=1000)
        print(st.session_state.loaded_portfolio.holdings)
    else:
        st.info('No portfolio loaded - load portfolio in side menu.')