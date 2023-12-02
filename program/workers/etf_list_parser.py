import sys
import os
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

# Read the Excel sheet into a DataFrame
# df = pd.read_excel('files/etf_list/most_traded_etfs.xlsx')

# print(df)


def calculate_annualized_return_dividend_no_reinvest(prices, dividends):
    start_price = prices.iloc[0]
    end_price = prices.iloc[-1]
    num_years = len(prices) / 252  # Assuming 252 trading days in a year
    total_dividends = dividends.sum()
    annualized_return = (((end_price + total_dividends)/ start_price)**(1 / num_years)) - 1
    return annualized_return


def calculate_annualized_return_dividend_with_reinvest(prices, dividends):
    taxes = 0.15
    transaction_cost = 0.0005
    quantity = 1
    start_price = prices.iloc[0]
    end_price = prices.iloc[-1]
    num_years = len(prices) / 252  # Assuming 252 trading days in a year

    # for dividend in dividends:


    # annualized_return = (((end_price + total_dividends) / start_price)**(1 / num_years)) - 1
    return annualized_return


def calculate_annualized_return(prices):
    start_price = prices.iloc[0]
    end_price = prices.iloc[-1]
    num_years = len(prices) / 252  # Assuming 252 trading days in a year
    annualized_return = (((end_price) / start_price)**(1 / num_years)) - 1
    return annualized_return


# for index, row in df.iterrows():
#     symbol = row['Symbol']
#     etf = yf.Ticker(symbol)
#     history = etf.history(period='max')
#     inception_date = history.index[0].date()
#     # Check if the inception data is before 2011 and if not, drop the row
#     if inception_date.year < 2011:
#         df.loc[index, 'Inception Date'] = inception_date
#     else:
#         df.drop(index, inplace=True)
#         continue

#     dividends = etf.dividends
#     annualized_return = calculate_annualized_return(history['Close'])
#     annualized_return_with_div = calculate_annualized_return_dividend_no_reinvest(history['Close'], dividends=dividends)
#     df.loc[index, 'Annualized Return'] = annualized_return
#     df.loc[index, 'Inception Date'] = inception_date
#     print(f'symbol: {symbol}, inception date: {inception_date}, annualized_return: {annualized_return}, annualized_return_with_div: {annualized_return_with_div}')

# df.to_excel('files/etf_list/most_traded_etfs_with_annualised_return.xlsx', index=False)

symbol = 'tsla'
etf = yf.Ticker(symbol)

# Calculate the start date for the past 10 years from the current date
end_date = datetime.now()
start_date = end_date - timedelta(days=10*365)

# Format the dates as strings in 'YYYY-MM-DD' format
start_date_str = start_date.strftime('%Y-%m-%d')
end_date_str = end_date.strftime('%Y-%m-%d')

# Fetch historical data for the specified period
history = etf.history(start=start_date_str, end=end_date_str)

inception_date = history.index[0].date()
prices = history['Close']
# Check if the inception data is before 2011 and if not, drop the row
print('history:', history)


dividends = etf.dividends

quantity = 1
for index, value in dividends.iteritems():
    # print(index)
    price_time_of_dividend = prices.loc[index]
    # print('price at time of dividend:', price_time_of_dividend)
    quantity += value / price_time_of_dividend

print('final quantity:', quantity)

start_price = prices.iloc[0]
end_price = prices.iloc[-1]

print('start price:', start_price)
print('end price:', end_price)
num_years = 10

annualized_return = (((end_price) / start_price)**(1 / num_years)) - 1
print('Total return: ', (end_price) / start_price * 100)
print('annualised return:', annualized_return)

annualized_return_div_reinvest = (((end_price*quantity) / start_price)**(1 / num_years)) - 1

print('Total return dividend reinvest: ', (end_price*quantity) / start_price * 100)
print('annualised return with reinvest:', annualized_return_div_reinvest)
