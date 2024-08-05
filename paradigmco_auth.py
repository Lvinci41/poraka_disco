import base64
import hmac
import time
import json
import requests

# API configuration
API_URL = "https://api.testnet.paradigm.trade"
ACCESS_KEY = "YOUR_ACCESS_KEY_HERE"
SECRET_KEY = b"YOUR_SECRET_KEY_HERE"

def sign_request(secret_key, method, path, body):
    signing_key = base64.b64decode(secret_key)
    timestamp = str(int(time.time() * 1000)).encode('utf-8')
    message = b'\n'.join([timestamp, method.upper(), path, body])
    digest = hmac.digest(signing_key, message, 'sha256')
    signature = base64.b64encode(digest)
    return timestamp, signature

def place_order(side, quantity, price, instrument_id):
    method = 'POST'
    path = '/v2/drfq/orders'
    
    payload = {
        "account_name": "YOUR_ACCOUNT_NAME",
        "type": "LIMIT",
        "time_in_force": "GOOD_TILL_CANCELED",
        "legs": [
            {
                "instrument_id": instrument_id,
                "price": str(price)
            }
        ],
        "quantity": str(quantity),
        "side": side
    }
    
    json_payload = json.dumps(payload)
    timestamp, signature = sign_request(
        secret_key=SECRET_KEY,
        method=method.encode('utf-8'),
        path=path.encode('utf-8'),
        body=json_payload.encode('utf-8')
    )
    
    headers = {
        'Paradigm-API-Timestamp': timestamp,
        'Paradigm-API-Signature': signature,
        'Authorization': f'Bearer {ACCESS_KEY}',
        'Content-Type': 'application/json'
    }
    
    response = requests.post(
        f"{API_URL}{path}",
        headers=headers,
        json=payload
    )
    
    return response

# Example usage
try:
    order_response = place_order("BUY", 250000, 17000, 11434)
    print(f"Status Code: {order_response.status_code}")
    print(f"Response: {order_response.text}")
except Exception as e:
    print(f"An error occurred: {str(e)}")
