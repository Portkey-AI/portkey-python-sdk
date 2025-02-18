from opentelemetry import trace
from opentelemetry.trace import SpanKind, Status, StatusCode

from portkey_ai.utils.json_utils import serialize_args, serialize_kwargs
from portkey_ai.api_resources.instrumentation.utils import (
    set_span_attribute,
    set_members,
)


def patch_openai(module: str, operation_name: str, version: str, tracer: trace.Tracer):
    def traced_func(wrapped, instance, args, kwargs):
        with tracer.start_as_current_span(
            name=operation_name, kind=SpanKind.CLIENT
        ) as span:
            try:
                module_name = module
                class_name = operation_name

                span.set_attribute("_source", "openai")
                span.set_attribute("_source_type", "LLM provider")
                span.set_attribute("framework.version", version)
                span.set_attribute("module", module_name)
                span.set_attribute("method", operation_name)
                span.set_attribute("args", serialize_args(*args))
                span.set_attribute("kwargs", serialize_kwargs(**kwargs))

                result = wrapped(*args, **kwargs)
                span.set_status(Status(StatusCode.OK))

                try:
                    set_members(span, instance, module_name, class_name)
                except Exception:
                    span.set_attribute(f"{module_name}.{class_name}.error", instance)

                set_span_attribute(span, "result", result)

            except Exception as e:
                span.record_exception(e)
                span.set_status(Status(StatusCode.ERROR, str(e)))
                raise
            return result

    return traced_func
