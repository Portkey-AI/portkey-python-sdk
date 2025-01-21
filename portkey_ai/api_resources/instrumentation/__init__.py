from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from .crewai import CrewAIInstrumentor
from .portkey_span_exporter import PortkeySpanExporter

__all__ = ["CrewAIInstrumentor", "PortkeySpanExporter", "initialize_instrumentation"]


def initialize_instrumentation(api_key: str):
    tracer_provider = TracerProvider()
    exporter = PortkeySpanExporter(api_key=api_key)
    trace.set_tracer_provider(tracer_provider)
    tracer_provider.add_span_processor(BatchSpanProcessor(exporter))
    CrewAIInstrumentor().instrument()
    print("CrewAI Instrumentation initialized")
