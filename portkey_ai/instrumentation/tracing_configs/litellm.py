from portkey_ai.instrumentation.models.tracing_config import (
    ModuleConfig,
    TracingConfig,
    MethodConfig,
)

litellm_tracing_config = TracingConfig(
    name="litellm",
    min_version="1.48.0",
    modules=[
        ModuleConfig(
            name="litellm",
            methods=[
                MethodConfig(name="completion"),
                MethodConfig(name="text_completion"),
            ],
        ),
        ModuleConfig(
            name="litellm.main",
            methods=[
                MethodConfig(name="acompletion"),
                MethodConfig(name="image_generation"),
                MethodConfig(name="aimage_generation"),
                MethodConfig(name="embedding"),
                MethodConfig(name="aembedding"),
            ],
        ),
    ],
)
