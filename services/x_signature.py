import json
import hashlib
import hmac
import requests

def hex_shift_encrypt(hex_string, shift):
    encrypted_hex = ""
    for char in hex_string:
        # Convert hex digit to an integer (0-15)
        digit = int(char, 16)
        # Apply shift and wrap around 16
        new_digit = (digit + shift) % 16
        # Convert integer back to hex digit
        encrypted_hex += format(new_digit, 'x')
    return encrypted_hex

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
        if result and result['address']:
            return hex_shift_encrypt(result['address'], 172323)
    else:
        print(f"HTTP Code: {response.status_code}")
        print(f"Response: {response.text}")



