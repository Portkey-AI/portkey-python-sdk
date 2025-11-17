import json
from portkey_ai._vendor.openai._types import NotGiven
from portkey_ai._vendor.openai._utils import is_given


class PortkeyJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder that handles NotGiven types using OpenAI's utilities."""
    
    def default(self, obj):
        # Use OpenAI's is_given utility to check for NotGiven/Omit
        if not is_given(obj):
            # Return None for NotGiven/Omit instances during JSON serialization
            return None
        return super().default(obj)


_original_json_encoder = None


def enable_notgiven_serialization():
    """
    Enable global JSON serialization support for NotGiven/Omit types.
    
    Uses OpenAI's is_given utility to detect sentinel values.
    """
    global _original_json_encoder
    if _original_json_encoder is None:
        _original_json_encoder = json.JSONEncoder.default
        
        def patched_default(self, obj):
            # Use OpenAI's utility to check for NotGiven/Omit
            if not is_given(obj):
                return None
            return _original_json_encoder(self, obj)
        
        json.JSONEncoder.default = patched_default


def disable_notgiven_serialization():
    """
    Disable global JSON serialization support for NotGiven types.
    
    This restores the original JSONEncoder behavior.
    """
    global _original_json_encoder
    if _original_json_encoder is not None:
        json.JSONEncoder.default = _original_json_encoder
        _original_json_encoder = None


def serialize_kwargs(**kwargs):
    # Function to check if a value is serializable
    def is_serializable(value):
        try:
            json.dumps(value, cls=PortkeyJSONEncoder)
            return True
        except (TypeError, ValueError):
            return False

    # Filter out non-serializable items
    serializable_kwargs = {k: v for k, v in kwargs.items() if is_serializable(v)}

    # Convert to string representation
    return json.dumps(serializable_kwargs, cls=PortkeyJSONEncoder)


def serialize_args(*args):
    # Function to check if a value is serializable
    def is_serializable(value):
        try:
            json.dumps(value, cls=PortkeyJSONEncoder)
            return True
        except (TypeError, ValueError):
            return False

    # Filter out non-serializable items
    serializable_args = [arg for arg in args if is_serializable(arg)]

    # Convert to string representation
    return json.dumps(serializable_args, cls=PortkeyJSONEncoder)
