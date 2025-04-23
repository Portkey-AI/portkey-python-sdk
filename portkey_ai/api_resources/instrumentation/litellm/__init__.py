from portkey_ai.api_resources.instrumentation.models.tracing_config import (
    TracingConfig,
)

litellm_tracing_config = TracingConfig(
    name="litellm",
    min_version="1.48.0",
    modules=[
        {
            "name": "litellm",
            "methods": [
                {"name": "completion"},
                {"name": "text_completion"},
            ],
        },
        {
            "name": "litellm.main",
            "methods": [
                {"name": "acompletion"},
                {"name": "image_generation"},
                {"name": "aimage_generation"},
                {"name": "embedding"},
                {"name": "aembedding"},
            ],
        },
    ],
)

__all__ = ["litellm_tracing_config"]
