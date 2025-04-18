from portkey_ai.api_resources.instrumentation.models.tracing_config import (
    TracingConfig,
    ModuleConfig,
    ClassConfig,
    MethodConfig,
)

langchain_community_tracing_config = TracingConfig(
    name="langchain_community",
    min_version="0.2.0",
    modules=[
        ModuleConfig(
            name="langchain_community.vectorstores",
            classes=[
                ClassConfig(
                    pattern=".*",
                    methods=[MethodConfig(pattern=".*")],
                ),
            ],
        ),
        ModuleConfig(
            name="langchain_community.document_loaders",
            classes=[
                ClassConfig(
                    pattern=".*",
                    methods=[MethodConfig(pattern=".*")],
                ),
            ],
        ),
    ],
)
