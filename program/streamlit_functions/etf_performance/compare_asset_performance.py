import streamlit as st
from program.workers.calculate_total_return import calculate_annualized_return_with_dividends
import pandas as pd


def analyse_asset_performance():
    st.header('Analyse asset performance')

    tickers = st.text_input('Enter tickers (comma separated)')

    start_year = st.slider('Start year', 1980, 2022, 2005)

    if len(tickers) != 0:
        tickers = tickers.split(',')
        tickers = [ticker.strip() for ticker in tickers]
        # also capitalise all tickers
        tickers = [ticker.upper() for ticker in tickers]
        st.write(f'Selected tickers: {tickers}')

        # CREATE A STREAMLIT CoLumn for each ticker

        columns = st.columns(len(tickers))

        for idx, ticker in enumerate(tickers):

            with st.spinner(f'Loading {ticker}...'):
                annualized_return, warning = calculate_annualized_return_with_dividends(
                    ticker, start_year)
                columns[idx].write(f'Annualized return for {ticker}:')
                if warning is not None:
                    columns[idx].warning(warning)
                else:
                    columns[idx].success(
                        f'Successfully calculated annualized return from {start_year}  to {pd.Timestamp.today().year - 1}')
                columns[idx].write(annualized_return)
                columns[idx].write('---')
