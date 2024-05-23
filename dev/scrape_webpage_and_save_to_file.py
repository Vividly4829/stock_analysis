import requests
from bs4 import BeautifulSoup
import re


def scrape(ticker: str):

    url = f'https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/spearn.htm'

    try:
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Make sure to specify the encoding as 'utf-8' here
            with open(f"{ticker}_holdings.html", "w", encoding="utf-8") as file:
                file.write(str(soup))
            print(f"Page saved to {ticker}_holdings.html successfully.")
        else:
            print(
                f"Failed to retrieve the webpage. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")


holding_info = scrape('spy2dgfg')
