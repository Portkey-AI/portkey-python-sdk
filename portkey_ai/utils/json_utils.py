import json
from portkey_ai._vendor.openai._utils import is_given


_BASE_JSON_DEFAULT = json.JSONEncoder.default
_patched_notgiven_serialization = False


class PortkeyJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder that handles NotGiven/Omit types using OpenAI's utilities."""
    
    def default(self, obj):
        # Use OpenAI's is_given utility to check for NotGiven/Omit sentinels
        if not is_given(obj):
            # Return None for NotGiven/Omit instances during JSON serialization
            return None
        return super().default(obj)


def enable_notgiven_serialization():
    """Enable global JSON serialization support for NotGiven/Omit types.
    
    Uses OpenAI's is_given utility to detect sentinel values.
    """
    global _patched_notgiven_serialization
    if _patched_notgiven_serialization:
        return

    def patched_default(self, obj):
        # Use OpenAI's utility to check for NotGiven/Omit
        if not is_given(obj):
            return None
        return _BASE_JSON_DEFAULT(self, obj)

    json.JSONEncoder.default = patched_default
    _patched_notgiven_serialization = True


def disable_notgiven_serialization():
    """Disable global JSON serialization support for NotGiven/Omit types.
    
    This restores the original JSONEncoder behavior.
    """
    global _patched_notgiven_serialization
    if not _patched_notgiven_serialization:
        return

    json.JSONEncoder.default = _BASE_JSON_DEFAULT
    _patched_notgiven_serialization = False


def _is_serializable(value) -> bool:
    """Return True if value can be serialized with PortkeyJSONEncoder."""
    try:
        json.dumps(value, cls=PortkeyJSONEncoder)
        return True
    except (TypeError, ValueError):
        return False


def serialize_kwargs(**kwargs):
    # Filter out non-serializable items
    serializable_kwargs = {k: v for k, v in kwargs.items() if _is_serializable(v)}

    # Convert to string representation
    return json.dumps(serializable_kwargs, cls=PortkeyJSONEncoder)


def serialize_args(*args):
    # Filter out non-serializable items
    serializable_args = [arg for arg in args if _is_serializable(arg)]

    # Convert to string representation
    return json.dumps(serializable_args, cls=PortkeyJSONEncoder)
