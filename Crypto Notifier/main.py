import json
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from requests import Request, Session
import requests
import time
from win10toast import ToastNotifier

toast = ToastNotifier()


url = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
    'start': '1',
    'limit': '5000',
    'convert': 'USD'
}
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': 'e0c16977-886c-4350-8cc4-a8c091ec98e4',
}

session = Session()
session.headers.update(headers)

try:
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    print(data['data'][0]['quote']['USD']['price'])
except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)


def get_crypto_price():
    url = 'https://api.coinmarketcap.com/data-api/v3/cryptocurrency/detail/chart?id=1&range=1D&interval=1M'
    response = requests.get(url)
    data = response.json()
    price = data['data']['points']["1683397200"]['c']
    print(price)


get_crypto_price()
current_coin_price = get_crypto_price()
toast.show_toast("Price", f"GEL {current_coin_price:.2f}", duration=5)

while True:
    time.sleep(60)  # wait for 1 minute before making the next request
    price = get_crypto_price()
    if price != current_coin_price:
        current_coin_price = price
        print(f"Current price: GEL {current_coin_price:.2f}")
        toast.show_toast(
            "crypto Price", f"GEL {current_coin_price:.2f}", duration=5)
