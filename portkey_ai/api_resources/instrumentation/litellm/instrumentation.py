import importlib.metadata
from typing import Any, Collection
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor  # type: ignore [attr-defined]
from opentelemetry.trace import get_tracer
from wrapt import wrap_function_wrapper

from portkey_ai.api_resources.instrumentation.litellm.patch import patch_litellm


class LitellmInstrumentor(BaseInstrumentor):
    methods_to_patch = [
        {
            "module": "litellm",
            "method": "completion",
        },
        {
            "module": "litellm",
            "method": "text_completion",
        },
        {
            "module": "litellm.main",
            "method": "acompletion",
        },
        {
            "module": "litellm.main",
            "method": "image_generation",
        },
        {
            "module": "litellm.main",
            "method": "aimage_generation",
        },
        {
            "module": "litellm.main",
            "method": "embedding",
        },
        {
            "module": "litellm.main",
            "method": "aembedding",
        },
    ]

    def instrumentation_dependencies(self) -> Collection[str]:
        return ["litellm >= 1.48.0"]

    def _instrument(self, **kwargs: Any) -> None:
        version = importlib.metadata.version("litellm")
        tracer_provider = kwargs.get("tracer_provider")
        tracer = get_tracer(__name__, "", tracer_provider)
        for method in self.methods_to_patch:
            wrap_function_wrapper(
                module=method["module"],
                name=method["method"],
                wrapper=patch_litellm(
                    method["module"], method["method"], version, tracer
                ),
            )

    def _uninstrument(self, **kwargs: Any) -> None:
        pass
