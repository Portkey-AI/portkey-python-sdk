from enum import Enum
import json
import time
from typing import Any, Dict, List, Optional
from portkey_ai.api_resources.apis.logger import Logger
from datetime import datetime
from llama_index.core.callbacks.schema import (
    CBEventType,
)
from uuid import uuid4
from llama_index.legacy.schema import NodeRelationship

try:
    from llama_index.core.callbacks.base_handler import (
        BaseCallbackHandler as LlamaIndexBaseCallbackHandler,
    )
    from llama_index.core.utilities.token_counting import TokenCounter
except ModuleNotFoundError:
    raise ModuleNotFoundError(
        "Please install llama-index to use Portkey Callback Handler"
    )
except ImportError:
    raise ImportError("Please pip install llama-index to use Portkey Callback Handler")


class PortkeyLlamaindex(LlamaIndexBaseCallbackHandler):
    def __init__(
        self,
        api_key: str,
    ) -> None:
        super().__init__(
            event_starts_to_ignore=[
                CBEventType.CHUNKING,
                CBEventType.NODE_PARSING,
                CBEventType.SYNTHESIZE,
                CBEventType.EXCEPTION,
            ],
            event_ends_to_ignore=[
                CBEventType.CHUNKING,
                CBEventType.NODE_PARSING,
                CBEventType.SYNTHESIZE,
                CBEventType.EXCEPTION,
            ],
        )

        self.api_key = api_key

        self.portkey_logger = Logger(api_key=api_key)

        self._token_counter = TokenCounter()
        self.completion_tokens = 0
        self.prompt_tokens = 0
        self.token_llm = 0

        self.log_object: Any = []
        self.prompt_records: Any = []

        self.request: Any = {}
        self.response: Any = {}

        self.global_trace_id: str = ""
        self.streamingMode: bool = False

        self.event_map: Any = {}
        self.event_array: List = []
        self.main_span_id: str = ""

        if not api_key:
            raise ValueError("Please provide an API key to use PortkeyCallbackHandler")

    def on_event_start(  # type: ignore
        self,
        event_type: Any,
        payload: Optional[Dict[str, Any]] = None,
        event_id: str = "",
        parent_id: str = "",
        **kwargs: Any,
    ) -> str:
        """Run when an event starts and return id of event."""

        span_id = str(event_id)
        parent_span_id = parent_id
        span_name = event_type
        start_time = int(datetime.now().timestamp())

        if parent_id == "root":
            parent_span_id = self.main_span_id

        if event_type == "llm":
            request_payload = self.llm_event_start(payload)
        elif event_type == "embedding":
            request_payload = self.embedding_event_start(payload)
        elif event_type == "agent_step":
            request_payload = self.agent_step_event_start(payload)
        elif event_type == "function_call":
            request_payload = self.function_call_event_start(payload)
        elif event_type == "query":
            request_payload = self.query_event_start(payload)
        elif event_type == "retrieve":
            request_payload = self.retrieve_event_start(payload)
        elif event_type == "templating":
            request_payload = self.templating_event_start(payload)
        else:
            request_payload = payload

        start_event_information = {
            "span_id": span_id,
            "parent_span_id": parent_span_id,
            "span_name": span_name.value,
            "trace_id": self.global_trace_id,
            "request": request_payload,
            "start_time": start_time,
        }
        self.event_map[span_id] = start_event_information

    def on_event_end(
        self,
        event_type: Any,
        payload: Optional[Dict[str, Any]] = None,
        event_id: str = "",
        **kwargs: Any,
    ) -> None:
        """Run when an event ends."""
        span_id = event_id

        if event_type == "llm":
            response_payload = self.llm_event_end(payload, event_id)
        elif event_type == "embedding":
            response_payload = self.embedding_event_end(payload, event_id)
        elif event_type == "agent_step":
            response_payload = self.agent_step_event_end(payload, event_id)
        elif event_type == "function_call":
            response_payload = self.function_call_event_end(payload, event_id)
        elif event_type == "query":
            response_payload = self.query_event_end(payload, event_id)
        elif event_type == "retrieve":
            response_payload = self.retrieve_event_end(payload, event_id)
        elif event_type == "templating":
            response_payload = self.templating_event_end(payload, event_id)
        else:
            response_payload = payload

        self.event_map[span_id]["response"] = response_payload
        self.event_array.append(self.event_map[span_id])

    def start_trace(self, trace_id: Optional[str] = None) -> None:
        """Run when an overall trace is launched."""

        if trace_id == "index_construction":
            self.global_trace_id = str(uuid4())

        self.main_span_id = ""

    def end_trace(
        self,
        trace_id: Optional[str] = None,
        trace_map: Optional[Dict[str, List[str]]] = None,
    ) -> None:
        """Run when an overall trace is exited."""

        self.log_object = self.event_array

        self.portkey_logger.log(log_object=self.log_object)
        self.event_array = []

    # ------------------- EVENT Handlers ------------------- #
    def llm_event_start(self, payload: Any) -> Any:
        self.request = {}
        if "messages" in payload:
            chunks = payload.get("messages", {})
            self.prompt_tokens = self._token_counter.estimate_tokens_in_messages(chunks)
            messages = payload.get("messages", {})
            self.prompt_records = [
                {"role": m.role.value, "content": m.content} for m in messages
            ]
        self.request["method"] = "POST"
        self.request["url"] = payload.get("serialized", {}).get(
            "api_base", "chat/completions"
        )
        self.request["provider"] = payload.get("serialized", {}).get("class_name", "")
        self.request["headers"] = {}
        self.request["body"] = {"messages": self.prompt_records}
        self.request["body"].update(
            {"model": payload.get("serialized", {}).get("model", "")}
        )
        self.request["body"].update(
            {"temperature": payload.get("serialized", {}).get("temperature", "")}
        )

        return self.request

    def llm_event_end(self, payload: Any, event_id) -> Any:
        if event_id in self.event_map:
            event = self.event_map[event_id]
            start_time = event["start_time"]

        self.response = {}

        data = payload.get("response", {})

        chunks = payload.get("messages", {})
        self.completion_tokens = self._token_counter.estimate_tokens_in_messages(chunks)
        self.token_llm = self.prompt_tokens + self.completion_tokens
        self.response["status"] = 200
        self.response["body"] = {
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": data.message.role.value,
                        "content": data.message.content,
                    },
                    "logprobs": data.logprobs,
                    "finish_reason": "done",
                }
            ]
        }
        self.response["body"].update(
            {
                "usage": {
                    "prompt_tokens": self.prompt_tokens,
                    "completion_tokens": self.completion_tokens,
                    "total_tokens": self.token_llm,
                }
            }
        )
        self.response["body"].update({"id": event_id})
        self.response["body"].update({"created": int(time.time())})
        self.response["body"].update({"model": data.raw.get("model", "")})
        self.response["headers"] = {}
        self.response["streamingMode"] = self.streamingMode

        end_time = int(datetime.now().timestamp())
        total_time = (end_time - start_time) * 1000

        self.response["response_time"] = total_time

        return self.response

    # ------------------------------------------------------ #
    def embedding_event_start(self, payload: Any) -> Any:
        self.request = {}
        if "serialized" in payload:
            self.request["method"] = "POST"
            self.request["url"] = payload.get("serialized", {}).get(
                "api_base", "embeddings"
            )
            self.request["provider"] = payload.get("serialized", {}).get(
                "class_name", ""
            )
            self.request["headers"] = {}
            self.request["body"] = {
                "model": payload.get("serialized", {}).get("model_name", "")
            }

        return self.request

    def embedding_event_end(self, payload: Any, event_id) -> Any:
        if event_id in self.event_map:
            event = self.event_map[event_id]
            # event["request"]["body"]["input"] = payload.get("chunks", "")
            # Setting as ...INPUT... to avoid logging the entire data input file
            event["request"]["body"]["input"] = "...INPUT..."

            start_time = event["start_time"]

        self.response = {}

        chunk_str = str(payload.get("chunks", ""))
        embd_str = str(payload.get("embeddings", ""))

        self.prompt_tokens = self._token_counter.get_string_tokens(chunk_str)
        self.completion_tokens = self._token_counter.get_string_tokens(embd_str)

        self.response["status"] = 200
        self.response["body"] = {
            "embedding": "...REDACTED...",
        }

        self.response["body"].update({"created": int(time.time())})

        self.response["body"].update(
            {
                "usage": {
                    "prompt_tokens": self.prompt_tokens,
                    "completion_tokens": self.completion_tokens,
                    "total_tokens": self.prompt_tokens + self.completion_tokens,
                }
            }
        )
        self.response["headers"] = {}

        end_time = int(datetime.now().timestamp())
        total_time = (end_time - start_time) * 1000

        self.response["response_time"] = total_time

        return self.response

    # ------------------------------------------------------ #
    def agent_step_event_start(self, payload: Any) -> Any:
        data = json.dumps(self.serialize(payload))
        return data

    def agent_step_event_end(self, payload: Any, event_id) -> Any:
        if event_id in self.event_map:
            event = self.event_map[event_id]
            start_time = event["start_time"]
        data = self.serialize(payload)
        json.dumps(data)
        result = self.transform_agent_step_end(data)
        end_time = int(datetime.now().timestamp())
        total_time = (end_time - start_time) * 1000

        result["response_time"] = total_time
        return result

    # ------------------------------------------------------ #
    def function_call_event_start(self, payload: Any) -> Any:
        result = self.transform_function_call_start(payload)
        return result

    def function_call_event_end(self, payload: Any, event_id) -> Any:
        if event_id in self.event_map:
            event = self.event_map[event_id]
            start_time = event["start_time"]
        data = self.serialize(payload)
        json.dumps(data)
        result = self.transform_function_call_end(data)
        end_time = int(datetime.now().timestamp())
        total_time = (end_time - start_time) * 1000

        result["response_time"] = total_time
        return result

    # ------------------------------------------------------ #
    def query_event_start(self, payload: Any) -> Any:
        data = json.dumps(self.serialize(payload))
        return data

    def query_event_end(self, payload: Any, event_id) -> Any:
        if event_id in self.event_map:
            event = self.event_map[event_id]
            start_time = event["start_time"]
        data = self.serialize(payload)
        json.dumps(data)
        result = self.transform_query_end(data)
        end_time = int(datetime.now().timestamp())
        total_time = (end_time - start_time) * 1000

        result["response_time"] = total_time
        return result

    # ------------------------------------------------------ #
    def retrieve_event_start(self, payload: Any) -> Any:
        data = json.dumps(self.serialize(payload))
        return data

    def retrieve_event_end(self, payload: Any, event_id) -> Any:
        if event_id in self.event_map:
            event = self.event_map[event_id]
            start_time = event["start_time"]

        data = self.serialize(payload)
        json.dumps(data)
        result = self.transform_retrieve_end(data)
        end_time = int(datetime.now().timestamp())
        total_time = (end_time - start_time) * 1000

        result["response_time"] = total_time
        return result

    # ------------------------------------------------------ #
    def templating_event_start(self, payload: Any) -> Any:
        data = self.serialize(payload)
        json.dumps(data)
        result = self.transform_templating_start(data)
        return result

    def templating_event_end(self, payload: Any, event_id) -> Any:
        if event_id in self.event_map:
            event = self.event_map[event_id]
            start_time = event["start_time"]
        result = self.transform_templating_end(event_id)

        end_time = int(datetime.now().timestamp())
        total_time = (end_time - start_time) * 1000

        result["response_time"] = total_time
        return result

    # ------------------------------------------------------ #

    # ----------------- EVENT Transformers ----------------- #
    def transform_agent_step_end(self, data: Any) -> Any:
        try:
            output_data = {
                "agent_chat_response": {
                    "response": data["response"]["response"],
                    "sources": [
                        {
                            "content": source["content"],
                            "tool_name": source["tool_name"],
                            "raw_input": source["raw_input"],
                            "raw_output": {
                                "response": source["raw_output"]["response"],
                                "source_nodes": [
                                    {
                                        "id": node["node"]["id_"],
                                        "metadata": node["node"]["metadata"],
                                        "text_excerpt": node["node"]["text"],
                                        "score": node["score"],
                                    }
                                    for node in source["raw_output"]["source_nodes"]
                                ],
                            },
                        }
                        for source in data["response"]["sources"]
                    ],
                }
            }
            return output_data
        except Exception:
            return data

    def transform_query_end(self, data: Any) -> Any:
        try:
            output_data = {
                "response": {
                    "content": data["response"]["response"],
                    "source_nodes": [],
                }
            }

            for source_node in data["response"]["source_nodes"]:
                node = source_node["node"]
                metadata = node["metadata"]
                text_excerpt = node["text"][
                    node["start_char_idx"] : node["end_char_idx"]
                ]

                output_data["response"]["source_nodes"].append(
                    {
                        "id": node["id_"],
                        "metadata": {
                            "file_path": metadata["file_path"],
                            "file_name": metadata["file_name"],
                            "file_type": metadata["file_type"],
                            "file_size": metadata["file_size"],
                            "creation_date": metadata["creation_date"],
                            "last_modified_date": metadata["last_modified_date"],
                        },
                        "text_excerpt": text_excerpt,
                        "score": source_node["score"],
                    }
                )
            return output_data
        except Exception:
            return data

    def transform_retrieve_end(self, data: Any) -> Any:
        try:
            output_data = {"nodes": []}  # type: ignore[var-annotated]

            for node_data in data["nodes"]:
                node = node_data["node"]
                metadata = node["metadata"]
                text_excerpt = node["text"][
                    node["start_char_idx"] : node["end_char_idx"]
                ]

                relationships = {}
                for relationship, details in node["relationships"].items():
                    relationships[relationship.name] = {
                        "node_id": details["node_id"],
                        "node_type": "DOCUMENT"
                        if relationship == NodeRelationship.SOURCE
                        else "TEXT",
                    }

                output_data["nodes"].append(
                    {
                        "id": node["id_"],
                        "metadata": {
                            "file_path": metadata["file_path"],
                            "file_name": metadata["file_name"],
                            "file_type": metadata["file_type"],
                            "file_size": metadata["file_size"],
                            "creation_date": metadata["creation_date"],
                            "last_modified_date": metadata["last_modified_date"],
                        },
                        "relationships": relationships,
                        "text_excerpt": text_excerpt,
                        "score": node_data["score"],
                    }
                )

            return output_data
        except Exception:
            return data

    def transform_templating_start(self, data: Any) -> Any:
        try:
            output_data = {
                "template": {
                    "system": data["template"].split("user:")[0].strip(),
                    "user": "Context information is below.\n---------------------\n{context_str}\n---------------------\nGiven the context information and not prior knowledge, answer the query.\nQuery: {query_str}\nAnswer: ",  # noqa: E501
                    "assistant": "",
                },
                "template_vars": {
                    "context_str": data["template_vars"]["context_str"],
                    "query_str": data["template_vars"]["query_str"],
                },
                "system_prompt": data["system_prompt"],
                "query_wrapper_prompt": data["query_wrapper_prompt"],
            }
            return output_data
        except Exception:
            return data

    def transform_templating_end(self, event_id) -> Any:
        try:
            request_data = self.event_map[event_id]["request"]
            context_str = request_data["template_vars"]["context_str"]
            query_str = request_data["template_vars"]["query_str"]
            replace_str = request_data["template"]["user"]
            output_data = {
                "template": {
                    "system": request_data["template"]["system"],
                    "user": replace_str.format(
                        context_str=context_str, query_str=query_str
                    ),
                    "assistant": request_data["template"]["assistant"],
                }
            }

            return output_data
        except Exception:
            return ""

    def transform_function_call_start(self, data: Any) -> Any:
        try:
            tool_meta = data.get("tool")
            output_data = {
                "function_call": data.get("function_call", ""),
                "tool": {
                    "description": tool_meta.description
                    if tool_meta.description
                    else "",
                    "name": tool_meta.name if tool_meta.name else "",
                },
            }
            return output_data
        except Exception:
            return data

    def transform_function_call_end(self, data: Any) -> Any:
        try:
            output_data = {"function_call_response": data["function_call_response"]}
            return output_data
        except Exception:
            return data

    # ----------------- HELPER FUNCTIONS ------------------- #

    def serialize(self, obj):
        if isinstance(obj, Enum):
            return obj.value
        if hasattr(obj, "__dict__"):
            return {key: self.serialize(value) for key, value in obj.__dict__.items()}
        if isinstance(obj, list):
            return [self.serialize(item) for item in obj]
        if isinstance(obj, dict):
            return {key: self.serialize(value) for key, value in obj.items()}
        if isinstance(obj, tuple):
            return tuple(self.serialize(item) for item in obj)
        return obj
