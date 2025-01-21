import importlib.metadata
from typing import Any, Collection
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor  # type: ignore [attr-defined]
from opentelemetry.trace import get_tracer
from wrapt import wrap_function_wrapper

from portkey_ai.api_resources.instrumentation.langgraph.patch import patch_langgraph


class LanggraphInstrumentor(BaseInstrumentor):
    methods_to_patch = [
        {
            "module": "langgraph.graph.state",
            "method": "StateGraph.add_node",
        },
        {
            "module": "langgraph.graph.state",
            "method": "StateGraph.add_edge",
        },
        {
            "module": "langgraph.graph.state",
            "method": "StateGraph.set_entry_point",
        },
        {
            "module": "langgraph.graph.state",
            "method": "StateGraph.set_finish_point",
        },
        {
            "module": "langgraph.graph.state",
            "method": "StateGraph.add_conditional_edges",
        },
    ]

    def instrumentation_dependencies(self) -> Collection[str]:
        return ["langgraph >= 0.2.0"]

    def _instrument(self, **kwargs: Any) -> None:
        version = importlib.metadata.version("langgraph")
        tracer_provider = kwargs.get("tracer_provider")
        tracer = get_tracer(__name__, "", tracer_provider)
        try:
            for method in self.methods_to_patch:
                wrap_function_wrapper(
                    module=method["module"],
                    name=method["method"],
                    wrapper=patch_langgraph(method["method"], version, tracer),
                )
        except Exception as e:
            print(f"Failed to instrument Langgraph: {e}")

    def _uninstrument(self, **kwargs: Any) -> None:
        pass
