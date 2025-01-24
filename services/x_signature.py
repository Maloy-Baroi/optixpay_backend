import json
import hashlib
import hmac
import requests


def x_signature_generate(user_id):
    platform_id = 1333
    secret = 'ebb620-d11037-56c184-d69d9e-f04a70'
    body = {
        "platformId": platform_id,
        "paymentId": 71,
        "orderId": user_id
    }

    # Formation of signature
    serialized_body = json.dumps(body, separators=(',', ':'), ensure_ascii=False)
    signature_contract = f"{platform_id};{serialized_body};{secret}"
    signature = hmac.new(secret.encode(), signature_contract.encode(), hashlib.sha256).hexdigest()
    headers = {
        'Content-Type': 'application/json',
        'x-signature': signature
    }

    # Sending request
    url = 'https://api.passimpay.io/v2/address'
    response = requests.post(url, headers=headers, data=serialized_body, timeout=10)

    # Result
    if response.status_code == 200:
        result = response.json()
        return result
