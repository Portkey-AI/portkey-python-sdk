from portkey_ai.api_resources.instrumentation.models.tracing_config import (
    TracingConfig,
)

openai_tracing_config = TracingConfig(
    name="openai",
    min_version="0.27.0",
    modules=[
        {
            "name": "openai.resources.chat.completions",
            "classes": [
                {"name": "Completions", "methods": [{"name": "create"}]},
                {"name": "AsyncCompletions", "methods": [{"name": "create"}]},
            ],
        },
        {
            "name": "openai.resources.images",
            "classes": [
                {"name": "Images", "methods": [{"name": "generate"}, {"name": "edit"}]},
                {"name": "AsyncImages", "methods": [{"name": "generate"}]},
            ],
        },
        {
            "name": "openai.resources.embeddings",
            "classes": [
                {"name": "Embeddings", "methods": [{"name": "create"}]},
                {"name": "AsyncEmbeddings", "methods": [{"name": "create"}]},
            ],
        },
    ],
)

__all__ = ["openai_tracing_config"]
