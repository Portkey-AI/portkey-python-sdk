from importlib.metadata import PackageNotFoundError, version
import json
import re
import inspect
from typing import Any
from opentelemetry import trace
from opentelemetry.trace import SpanKind, Status, StatusCode, Span

from portkey_ai.instrumentation.models.tracing_config import MethodConfig


# Function to check if a value is serializable
def is_serializable(value):
    try:
        json.dumps(value)
        return True
    except (TypeError, ValueError):
        return False


def is_package_installed(pkg_name):
    try:
        version(pkg_name)
        return True
    except PackageNotFoundError:
        return False


def set_span_attribute(
    span: Span,
    key: str,
    value: Any,
    _processed=None,
    depth=0,
    pattern: str = "^(?!_)(?!.*\._).*",
):
    regex = re.compile(pattern)
    if depth > 2 or not regex.match(key):
        return
    if value is None:
        return

    # Initialize processed set on first call
    if _processed is None:
        _processed = set()

    # Get object id to track circular references
    obj_id = id(key)
    if obj_id in _processed:
        return

    try:
        if is_serializable(value):
            span.set_attribute(key, value)
        else:
            str_value = str(value)
            if re.match(r"<.*object at 0x[0-9a-f]+>", str_value):
                return
            span.set_attribute(key, str(value))
    except Exception:
        pass


def get_value(value):
    if is_serializable(value):
        return value
    str_value = str(value)
    if re.match(r"<.*object at 0x[0-9a-f]+>", str_value):
        return "OBJECT_OMITTED_FROM_TRACE"
    return str(value)


def set_members(span: Span, instance: Any, module_name: str, class_name: str):
    if instance is None:
        return
    for key, value in instance.__dict__.items():
        set_span_attribute(span, f"{module_name}.{class_name}.{key}", value)


def serialize_kwargs(pattern: str = ".*", **kwargs):
    # Filter out non-serializable items
    regex = re.compile(pattern if pattern else ".*")
    serializable_kwargs = {k: get_value(v) for k, v in kwargs.items() if regex.match(k)}

    # Convert to string representation
    return json.dumps(serializable_kwargs)


class Patcher:
    def __init__(self, source: str, version: str, tracer: trace.Tracer):
        self.source = source
        self.version = version
        self.tracer = tracer

    def patch_operation(self, operation_name: str, config: MethodConfig):
        def traced_func(wrapped, instance, args, kwargs):
            with self.tracer.start_as_current_span(
                name=operation_name, kind=SpanKind.CLIENT
            ) as span:
                try:
                    module_name = instance.__module__
                    class_name = instance.__class__.__name__

                    sig = inspect.signature(wrapped)
                    bound_args = sig.bind(*args, **kwargs)
                    bound_args.apply_defaults()

                    span.set_attribute("_source", self.source)
                    span.set_attribute("framework.version", self.version)
                    span.set_attribute("module", module_name)
                    span.set_attribute("method", operation_name)
                    span.set_attribute(
                        "arguments",
                        serialize_kwargs(config.args, **bound_args.arguments),
                    )

                    try:
                        set_members(span, instance, module_name, class_name)
                    except Exception as e:
                        span.record_exception(e)

                except Exception as e:
                    span.record_exception(e)
                    span.set_status(Status(StatusCode.ERROR, str(e)))

                try:
                    result = wrapped(*args, **kwargs)
                except Exception as e:
                    span.record_exception(e)
                    span.set_status(Status(StatusCode.ERROR, str(e)))
                    raise

                try:
                    if isinstance(result, instance.__class__):
                        pass
                    elif config.result:
                        set_span_attribute(
                            span, "result", result, pattern=config.result
                        )

                    span.set_status(Status(StatusCode.OK))
                except Exception as e:
                    span.record_exception(e)
                    span.set_status(Status(StatusCode.ERROR, str(e)))
                return result

        return traced_func
