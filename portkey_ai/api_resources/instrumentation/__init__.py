from importlib.metadata import version, PackageNotFoundError
from typing import Dict, Any
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from portkey_ai.api_resources.instrumentation.PortkeyBaseInstrumentor import PortkeyBaseInstrumentor  # type: ignore [attr-defined]
from portkey_ai.api_resources.instrumentation.portkey_span_exporter import (
    PortkeySpanExporter,
)
from portkey_ai.api_resources.instrumentation.tracing_configs import tracing_configs
from portkey_ai.api_resources.instrumentation.utils import is_package_installed
from portkey_ai.api_resources.instrumentation.decorator import watch


def initialize_instrumentation(api_key: str, base_url: str):
    if not isinstance(trace.get_tracer_provider(), TracerProvider):
        tracer_provider = TracerProvider()
        trace.set_tracer_provider(tracer_provider)
    else:
        tracer_provider = trace.get_tracer_provider()
    exporter = PortkeySpanExporter(api_key=api_key, base_url=base_url)
    tracer_provider.add_span_processor(BatchSpanProcessor(exporter))
    for package, config in tracing_configs.items():
        if is_package_installed(package):
            InstrumentorClass = type(
                f"{package}Instrumentor", (PortkeyBaseInstrumentor,), {"config": config}
            )
            instrumentor = InstrumentorClass(config)
            instrumentor.instrument()
            print(f"Portkey: {package} Instrumentation initialized")


__all__ = ["initialize_instrumentation", "watch"]
