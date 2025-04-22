from portkey_ai.api_resources.instrumentation.models.tracing_config import (
    TracingConfig,
    ModuleConfig,
    ClassConfig,
    MethodConfig,
)

langchain_tracing_config = TracingConfig(
    name="langchain",
    min_version="0.2.0",
    modules=[
        ModuleConfig(
            name="langchain.agents.agent",
            classes=[
                ClassConfig(
                    name="RunnableAgent",
                    methods=[
                        MethodConfig(name="plan"),
                        MethodConfig(name="aplan"),
                    ],
                ),
                ClassConfig(
                    name="RunnableMultiActionAgent",
                    methods=[
                        MethodConfig(name="plan"),
                        MethodConfig(name="aplan"),
                    ],
                ),
            ],
        ),
    ],
)
