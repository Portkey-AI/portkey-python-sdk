from opentelemetry import trace
from opentelemetry.trace import SpanKind, Status, StatusCode

from portkey_ai.utils.json_utils import serialize_args, serialize_kwargs
from portkey_ai.api_resources.instrumentation.utils import (
    set_span_attribute,
    set_members,
)
from portkey_ai.utils import string_to_uuid


def patch_litellm(module: str, operation_name: str, version: str, tracer: trace.Tracer):
    def traced_func(wrapped, instance, args, kwargs):
        with tracer.start_as_current_span(
            name=operation_name, kind=SpanKind.CLIENT
        ) as span:
            try:
                module_name = module
                class_name = operation_name

                if operation_name == "completion":
                    headers = kwargs.get("headers", {})
                    headers["x-portkey-trace-id"] = str(
                        string_to_uuid(span.get_span_context().trace_id)
                    )
                    headers["x-portkey-span-id"] = str(span.get_span_context().span_id)
                    headers["x-portkey-parent-span-id"] = (
                        str(span.parent.span_id) if span.parent else None
                    )
                    headers["x-portkey-span-name"] = span.name
                    kwargs["headers"] = headers

                span.set_attribute("framework.version", version)
                span.set_attribute("_source", "litellm")
                span.set_attribute("_source_type", "routing library")
                span.set_attribute("module", module_name)
                span.set_attribute("method", operation_name)
                span.set_attribute("args", serialize_args(*args))
                span.set_attribute("kwargs", serialize_kwargs(**kwargs))

                result = wrapped(*args, **kwargs)
                span.set_status(Status(StatusCode.OK))

                try:
                    set_members(span, instance, module_name, class_name)
                except Exception as e:
                    span.record_exception(e)

                set_span_attribute(span, "result", result)

            except Exception as e:
                span.record_exception(e)
                span.set_status(Status(StatusCode.ERROR, str(e)))
                raise
            return result

    return traced_func
