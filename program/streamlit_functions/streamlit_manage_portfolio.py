from program.workers.firebase import firebaseUserPortfolio
import streamlit as st

import os
import sys
import pandas as pd

sys.path.insert(1, os.path.abspath('.'))


def streamlit_manage_portfolio():
    user_portfolio = st.selectbox(
        "Select portfolio", options=['ruben_account'])
    loaded_portfolio = firebaseUserPortfolio(user_portfolio)
    with st.expander("Show portfolio:"):
        st.write(loaded_portfolio.user_portfolio)

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
                    else:
                        st.error("Failed to upload portfolio")
                else:
                    st.error("No excel file uploaded")

    column_config = {
        "Account":
            st.column_config.SelectboxColumn(
                "account ",
                help="Select the account",
                width="medium",
                options=['nordnet', 'bolero', 'DNB', 'DNB LIV', 'KBC'],
            ),
        "Currency":
            st.column_config.SelectboxColumn(
                "Currency",
                help="Select the currency",
                width="medium",
                options=['NOK', 'EUR', 'USD'],
            )
    }

    with st.form(key="Update portfolio"):
        st.info(
            "Select row and press 'del' button on keyboard to delete. Press '+' to add a new row")
        loaded_portfolio.holdings = st.data_editor(loaded_portfolio.holdings, num_rows="dynamic", column_config=column_config)  # type: ignore
        if st.form_submit_button(label="Update portfolio"):
            loaded_portfolio.update_portfolio_holdings()
            st.success("Portfolio updated")
