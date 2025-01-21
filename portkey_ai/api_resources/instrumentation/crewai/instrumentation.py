import importlib.metadata
from typing import Any, Collection
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor  # type: ignore [attr-defined]
from opentelemetry.trace import get_tracer
from wrapt import wrap_function_wrapper

from portkey_ai.api_resources.instrumentation.crewai.patch import patch_crew


class CrewAIInstrumentor(BaseInstrumentor):
    methods_to_patch = [
        {
            "module": "crewai.crew",
            "method": "Crew.kickoff",
        },
        {
            "module": "crewai.crew",
            "method": "Crew.kickoff_for_each",
        },
        {
            "module": "crewai.crew",
            "method": "Crew.kickoff_async",
        },
        {
            "module": "crewai.crew",
            "method": "Crew.kickoff_for_each_async",
        },
        {
            "module": "crewai.agent",
            "method": "Agent.execute_task",
        },
        {
            "module": "crewai.task",
            "method": "Task.execute_sync",
        },
        {
            "module": "crewai.memory.storage.rag_storage",
            "method": "RAGStorage.save",
        },
        {
            "module": "crewai.memory.storage.rag_storage",
            "method": "RAGStorage.search",
        },
        {
            "module": "crewai.memory.storage.rag_storage",
            "method": "RAGStorage.reset",
        },
    ]

    def instrumentation_dependencies(self) -> Collection[str]:
        return ["crewai >= 0.32.0"]

    def _instrument(self, **kwargs: Any) -> None:
        version = importlib.metadata.version("crewai")
        tracer_provider = kwargs.get("tracer_provider")
        tracer = get_tracer(__name__, "", tracer_provider)
        try:
            for method in self.methods_to_patch:
                wrap_function_wrapper(
                    module=method["module"],
                    name=method["method"],
                    wrapper=patch_crew(method["method"], version, tracer),
                )
        except Exception as e:
            print(f"Failed to instrument CrewAI: {e}")

    def _uninstrument(self, **kwargs: Any) -> None:
        pass
