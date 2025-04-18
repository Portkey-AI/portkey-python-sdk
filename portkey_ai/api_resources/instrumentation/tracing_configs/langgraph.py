from portkey_ai.api_resources.instrumentation.models.tracing_config import (
    TracingConfig,
    ModuleConfig,
    ClassConfig,
    MethodConfig,
)

langgraph_tracing_config = TracingConfig(
    name="langgraph",
    min_version="0.2.0",
    modules=[
        ModuleConfig(
            name="langgraph.graph.state",
            classes=[
                ClassConfig(
                    name="StateGraph",
                    methods=[
                        MethodConfig(name="add_node"),
                        MethodConfig(name="add_edge"),
                        MethodConfig(name="set_entry_point"),
                        MethodConfig(name="set_finish_point"),
                        MethodConfig(name="add_conditional_edges"),
                    ],
                ),
            ],
        ),
    ],
)
