import requests
import json

from django.conf import settings
from django.db.models.expressions import result


def grant_token(app_key, app_secret, username, password):
    url = f"{settings.BKASH_BASE_URL}/tokenized/checkout/token/grant"
    payload = json.dumps({
        "app_key": app_key,
        "app_secret": app_secret
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'username': username,
        'password': password
    }

    # proxies = {
    #     'https': 'https://46.202.159.210:8000',
    # }

    response = requests.post(url, headers=headers, data=payload, proxies=proxies)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def create_checkout_session(mode, payer_reference, callback_url, amount, currency, intent, merchant_invoice_number, authorization, app_key):
    url = f"{settings.BKASH_BASE_URL}/tokenized/checkout/create"
    """
    This function sends a POST request to create a checkout session with given parameters.

    Parameters:
    - mode (str): Transaction mode
    - payer_reference (str): Reference number for the payer
    - callback_url (str): URL to which responses are sent
    - amount (int): Amount of the transaction
    - currency (str): Currency of the transaction
    - intent (str): Transaction intent
    - merchant_invoice_number (str): Unique merchant invoice number
    - authorization (str): Authorization token
    - app_key (str): Application key for API access
    - url (str): API endpoint URL

    Returns:
    - str: Response text from the API
    """
    payload = json.dumps({
        "mode": mode,
        "payerReference": payer_reference,
        "callbackURL": callback_url,
        "amount": amount,
        "currency": currency,
        "intent": intent,
        "merchantInvoiceNumber": merchant_invoice_number
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': authorization,
        'x-app-key': app_key
    }

    response = requests.post(url, headers=headers, data=payload)
    if response.status_code == 200:
        return response.json()  # Returns the response text from the API
    else:
        return None

# Example usage:
mode = "0011"
payer_reference = "01303838765"
callback_url = "https://optixpay.com/"
amount = 1
currency = "BDT"
intent = "authorization"
merchant_invoice_number = "ajkgnsjgns"
authorization = 'your_authorization_token'
app_key = 'E8QGBD19aGNfjYVmKgqfo9f1tc'

