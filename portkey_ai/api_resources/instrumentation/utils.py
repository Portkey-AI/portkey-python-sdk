import json
from typing import Any
from opentelemetry.trace import Span


def set_span_attribute(span: Span, key: str, value: Any):
    try:
        if isinstance(value, (dict, list, tuple, set, str, int, float, bool, None)):
            span.set_attribute(key, json.dumps(value))
        else:
            for child_key, child_value in value.__dict__.items():
                set_span_attribute(span, f"{key}.{child_key}", child_value)
    except Exception:
        span.set_attribute(key, str(value))
