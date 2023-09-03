import pandas as pd
import yfinance as yf
from forex_python.converter import CurrencyRates
import traceback
from dataclasses import dataclass

# Read the Excel sheet into a DataFrame
df = pd.read_excel('formue.xlsx')

# Create a currency converter object
c = CurrencyRates()


def calculate_portfolio_value(dataframe: pd.DataFrame):

    # Define a function to calculate the current value in NOK, EUR, and USD
    def calculate_value(row):
        ticker = row['Ticker']
        quantity = row['quantity']
        currency = row['currency']
        account = row['account']
        proxy = row['Proxy']


        ticker = ticker.strip()  # Remove leading/trailing whitespaces


        if ticker == 'CASH' or ticker == 'FUND':
            value = quantity
        else:
            try:
                print(f'Fetching data for {ticker}...')
                stock = yf.Ticker(ticker)
                current_price = stock.info['previousClose']
                value = current_price * quantity
                currency = stock.info['currency']
            except:
                print(f'Failed to fetch data for {ticker}...')
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

    # log the values of the portfolio
    todays_date = pd.Timestamp.today().strftime('%Y-%m-%d')
    day_log_df = df[['account', 'Ticker', 'quantity', 'Value (NOK)', 'Value (EUR)', 'Value (USD)']]
    day_log_df.to_csv(f'{todays_date}.csv', index=False)

    # calculate the key values for the portfolio
    portfolio_summary = {}

    portfolio_summary['total_nok_value'] = df['Value (NOK)'].sum()

    for account in df['account'].unique():
        account_df = df[df['account'] == account]
        account_nok_value = account_df['Value (NOK)'].sum()
        portfolio_summary[account] = account_nok_value


    # Find the total amount of cash
    cash_df = df[df['Ticker'] == 'CASH']
    total_cash = cash_df['Value (NOK)'].sum()

    portfolio_summary['total_cash'] = total_cash

    # Find the sum of all items that have ticker 'IAU', 'IAUM' or 'GLD
    gold_df = df[df['Ticker'].isin(['IAU', 'IAUM', 'GLD'])]
    total_gold = gold_df['Value (NOK)'].sum()

    portfolio_summary['total_gold'] = total_gold
    portfolio_summary['total_stocks'] = portfolio_summary['total_nok_value'] - total_cash - total_gold

    print(portfolio_summary)

    # portfolio_visualiser_df = df.groupby(
    #     'Proxy').sum().reset_index()  # Loop through all the accounts and print the total value for each account

    # Data for portfolio visualiser only.

    # portfolio_visualiser_df = df[['Proxy', 'Value (NOK)']]
    # portfolio_visualiser_df = portfolio_visualiser_df.groupby('Proxy').sum().reset_index()  # Loop through all the accounts and print the total value for each account
    # portfolio_visualiser_df = portfolio_visualiser_df[~portfolio_visualiser_df['Proxy'].isin(['CASH', 'FUND'])]
    # portfolio_visualiser_df.to_csv('portfolio_visualiser.csv', index=False)
