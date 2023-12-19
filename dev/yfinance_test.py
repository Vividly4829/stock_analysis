import yfinance as yf

stock = yf.Ticker('EUNL.DE')
current_price = stock.info['previousClose']
print(current_price)