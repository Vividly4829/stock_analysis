import sys
import os
from google.cloud import firestore

sys.path.insert(1, os.path.abspath('.'))

# Authenticate to Firestore with the JSON account key.
db = firestore.Client.from_service_account_json("files\\firebase\\mona-one-dev-firebase-adminsdk-u35bk-3ae0c43dda.json")



class firebaseUserPortfolio:

    def __init__(self, user_portfolio_name):
        self.user_portfolio_name = user_portfolio_name

    def get_portfolio(self):
     
        doc_ref = db.collection("user_portfolio").document(self.user_portfolio_name)
        return  doc_ref.get().to_dict()

    def upload_excel_portfolio(self, new_portfolio: dict, portfolio_name: str):
        # fix me 
        portfolio = self.get_portfolio()

        # If the document exists and has 'portfolios' field
        if portfolio and 'portfolios' in portfolio:
            current_portfolios = portfolio['portfolios']
        else:
            current_portfolios = {}

        current_portfolios[portfolio_name] = new_portfolio


        doc_ref = db.collection("user_portfolio").document(self.user_portfolio_name)
        doc_ref.update({'portfolios': {portfolio_name:  new_portfolio}})





# 