from portkey_ai.api_resources.instrumentation.models.tracing_config import (
    TracingConfig,
)

crewai_tracing_config = TracingConfig(
    name="crewai",
    min_version="0.32.0",
    modules=[
        {
            "name": "crewai.crew",
            "classes": [
                {
                    "name": "Crew",
                    "methods": [
                        {"name": "kickoff"},
                        {"name": "kickoff_for_each"},
                        {"name": "kickoff_async"},
                        {"name": "kickoff_for_each_async"},
                    ],
                },
            ],
        },
        {
            "name": "crewai.agent",
            "classes": [{"name": "Agent", "methods": [{"name": "execute_task"}]}],
        },
        {
            "name": "crewai.task",
            "classes": [{"name": "Task", "methods": [{"name": "execute_sync"}]}],
        },
        {
            "name": "crewai.memory.storage.rag_storage",
            "classes": [
                {
                    "name": "RAGStorage",
                    "methods": [
                        {"name": "save"},
                        {"name": "search"},
                        {"name": "reset"},
                    ],
                }
            ],
        },
    ],
)

__all__ = ["crewai_tracing_config"]
