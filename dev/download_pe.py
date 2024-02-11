import yfinance as yf
import pandas as pd

tesla = yf.Ticker('SOXX')
stock_info = tesla.financials

for i in stock_info:
    print(i, stock_info[i])
