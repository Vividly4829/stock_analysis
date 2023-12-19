import requests
from bs4 import BeautifulSoup
import re


def get_exchange_rates():
    # Example URL (this should be replaced with a URL you have permission to scrape)
    url = 'https://www.xe.com/currencyconverter/convert/?Amount=1&From=USD&To=EUR'


    # Send a request to the website
    response = requests.get(url)

    def extract_exchange_rates(data):
        nok_pattern = r'"NOK":(\d+\.\d+)'
        eur_pattern = r'"EUR":(\d+\.\d+)'

        nok_match = re.search(nok_pattern, data)
        eur_match = re.search(eur_pattern, data)

        usd_to_nok_rate = float(nok_match.group(1)) if nok_match else None
        usd_to_eur_rate = float(eur_match.group(1)) if eur_match else None

        # Calculate EUR to NOK rate if both rates are found
        eur_to_nok_rate = None
        if usd_to_nok_rate and usd_to_eur_rate:
            eur_to_nok_rate = usd_to_nok_rate / usd_to_eur_rate

        return  usd_to_nok_rate, usd_to_eur_rate, eur_to_nok_rate


    return extract_exchange_rates(response.text)

