from portkey_ai.api_resources.instrumentation.models.tracing_config import (
    TracingConfig,
    ModuleConfig,
    ClassConfig,
    MethodConfig,
)


langchain_core_tracing_config = TracingConfig(
    name="langchain_core",
    min_version="0.2.0",
    modules=[
        ModuleConfig(
            name="langchain_core.documents",
            classes=[ClassConfig(pattern=".*", methods=[MethodConfig(pattern=".*")])],
        ),
    ],
)
