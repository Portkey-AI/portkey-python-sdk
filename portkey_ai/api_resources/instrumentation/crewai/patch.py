from opentelemetry import trace
from opentelemetry.trace import SpanKind, Status, StatusCode

from portkey_ai.utils.json_utils import serialize_args, serialize_kwargs
from portkey_ai.api_resources.instrumentation.utils import (
    set_members,
    set_span_attribute,
)


def patch_crew(operation_name: str, version: str, tracer: trace.Tracer):
    def traced_func(wrapped, instance, args, kwargs):
        with tracer.start_as_current_span(
            name=operation_name, kind=SpanKind.CLIENT
        ) as span:
            try:
                module_name = instance.__module__
                class_name = instance.__class__.__name__

                span.set_attribute("_source", "crewai")
                span.set_attribute("_source_type", "agent framework")
                span.set_attribute("framework.version", version)
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

                if class_name == "Crew":
                    for attr in ["tasks_output", "token_usage", "usage_metrics"]:
                        if hasattr(result, attr):
                            span.set_attribute(
                                f"crewai.crew.{attr}", str(getattr(result, attr))
                            )
            except Exception as e:
                span.record_exception(e)
                span.set_status(Status(StatusCode.ERROR, str(e)))
                raise
            return result

    return traced_func
