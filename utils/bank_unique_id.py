from utils.generate_unique_id import generate_short_uuid


def get_bank_unique_id():
    return f"BID_{generate_short_uuid()}"
