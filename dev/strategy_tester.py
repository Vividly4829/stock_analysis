import yfinance as yf
from datetime import datetime, timedelta
import time
import pandas as pd
from matplotlib import pyplot as plt

# Define the start and end dates
start_date = '2010-11-01'
end_date = '2023-04-30'

benchmarks = ['SPY', 'IAU', 'TQQQ', 'QQQ']
etf_portfolio = {'IAU': 0.5, 'TQQQ': 0.5}
rebalance_treshold = 30 # days we allow portfolio to be out of balance before rebalancing
initial_capital = 100

transaction_cost = 0.0035 # 0.35% transaction cost
rebalance_variance = 0.05 # 5% variance from the desired ratio before rebalancing

days_out_of_balance = 0 # number of days the portfolio is out of balance
total_portfolio_value = 0 # total value of the portfolio

cash = 0 # cash available for trading

balance = {} # dictionary containing the number of shares, value, price and ratio of each ETF in the portfolio
benchmarks_balance = {} # dictionary containing the number of shares, value, price and ratio of each ETF in the benchmarks to compare against.

# Initiate the balance dataframe that logs the portfolio value, number of days out of balance, value of each ETF and ratio of each ETF
balance_df_columns = ['Total Portfolio Value', 'Days Out of Balance']
for key in etf_portfolio.keys():
    balance_df_columns.append(f'{key} Value')
    balance_df_columns.append(f'{key} Ratio')
balance_df = pd.DataFrame(columns=balance_df_columns)

# Initiate the benchmarks dataframe that logs the value of each benchmark
benchmarks_df_columns = []
for key in benchmarks:
    benchmarks_df_columns.append(f'{key} Value')
benchmarks_df = pd.DataFrame(columns=benchmarks_df_columns)



def download_historical_stock_data(start_date, end_date, etf_portfolio: dict):
    historical_stock_data = {}
    for i in etf_portfolio.keys():
        data = yf.download(i, start=start_date, end=end_date)
        historical_stock_data[i] = data

    for i in benchmarks:
        if i not in etf_portfolio.keys():
            data = yf.download(i, start=start_date, end=end_date)
            historical_stock_data[i] = data

    return historical_stock_data


def create_list_of_dates_string_format(start_date, end_date):

    dates_string_format = []
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    # Loop through each date
    current_date = start_date
    while current_date <= end_date:
        #print(current_date.strftime('%Y-%m-%d'))  # print out the date as a string in 'YYYY-MM-DD' format
        dates_string_format.append(current_date.strftime('%Y-%m-%d'))
        current_date += timedelta(days=1)  # increment the current date by one day
    return dates_string_format

def define_starting_portfolio (etf_portfolio: dict, initial_capital, etf_prices: dict, dates_string_format: list):

    start_balance = {}
    for date in dates_string_format:
        if len(start_balance.keys()) != len(etf_portfolio.keys()):
            for etf in etf_portfolio.keys():
                try:
                    if etf not in start_balance.keys():
                        etf_start_price = etf_prices[etf].loc[datetime.strptime(date, '%Y-%m-%d'), 'Close']
                        start_balance[etf] = {'number_of_shares' : initial_capital * etf_portfolio[etf] / etf_start_price, 'value': initial_capital * etf_portfolio[etf], 'price': etf_start_price,}
                        # print(f'{etf} start price: {etf_start_price} date: {date}')

                except:
                    pass
                    # print('error not a market day.')
    return start_balance

def starting_volumne_benchamarks (benchmarks: list, initial_capital, etf_prices: dict, dates_string_format: list):

    start_balance = {}
    for date in dates_string_format:
        if len(start_balance.keys()) != len(benchmarks):
            for benchmark in benchmarks:
                try:
                    if benchmark not in start_balance.keys():
                        etf_start_price = etf_prices[benchmark].loc[datetime.strptime(date, '%Y-%m-%d'), 'Close']
                        start_balance[benchmark] = {
                            'number_of_shares': initial_capital  / etf_start_price,
                            'value': initial_capital,
                            'price': etf_start_price,
                        }
                        # print(f'{etf} start price: {etf_start_price} date: {date}')

                except:
                    pass
                    # print('error not a market day.')
    return start_balance


def update_balance(date, balance: dict, etf_prices: dict):
    for etf in etf_portfolio.keys():
        try:
            etf_price = etf_prices[etf].loc[datetime.strptime(date, '%Y-%m-%d'), 'Close']

            balance[etf]['value'] = balance[etf]['number_of_shares'] * etf_price
            balance[etf]['price'] = etf_price
            balance = check_balance_ratio(balance, date)
            # print(f'{etf} price: {etf_price}')¨
        except:
            pass

def update_benchmarks(date, benchmarks_balance: dict, etf_prices: dict):

    for benchmark in benchmarks:
        try:
            benchmark_price = etf_prices[benchmark].loc[datetime.strptime(date, '%Y-%m-%d'), 'Close']
            benchmarks_balance[benchmark]['value'] = benchmarks_balance[benchmark]['number_of_shares'] * benchmark_price
            benchmarks_balance[benchmark]['price'] = benchmark_price
            # print(f'{etf} price: {etf_price}')¨

            new_row = {}
            for key in benchmarks_balance.keys():
                new_row[f'{key} Value'] = benchmarks_balance[key]['value']

            benchmarks_df.loc[date] = new_row

        except:
            pass

def check_balance_ratio(balance: dict, date) -> dict:

    global days_out_of_balance
    global total_portfolio_value
    global transaction_cost

    unbalanced = False
    total_portfolio_value = 0
    for key in balance.keys():
        total_portfolio_value += balance[key]['value']

    for key in balance.keys():
        balance[key]['ratio'] = balance[key]['value'] / total_portfolio_value
        if balance[key]['ratio'] > etf_portfolio[key] + rebalance_variance:
            unbalanced = True

    if unbalanced:
        days_out_of_balance += 1
        if days_out_of_balance > rebalance_treshold:
            print(f'Out of balance for {days_out_of_balance} days. Rebalancing on date {date}.')
            balance = rebalance(balance, transaction_cost)
            check_balance_ratio(balance, date) # recalculate the balance ratio after rebalancing
            days_out_of_balance = 0

    else:
        days_out_of_balance = 0



    new_row = {
        'Total Portfolio Value': total_portfolio_value,
        'Days Out of Balance': days_out_of_balance
    }

    for key in balance.keys():
        new_row[f'{key} Value'] = balance[key]['value']
        new_row[f'{key} Ratio'] = balance[key]['ratio']


    # add a new row to the dataframe with the date, total portfolio value, iau value, tqqq value, iau ratio, tqqq ratio and number of days unbalanced
    balance_df.loc[date] = new_row

    return balance

def rebalance(balance: dict, transaction_cost: float,) -> dict:
    # Loop through each ETF in the portfolio
    global total_portfolio_value
    global cash

    print('Rebalancing')

    # Sell first to generate cash
    for key in balance.keys():
        if balance[key]['ratio'] > etf_portfolio[key] + rebalance_variance:
            desired_number_shares = total_portfolio_value * etf_portfolio[key] / balance[key]['price']
            number_of_shares_to_sell = balance[key]['number_of_shares'] - desired_number_shares
            cash += number_of_shares_to_sell * balance[key]['price'] * (1 - transaction_cost)
            balance[key]['number_of_shares'] -= number_of_shares_to_sell
            balance[key]['value'] = balance[key]['number_of_shares'] * balance[key]['price']

    # Buy with available cash
    for key in balance.keys():
        if balance[key]['ratio'] < etf_portfolio[key] - rebalance_variance:
            desired_number_shares = total_portfolio_value * etf_portfolio[key] / balance[key]['price']
            number_of_shares_to_buy = (desired_number_shares - balance[key]['number_of_shares']) * (1 -transaction_cost) # we need to deduct the ammount of transaction cost
            cash -= (desired_number_shares - balance[key]['number_of_shares']) * balance[key]['price']
            balance[key]['number_of_shares'] += number_of_shares_to_buy
            balance[key]['value'] = balance[key]['number_of_shares'] * balance[key]['price']

    return balance




print("🏁" * 10)


dates_string_format = create_list_of_dates_string_format(start_date, end_date)
etf_prices = download_historical_stock_data(start_date, end_date, etf_portfolio=etf_portfolio)
balance = define_starting_portfolio(etf_portfolio, initial_capital, etf_prices, dates_string_format)
balance = check_balance_ratio(balance, start_date)
benchmarks_balance = starting_volumne_benchamarks(benchmarks, initial_capital, etf_prices, dates_string_format)


print(f'balance: {balance}')
for key in balance.keys():
    print(f'{key} value: {balance[key]["value"]}')
    print(f'{key} price: {balance[key]["price"]}')
    print(f'{key} number of shares: {balance[key]["number_of_shares"]}')
    print(f'{key} ratio: {balance[key]["ratio"]}')


# Now we wish to loop through each date and and update the balance
# Loop through each date
for date in dates_string_format:
    update_balance(date, balance, etf_prices)
    update_benchmarks(date, benchmarks_balance, etf_prices)


# Analyse the results

print("🏁" * 10)


print(benchmarks_df)

for key in balance.keys():
    print(f'{key} value: {balance[key]["value"]}')
    print(f'{key} price: {balance[key]["price"]}')
    print(f'{key} number of shares: {balance[key]["number_of_shares"]}')
    print(f'{key} ratio: {balance[key]["ratio"]}')

print(f'cash: {cash}')
print(f'days out of balance: {days_out_of_balance}')
print(f'total portfolio value: {total_portfolio_value}')
print(f'Total return on investment: {total_portfolio_value/initial_capital*100} %')


# export the dataframe to csv
balance_df.to_csv('portfolio_value.csv')

# Specify the columns to plot of the balance dataframe
columns_to_plot = ['Total Portfolio Value']
for key in etf_portfolio.keys():
    columns_to_plot.append(f'{key} Value')


plt.style.use('dark_background')

# Create a figure and subplots
fig, ax = plt.subplots()

# Plot the specified columns of the balance dataframe and benchmarks dataframe
balance_df[columns_to_plot].plot(ax=ax, linestyle='dotted')

benchmarks_df.plot(ax=ax)


# Add vertical lines for 'Days Out of Balance' column with value '30'
vertical_dates = balance_df[balance_df['Days Out of Balance'] == 30].index
for date in vertical_dates:
    ax.axvline(x=date, color='red', linestyle='--')
    ax.plot(date, 0, marker='o', markersize=5, color='red')  # Add red dot on the horizontal axis



# Add labels and title to the plot
plt.xlabel('Date')
plt.ylabel('Values')
plt.title('Portfolio Data')

# Display the plot
plt.show()
