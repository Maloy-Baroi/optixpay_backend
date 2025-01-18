from utils.generate_unique_id import generate_short_uuid


def generate_order_id():
    prefix = "ord_"
    unique_id = prefix + generate_short_uuid()

    return unique_id