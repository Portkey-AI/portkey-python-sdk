from importlib.metadata import version
from typing import Dict
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor  # type: ignore [attr-defined]

from .crewai import CrewAIInstrumentor
from .litellm import LitellmInstrumentor
from .portkey_span_exporter import PortkeySpanExporter
from .langgraph import LanggraphInstrumentor

__all__ = ["initialize_instrumentation"]

package_instrumentor_map: Dict[str, BaseInstrumentor] = {
    "crewai": CrewAIInstrumentor,
    "litellm": LitellmInstrumentor,
    "langgraph": LanggraphInstrumentor,
}


def is_package_installed(pkg_name):
    try:
        version(pkg_name)
        return True
    except:
        return False


def initialize_instrumentation(api_key: str, base_url: str):
    tracer_provider = TracerProvider()
    exporter = PortkeySpanExporter(api_key=api_key, base_url=base_url)
    trace.set_tracer_provider(tracer_provider)
    tracer_provider.add_span_processor(BatchSpanProcessor(exporter))
    for package, instrumentor in package_instrumentor_map.items():
        if is_package_installed(package):
            instrumentor().instrument()
            print(f"Portkey: {package} Instrumentation initialized")
