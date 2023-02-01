import requests
import os
from dotenv import load_dotenv
import time
import json
import hmac
import hashlib

# Constants
BASE_URL: str = 'https://coinbase.com'
ENDPOINT_URL: str = '/api/v3/brokerage'
API_RESOURCE: str = '/orders'

# Create signature for Advanced Trade API authentication header
def sign(secret: str, timestamp: str, method: str, requestPath: str, body: str = '') -> bytes:
    combined: str = timestamp + method + requestPath + body
    
    signature: bytes = hmac.new(secret.encode('utf-8'), combined.encode('utf-8'), digestmod=hashlib.sha256).digest()

    return signature

# Trade USD for currency defined in PRODUCT_ID
def trade() -> None:
    # Env variables
    load_dotenv()
    api_key: str = os.environ['API_KEY']
    api_secret: str = os.environ['API_SECRET']
    product_id: str = os.environ['PRODUCT_ID']
    quote_size: str = os.environ['AMT_USD']

    # Request headers
    timestamp: str = str(int(time.time()))
    sig: bytes = sign(api_secret, timestamp, 'POST', ENDPOINT_URL + API_RESOURCE)
    headers: dict = {
        'accept': 'application/json',
        'CB-ACCESS-KEY': api_key,
        'CB-ACCESS-SIGN': sig.hex(),
        'CB-ACCESS-TIMESTAMP': timestamp
    }

    # Request body
    body: dict = {
        'client_order_id': timestamp,
        'product_id': product_id,
        'side': 'BUY',
        'order_configuration': {
            'market_market_ioc': {
                'quote_size': quote_size
            }
        }
    }
    res: requests.Response = requests.post(BASE_URL + ENDPOINT_URL + API_RESOURCE, headers = headers, data = json.dumps(body))
    
    if (res.status_code == 200):
        print(json.dumps(res.json(), indent=2))
    else:
        print(res.content.decode('utf-8'))

if __name__ == '__main__':
    trade()
