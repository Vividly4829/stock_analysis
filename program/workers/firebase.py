import sys
import os
from google.cloud import firestore
import pandas as pd
import yfinance as yf
from datetime import datetime
import traceback

sys.path.insert(1, os.path.abspath('.'))

# Authenticate to Firestore with the JSON account key.
db = firestore.Client.from_service_account_json("files\\firebase\\mona-one-dev-firebase-adminsdk-u35bk-3ae0c43dda.json")



class firebaseUserPortfolio:

    def __init__(self, user_portfolio_name):
        self.user_portfolio_name = user_portfolio_name
        self.user_portfolio = self.get_portfolio()
        self.holdings = self.get_portfolio_holdings_df() # A dataframe with the portfolio holdings
        self.accounts = self.get_portfolio_accounts() # A list with the portfolio accounts
        self.categories = self.get_portfolio_categories() # A list with the portfolio categories|
    


    def get_etf_inception_date_yfinance(self, ticker):
        
        try:
            etf = yf.Ticker(ticker)
            history = etf.history(period='max')
            inception_date = history.index[0].date()         
            return inception_date
        
        except:
            # return the date of today if the inception date could not be found
            return datetime.today().strftime('%Y-%m-%d')
        


    def get_portfolio_holdings_df(self) -> pd.DataFrame | None:
        if self.user_portfolio is not None:
            try:
                holdings = self.user_portfolio['holdings']
                df = pd.DataFrame(holdings)
                df['Inception Date'] = df['Ticker'].apply(lambda x: self.get_etf_inception_date_yfinance(x))
          
                return df
            
            except:
                tb = traceback.format_exc()
                print(tb)
                return None
            
    def get_portfolio_accounts(self) -> list | None:
        if self.user_portfolio is not None:
            try:
                accounts = self.user_portfolio['accounts']
                return accounts
            except:
                return []
            
    def get_portfolio_categories(self) -> list | None:
        if self.user_portfolio is not None:
            try:
                categories = self.user_portfolio['categories']
                return categories
            except:
                return []
    
    def get_portfolio(self) -> dict | None:
        
        try:
            doc_ref = db.collection("user_portfolio").document(self.user_portfolio_name)
            return  doc_ref.get().to_dict()
        except:
            return None
        
    def upload_excel_portfolio(self, new_portfolio: list):
        try:
            doc_ref = db.collection("user_portfolio").document(self.user_portfolio_name)
            doc_ref.update({'holdings': new_portfolio})
            return True
        except:
            return False

    def update_portfolio_holdings(self):
        if self.holdings is not None:
            doc_ref = db.collection("user_portfolio").document(self.user_portfolio_name)
            doc_ref.update({'holdings': self.holdings.to_dict(orient='records')})

    def update_portfolio_accounts(self):
        if self.accounts is not None:
            doc_ref = db.collection("user_portfolio").document(self.user_portfolio_name)
            doc_ref.update({'accounts': self.accounts})

    def update_portfolio_categories(self):
        if self.categories is not None:
            doc_ref = db.collection("user_portfolio").document(self.user_portfolio_name)
            doc_ref.update({'categories': self.categories})

    


portfolio = firebaseUserPortfolio('ruben_account')
print(portfolio.holdings)
