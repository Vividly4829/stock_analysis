import yfinance as yf

class portfolio_simulator:
    def __init__(self, rebalancing_frequency_days: int, rebalancing_treshold_percentage: float, rebalancing_cost_percentage: float): 
        rebalancing_frequency_days = 20
        rebalancing_treshold_percentage = 5
        rebalancing_cost_percentage = 0.05
        self.holdings = {}

    def add_stock(self, ticker: str, weight: float):
        stock = yf.Ticker(ticker)
        stock_data = stock.history(period="max")  # 
        inception_date = stock_data.index[0]

        self.holdings[ticker] = {'weight': weight, 'stock_data': stock_data, 'inception_date': inception_date}
        # If the total weight in the portfolio exceeds 100%, normalize the weights
        

    def simulate_portfolio(self):
        # Find the holding with the shortest history and use that as the inception date
        inception_date = max([value['inception_date'] for value in self.holdings.values()])
        print(f'inception_date: {inception_date}')


my_portfolio = portfolio_simulator(20, 5, 0.05)
my_portfolio.add_stock('AAPL', 0.5)
my_portfolio.add_stock('MSFT', 0.5)
my_portfolio.simulate_portfolio()



        



        

    



