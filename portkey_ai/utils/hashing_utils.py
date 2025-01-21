import uuid


def string_to_uuid_v3(input_string: str) -> str:
    if input_string is None:
        return None
    # Using UUID v3 (MD5-based) - less secure but faster
    return str(uuid.uuid3(uuid.NAMESPACE_DNS, str(input_string)))
