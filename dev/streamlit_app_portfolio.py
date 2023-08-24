import streamlit as st


from classes.portfolio_class import PortfolioDefiner

st.title('TOTAL PORTFOLIO ANALYSER')
manage_portfolio, portfolio_performance, portfolio_analysis = st.tabs(["Manage portfolio", "Performance", "Analysis"])

# crate a streamlit tab called *Manage portfolio*
with manage_portfolio:
    portfolio = st.selectbox('Select portfolio', ['formue'])


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

    portfolio_definer = PortfolioDefiner(portfolio)
    with st.form(key="Update portfolio"):
        st.info("Select row and press 'del' button on keyboard to delete. Press '+' to add a new row")
        portfolio_definer.update_dataframe(st.data_editor(portfolio_definer.portfolio_df, num_rows="dynamic", column_config=column_config))
        if st.form_submit_button(label="Update portfolio"):
            st.success("Portfolio updated")

    # Create a streamlit form to add a new item to the portfolio
