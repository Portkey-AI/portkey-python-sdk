from portkey_ai.api_resources.instrumentation.models.tracing_config import (
    TracingConfig,
)

langgraph_tracing_config = TracingConfig(
    name="langgraph",
    min_version="0.2.0",
    modules=[
        {
            "name": "langgraph.graph.state",
            "classes": [
                {
                    "name": "StateGraph",
                    "methods": [
                        {"name": "add_node"},
                        {"name": "add_edge"},
                        {"name": "set_entry_point"},
                        {"name": "set_finish_point"},
                        {"name": "add_conditional_edges"},
                    ],
                },
            ],
        },
    ],
)

__all__ = ["langgraph_tracing_config"]
