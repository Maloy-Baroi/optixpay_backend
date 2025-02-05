import json
import hashlib
import hmac
import requests
from django.conf import settings


def send_request_with_signature(agent_unique_id):
    platform_id = settings.PASSIMPAY_PLATFORM_ID
    secret = settings.PASSIMPAY_SECRET_KEY
    body = {
        "platformId": platform_id,
        "paymentId": 71,
        "orderId": agent_unique_id
    }
    # Serialize body to JSON ensuring it matches the format expected by the API
    serialized_body = json.dumps(body, separators=(',', ':'), ensure_ascii=False)
    signature_contract = f"{platform_id};{serialized_body};{secret}"
    signature = hmac.new(secret.encode(), signature_contract.encode(), hashlib.sha256).hexdigest()

    # Set up headers with the signature
    headers = {
        'Content-Type': 'application/json',
        'x-signature': signature
    }

    # Define the API endpoint
    url = 'https://api.passimpay.io/v2/address'

    # Perform the POST request
    try:
        response = requests.post(url, headers=headers, data=serialized_body, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "status_code": response.status_code,
                "response": response.text
            }
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


# Example usage
# platform_id = 1333
# secret = 'ebb620-d11037-56c184-d69d9e-f04a70'
# body = {
#     "platformId": platform_id,
#     "paymentId": 71,
#     "orderId": "agent8e106dc357cb"
# }
#
# result = send_request_with_signature(platform_id, secret, body)
