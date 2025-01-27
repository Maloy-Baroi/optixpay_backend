import uuid


def get_unique_default():
    """
    Generate a unique identifier based on UUID.

    Returns a string formatted UUID that can be used as a unique transaction ID.
    This ensures that every default is unique across all instances of Settlement.
    """
    return f"None__{str(uuid.uuid4())}"
