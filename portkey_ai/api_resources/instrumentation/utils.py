from importlib.metadata import PackageNotFoundError, version
import json
from typing import Any
from opentelemetry import trace
from opentelemetry.trace import SpanKind, Status, StatusCode, Span

from portkey_ai.utils.json_utils import serialize_args, serialize_kwargs


def is_package_installed(pkg_name):
    try:
        version(pkg_name)
        return True
    except PackageNotFoundError:
        return False


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
                if child_key.startswith("_") or child_value is None:
                    continue
                set_span_attribute(
                    span, f"{key}.{child_key}", child_value, _processed, depth + 1
                )
    except Exception:
        span.set_attribute(key, str(value))


def set_members(span: Span, instance: Any, module_name: str, class_name: str):
    if instance is None:
        return
    for key, value in instance.__dict__.items():
        set_span_attribute(span, f"{module_name}.{class_name}.{key}", value)


class Patcher:
    def __init__(self, source: str, version: str, tracer: trace.Tracer):
        self.source = source
        self.version = version
        self.tracer = tracer

    def patch_operation(self, operation_name: str):
        def traced_func(wrapped, instance, args, kwargs):
            with self.tracer.start_as_current_span(
                name=operation_name, kind=SpanKind.CLIENT
            ) as span:
                try:
                    module_name = instance.__module__
                    class_name = instance.__class__.__name__

                    span.set_attribute("_source", self.source)
                    span.set_attribute("framework.version", self.version)
                    span.set_attribute("module", module_name)
                    span.set_attribute("method", operation_name)
                    span.set_attribute("args", serialize_args(*args))
                    span.set_attribute("kwargs", serialize_kwargs(**kwargs))

                    result = wrapped(*args, **kwargs)
                    if isinstance(result, instance.__class__):
                        pass
                    else:
                        set_span_attribute(span, "result", result)

                    span.set_status(Status(StatusCode.OK))

                    try:
                        set_members(span, instance, module_name, class_name)
                    except Exception as e:
                        span.record_exception(e)

                except Exception as e:
                    span.record_exception(e)
                    span.set_status(Status(StatusCode.ERROR, str(e)))
                    raise
                return result

        return traced_func
