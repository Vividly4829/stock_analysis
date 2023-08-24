import traceback
import yfinance as yf
from datetime import datetime, timedelta
import time
import pandas as pd
from matplotlib import pyplot as plt


class PortfolioTracker:

    def __init__(self, start_date: str, end_date: str, benchmarks: list, etf_portfolio: dict, rebalance_treshold: int,
                 initial_capital: float, transaction_cost: float, rebalance_variance: float,):

        # Configurable parameters
        self.start_date = start_date
        self.end_date = end_date
        self.benchmarks = benchmarks
        self.etf_portfolio = etf_portfolio
        self.rebalance_treshold = rebalance_treshold
        self.initial_capital = initial_capital
        self.transaction_cost = transaction_cost
        self.rebalance_variance = rebalance_variance


        # Internal parameters
        self.days_out_of_balance = 0
        self.total_portfolio_value = 0
        self.cash = 0

        self.balance = {}
        self.benchmarks_balance = {}

        # Calculate the dates between the start and end date and add them as strings to a list
        self.dates_string_format = self.create_list_of_dates_string_format()

        # Find all ETF prices between the start and end date
        self.etf_prices = self.download_historical_stock_data()
        print('etf prices', self.etf_prices.keys())
        # print all the indexes of self.etf_prices['SPY']
        print(self.etf_prices['SPY'].index)
        # print the datatype of the index
        print(type(self.etf_prices['SPY'].index))
        print(self.etf_prices['SPY'].loc[datetime.strptime('2021-04-30', '%Y-%m-%d'), 'Close'])

        # Create a dataframe to store the balance ratio and total portfolio value for each date
        balance_df_columns = ['Total Portfolio Value', 'Days Out of Balance']
        for key in self.etf_portfolio.keys():
            balance_df_columns.append(f'{key} Value')
            balance_df_columns.append(f'{key} Ratio')
        self.balance_df = pd.DataFrame(columns=balance_df_columns)

        # Create a dataframe to store the value of each benchmark for each date
        benchmarks_df_columns = []
        for key in self.benchmarks:
            benchmarks_df_columns.append(f'{key} Value')
        self.benchmarks_df = pd.DataFrame(columns=benchmarks_df_columns)

        # Calculate the starting portfolio and starting value of benchmarks
        self.define_starting_portfolio()
        self.check_balance_ratio(self.start_date)
        self.starting_volume_benchmarks()

    def create_list_of_dates_string_format(self):

        dates_string_format = []
        start_date = datetime.strptime(self.start_date, '%Y-%m-%d')
        end_date = datetime.strptime(self.end_date, '%Y-%m-%d')

        # Loop through each date
        current_date = start_date
        while current_date <= end_date:
            #print(current_date.strftime('%Y-%m-%d'))  # print out the date as a string in 'YYYY-MM-DD' format
            dates_string_format.append(current_date.strftime('%Y-%m-%d'))
            current_date += timedelta(days=1)  # increment the current date by one day
        return dates_string_format

    def download_historical_stock_data(self):
        etf_prices = {}
        for i in self.etf_portfolio.keys():
            data = yf.download(i, start=self.start_date, end=self.end_date)
            etf_prices[i] = data

        for i in self.benchmarks:
            if i not in self.etf_portfolio.keys():
                data = yf.download(i, start=self.start_date, end=self.end_date)
                etf_prices[i] = data
        return etf_prices


    def define_starting_portfolio(self):
       
        for date in self.dates_string_format:
            if len(self.balance.keys()) != len(self.etf_portfolio.keys()):
                for etf in self.etf_portfolio.keys():
                    try:
                        if etf not in self.balance.keys():
                            etf_start_price = self.etf_prices[etf].loc[datetime.strptime(date, '%Y-%m-%d'), 'Close']
                            self.balance[etf] = {
                                'number_of_shares': self.initial_capital * self.etf_portfolio[etf] / etf_start_price,
                                'value': self.initial_capital * self.etf_portfolio[etf],
                                'price': etf_start_price,
                            }
                    except:
                        pass
       
    def starting_volume_benchmarks(self):

        for date in self.dates_string_format:
            if len(self.benchmarks_balance.keys()) != len(self.benchmarks):
                for benchmark in self.benchmarks:
                    try:
                        if benchmark not in self.benchmarks_balance.keys():
                            etf_start_price = self.etf_prices[benchmark].loc[datetime.strptime(date, '%Y-%m-%d'),
                                                                             'Close']
                            self.benchmarks_balance[benchmark] = {
                                'number_of_shares': self.initial_capital / etf_start_price,
                                'value': self.initial_capital,
                                'price': etf_start_price,
                            }
                    except:
                        pass

    def update_balance(self, date):
        for etf in self.etf_portfolio.keys():
            try:
                # print(f'Updating balance for {etf} on date {date}')
                etf_price = self.etf_prices[etf].loc[datetime.strptime(date, '%Y-%m-%d'), 'Close']
                self.balance[etf]['value'] = self.balance[etf]['number_of_shares'] * etf_price
                self.balance[etf]['price'] = etf_price
                self.check_balance_ratio(date)
                # print(f'successfully updated balance for {etf} on date {date}')
            except:
                tb = traceback.format_exc()
                # print(f'Date {date} not found for {etf}.')
                pass

    def update_benchmarks(self, date):
        for benchmark in self.benchmarks:
            try:
                
                benchmark_price = self.etf_prices[benchmark].loc[datetime.strptime(date, '%Y-%m-%d'), 'Close']
                self.benchmarks_balance[benchmark]['value'] = self.benchmarks_balance[benchmark]['number_of_shares'] * benchmark_price
                self.benchmarks_balance[benchmark]['price'] = benchmark_price
                new_row = {}
                for key in self.benchmarks_balance.keys():
                    new_row[f'{key} Value'] = self.benchmarks_balance[key]['value']

                self.benchmarks_df.loc[date] = new_row
                # print(f'successfully updated benchmarks for {benchmark} on date {date}')
            except:
                tb = traceback.format_exc()
                # print(self.etf_prices[benchmark])
                # print(f'Date {date} not found for {benchmark}')
                pass

    def check_balance_ratio(self, date):

        unbalanced = False
        self.total_portfolio_value = 0
        for key in self.balance.keys():
            self.total_portfolio_value += self.balance[key]['value']

        for key in self.balance.keys():
            self.balance[key]['ratio'] = self.balance[key]['value'] / self.total_portfolio_value
            if self.balance[key]['ratio'] > self.etf_portfolio[key] + self.rebalance_variance:
                unbalanced = True

        if unbalanced:
            self.days_out_of_balance += 1
            if self.days_out_of_balance > self.rebalance_treshold:
                print(f'Out of balance for {self.days_out_of_balance} days. Rebalancing on date {date}.')
                self.rebalance()
                self.check_balance_ratio(date) # recalculate the balance ratio after rebalancing
                self.days_out_of_balance = 0

        else:
            self.days_out_of_balance = 0

        new_row = {
            'Total Portfolio Value': self.total_portfolio_value,
            'Days Out of Balance': self.days_out_of_balance
        }

        for key in self.balance.keys():
            new_row[f'{key} Value'] = self.balance[key]['value']
            new_row[f'{key} Ratio'] = self.balance[key]['ratio']

        # add a new row to the dataframe with the date, total portfolio value, iau value, tqqq value, iau ratio, tqqq ratio and number of days unbalanced
        self.balance_df.loc[date] = new_row


    def rebalance(self):
        print('Rebalancing')

        # Sell first to generate cash
        for key in self.balance.keys():
            if self.balance[key]['ratio'] > self.etf_portfolio[key] + self.rebalance_variance:
                desired_number_shares = self.total_portfolio_value * self.etf_portfolio[key] / self.balance[key]['price']
                number_of_shares_to_sell = self.balance[key]['number_of_shares'] - desired_number_shares
                self.cash += number_of_shares_to_sell * self.balance[key]['price'] * (1 - self.transaction_cost)
                self.balance[key]['number_of_shares'] -= number_of_shares_to_sell
                self.balance[key]['value'] = self.balance[key]['number_of_shares'] * self.balance[key]['price']

        # Buy with available cash
        for key in self.balance.keys():
            if self.balance[key]['ratio'] < self.etf_portfolio[key] - self.rebalance_variance:
                desired_number_shares = self.total_portfolio_value * self.etf_portfolio[key] / self.balance[key]['price']
                number_of_shares_to_buy = (desired_number_shares - self.balance[key]['number_of_shares']) * (1 - self.transaction_cost)
                self.cash -= (desired_number_shares - self.balance[key]['number_of_shares']) * self.balance[key]['price']
                self.balance[key]['number_of_shares'] += number_of_shares_to_buy
                self.balance[key]['value'] = self.balance[key]['number_of_shares'] * self.balance[key]['price']


    def simulate(self):
        """ Simulate the portfolio over the given time period with set parameters"""


        for date in self.dates_string_format:
            self.update_balance(date)
            self.update_benchmarks(date)

        # Specify the columns to plot of the balance dataframe


        print('balance_df', self.balance_df)

        columns_to_plot = ['Total Portfolio Value']
        for key in self.etf_portfolio.keys():
            columns_to_plot.append(f'{key} Value')

        plt.style.use('dark_background')

        # Create a figure and subplots
        fig, ax = plt.subplots()

        # Plot the specified columns of the balance dataframe and benchmarks dataframe
        self.balance_df[columns_to_plot].plot(ax=ax, linestyle='dotted')

        self.benchmarks_df.plot(ax=ax)


        # Add labels and title to the plot
        plt.xlabel('Date')
        plt.ylabel('Values')
        plt.title('Portfolio Data')

        # Display the plot
        plt.show()



if __name__ == '__main__':
    # Get input from users
    start_date = datetime(2010, 11, 1)
    end_date = datetime(2023, 4, 30)
    initial_capital = 100
    transaction_cost = 0.0035
    rebalance_variance = 0.05
    rebalance_treshold = 30

    benchmarks = ['SPY', 'IAU', 'TQQQ', 'QQQ']
    etf_portfolio = {'IAU': 0.5, 'TQQQ': 0.5}

    # Converting date objects to string format for further processing
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")

    # Convert percentage to actual fraction
    transaction_cost /= 100
    rebalance_variance /= 100

    portfolio_tracker = PortfolioTracker(start_date, end_date, benchmarks, etf_portfolio, rebalance_treshold,
                                         initial_capital, transaction_cost, rebalance_variance)

    portfolio_tracker.simulate()

    portfolio_tracker.balance_df.to_csv('portfolio_value_object_oriented.csv')