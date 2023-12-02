
import sys
import os
import pandas as pd
import yfinance as yf
from datetime import datetime
import traceback
import json
import streamlit as st

sys.path.insert(1, os.path.abspath('.'))

data_folder = "data"

def read_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def write_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

@st.cache_data
def get_portfolio_names(user_name):
    try:
        user_folder = os.path.join(data_folder, user_name)
        return [f.replace('.json', '') for f in os.listdir(user_folder) if f.endswith('.json')]
    except:
        return []

class JsonBaseUserPortfolio:

    def __init__(self, user_name, user_portfolio_name):
        self.user_name = user_name
        self.user_portfolio_name = user_portfolio_name
        self.user_portfolio = self.get_portfolio()
        self.holdings = self.get_portfolio_holdings_df()
        self.accounts = self.get_portfolio_accounts()
        self.categories = self.get_portfolio_categories()
        self.proxies = self.get_portfolio_proxies()

    def get_etf_inception_date_yfinance(self, ticker):
        try:
            etf = yf.Ticker(ticker)
            history = etf.history(period='max')
            inception_date = history.index[0].date()         
            return inception_date
        except:
            return datetime.today().strftime('%Y-%m-%d')

    def get_portfolio_holdings_df(self):
        if self.user_portfolio is not None:
            try:
                holdings = self.user_portfolio['holdings']
                df = pd.DataFrame(holdings)
                return df
            except:
                tb = traceback.format_exc()
                print(tb)
                return None

    def load_inception_date_styling(self):
        pass

    def load_inception_dates(self):
        if self.holdings is not None:
            self.holdings['Inception Date'] = self.holdings['Ticker'].apply(lambda x: self.get_etf_inception_date_yfinance(x))

    def get_portfolio_proxies(self):
        if self.user_portfolio is not None:
            try:
                proxies = self.user_portfolio['proxies']
                return proxies
            except:
                return []

    def get_portfolio_accounts(self):
        if self.user_portfolio is not None:
            try:
                accounts = self.user_portfolio['accounts']
                return accounts
            except:
                return []

    def get_portfolio_categories(self):
        if self.user_portfolio is not None:
            try:
                categories = self.user_portfolio['categories']
                return categories
            except:
                return []

    def get_portfolio(self):
        try:
            file_path = os.path.join(data_folder, self.user_name, f'{self.user_portfolio_name}.json')
            return read_json(file_path)
        except:
            return None

    def save_portfolio(self):
        try:
            file_path = os.path.join(data_folder, self.user_name, f'{self.user_portfolio_name}.json')
            write_json(file_path, self.user_portfolio)
            return True
        except:
            return False
        
    def upload_excel_portfolio(self, new_portfolio: list):
        try:
            print('uploading excel portfolio')
            print(new_portfolio)
            if self.user_portfolio is not None:
                self.user_portfolio['holdings'] = new_portfolio
                self.save_portfolio()
                self.holdings = self.get_portfolio_holdings_df()
        except:
            return False

    def update_portfolio_holdings(self):
        if self.holdings is not None and self.user_portfolio is not None:
            self.user_portfolio['holdings'] = self.holdings.to_dict(orient='records')
            self.save_portfolio()
        else:
            print('failed to update holdings')

    def update_portfolio_accounts(self):
        if self.accounts is not None and self.user_portfolio is not None:
            self.user_portfolio['accounts'] = self.accounts
            self.save_portfolio()
        else: 
            print('failed to update accounts')

    def update_portfolio_categories(self):
        if self.categories is not None and self.user_portfolio is not None:
            self.user_portfolio['categories'] = self.categories
            self.save_portfolio()
        else: 
            print('failed to update categories')

    def update_portfolio_proxies(self):
        if self.proxies is not None and self.user_portfolio is not None:
            self.user_portfolio['proxies'] = self.proxies
            self.save_portfolio()
        else:
            print('failed to update proxies')


# Example usage
portfolios = get_portfolio_names('ruben')
print(portfolios)

user_portfolio = JsonBaseUserPortfolio('ruben', portfolios[0])
print(user_portfolio.holdings)
print(user_portfolio.accounts)
print(user_portfolio.categories)


