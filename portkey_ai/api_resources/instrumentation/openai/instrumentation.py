import importlib.metadata
from typing import Any, Collection
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor  # type: ignore [attr-defined]
from opentelemetry.trace import get_tracer
from wrapt import wrap_function_wrapper

from portkey_ai.api_resources.instrumentation.openai.patch import patch_openai


class OpenaiInstrumentor(BaseInstrumentor):
    methods_to_patch = [
        {
            "module": "openai.resources.chat.completions",
            "method": "Completions.create",
        },
        {
            "module": "openai.resources.chat.completions",
            "method": "AsyncCompletions.create",
        },
        {
            "module": "openai.resources.images",
            "method": "Images.generate",
        },
        {
            "module": "openai.resources.images",
            "method": "AsyncImages.generate",
        },
        {
            "module": "openai.resources.images",
            "method": "Images.edit",
        },
        {
            "module": "openai.resources.embeddings",
            "method": "Embeddings.create",
        },
        {
            "module": "openai.resources.embeddings",
            "method": "AsyncEmbeddings.create",
        },
    ]

    def instrumentation_dependencies(self) -> Collection[str]:
        return ["openai >= 0.27.0"]

    def _instrument(self, **kwargs: Any) -> None:
        version = importlib.metadata.version("openai")
        tracer_provider = kwargs.get("tracer_provider")
        tracer = get_tracer(__name__, "", tracer_provider)
        for method in self.methods_to_patch:
            wrap_function_wrapper(
                module=method["module"],
                name=method["method"],
                wrapper=patch_openai(
                    method["module"], method["method"], version, tracer
                ),
            )

    def _uninstrument(self, **kwargs: Any) -> None:
        pass
