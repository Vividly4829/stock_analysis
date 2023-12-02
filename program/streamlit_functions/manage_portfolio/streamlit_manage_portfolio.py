

import streamlit as st
from program.streamlit_functions.manage_portfolio.proxy_etf_list import find_proxy_etf
from program.workers.jsonbase import *
import os
import sys
import pandas as pd
import time



def streamlit_manage_portfolio():

    trigger_rerun = False
    
    if not 'loaded_portfolio' in st.session_state:
        st.info('No portfolio loaded - load portfolio in side menu.')
  
    if 'loaded_portfolio_name' in st.session_state:
        

        portfolio_accounts = st.session_state.loaded_portfolio.accounts.copy()
        # add the option to select all accounts to the first position in the array
        portfolio_accounts.insert(0, 'All accounts')
        selected_account = st.selectbox('Select portfolio account', portfolio_accounts) 

        st.sidebar.title(
            f'LOADED PORTFOLIO: {st.session_state.loaded_portfolio_name}'.upper())
        st.session_state.loaded_portfolio = st.session_state.loaded_portfolio

        st.sidebar.write('Options:')
        if st.sidebar.button('Load inception dates:'):
            with st.spinner('Loading inception dates...'):
                trigger_rerun = True
                st.session_state.loaded_portfolio.load_inception_dates()
        
        if st.sidebar.button('Load inception date styling:'):
                st.session_state.loaded_portfolio.load_inception_date_styling()
                trigger_rerun = True

        column_config = {
        "Account":
            st.column_config.SelectboxColumn(
                "Account ",
                help="Select the account",
                width="medium",
                options=st.session_state.loaded_portfolio.accounts,
            ),
        "Currency":
            st.column_config.SelectboxColumn(
                "Currency",
                help="Select the currency",
                width="medium",
                options=['NOK', 'EUR', 'USD'],
            ),

        "Category":
            st.column_config.SelectboxColumn(
                "Category",
                help="Select the Category",
                width="medium",
                options=st.session_state.loaded_portfolio.categories,
            ),


        # "Proxy":
        #     st.column_config.SelectboxColumn(
        #         "Proxy",
        #         help="Select the Category",
        #         width="medium",
        #         options=st.session_state.proxies['name'].tolist(),
        #     )
    }

        st.write('Update portfolio')
        st.info(
            "Select row and press 'delete' button on the keyboard to delete . Press '+' to add a new row")
        
        with st.form(key="Update portfolio"):
            if selected_account != 'All accounts':
                portfolio_data = st.session_state.loaded_portfolio.holdings[st.session_state.loaded_portfolio.holdings['account'] == selected_account]
            else: 
                portfolio_data = st.session_state.loaded_portfolio.holdings

            updated_portfolio_data  = st.data_editor(
                portfolio_data, num_rows="dynamic", column_config=column_config)  # type: ignore
            
            if st.form_submit_button(label="Update portfolio"):
                
                # Replaced the data in the portfolio with the updated data for the selected acount
                if selected_account != 'All accounts':
                    st.session_state.loaded_portfolio.holdings.loc[st.session_state.loaded_portfolio.holdings['account'] == selected_account] = updated_portfolio_data
                else: 
                    st.session_state.loaded_portfolio.holdings = updated_portfolio_data


                st.session_state.loaded_portfolio.update_portfolio_holdings()
                st.success("Portfolio updated")


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
                    trigger_rerun = True

                new_proxy = st.text_input("Add new proxy")
                if st.button('Add proxy'):
                    if new_proxy is not None:
                        if len(new_proxy) > 0 and new_proxy not in st.session_state.loaded_portfolio.proxies:
                            st.session_state.loaded_portfolio.proxies.append(new_proxy)
                            st.session_state.loaded_portfolio.update_portfolio_proxies()
                            st.success(f'Proxy {new_proxy} added')
                            trigger_rerun = True
                        else:
                            st.error(f'Proxy {new_proxy} was not added.')


            if st.button('Load new ETF proxies'):
                with st.spinner('Loading proxies...'):
                    st.session_state.proxies = find_proxy_etf(min_proxy_age)
                    trigger_rerun = True

            if 'proxies' in st.session_state:
                st.success('Loaded proxies:')
                selected_proxies = st.data_editor(st.session_state.proxies)
                # list of selected proxie tickers
                selected_proxy_tickers = selected_proxies['Symbol'].tolist()
                # if st.button('Add proxies'):
                #     loaded_portfolio.update_portfolio_proxies(selected_proxies)
                    
                #     trigger_rerun = True

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
                    trigger_rerun = True

                new_account = st.text_input("Add new account")
                if st.button('Add account'):
                    if new_account is not None:
                        if len(new_account) > 0 and new_account not in st.session_state.loaded_portfolio.accounts:
                            st.session_state.loaded_portfolio.accounts.append(new_account)
                            st.session_state.loaded_portfolio.update_portfolio_accounts()
                            st.success(f'Account {new_account} added')
                            trigger_rerun = True
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
                    trigger_rerun = True

                new_category = st.text_input("Add new category")
                if st.button('Add category'):
                    if new_category is not None:
                        if len(new_category) > 1 and new_category not in st.session_state.loaded_portfolio.categories:
                            st.session_state.loaded_portfolio.categories.append(new_category)
                            st.session_state.loaded_portfolio.update_portfolio_categories()
                            st.success(f'Category {new_category} added')
                            
                            trigger_rerun = True
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
                            trigger_rerun = True
                        else:
                            st.error("Failed to upload portfolio")
                    else:
                        st.error("No excel file uploaded")

    

        if trigger_rerun:

            if 'rerun_count' not in st.session_state:
                st.session_state.rerun_count = 1
            else:
                st.session_state.rerun_count += 1
            print(
                f'reran program for the {st.session_state.rerun_count} time')
            st.experimental_rerun()
