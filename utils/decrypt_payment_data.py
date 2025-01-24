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


def decrypt_data(encrypted_data, app_key, secret_key):
    # Generate a secure AES key from the encryption key
    aes_key = generate_aes_key_from_encryption_key(app_key, secret_key)

    # Decode the encrypted data from base64
    encrypted_data = base64.b64decode(encrypted_data)

    # Extract the IV and the encrypted message
    iv = encrypted_data[:16]
    encrypted_message = encrypted_data[16:]

    # Create a cipher object and decrypt the data
    cipher = Cipher(algorithms.AES(aes_key), modes.CFB8(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_message) + decryptor.finalize()

    # Convert the decrypted data back to a string and then to a dictionary
    return json.loads(decrypted_data.decode())


# Example usage:
def decrypt_payment_data(encrypted_data, app_key, secret_key) -> dict or None:
    decrypted_data = decrypt_data(encrypted_data, app_key, secret_key)
    try:
        if decrypted_data is not None and isinstance(decrypted_data, dict):
            return decrypted_data
    except Exception as e:
        return None

