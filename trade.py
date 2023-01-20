import requests
import os
from dotenv import load_dotenv
from sig import sign
import time

BASE_URL = "https://coinbase.com"
ENDPOINT_URL = "/api/v3/brokerage"
API_RESOURCE = "/products"

def trade():
    load_dotenv()
    api_key = os.environ["API_KEY"]
    api_secret = os.environ["API_SECRET"]

    timestamp = str(int(time.time()))

    sig = sign(api_secret, timestamp, "GET", ENDPOINT_URL + API_RESOURCE)

    headers = {
        "accept": "application/json",
        "CB-ACCESS-KEY": api_key,
        "CB-ACCESS-SIGN": sig.hex(),
        "CB-ACCESS-TIMESTAMP": timestamp
    }
    res = requests.get(BASE_URL + ENDPOINT_URL + API_RESOURCE, headers = headers)
    res_code = res.status_code

    if (res_code == 200):
        print(res.json())
    else:
        print(res.content.decode('utf-8'))

if __name__ == "__main__":
    trade()
