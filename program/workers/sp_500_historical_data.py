import pandas as pd
from program.workers.find_etf_holdings import find_etf_holdings

# open the csv file and read it into a pandas dataframe
hist = pd.read_csv('files/historical_sp500/historical_sp500_monthly.csv')

# Check if there is an entry for the current month and year in the dataframe, if not, we need to add it.
# Get the current date
current_date = pd.Timestamp.today()
# Get the current month and year
current_month = current_date.month
current_year = current_date.year

# Check the month and year of the last entry in the dataframe
last_entry = hist.iloc[-1]
last_month = last_entry['Month']
last_year = last_entry['Year']

# If the last entry is not from the current month and year, we need to add a new entry
if last_month != current_month or last_year != current_year:
    # Create a new entry
    

