import requests
from bs4 import BeautifulSoup
import re

# Example URL (this should be replaced with a URL you have permission to scrape)
url = 'https://www.xe.com/currencyconverter/convert/?Amount=1&From=USD&To=EUR'


# Send a request to the website
response = requests.get(url)




def extract_exchange_rates(data):
    nok_pattern = r'"NOK":(\d+\.\d+)'
    eur_pattern = r'"EUR":(\d+\.\d+)'

    nok_match = re.search(nok_pattern, data)
    eur_match = re.search(eur_pattern, data)

    nok_rate = float(nok_match.group(1)) if nok_match else None
    eur_rate = float(eur_match.group(1)) if eur_match else None

    # Calculate EUR to NOK rate if both rates are found
    eur_to_nok_rate = None
    if nok_rate and eur_rate:
        eur_to_nok_rate = nok_rate / eur_rate

    return nok_rate, eur_rate, eur_to_nok_rate


print(extract_exchange_rates(response.text))    

# Parse the HTML content
# soup = BeautifulSoup(response.text, 'html.parser')

# # Find data in the parsed HTML (this is a placeholder and will depend on the structure of the HTML)
# data = soup.find('div', {'class': 'target-class'}).get_text()

# print(data)
