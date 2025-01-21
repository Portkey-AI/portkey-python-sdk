from opentelemetry import trace
from opentelemetry.trace import SpanKind, Status, StatusCode

from portkey_ai.utils.json_utils import serialize_args, serialize_kwargs
from portkey_ai.api_resources.instrumentation.utils import set_span_attribute


def patch_crew(operation_name: str, version: str, tracer: trace.Tracer):
    def traced_func(wrapped, instance, args, kwargs):
        with tracer.start_as_current_span(
            name=operation_name, kind=SpanKind.CLIENT
        ) as span:
            try:
                module_name = instance.__module__
                class_name = instance.__class__.__name__

                span.set_attribute("crew.version", version)
                span.set_attribute("module", module_name)
                span.set_attribute("method", operation_name)
                span.set_attribute("args", serialize_args(*args))
                span.set_attribute("kwargs", serialize_kwargs(**kwargs))

                result = wrapped(*args, **kwargs)
                span.set_attribute("result", str(result))
                span.set_status(Status(StatusCode.OK))

                for key, value in instance.__dict__.items():
                    set_span_attribute(span, f"{module_name}.{class_name}.{key}", value)

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
