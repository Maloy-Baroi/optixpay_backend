from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
import base64
import json


def generate_aes_key_from_encryption_key(app_key, secret_key):
    # Create an encryption key string
    encryption_key = f"app_key__{app_key}__secret_key__{secret_key}".encode()

    # Derive a cryptographic key using HKDF
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'handshake data',
        backend=default_backend()
    )
    return hkdf.derive(encryption_key)


def encrypt_data(data, app_key, secret_key):
    # Generate a secure AES key from the encryption key
    aes_key = generate_aes_key_from_encryption_key(app_key, secret_key)

    # Serialize data
    data_bytes = json.dumps(data).encode()

    # Create a cipher object and encrypt the data
    iv = os.urandom(16)  # Initialization vector
    cipher = Cipher(algorithms.AES(aes_key), modes.CFB8(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = iv + encryptor.update(data_bytes) + encryptor.finalize()

    # Return the encrypted data encoded in base64 to ensure readability
    return base64.b64encode(encrypted_data).decode()


# Example usage:
app_key = "iYITUogblJiSlvjfuKOILCeqApWP_8nDRFNLBhSh1WI"
secret_key = "PO6LUi97w-MokPDBycTfl1a1jN4Vck3jNCBYSAhd76UWv5ObhTt0zqdg4NFzb_baLmr-ZwmeY1CYcXtep883kA"
data = """{
    "customer_id": "14ejsn",
    "order_id": "213enjdsfn",
    "bank_name": "bkash",
    "requested_amount": 1000,
    "requested_currency": "BDT"
}"""




def encrypt_payment_data(data: str, app_key: str, secret_key: str) -> str or bool:
    try:
        encrypted_data = encrypt_data(data, app_key, secret_key)
        return encrypted_data
    except Exception as e:
        return False


