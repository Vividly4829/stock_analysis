import pandas as pd
import yfinance as yf
import streamlit as st
from datetime import datetime, timedelta
import os
import json
from datetime import datetime, timedelta

from program.workers.find_etf_holdings import find_etf_holdings


class stock_info:
    def __init__(self, ticker: str):
        self.ticker = ticker

        self.stock_data, self.stock_info = self.download_stock_data()
        self.holdings = self.load_etf_holdings()

    def download_stock_data(self) -> tuple[pd.DataFrame, dict]:

        # check if the directory exists and make it if not, but use an if statement not a try
        if not os.path.exists(f'data/stock_database/{self.ticker}'):
            print(
                f'The directory {self.ticker} does not exist. We will create it and download the data for the first time!')
            os.makedirs(f'data/stock_database/{self.ticker}')
            stock = yf.Ticker(self.ticker)
            hist = stock.history(period="max")
            hist.to_csv(
                f'data/stock_database/{self.ticker}/{self.ticker}_historical_data.csv')

            with open(f'data/stock_database/{self.ticker}/{self.ticker}_info.json', 'w') as f:
                json.dump(stock.info, f)
            return hist, stock.info

        else:
            # If the data exists, we want to load or append rather then just download the data

            current_time = datetime.now()
            file_mod_time = datetime.fromtimestamp(os.path.getmtime(
                f'data/stock_database/{self.ticker}/{self.ticker}_historical_data.csv'))

            # Check if the file is no older than 1 month
            if (current_time - file_mod_time) <= timedelta(days=1):

                print(
                    f'The data was already downloaded today for {self.ticker}! Skipping data download entirely.')

                with open(f'data/stock_database/{self.ticker}/{self.ticker}_info.json', 'r') as r:
                    stock_info = json.load(r)

                hist_log = pd.read_csv(
                    f'data/stock_database/{self.ticker}/{self.ticker}_historical_data.csv')

                # Convert the date column to datetime
                hist_log['Date'] = pd.to_datetime(hist_log['Date'])

                # Set the date as the index
                hist_log.set_index('Date', inplace=True)

                return hist_log, stock_info

            # Check if the file is no older than 1 month
            elif (current_time - file_mod_time) <= timedelta(days=14):

                print(
                    f'The data was already downloaded in past 14 days {self.ticker}! Skipping historical data download and only getting info.')

                stock = yf.Ticker(self.ticker)
                stock_info = stock.info
                # save stock info as json file
                with open(f'data/stock_database/{self.ticker}/{self.ticker}_info.json', 'w') as f:
                    json.dump(stock_info, f)

                hist_log = pd.read_csv(
                    f'data/stock_database/{self.ticker}/{self.ticker}_historical_data.csv')

                # Convert the date column to datetime
                hist_log['Date'] = pd.to_datetime(hist_log['Date'])

                # Set the date as the index
                hist_log.set_index('Date', inplace=True)

                return hist_log, stock_info

            else:  # If the data was older then one day, redownload info and append the data
                print(
                    f'The data existed from before but was not up to date for {self.ticker}! Downloading new data and appending to the old data.')
                stock = yf.Ticker(self.ticker)
                stock_info = stock.info
                # save stock info as json file
                with open(f'data/stock_database/{self.ticker}/{self.ticker}_info.json', 'w') as f:
                    json.dump(stock_info, f)

                hist = stock.history(period="max")
                hist.to_csv(
                    f'data/stock_database/{self.ticker}/{self.ticker}_historical_data.csv')
                return hist, stock_info

    def load_etf_holdings(self):
        if self.stock_info is not None and self.stock_info['quoteType'] == 'ETF':
            # Define the path to the holdings file
            holdings_file_path = f'data/stock_database/{self.ticker}/{self.ticker}_holdings.json'

            # Check if the holdings file exists
            if os.path.exists(holdings_file_path):
                # Get the current time and the file's last modification time
                current_time = datetime.now()
                file_mod_time = datetime.fromtimestamp(
                    os.path.getmtime(holdings_file_path))

                # Check if the file is no older than 1 month
                if (current_time - file_mod_time) <= timedelta(days=30):
                    print(
                        f'holdings for {self.ticker} already exists from past 30 days, skipping!')
                    # If the file is recent, load and return the holdings
                    with open(holdings_file_path, 'r') as r:
                        holdings = json.load(r)
                    return holdings

            print(
                f'holdings for {self.ticker} did not exist or was older than 30 days, downloading!')
            # If the file doesn't exist or is older than 1 month, fetch new holdings
            holdings = find_etf_holdings(self.ticker)
            # Save the new holdings to the file
            os.makedirs(os.path.dirname(holdings_file_path), exist_ok=True)
            with open(holdings_file_path, 'w') as f:
                json.dump(holdings, f)
            return holdings

    def find_previous_close_price(self):
        if self.stock_data is None:
            return None
        return self.stock_info['previousClose']

    def find_currency(self):
        if self.stock_info is None:
            return None
        return self.stock_info['currency']
