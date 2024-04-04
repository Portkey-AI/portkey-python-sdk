from typing import Any, Dict, List, Optional
from llama_index.core.callbacks import BaseCallbackHandler
from llama_index.core.callbacks.schema import BASE_TRACE_EVENT, CBEventType
from llama_index.core.callbacks.base_handler import (
        BaseCallbackHandler as LlamaIndexBaseCallbackHandler,
    )

from portkey_ai.api_resources.apis.logger import Logger 



class PortkeyCallbackHandler(LlamaIndexBaseCallbackHandler):
    def __init__(
        self,
        api_key: str,
    ) -> None:
        super().__init__(
            event_starts_to_ignore=[],
            event_ends_to_ignore=[],
        )

        self.api_key = api_key


        self.portkey_logger = Logger(api_key=api_key)

    def on_event_start(
        self,
        event_type: CBEventType,
        payload: Optional[Dict[str, Any]] = None,
        event_id: str = "",
        parent_id: str = "",
        **kwargs: Any,
    ) -> str:
        """Run when an event starts and return id of event."""

        print("on_event_start event_type", event_type)
        print("on_event_start payload", payload)
        print("on_event_start event_id", event_id)
        print("on_event_start parent_id", parent_id)
        print("on_event_start kwargs", kwargs)

    def on_event_end(
        self,
        event_type: CBEventType,
        payload: Optional[Dict[str, Any]] = None,
        event_id: str = "",
        **kwargs: Any,
    ) -> None:
        """Run when an event ends."""
        print("on_event_end event_type", event_type)
        print("on_event_end payload", payload)
        print("on_event_end event_id", event_id)

    def start_trace(self, trace_id: Optional[str] = None) -> None:
        """Run when an overall trace is launched."""
        print("start_trace trace_id", trace_id)

    def end_trace(
        self,
        trace_id: Optional[str] = None,
        trace_map: Optional[Dict[str, List[str]]] = None,
    ) -> None:
        """Run when an overall trace is exited."""
        print("end_trace trace_id",trace_id)
        print("end_trace trace_map",trace_map)