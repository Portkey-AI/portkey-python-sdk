import importlib
import inspect
import re
from typing import Any, Collection
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor  # type: ignore [attr-defined]
from opentelemetry.trace import get_tracer
from wrapt import wrap_function_wrapper

from portkey_ai.api_resources.instrumentation.utils import Patcher
from portkey_ai.api_resources.instrumentation.models.tracing_config import (
    TracingConfig,
    ModuleConfig,
    MethodConfig,
)


class PortkeyBaseInstrumentor(BaseInstrumentor):
    def __init__(self, config: TracingConfig):
        self.config = config

    def instrumentation_dependencies(self) -> Collection[str]:
        return [f"{self.config.name} >= {self.config.min_version}"]

    def _get_methods_to_instrument(
        self,
        method_to_instrument: MethodConfig,
        module: ModuleConfig,
        imported_module: Any | None,
        class_name: str,
    ):
        flattened_list = []
        if method_to_instrument.pattern is not None:
            method_regex = re.compile(method_to_instrument.pattern)
            imported_class = getattr(imported_module, class_name)
            methods = inspect.getmembers(
                imported_class,
                lambda x: inspect.isfunction(x),
            )
            for method_name, _ in methods:
                if not method_name.startswith("_") and method_regex.match(method_name):
                    flattened_list.append(
                        {
                            "module": module.name,
                            "method": f"{class_name}.{method_name}",
                            "config": method_to_instrument,
                        }
                    )
        elif method_to_instrument.name is not None:
            flattened_list.append(
                {
                    "module": module.name,
                    "method": f"{class_name}.{method_to_instrument.name}",
                    "config": method_to_instrument,
                }
            )
        return flattened_list

    def _instrument(self, **kwargs: Any) -> None:
        version = importlib.metadata.version(self.config.name)
        tracer_provider = kwargs.get("tracer_provider")
        tracer = get_tracer(f"{self.config.name}-instrumentor", "", tracer_provider)
        try:
            patcher = Patcher(source=self.config.name, version=version, tracer=tracer)
            flattened_list = []
            for module in self.config.modules:
                try:
                    classes_to_instrument = module.classes
                    for class_to_instrument in classes_to_instrument:
                        try:
                            if class_to_instrument.pattern is not None:
                                class_regex = re.compile(class_to_instrument.pattern)
                                imported_module = importlib.import_module(module.name)
                                if (
                                    getattr(imported_module, "_module_lookup", None)
                                    is not None
                                ):
                                    classes = [
                                        [x, ""]
                                        for x in getattr(
                                            imported_module, "_module_lookup", []
                                        ).keys()
                                    ]
                                else:
                                    classes = inspect.getmembers(
                                        imported_module,
                                        lambda x: inspect.isclass(x)
                                        and class_regex.match(x.__name__),
                                    )
                                for class_name, _ in classes:
                                    for (
                                        method_to_instrument
                                    ) in class_to_instrument.methods:
                                        flattened_list.extend(
                                            self._get_methods_to_instrument(
                                                method_to_instrument,
                                                module,
                                                imported_module,
                                                class_name,
                                            )
                                        )
                            elif class_to_instrument.name is not None:
                                methods_to_instrument = class_to_instrument.methods
                                imported_module = importlib.import_module(module.name)
                                for method_to_instrument in methods_to_instrument:
                                    flattened_list.extend(
                                        self._get_methods_to_instrument(
                                            method_to_instrument,
                                            module,
                                            imported_module,
                                            class_to_instrument.name,
                                        )
                                    )
                        except Exception as e:
                            pass  # TODO: report error to portkey
                except Exception as e:
                    pass  # TODO: report error to portkey
            for method_to_instrument in flattened_list:
                try:
                    method_name = method_to_instrument["method"]
                    wrap_function_wrapper(
                        module=method_to_instrument["module"],
                        name=method_name,
                        wrapper=patcher.patch_operation(
                            method_name,
                            method_to_instrument["config"],
                        ),
                    )
                except Exception as e:
                    pass
        except Exception as e:
            pass

    def _uninstrument(self, **kwargs: Any) -> None:
        pass
