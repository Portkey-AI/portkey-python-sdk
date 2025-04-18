from portkey_ai.api_resources.instrumentation.models.tracing_config import (
    TracingConfig,
)

langchain_core_tracing_config = TracingConfig(
    name="langchain_core",
    min_version="0.2.0",
    modules=[
        {
            "name": "langchain_core.language_models.chat_models",
            "methods": [
                {"name": "chatmodel"},
            ],
        },
        {
            "name": "langchain_core.language_models.base",
            "methods": [
                {"name": "language_model"},
            ],
        },
        {
            "name": "langchain_core.retrievers",
            "methods": [
                {"name": "retriever"},
            ],
        },
        {
            "module": "langchain_core.prompts.chat",
            "method": "prompt",
        },
        {
            "module": "langchain_core.language_models.llms",
            "method": "generate",
        },
        {
            "module": "langchain_core.runnables.base",
            "method": "runnable",
        },
        {
            "module": "langchain_core.runnables.passthrough",
            "method": "runnablepassthrough",
        },
        {
            "module": "langchain_core.output_parsers.string",
            "method": "stroutputparser",
        },
        {
            "module": "langchain_core.output_parsers.json",
            "method": "jsonoutputparser",
        },
        {
            "module": "langchain_core.output_parsers.list",
            "method": "listoutputparser",
        },
        {
            "module": "langchain_core.output_parsers.xml",
            "method": "xmloutputparser",
        },
    ],
)
