import json
import requests
from bs4 import BeautifulSoup
import time


def find_etf_holdings(ticker: str):

    # Rate limiting
    time.sleep(2)  # Adjust the sleep time as necessary
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    url = f'https://stockanalysis.com/etf/{ticker}/holdings/'

    # Use session for connection pooling
    with requests.Session() as session:
        session.headers.update(headers)
        try:
            response = session.get(url)

            # Check if the request was successful
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                table = soup.find('table')

                # Initialize a dictionary to store the holdings
                holdings = {}

                # Extract data from each row of the table
                for row in table.find_all('tr')[1:]:  # type: ignore
                    cells = row.find_all('td')
                    if len(cells) >= 4:  # Ensure there are enough cells
                        # Extract the ticker symbol
                        cell_ticker = cells[1].get_text().strip()
                        weight_str = cells[3].get_text().strip().replace(
                            '%', '')  # Extract the weight and remove '%'

                        # Convert the weight to a decimal and store in the dictionary
                        try:
                            weight = float(weight_str) / 100
                            holdings[cell_ticker] = weight
                        except ValueError:
                            continue  # Skip rows where conversion fails

                return holdings
            else:
                print(
                    f"Failed to retrieve data, status code: {response.status_code}")
        except Exception as e:
            print(f"An error occurred: {e}")
