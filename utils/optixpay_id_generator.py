from utils.generate_unique_id import generate_short_uuid


def generate_opx_id():
    prefix = "opx_"
    unique_id = prefix + generate_short_uuid()

    return unique_id


def generate_settlement_id():
    prefix = "sid_"
    unique_id = prefix + generate_short_uuid()

    return unique_id
