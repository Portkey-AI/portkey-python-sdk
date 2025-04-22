import json
import re


def serialize_kwargs(pattern: str = ".*", **kwargs):
    # Function to check if a value is serializable
    def is_serializable(value):
        try:
            json.dumps(value)
            return True
        except (TypeError, ValueError):
            return False

    # Filter out non-serializable items
    regex = re.compile(pattern) if pattern else None
    serializable_kwargs = {
        k: v
        for k, v in kwargs.items()
        if regex and regex.match(k) and is_serializable(v)
    }

    # Convert to string representation
    return json.dumps(serializable_kwargs)


def serialize_args(pattern: str = ".*", *args):
    # Function to check if a value is serializable
    def is_serializable(value):
        try:
            json.dumps(value)
            return True
        except (TypeError, ValueError):
            return False

    # Filter out non-serializable items
    regex = re.compile(pattern) if pattern else None
    serializable_args = [
        arg for arg in args if regex and regex.match(arg) and is_serializable(arg)
    ]

    # Convert to string representation
    return json.dumps(serializable_args)
