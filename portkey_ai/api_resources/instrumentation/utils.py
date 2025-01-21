import json
from typing import Any
from opentelemetry.trace import Span


def set_span_attribute(span: Span, key: str, value: Any, _processed=None, depth=0):
    if value is None or depth > 2:
        return

    # Initialize processed set on first call
    if _processed is None:
        _processed = set()

    # Get object id to track circular references
    obj_id = id(value)
    if obj_id in _processed:
        return

    try:
        if isinstance(value, (dict, list, tuple, set, str, int, float, bool)):
            span.set_attribute(key, json.dumps(value))
        else:
            _processed.add(obj_id)
            for child_key, child_value in value.__dict__.items():
                set_span_attribute(
                    span, f"{key}.{child_key}", child_value, _processed, depth + 1
                )
    except Exception:
        span.set_attribute(key, str(value))
