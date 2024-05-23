import yfinance as yf

stock = yf.Ticker('TSLA')
current_price = stock.financials
print(current_price)
