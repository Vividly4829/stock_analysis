import pandas as pd
import yfinance as yf

import traceback
import streamlit as st
import datetime

from program.workers.find_fund_valuation import find_norwegian_mutual_fund_value
from program.workers.currency_exchange_rate_scraper import get_exchange_rates
# Create a currency converter object


def calculate_portfolio_value(df: pd.DataFrame, tickers=None):

    print('Calculating portfolio value... for tickers:', tickers)
    usd_to_nok_rate, usd_to_eur_rate, eur_to_nok_rate = get_exchange_rates()

    def calculate_value(row):
        if tickers is not None and row['Ticker'] not in tickers:
            return row['Value (NOK)'], row['Value (EUR)'], row['Value (USD)'], row['Currency']

        ticker = row['Ticker']

        # Skip tickers that are not in the list of tickers if the list is not empty
        quantity = row['Quantity']
        currency = row['Currency']
        category = row['Category']
        type = row['Type']

        ticker = ticker.strip()  # Remove leading/trailing whitespaces
        if category == 'CASH':
            value = quantity

        elif 'FUND' in type:
            fund_name = ticker.split('!')[0]

            st.warning(f'Fetching data for fund {fund_name}...')
            value = find_norwegian_mutual_fund_value(quantity, fund_name)
            currency = 'NOK'
            if value is None:
                st.error(f'Failed to fetch data for fund{ticker}...')
                tb = traceback.format_exc()
                print(f'Failed to fetch data for {ticker}...')
                print(tb)
                value = 0
                currency = 'NOK'  # Set currency to NOK if data fetching fails
        else:
            try:
                st.info(f'Fetching data for stock {ticker}...')
                # print(f'Fetching data for stock {ticker}...')
                stock = yf.Ticker(ticker)
                # 'max' for all available data
                hist = stock.history(period="max")
                hist.to_csv(
                    f'data/historical_stock_data/{ticker}_historical_data.csv')

                current_price = stock.info['previousClose']
                value = current_price * quantity
                currency = stock.info['currency']
                # print(f'Found data for  {ticker}...' + str(value))
            except:
                st.error(f'Failed to fetch data for stock {ticker}...')
                tb = traceback.format_exc()
                print(f'Failed to fetch data for {ticker}...')
                print(tb)
                value = 0
                currency = 'NOK'  # Set currency to NOK if data fetching fails

        if currency == 'NOK':
            nok_value = value
            eur_value = value / eur_to_nok_rate  # type: ignore
            usd_value = value / usd_to_nok_rate  # type: ignore
        elif currency == 'EUR':
            nok_value = value * eur_to_nok_rate  # type: ignore
            eur_value = value
            usd_value = value / usd_to_eur_rate  # type: ignore
        elif currency == 'USD':
            nok_value = value * usd_to_nok_rate  # type: ignore
            eur_value = value * usd_to_eur_rate  # type: ignore
            usd_value = value
        else:
            nok_value = 0
            eur_value = 0
            usd_value = 0

        return int(nok_value), int(eur_value), int(usd_value), currency

    # Apply the function to calculate the current value for each row
    df['Value (NOK)'], df['Value (EUR)'], df['Value (USD)'], df['Currency'] = zip(
        *df.apply(calculate_value, axis=1))

    exchange_rates = {'EUR NOK': eur_to_nok_rate,
                      'USD EUR': usd_to_eur_rate, 'USD NOK': usd_to_nok_rate}
    # Return the updated dataframe and the used exchange rates
    return df, exchange_rates


def calculate_portfolio_total_value(df: pd.DataFrame):
    # Calculate the total value of the portfolio in NOK, EUR, and USD
    total_value_nok = int(df['Value (NOK)'].sum())
    total_value_eur = int(df['Value (EUR)'].sum())
    total_value_usd = int(df['Value (USD)'].sum())

    # Return a dict with the total values
    return {'NOK': total_value_nok, 'EUR': total_value_eur, 'USD': total_value_usd}
