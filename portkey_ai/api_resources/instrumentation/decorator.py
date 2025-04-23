from functools import wraps
import inspect
from typing import Any, Callable
from opentelemetry import trace
from opentelemetry.trace import (
    get_tracer,
    SpanKind,
    Status,
    StatusCode,
    get_tracer_provider,
)

from portkey_ai.api_resources.instrumentation.utils import (
    set_span_attribute,
)
from portkey_ai.utils.json_utils import serialize_args, serialize_kwargs


def watch(input: bool = True, output: bool = True):
    """
    A decorator that instruments a method with OpenTelemetry tracing.

    Args:
        source: The source of the instrumentation (e.g., module name)
        version: The version of the source package

    Example:
        @instrument_method(source="my_module", version="1.0.0")
        def my_method(self, *args, **kwargs):
            ...
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Get the tracer
            tracer_provider = get_tracer_provider()
            tracer = get_tracer("portkey-instrumentor", "", tracer_provider)

            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()

            with tracer.start_as_current_span(
                name=func.__name__, kind=SpanKind.CLIENT
            ) as span:
                try:
                    module_name = func.__module__

                    span.set_attribute("_source", "decorator")
                    span.set_attribute("framework.version", "1.0.0")
                    span.set_attribute("module", module_name)
                    span.set_attribute("method", func.__name__)
                    if input:
                        span.set_attribute(
                            "arguments", serialize_kwargs(".*", **bound_args.arguments)
                        )

                    result = func(*args, **kwargs)
                    if isinstance(result, func.__class__):
                        pass
                    elif output:
                        set_span_attribute(span, "result", result)

                    span.set_status(Status(StatusCode.OK))

                except Exception as e:
                    span.record_exception(e)
                    span.set_status(Status(StatusCode.ERROR, str(e)))
                    raise
                return result

        return wrapper

    return decorator
