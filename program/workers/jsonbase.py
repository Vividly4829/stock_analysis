
import sys
import os
import pandas as pd
import yfinance as yf
from datetime import datetime
import traceback
import json
import streamlit as st
from program.workers.find_valuation import calculate_portfolio_value, calculate_portfolio_total_value


data_folder = "data"

def read_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def write_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

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
        self.update_portfolio_holdings()
        self.save_portfolio()
        self.accounts = self.get_portfolio_accounts()
        self.categories = self.get_portfolio_categories()
        self.types = self.get_portfolio_types()
        self.total_value = None
        self.exchange_rates = None

    def create_new_portfolio(self):
        try:
            file_path = os.path.join(data_folder, self.user_name, f'{self.user_portfolio_name}.json')
            data = {
                'holdings': [{
                    "Ticker": "Example",
                    "Type": "Example",
                    "Category": "Example",
                    "Quantity": 1,
                    "Account": "Example",
                    "Currency": 'NOK',
                    "Value (NOK)": 1,
                    "Value (EUR)": 1,
                    "Value (USD)": 1,
                }],
                'accounts': [],
                'categories': [],
                'types': []
            }
            write_json(file_path, data)
            return True
        except:
            return False

    def get_etf_inception_date_yfinance(self, ticker):
        try:
            if ticker == 'Cash':
                return datetime.today().strftime('%Y-%m-%d')
            etf = yf.Ticker(ticker)
            history = etf.history(period='max')
            inception_date = history.index[0].date()          
            return inception_date
        except:
            return datetime.today().strftime('%Y-%m-%d')

    def get_portfolio_holdings_df(self, tickers: list | None = None):

        if self.user_portfolio is not None:
            try:
                holdings = self.user_portfolio['holdings']
                df = pd.DataFrame(holdings)
                # Get all the accounts and categories from the holdings and update the categories and accounts in the portfolio with values that were not there before
                accounts = df['Account'].unique().tolist()
                categories = df['Category'].unique().tolist()
  

                # Update the accounts and categories in the portfolio
                self.accounts = accounts
                self.categories = categories
  

                self.update_portfolio_accounts()
                self.update_portfolio_categories()
             

                df, exchange_rates = calculate_portfolio_value(df, tickers=tickers)
                total_values = calculate_portfolio_total_value(df)

                self.exchange_rates = exchange_rates
                self.total_value = total_values
                # Save with the new valuation
      
                self.save_portfolio()
                self.holdings = df
                
                
                return df
            except:
                tb = traceback.format_exc()
                print(tb)
                return None
            


    def load_inception_dates(self):
        if self.holdings is not None:
            self.holdings['Inception Date'] = self.holdings['Ticker'].apply(lambda x: self.get_etf_inception_date_yfinance(x))

    def get_portfolio_types(self):
        if self.user_portfolio is not None:
            try:
                types = self.user_portfolio['types']
                return types
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
            tb = traceback.format_exc()
            print(tb)
            print('failed to get portfolio, ', self.user_name, self.user_portfolio_name)
            return None

    def save_portfolio(self):
        try:
            file_path = os.path.join(data_folder, self.user_name, f'{self.user_portfolio_name}.json')
            write_json(file_path, self.user_portfolio)

            # Also write the portfolio to a folder called 'portfolio logs' with the date as the name of the file
            portfolio_logs_folder = os.path.join(data_folder, self.user_name, 'portfolioLogs', self.user_portfolio_name)
            if not os.path.exists(portfolio_logs_folder):
                os.makedirs(portfolio_logs_folder)
            date = datetime.today().strftime('%Y-%m-%d')
            file_path = os.path.join(portfolio_logs_folder, f'{date}.json')
            write_json(file_path, self.user_portfolio)
            
            return True
        except:
            return False
        
    def upload_excel_portfolio(self, new_portfolio: list):
        try:
 
            if self.user_portfolio is not None:
                self.user_portfolio['holdings'] = new_portfolio
                self.save_portfolio()
                self.holdings = self.get_portfolio_holdings_df()
        except:
            return False
        
    def update_portfolio_holdings(self):
        if self.holdings is not None and self.user_portfolio is not None:
            self.user_portfolio['holdings'] = self.holdings.to_dict(orient='records')
            self.user_portfolio['total value'] = self.total_value
            self.user_portfolio['exchange rates'] = self.exchange_rates
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

    def update_portfolio_types(self):
        if self.types is not None and self.user_portfolio is not None:
            self.user_portfolio['types'] = self.types
            self.save_portfolio()
        else:
            print('failed to update types')

