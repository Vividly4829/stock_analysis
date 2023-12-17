import pandas as pd
import yfinance as yf
from forex_python.converter import CurrencyRates
import traceback
from dataclasses import dataclass
import streamlit as st

# Create a currency converter object
c = CurrencyRates()


def calculate_portfolio_value(df: pd.DataFrame, tickers = None) -> pd.DataFrame:

# Define a function to calculate the current value in NOK, EUR, and USD
    def calculate_value(row):
        ticker = row['Ticker']

        # Skip tickers that are not in the list of tickers if the list is not empty
        if tickers is not None and ticker not in tickers:
            return row['Value (NOK)'], row['Value (EUR)'], row['Value (USD)']
        quantity = row['Quantity']
        currency = row['Currency']

        ticker = ticker.strip()  # Remove leading/trailing whitespaces
        if ticker == 'CASH' or ticker == 'FUND':
            value = quantity
        else:
            try:
                st.info(f'Fetching data for {ticker}...')
                stock = yf.Ticker(ticker)
                current_price = stock.info['previousClose']
                value = current_price * quantity
                currency = stock.info['currency']
            except:
                st.error(f'Failed to fetch data for {ticker}...')
                tb = traceback.format_exc()
                print(f'Failed to fetch data for {ticker}...')
                print(tb)
                value = 0
                currency = 'NOK'  # Set currency to NOK if data fetching fails

        if currency == 'NOK':
            nok_value = value
            eur_value = c.convert('NOK', 'EUR', value)
            usd_value = c.convert('NOK', 'USD', value)
        elif currency == 'EUR':
            nok_value = c.convert('EUR', 'NOK', value)
            eur_value = value
            usd_value = c.convert('EUR', 'USD', value)
        elif currency == 'USD':
            nok_value = c.convert('USD', 'NOK', value)
            eur_value = c.convert('USD', 'EUR', value)
            usd_value = value
        else:
            nok_value = 0
            eur_value = 0
            usd_value = 0

        return int(nok_value), int(eur_value), int(usd_value)

    # Apply the function to calculate the current value for each row
    df['Value (NOK)'], df['Value (EUR)'], df['Value (USD)'] = zip(*df.apply(calculate_value, axis=1))
    return df

def calculate_portfolio_total_value(df: pd.DataFrame):
    # Calculate the total value of the portfolio in NOK, EUR, and USD
    total_value_nok = int(df['Value (NOK)'].sum())
    total_value_eur = int(df['Value (EUR)'].sum())
    total_value_usd = int(df['Value (USD)'].sum())

    # Return a dict with the total values
    return {'NOK': total_value_nok, 'EUR': total_value_eur, 'USD': total_value_usd}