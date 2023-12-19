import requests
from bs4 import BeautifulSoup
import re

def find_norwegian_mutual_fund_value(amount, fund_ticker):


    url = f'https://e24.no/bors/instrument/{fund_ticker}'

    # Requesting the webpage

    try:
        response = requests.get(url)

        # Checking if the request was successful
        if response.status_code == 200:
            # Parsing the content
            soup = BeautifulSoup(response.content, 'html.parser')

            # Finding the meta tag with name="description"
            description_tag = soup.find('meta', {'name': 'description'})

            if description_tag is None:
                return None
            # Extracting the content from the tag
            
            description_content = description_tag['content'] # type: ignore

            # Using regex to extract the specific value
            match = re.search(r'kurs er ([\d.]+),', description_content) # type: ignore
            if match:
                value = match.group(1)
                # print(f"The extracted value is: {value}")
                return float(value) * amount
            else:
                print("Value not found in the description.")
        else:
            print(
                f"Failed to retrieve the webpage. Status code: {response.status_code}")
        
            
    except:
        print('Failed to retrieve the webpage.')
        return 0



