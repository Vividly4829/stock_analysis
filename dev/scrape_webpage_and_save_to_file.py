import requests
from bs4 import BeautifulSoup
import re


def scrape(ticker: str):

    url = f'https://www.etf.com/SPY'

    try:
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Make sure to specify the encoding as 'utf-8' here
            with open(f"{ticker}_holdings.html", "w", encoding="utf-8") as file:
                file.write(str(soup))
            print(f"Page saved to {ticker}_holdings.html successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")


holding_info = scrape('spy2')
