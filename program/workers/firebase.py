import sys
import os
from google.cloud import firestore
import pandas as pd

sys.path.insert(1, os.path.abspath('.'))

# Authenticate to Firestore with the JSON account key.
db = firestore.Client.from_service_account_json("files\\firebase\\mona-one-dev-firebase-adminsdk-u35bk-3ae0c43dda.json")



class firebaseUserPortfolio:

    def __init__(self, user_portfolio_name):
        self.user_portfolio_name = user_portfolio_name
        self.user_portfolio = self.get_portfolio()
        self.holdings = self.get_portfolio_holdings_df() # A dataframe with the portfolio holdings
    

    def get_portfolio_holdings_df(self) -> pd.DataFrame | None:
        if self.user_portfolio is not None:
            try:
                holdings = self.user_portfolio['holdings']
                df = pd.DataFrame(holdings)
                return df
            except:
                return None
    
    def get_portfolio(self) -> dict | None:
        
        try:
            doc_ref = db.collection("user_portfolio").document(self.user_portfolio_name)
            return  doc_ref.get().to_dict()
        except:
            return None
        
    def upload_excel_portfolio(self, new_portfolio: list):
        try:
            doc_ref = db.collection("user_portfolio").document(self.user_portfolio_name)
            doc_ref.set({'holdings': new_portfolio})
            return True
        except:
            return False

    def update_portfolio_holdings(self):
        if self.holdings is not None:
            doc_ref = db.collection("user_portfolio").document(self.user_portfolio_name)
            print(f'holdings as dict: {self.holdings.to_dict(orient="records")}')
            doc_ref.set({'holdings': self.holdings.to_dict(orient='records')})




# 