import yfinance as yf
import pandas as pd
from program.workers.stock_info import stock_info


def calculate_annualized_return_with_dividends(stock_ticker, start_year: int | None = None) -> tuple[dict, str | None]:

    # A place to store warning or status messages.
    warning = None

    print(
        f'calculating annualised return for stock_ticker: {stock_ticker} and start_year: {start_year}')

    # Fetch historical data for the stock from the earliest available date
    stock = stock_info(stock_ticker)
    stock_data = stock.stock_data
    # print(f'stock_data: {stock_data}')
    # Get inception date (first date in the data)
    inception_date = stock_data.index[0]

    # Get the year of the inception date
    inception_year: int = int(inception_date.year)

    # print(f'inception_year: {inception_year} of stock {stock_ticker}')

    # Find the number of years between 01/01/inception year +1 and today
    today = pd.Timestamp.today()

    # if we have a start year, use that instead of the inception year
    if start_year is None:
        years = today.year - inception_year
        start_year = inception_year
    else:

        if int(start_year) <= inception_year:
            start_year = inception_year
            warning = f'Start year was before inception year. Using inception year {inception_year} instead.'
        years = today.year - start_year
    max_drawdown = 0
    max_drawdown_date = None
    highest_price = None
    data_per_year = {}
    # Loop through each year and calculate the annualized return
    for year in range(0, years):

        selected_year = start_year + year

        # Filter the dataframe to include rows where the date columns contains the given year
        # type: ignore

        # Convert the index to a datetime index
        stock_data.index = pd.to_datetime(stock_data.index, utc=True)

        stock_data_for_year = stock_data[stock_data.index.year ==  # type: ignore
                                         selected_year]
        # Initialize the number of shares and total investment value
        initial_investment = stock_data_for_year['Close'][0]
        if highest_price is None:
            highest_price = initial_investment
        shares_owned = 1  # Start with one share for simplicity

        dividends = {}

        for date, row in stock_data_for_year.iterrows():
            if row['Close'] > highest_price:
                highest_price = row['Close']
            else:
                drawdown = (highest_price - row['Close']) / highest_price
                if drawdown > max_drawdown:
                    max_drawdown = drawdown
                    max_drawdown_date = date

            if row['Dividends'] > 0:
                dividends[str(date)] = row['Dividends']
                # Calculate reinvested shares (after tax)
                dividend_after_tax = row['Dividends'] * 0.85
                reinvested_shares = dividend_after_tax / row['Close']
                shares_owned += reinvested_shares

        # Calculate final investment value
        final_investment_value = shares_owned * \
            stock_data_for_year['Close'][-1]
        # print(f'final_investment_value: {final_investment_value}')

        # Calculate total return
        total_return = final_investment_value / initial_investment - 1

        data_per_year[selected_year] = {}
        # print(f"Total return for {selected_year}: {total_return:.2%}")
        data_per_year[selected_year]['total_return'] = total_return
        # data_per_year[selected_year]['dividends'] = dividends
        data_per_year[selected_year]['dividend_yield'] = sum(
            dividends.values()) / initial_investment

       # Calculate average return
    average_return = sum([data['total_return']
                         for data in data_per_year.values()]) / len(data_per_year)

    # Function to calculate average return for the past 'n' years
    def calculate_past_return(n):
        return sum([data['total_return'] for data in list(data_per_year.values())[-n:]]) / min(n, len(data_per_year))

    return_past_3_years = calculate_past_return(3) if years > 3 else None
    return_past_5_years = calculate_past_return(5) if years > 5 else None
    return_past_10_years = calculate_past_return(10) if years > 10 else None
    return_past_7_years = calculate_past_return(7) if years > 7 else None
    return_past_15_years = calculate_past_return(15) if years > 15 else None
    return_past_20_years = calculate_past_return(20) if years > 20 else None
    return_past_25_years = calculate_past_return(25) if years > 25 else None

    performance = {
        'max_drawdown': max_drawdown,
        'max_drawdown_date': str(max_drawdown_date),
        'inception_date': str(inception_date),  # type: ignore
        'average_return': average_return,
        'return_past_3_years': return_past_3_years,
        'return_past_5_years': return_past_5_years,
        'return_past_7_years': return_past_7_years,
        'return_past_10_years': return_past_10_years,
        'return_past_15_years': return_past_15_years,
        'return_past_20_years': return_past_20_years,
        'return_past_25_years': return_past_25_years,
        'return_per_year': data_per_year,
    }

    return performance, warning
