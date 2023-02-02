import requests
import os
from dotenv import load_dotenv
import time
import json
import hmac
import hashlib

# Constants
BASE_URL: str = 'https://api.coinbase.com'
ENDPOINT_URL: str = '/api/v3/brokerage'
API_RESOURCE: str = '/orders'

# Create signature for Advanced Trade API authentication header
def sign(secret: str, timestamp: str, method: str, requestPath: str, body: str = '') -> bytes:
    combined: str = timestamp + method + requestPath.split('?')[0] + body
    
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

    print(f'Initializing trade for {product_id} with ${quote_size}')

    # Create request body
    timestamp: str = str(int(time.time()))
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

    # Create request headers
    print('Creating auth headers...')
    sig: bytes = sign(api_secret, timestamp, 'POST', ENDPOINT_URL + API_RESOURCE, json.dumps(body))
    headers: dict = {
        'Content-Type': 'application/json',
        'accept': 'application/json',
        'CB-ACCESS-KEY': api_key,
        'CB-ACCESS-SIGN': sig.hex(),
        'CB-ACCESS-TIMESTAMP': timestamp
    }

    # Create order
    print('Creating order...')
    res: requests.Response = requests.post(BASE_URL + ENDPOINT_URL + API_RESOURCE, headers = headers, data = json.dumps(body))
    
    if (res.status_code == 200):
        print(json.dumps(res.json(), indent=2))
    else:
        print('Error: ' + str(res.status_code) + ' ' + res.content.decode('utf-8'))

if __name__ == '__main__':
    trade()
