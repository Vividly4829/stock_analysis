import streamlit as st

import os
import sys
import pandas as pd

sys.path.insert(1, os.path.abspath('.'))

from program.workers.firebase import firebaseUserPortfolio


def streamlit_manage_portfolio():
    user_portfolio = st.selectbox("Select portfolio", options=['ruben_account'])
    loaded_portfolio = firebaseUserPortfolio(user_portfolio)
    st.write(loaded_portfolio.get_portfolio())

    with st.expander("Upload portfolio from excel"):
        # Create a streamlit form to upload a portfolio from an excel file
        with st.form(key="Upload portfolio"):
            excel_file = st.file_uploader("Upload excel file", type=['xlsx'])
            portfolio_name = st.text_input("Portfolio name")
       
            if st.form_submit_button(label="Upload portfolio"):
                if excel_file is not None:
                    df = pd.read_excel(excel_file)
                    df_dict = df.to_dict(orient='records')

                    loaded_portfolio.upload_excel_portfolio(df_dict, portfolio_name)

                    st.success("Portfolio uploaded")
                    print(df_dict)
                else:
                    st.error("No excel file uploaded")
       

    # column_config = {
    #     "Account":
    #         st.column_config.SelectboxColumn(
    #             "account ",
    #             help="Select the account",
    #             width="medium",
    #             options=['nordnet', 'bolero', 'DNB', 'DNB LIV', 'KBC'],
    #         ),
    #     "Currency":
    #         st.column_config.SelectboxColumn(
    #             "Currency",
    #             help="Select the currency",
    #             width="medium",
    #             options=['NOK', 'EUR', 'USD'],
    #         )
    # }

    # portfolio_definer = PortfolioDefiner(portfolio)
    # with st.form(key="Update portfolio"):
    #     st.info("Select row and press 'del' button on keyboard to delete. Press '+' to add a new row")
    #     portfolio_definer.update_dataframe(st.data_editor(portfolio_definer.portfolio_df, num_rows="dynamic", column_config=column_config))
    #     if st.form_submit_button(label="Update portfolio"):
    #         st.success("Portfolio updated")

    # # Create a streamlit form to add a new item to the portfolio
