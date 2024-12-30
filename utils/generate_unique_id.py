import hashlib
import uuid


def generate_short_uuid():
    """Generates a 10-character unique key using a UUID and hashing."""
    uuid_str = str(uuid.uuid4())
    hash_object = hashlib.sha256(uuid_str.encode())
    hex_digest = hash_object.hexdigest()
    return hex_digest[:10]