

import os
import sys
import pandas as pd

sys.path.insert(1, os.path.abspath('.'))

from program.workers.firebase import firebaseUserPortfolio
from program.streamlit_functions.manage_portfolio.proxy_etf_list import find_proxy_etf
import streamlit as st

def streamlit_manage_portfolio():

    

    trigger_rerun = False

    user_portfolio = st.selectbox(
        "Select portfolio", options=['ruben_account'])
    loaded_portfolio = firebaseUserPortfolio(user_portfolio)

    with st.expander("Manage proxies"):
        st.info("Proxies are used to predict future results of newer ETF's based on historical results of ETF's with similar characteristics that have existed for X years or more. The older, the better the prediction of correlation in a portfolio.")
        min_proxy_age = st.slider("Select min age of proxies", min_value=0, max_value=30, value=20)
        proxies = find_proxy_etf(min_proxy_age)
        st.dataframe(proxies)

    with st.expander("Manage accounts"):
        # Create a streamlit select box to select an account
        if loaded_portfolio.accounts is not None:
            account = st.selectbox(
                "Select account", options=list(loaded_portfolio.accounts)) 
            if st.button('Delete account'):
                loaded_portfolio.accounts.remove(account)
                loaded_portfolio.update_portfolio_accounts()
                st.success(f'Account {account} deleted')
                trigger_rerun = True
        
            new_account = st.text_input("Add new account")
            if st.button('Add account'):
                if new_account is not None:
                    if len(new_account) > 0 and new_account not in loaded_portfolio.accounts:      
                        loaded_portfolio.accounts.append(new_account)
                        loaded_portfolio.update_portfolio_accounts()
                        st.success(f'Account {new_account} added')
                        trigger_rerun = True
                    else:
                        st.error(f'Account {new_account} was not added.')

    with st.expander("Manage categories"):
        # Create a streamlit select box to select an account
        if loaded_portfolio.categories is not None:
            category = st.selectbox(
                "Select category", options=list(loaded_portfolio.categories)) 
            if st.button('Delete category'):
                loaded_portfolio.categories.remove(category)
                loaded_portfolio.update_portfolio_categories()
                st.success(f'Category {category} deleted')
                trigger_rerun = True
        
            new_category = st.text_input("Add new category")
            if st.button('Add category'):
                if category is not None:
                    if len(new_category) > 0 and new_category not in loaded_portfolio.categories:      
                        loaded_portfolio.categories.append(new_category)
                        loaded_portfolio.update_portfolio_categories()
                        st.success(f'Category {new_category} added')
                        trigger_rerun = True

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
            excel_file = st.file_uploader("Upload excel file", type=['xlsx'])

            if st.form_submit_button(label="Upload portfolio"):
                if excel_file is not None:
                    df = pd.read_excel(excel_file)
                    df_dict = df.to_dict(orient='records')

                    upload_status = loaded_portfolio.upload_excel_portfolio(
                        df_dict)

                    if upload_status:
                        st.success("Portfolio uploaded")
                        trigger_rerun = True
                    else:
                        st.error("Failed to upload portfolio")
                else:
                    st.error("No excel file uploaded")

    column_config = {
        "Account":
            st.column_config.SelectboxColumn(
                "Account ",
                help="Select the account",
                width="medium",
                options=loaded_portfolio.accounts,
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
                options=loaded_portfolio.categories,
            )
    }

    with st.form(key="Update portfolio"):
        st.info(
            "Select row and press 'delete' button on the keyboard to delete . Press '+' to add a new row")
        loaded_portfolio.holdings = st.data_editor(loaded_portfolio.holdings, num_rows="dynamic", column_config=column_config)  # type: ignore
        if st.form_submit_button(label="Update portfolio"):
            loaded_portfolio.update_portfolio_holdings()
            st.success("Portfolio updated")

    if trigger_rerun:
        st.experimental_rerun()