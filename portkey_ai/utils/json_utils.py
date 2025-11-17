import json
from portkey_ai._vendor.openai._utils import is_given


_BASE_JSON_DEFAULT = json.JSONEncoder.default
_patched_notgiven_serialization = False


class PortkeyJSONEncoder(json.JSONEncoder):
    """JSON encoder that treats OpenAI/Portkey "not provided" markers as null."""

    def default(self, obj):  # type: ignore[override]
        # If this is one of OpenAI's internal "not provided" / omit markers,
        # encode it as None (null in JSON) instead of raising TypeError.
        if not is_given(obj):
            return None
        return super().default(obj)


def enable_notgiven_serialization() -> None:
    """Enable global JSON support for OpenAI/Portkey "not provided" markers.

    After this is called (done automatically in portkey_ai.__init__), any
    json.dumps(...) that encounters these markers will encode them as null
    instead of raising a TypeError.
    """
    global _patched_notgiven_serialization
    if _patched_notgiven_serialization:
        return

    def patched_default(self, obj):  # type: ignore[override]
        if not is_given(obj):
            return None
        return _BASE_JSON_DEFAULT(self, obj)

    json.JSONEncoder.default = patched_default
    _patched_notgiven_serialization = True


def disable_notgiven_serialization() -> None:
    """Disable global JSON support for OpenAI/Portkey "not provided" markers.

    Restores the original JSONEncoder.default implementation.
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
