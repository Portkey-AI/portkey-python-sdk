from portkey_ai.api_resources.instrumentation.models.tracing_config import (
    TracingConfig,
)

langchain_community_tracing_config = TracingConfig(
    name="langchain_community",
    min_version="0.2.0",
    modules=[
        {
            "name": "langchain_community.vectorstores",
            "classes": [
                {
                    "include_pattern": ".*",
                    "methods": [
                        {
                            "include_pattern": ".*",
                        }
                    ],
                }
            ],
        }
    ],
)
