import pandas as pd
import yfinance as yf
import streamlit as st
from datetime import datetime, timedelta
import os
import json

from program.workers.find_etf_holdings import find_etf_holdings
from program.workers.find_fund_valuation import find_norwegian_mutual_fund_value


class asset_info:
    def __init__(self, ticker: str, type: str = 'stock'):
        self.ticker = ticker
        self.type = type
        self.stock_data = None
        self.stock_info = None
        self.holdings = None

    def download_norwegian_mutual_fund_value(self):
        if type == 'NORWEGIAN MUTUAL FUND':

            # check if the directory exists and make it if not
            if not os.path.exists(f'data/norwegian_mutual_fund_database/{self.ticker}'):
                os.makedirs(
                    f'data/norwegian_mutual_fund_database/{self.ticker}')
                print(
                    f'Directory {self.ticker} created. Downloading data for the first time!')

                value = find_norwegian_mutual_fund_value(1, self.ticker)

                # Write the value to a json file
                with open(f'data/norwegian_mutual_fund_database/{self.ticker}/{self.ticker}_value.json', 'w') as f:
                    json.dump(value, f)

                return value

            else:
                current_time = datetime.now()
                file_mod_time = datetime.fromtimestamp(os.path.getmtime(
                    f'data/norwegian_mutual_fund_database/{self.ticker}/{self.ticker}_value.json'))

                if (current_time - file_mod_time) > timedelta(days=1):
                    print(
                        f'Data for {self.ticker} is not up to date. Downloading new data.')
                    value = find_norwegian_mutual_fund_value(1, self.ticker)
                    with open(f'data/norwegian_mutual_fund_database/{self.ticker}/{self.ticker}_value.json', 'w') as f:
                        json.dump(value, f)
                    return value
                else:
                    with open(f'data/norwegian_mutual_fund_database/{self.ticker}/{self.ticker}_value.json', 'r') as r:
                        value = json.load(r)
                    return value

    def download_stock_historical_data(self) -> pd.DataFrame:
        # Check if the directory exists and make it if not
        if not os.path.exists(f'data/stock_database/{self.ticker}'):
            os.makedirs(f'data/stock_database/{self.ticker}')
            print(
                f'Directory {self.ticker} created. Downloading historical data for the first time!')

            stock = yf.Ticker(self.ticker)
            hist = stock.history(period="max")
            hist.to_csv(
                f'data/stock_database/{self.ticker}/{self.ticker}_historical_data.csv')
            return hist
        else:
            current_time = datetime.now()
            file_mod_time = datetime.fromtimestamp(os.path.getmtime(
                f'data/stock_database/{self.ticker}/{self.ticker}_historical_data.csv'))

            if (current_time - file_mod_time) > timedelta(days=14):
                print(
                    f'Data for {self.ticker} is not up to date. Downloading new data.')
                stock = yf.Ticker(self.ticker)
                hist = stock.history(period="max")
                hist.to_csv(
                    f'data/stock_database/{self.ticker}/{self.ticker}_historical_data.csv')

            hist_log = pd.read_csv(
                f'data/stock_database/{self.ticker}/{self.ticker}_historical_data.csv')
            hist_log['Date'] = pd.to_datetime(hist_log['Date'])
            hist_log.set_index('Date', inplace=True)
            self.stock_data = hist_log
            return hist_log

    def download_stock_info(self) -> dict:
        if not os.path.exists(f'data/stock_database/{self.ticker}'):
            os.makedirs(f'data/stock_database/{self.ticker}', exist_ok=True)

        stock = yf.Ticker(self.ticker)
        if not os.path.exists(f'data/stock_database/{self.ticker}/{self.ticker}_info.json'):
            with open(f'data/stock_database/{self.ticker}/{self.ticker}_info.json', 'w') as f:
                json.dump(stock.info, f)
        else:
            current_time = datetime.now()
            file_mod_time = datetime.fromtimestamp(os.path.getmtime(
                f'data/stock_database/{self.ticker}/{self.ticker}_info.json'))
            if (current_time - file_mod_time) > timedelta(days=1):
                print(
                    f'Info for {self.ticker} is not up to date. Downloading new info.')
                with open(f'data/stock_database/{self.ticker}/{self.ticker}_info.json', 'w') as f:
                    json.dump(stock.info, f)

        with open(f'data/stock_database/{self.ticker}/{self.ticker}_info.json', 'r') as r:
            stock_info = json.load(r)
        self.stock_info = stock_info
        return stock_info

    # The rest of the class remains unchanged...

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

            self.holdings = holdings
            return holdings

    def find_previous_close_price(self):
        if self.type == 'NORWEGIAN MUTUAL FUND':
            return self.download_norwegian_mutual_fund_value()

        else:
            if self.stock_data is None and self:
                self.download_stock_info()
            return self.stock_info['previousClose']  # type: ignore

    def find_currency(self):
        if self.stock_info is None:
            self.download_stock_info()
        return self.stock_info['currency']  # type: ignore
