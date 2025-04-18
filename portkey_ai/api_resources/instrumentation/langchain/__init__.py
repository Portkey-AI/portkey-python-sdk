from portkey_ai.api_resources.instrumentation.models.tracing_config import (
    TracingConfig,
)

langchain_tracing_config = TracingConfig(
    name="langchain",
    min_version="0.2.0",
    modules=[
        {
            "name": "langchain.agents",
            "classes": [
                {
                    "name": "RunnableAgent",
                    "methods": [
                        {"name": "plan"},
                        {"name": "aplan"},
                    ],
                },
                {
                    "name": "RunnableMultiActionAgent",
                    "methods": [
                        {"name": "plan"},
                        {"name": "aplan"},
                    ],
                },
            ],
        },
    ],
)

__all__ = ["langchain_tracing_config"]
