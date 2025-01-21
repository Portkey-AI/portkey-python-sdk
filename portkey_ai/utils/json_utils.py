import json


def serialize_kwargs(**kwargs):
    # Function to check if a value is serializable
    def is_serializable(value):
        try:
            json.dumps(value)
            return True
        except (TypeError, ValueError):
            return False

    # Filter out non-serializable items
    serializable_kwargs = {k: v for k, v in kwargs.items() if is_serializable(v)}

    # Convert to string representation
    return json.dumps(serializable_kwargs)


def serialize_args(*args):
    # Function to check if a value is serializable
    def is_serializable(value):
        try:
            json.dumps(value)
            return True
        except (TypeError, ValueError):
            return False

    # Filter out non-serializable items
    serializable_args = [arg for arg in args if is_serializable(arg)]

    # Convert to string representation
    return json.dumps(serializable_args)
