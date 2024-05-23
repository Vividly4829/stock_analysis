import streamlit as st
import time
from program.workers.portfolio_database import JsonBaseUserPortfolio


def log_portfolio_change(df):
    st.write('Log changes to portfolio:')
    trade_type = st.selectbox(
        'Type', options=['change', 'initial', 'delete'])

    if trade_type == 'initial':
        col1, col2, col3, col4, col5, col6 = st.columns(6)

        trade_account = col1.selectbox(
            'Account', options=st.session_state.loaded_portfolio.accounts)
        trade_category = col2.selectbox(
            'Category', options=st.session_state.loaded_portfolio.categories)
        trade_ticker = col3.text_input('Ticker')
        trade_type = col4.selectbox(
            'type', options=st.session_state.loaded_portfolio.types + [None])
        trade_units = col5.number_input('Units', value=0)
        trade_currency = col6.selectbox(
            'Currency', options=[None, 'NOK', 'USD', 'EUR'])

        if st.button('Create position'):
            # Add the new line to the dataframe in st.session_state.loaded_portfolio.holdings
            new_line = {
                'Ticker': trade_ticker,
                'Type': trade_type,
                'Category': trade_category,
                'Quantity': trade_units,
                'Account': trade_account,
                'Currency': trade_currency,
            }

            # Add the line to the dataframe

            # Assuming st.session_state.loaded_portfolio.holdings is a pandas DataFrame
            st.session_state.loaded_portfolio.holdings = st.session_state.loaded_portfolio.holdings.append(
                new_line, ignore_index=True)
            # Saves to the database
            st.session_state.loaded_portfolio.update_portfolio_holdings()
            # Reloads the value of the dataframe
            st.session_state.loaded_portfolio.get_portfolio_holdings_df(tickers=[
                                                                        trade_ticker])
            st.success(
                f'Position {trade_ticker} in account {trade_account} created')
            time.sleep(0.3)
            st.session_state['trigger_rerun'] = True

    if trade_type == 'change':

        col1, col2, col3, col4, col5, col6 = st.columns(6)
        trade_account = col1.selectbox(
            'Account', options=df['Account'].unique().tolist())
        trade_ticker = col2.selectbox(
            'Ticker', options=df['Ticker'].unique().tolist())
        trade_category = col3.selectbox('Category', options=df['Category'].unique().tolist(), index=df['Category'].unique(
        ).tolist().index(df.loc[(df['Account'] == trade_account) & (df['Ticker'] == trade_ticker)]['Category'].values[0]))
        trade_type = col4.selectbox(
            'type', options=df['Type'].unique().tolist(), index=df['Type'].unique().tolist().index(df.loc[(df['Account'] == trade_account) & (df['Ticker'] == trade_ticker)]['Type'].values[0]))
        trade_units = col5.number_input('Units', value=int(st.session_state.loaded_portfolio.holdings.loc[(st.session_state.loaded_portfolio.holdings['Account'] == trade_account) & (
            st.session_state.loaded_portfolio.holdings['Ticker'] == trade_ticker)]['Quantity'].values[0]), step=1)

        trade_currency = col6.selectbox(
            'Currency', options=['NOK', 'USD', 'EUR'])
        if st.button('Edit position'):

            # Replace the existing line in the dataframe in st.session_state.loaded_portfolio.holdings where account and ticker match
            st.session_state.loaded_portfolio.holdings.loc[
                (st.session_state.loaded_portfolio.holdings['Account'] == trade_account) &
                (st.session_state.loaded_portfolio.holdings['Ticker'] == trade_ticker),
                ['Ticker', 'Type', 'Category',
                    'Quantity', 'Account', 'Currency']
            ] = [trade_ticker, trade_type, trade_category, trade_units, trade_account, trade_currency]

            # Saves to the database
            st.session_state.loaded_portfolio.update_portfolio_holdings()
            # Reloads the value of the dataframe
            print('Trying to reload the portfolio holdings for ticker: ', trade_ticker)
            st.session_state.loaded_portfolio.get_portfolio_holdings_df(tickers=[
                                                                        trade_ticker])
            st.success(
                f'Position {trade_ticker} in account {trade_account} updated')
            time.sleep(0.3)
            st.session_state['trigger_rerun'] = True

    if trade_type == 'delete':
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        trade_account = col1.selectbox(
            'Account', options=df['Account'].unique().tolist())
        trade_ticker = col2.selectbox(
            'Ticker', options=df['Ticker'].unique().tolist())
        if st.button('Delete position'):
            # Delete the existing line in the dataframe in st.session_state.loaded_portfolio.holdings where account and ticker match
            st.session_state.loaded_portfolio.holdings = st.session_state.loaded_portfolio.holdings[~(
                (st.session_state.loaded_portfolio.holdings['Account'] == trade_account) & (st.session_state.loaded_portfolio.holdings['Ticker'] == trade_ticker))]
            st.session_state.loaded_portfolio.update_portfolio_holdings()

            st.success(
                f'Position {trade_ticker} in account {trade_account} deleted')
            time.sleep(0.3)
            st.session_state['trigger_rerun'] = True

    if st.session_state['trigger_rerun']:
        st.experimental_rerun()
