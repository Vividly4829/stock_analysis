import streamlit as st
from program.streamlit_functions.manage_portfolio.proxy_etf_list import find_proxy_etf
from program.streamlit_functions.manage_portfolio.log_change import log_portfolio_change    
from program.workers.jsonbase import *
import os
import sys
import pandas as pd
import time



def streamlit_manage_portfolio():


    st.session_state['trigger_rerun'] = False
    
    if not 'loaded_portfolio' in st.session_state:
        st.info('No portfolio loaded - load portfolio in side menu.')
  
    if 'loaded_portfolio' in st.session_state:
        
        
        st.sidebar.write('Options:')
        if st.sidebar.button('Load inception dates:'):
            with st.spinner('Loading inception dates...'):
                st.session_state['trigger_rerun'] = True
                st.session_state.loaded_portfolio.load_inception_dates()
   
        df = pd.DataFrame(st.session_state.loaded_portfolio.holdings)
    
        # Multi-select for accounts and categories
        available_accounts = df['Account'].unique().tolist()
        selected_accounts = st.multiselect('Select Accounts', available_accounts, default=available_accounts)
        df = df[df['Account'].isin(selected_accounts)]
        
        available_categories = df['Category'].unique().tolist()
        selected_categories = st.multiselect(
            'Select Categories', available_categories, default=available_categories)
        df = df[df['Category'].isin(selected_categories)]

        # Currency selection
        currency_options = ['NOK', 'USD', 'EUR']
        selected_currency = st.selectbox('Choose Currency', currency_options)

        st.markdown('---')
    
        log_portfolio_change(df)

        st.markdown('---')

        df = df.style.background_gradient(cmap='Reds', subset=[f'Value ({selected_currency})'])
        st.dataframe(df)


        with st.expander("Manage proxies"):
            st.info("Proxies are used to predict future results of newer ETF's based on historical results of ETF's with similar characteristics that have existed for X years or more. The older, the better the prediction of correlation in a portfolio.")
            min_proxy_age = st.slider(
                "Select min age of proxies", min_value=0, max_value=30, value=20)
            
            # Create a streamlit select box to select a proxy
            if st.session_state.loaded_portfolio.proxies is not None:
                proxy = st.selectbox(
                    "Select proxy", options=list(st.session_state.loaded_portfolio.proxies))
                if st.button('Delete proxy'):
                    st.session_state.loaded_portfolio.proxies.remove(proxy)
                    st.session_state.loaded_portfolio.update_portfolio_proxies()
                    st.success(f'Proxy {proxy} deleted')
                    st.session_state['trigger_rerun'] = True

                new_proxy = st.text_input("Add new proxy")
                if st.button('Add proxy'):
                    if new_proxy is not None:
                        if len(new_proxy) > 0 and new_proxy not in st.session_state.loaded_portfolio.proxies:
                            st.session_state.loaded_portfolio.proxies.append(new_proxy)
                            st.session_state.loaded_portfolio.update_portfolio_proxies()
                            st.success(f'Proxy {new_proxy} added')
                            st.session_state['trigger_rerun'] = True
                        else:
                            st.error(f'Proxy {new_proxy} was not added.')


            if st.button('Load new ETF proxies'):
                with st.spinner('Loading proxies...'):
                    st.session_state.proxies = find_proxy_etf(min_proxy_age)
                    st.session_state['trigger_rerun'] = True

            if 'proxies' in st.session_state:
                st.success('Loaded proxies:')
                selected_proxies = st.data_editor(st.session_state.proxies)
                # list of selected proxie tickers
                selected_proxy_tickers = selected_proxies['Symbol'].tolist()
                # if st.button('Add proxies'):
                #     loaded_portfolio.update_portfolio_proxies(selected_proxies)
                    
                #     st.session_state['trigger_rerun'] = True

            else:
                st.error('No proxies loaded')

         

        with st.expander("Manage accounts"):
            # Create a streamlit select box to select an account
            if st.session_state.loaded_portfolio.accounts is not None:
                account = st.selectbox(
                    "Select account", options=list(st.session_state.loaded_portfolio.accounts))
                if st.button('Delete account'):
                    st.session_state.loaded_portfolio.accounts.remove(account)
                    st.session_state.loaded_portfolio.update_portfolio_accounts()
                    st.success(f'Account {account} deleted')
                    st.session_state['trigger_rerun'] = True

                new_account = st.text_input("Add new account")
                if st.button('Add account'):
                    if new_account is not None:
                        if len(new_account) > 0 and new_account not in st.session_state.loaded_portfolio.accounts:
                            st.session_state.loaded_portfolio.accounts.append(new_account)
                            st.session_state.loaded_portfolio.update_portfolio_accounts()
                            st.success(f'Account {new_account} added')
                            st.session_state['trigger_rerun'] = True
                        else:
                            st.error(f'Account {new_account} was not added.')

        with st.expander("Manage categories"):
            # Create a streamlit select box to select an account
            if st.session_state.loaded_portfolio.categories is not None:
                category = st.selectbox(
                    "Select category", options=list(st.session_state.loaded_portfolio.categories))
                if st.button('Delete category'):
                    st.session_state.loaded_portfolio.categories.remove(category)
                    st.session_state.loaded_portfolio.update_portfolio_categories()
                    st.success(f'Category {category} deleted')
                    st.session_state['trigger_rerun'] = True

                new_category = st.text_input("Add new category")
                if st.button('Add category'):
                    if new_category is not None:
                        if len(new_category) > 1 and new_category not in st.session_state.loaded_portfolio.categories:
                            st.session_state.loaded_portfolio.categories.append(new_category)
                            st.session_state.loaded_portfolio.update_portfolio_categories()
                            st.success(f'Category {new_category} added')
                            
                            st.session_state['trigger_rerun'] = True
                        else:
                            st.error(f'Category {new_category} was not added because it was too short or already existed.')
               

        with st.expander("Upload portfolio from excel"):
            # Create a streamlit form to upload a portfolio from an excel file
           
            with open("files\\portfolios\\formue.xlsx", "rb") as file:

                st.download_button(
                    label="Download excel template",
                    data=file,
                    file_name="excel_portfolio_template.xlsx",
                    mime="application/wps-office.xlsx/xlsx"
                )

            with st.form(key="Upload portfolio"):
                excel_file = st.file_uploader(
                    "Upload excel file", type=['xlsx'])

                if st.form_submit_button(label="Upload portfolio"):
                    if excel_file is not None:
                        df = pd.read_excel(excel_file)
                        df_dict = df.to_dict(orient='records')

                        upload_status = st.session_state.loaded_portfolio.upload_excel_portfolio(df_dict)

                        if upload_status:
                            st.success("Portfolio uploaded")
                            st.session_state['trigger_rerun'] = True
                        else:
                            st.error("Failed to upload portfolio")
                    else:
                        st.error("No excel file uploaded")

    
        if 'trigger_rerun' in st.session_state:
   
            if st.session_state.trigger_rerun:

                if 'rerun_count' not in st.session_state:
                    st.session_state.rerun_count = 1
                else:
                    st.session_state.rerun_count += 1
                print(
                    f'reran program for the {st.session_state.rerun_count} time')
                st.experimental_rerun()
