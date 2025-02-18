import uuid


def string_to_uuid(input_string: str) -> str:
    if input_string is None:
        return None
    # Using UUID v5 (SHA-1-based) - more secure but slower
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, str(input_string)))
