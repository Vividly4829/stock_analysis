import requests


def get_earnings(ticker: str):
    url = f'https://www.alphavantage.co/query?function=EARNINGS&symbol={ticker}&apikey=d15JS5MD6R8GOQL6V'
    r = requests.get(url)
    data = r.json()

    data = data['quarterlyEarnings']

    return data
#
