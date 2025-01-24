from django.conf import settings

from app_profile.models.merchant import MerchantProfile
from utils.encrypt_payment_data import secret_key

from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
import base64
import json


def generate_aes_key_from_encryption_key(app_key, global_secret_key):
    # Create an encryption key string
    encryption_key = f"app_key__{app_key}__secret_key__{global_secret_key}".encode()

    # Derive a cryptographic key using HKDF
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'handshake data',
        backend=default_backend()
    )
    return hkdf.derive(encryption_key)


def encrypt_data(data, app_key, global_secret_key):
    # Generate a secure AES key from the encryption key
    aes_key = generate_aes_key_from_encryption_key(app_key, global_secret_key)

    # Serialize data
    data_bytes = json.dumps(data).encode()

    # Create a cipher object and encrypt the data
    iv = os.urandom(16)  # Initialization vector
    cipher = Cipher(algorithms.AES(aes_key), modes.CFB8(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = iv + encryptor.update(data_bytes) + encryptor.finalize()

    # Return the encrypted data encoded in base64 to ensure readability
    return base64.b64encode(encrypted_data).decode()


def encrypt_deposit_p2p_data(data):
    oxp_id = data.get('oxp_id')
    merchant_id = data.get('merchant_id')
    order_id = data.get('order_id')
    merchant = MerchantProfile.objects.get(id=merchant_id)
    app_key = merchant.app_key
    global_secret_key = settings.SECRET_KEY
    deposit_dict = {
        "oxp_id": oxp_id,
        "merchant_id": merchant_id,
        "order_id": order_id,
    }

    encrypted_data = encrypt_data(deposit_dict, app_key, global_secret_key)
    return encrypted_data
