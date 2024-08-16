from enum import Enum
import json
import time
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from portkey_ai.api_resources.apis.logger import Logger
import re
from datetime import datetime

try:
    from langchain_core.callbacks.base import BaseCallbackHandler
except ImportError:
    raise ImportError("Please pip install langchain-core to use PortkeyLangchain")


class LangchainCallbackHandler(BaseCallbackHandler):
    def __init__(
        self,
        api_key: str,
        metadata: Optional[Dict[str, Any]] = {},
    ) -> None:
        super().__init__()

        self.api_key = api_key
        self.metadata = metadata

        self.portkey_logger = Logger(api_key=api_key)

        self.log_object: Any = []
        self.prompt_records: Any = []

        self.request: Any = {}
        self.response: Any = {}

        self.responseStatus: int = 0

        self.streamingMode: bool = False

        self.global_trace_id: str = ""
        self.event_map: Any = {}
        self.event_array: List = []
        self.main_span_id: str = ""

        if not api_key:
            raise ValueError("Please provide an API key to use PortkeyCallbackHandler")

    def on_llm_start(
        self,
        serialized: Dict[str, Any],
        prompts: List[str],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """Run when LLM starts running.

        **ATTENTION**: This method is called for non-chat models (regular LLMs). If
            you're implementing a handler for a chat model,
            you should use on_chat_model_start instead.
        """

        request_payload = self.on_llm_start_transformer(
            serialized, prompts, kwargs=kwargs
        )
        info_obj = self.start_event_information(
            run_id,
            parent_run_id,
            "llm_start",
            self.global_trace_id,
            request_payload,
            self.metadata,
        )
        self.event_map["llm_start_" + str(run_id)] = info_obj
        pass

    def on_chat_model_start(
        self,
        serialized: Dict[str, Any],
        messages: List[List[Any]],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        """Run when a chat model starts running.

        **ATTENTION**: This method is called for chat models. If you're implementing
            a handler for a non-chat model, you should use on_llm_start instead.
        """
        # NotImplementedError is thrown intentionally
        # Callback handler will fall back to on_llm_start if this is exception is thrown

        request_payload = self.on_chat_model_start_transformer(
            serialized, messages, kwargs=kwargs
        )
        info_obj = self.start_event_information(
            run_id,
            parent_run_id,
            "chat_model_start",
            self.global_trace_id,
            request_payload,
            self.metadata,
        )
        self.event_map["chat_model_start_" + str(run_id)] = info_obj
        self.event_array.append(self.event_map["chat_model_start_" + str(run_id)])

        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement `on_chat_model_start`"
        )

    def on_llm_end(
        self,
        response: Any,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> None:
        """Run when LLM ends running."""

        start_time = self.event_map["llm_start_" + str(run_id)]["start_time"]
        end_time = int(datetime.now().timestamp())
        total_time = (end_time - start_time) * 1000

        response_payload = self.on_llm_end_transformer(response, kwargs=kwargs)
        self.event_map["llm_start_" + str(run_id)]["response"] = response_payload
        self.event_map["llm_start_" + str(run_id)]["response"][
            "response_time"
        ] = total_time

        self.event_array.append(self.event_map["llm_start_" + str(run_id)])
        pass

    def on_chain_start(
        self,
        serialized: Dict[str, Any],
        inputs: Dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """Run when chain starts running."""

        if parent_run_id is None:
            self.global_trace_id = self.metadata.get("traceId", str(uuid4()))  # type: ignore [union-attr]
            self.main_span_id = ""
        parent_span_id = (
            self.main_span_id if parent_run_id is None else str(parent_run_id)
        )

        request_payload = self.on_chain_start_transformer(
            serialized, inputs, kwargs=kwargs
        )
        info_obj = self.start_event_information(
            run_id,
            parent_span_id,
            "chain_start",
            self.global_trace_id,
            request_payload,
            self.metadata,
        )

        self.event_map["chain_start_" + str(run_id)] = info_obj
        pass

    def on_chain_end(
        self,
        outputs: Dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> None:
        """Run when chain ends running."""

        start_time = self.event_map["chain_start_" + str(run_id)]["start_time"]
        end_time = int(datetime.now().timestamp())
        total_time = (end_time - start_time) * 1000

        response_payload = self.on_chain_end_transformer(outputs)

        self.event_map["chain_start_" + str(run_id)]["response"] = response_payload
        self.event_map["chain_start_" + str(run_id)]["response"][
            "response_time"
        ] = total_time

        self.event_array.append(self.event_map["chain_start_" + str(run_id)])

        if parent_run_id is None:
            self.log_object = self.event_array
            self.portkey_logger.log(log_object=self.log_object)

            self.event_array = []
            self.event_map = {}

        pass

    def on_tool_start(
        self,
        serialized: Dict[str, Any],
        input_str: str,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        inputs: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """Run when tool starts running."""
        request_payload = self.on_tool_start_transformer(serialized, input_str, inputs)
        info_obj = self.start_event_information(
            run_id,
            parent_run_id,
            "tool_start",
            self.global_trace_id,
            request_payload,
            self.metadata,
        )
        self.event_map["tool_start_" + str(run_id)] = info_obj
        pass

    def on_tool_end(
        self,
        output: Any,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> None:
        """Run when tool ends running."""

        start_time = self.event_map["tool_start_" + str(run_id)]["start_time"]
        end_time = int(datetime.now().timestamp())
        total_time = (end_time - start_time) * 1000

        response_payload = self.on_tool_end_transformer(output)
        self.event_map["tool_start_" + str(run_id)]["response"] = response_payload
        self.event_map["tool_start_" + str(run_id)]["response"][
            "response_time"
        ] = total_time
        self.event_array.append(self.event_map["tool_start_" + str(run_id)])
        pass

    def on_text(
        self,
        text: str,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> None:
        """Run on arbitrary text."""

        parent_span_id = (
            self.main_span_id if parent_run_id is None else str(parent_run_id)
        )
        request_payload = self.on_text_transformer(text)
        info_obj = self.start_event_information(
            run_id,
            parent_span_id,
            "text",
            self.global_trace_id,
            request_payload,
            self.metadata,
        )
        self.event_map["text_" + str(run_id)] = info_obj
        self.event_array.append(self.event_map["text_" + str(run_id)])
        pass

    def on_agent_action(
        self,
        action: Any,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> None:
        """Run on agent action."""

        parent_span_id = (
            self.main_span_id if parent_run_id is None else str(parent_run_id)
        )
        request_payload = self.on_agent_action_transformer(action)
        info_obj = self.start_event_information(
            run_id,
            parent_span_id,
            "agent_action",
            self.global_trace_id,
            request_payload,
            self.metadata,
        )
        self.event_map["agent_action_" + str(run_id)] = info_obj
        pass

    def on_agent_finish(
        self,
        finish: Any,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> None:
        """Run on agent end."""

        start_time = self.event_map["agent_action_" + str(run_id)]["start_time"]
        end_time = int(datetime.now().timestamp())
        total_time = (end_time - start_time) * 1000

        response_payload = self.on_agent_finish_transformer(finish)
        self.event_map["agent_action_" + str(run_id)]["response"] = response_payload
        self.event_map["agent_action_" + str(run_id)]["response"][
            "response_time"
        ] = total_time
        self.event_array.append(self.event_map["agent_action_" + str(run_id)])
        pass

    def on_retriever_start(
        self,
        serialized: Dict[str, Any],
        query: str,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """Run on retriever start."""
        pass

    def on_retriever_end(
        self,
        documents: Any,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> None:
        """Run on retriever end."""
        pass

    #  -------------- Helpers ------------------------------------------
    def start_event_information(
        self,
        span_id,
        parent_span_id,
        span_name,
        trace_id,
        request_payload,
        metadata=None,
    ):
        start_time = int(datetime.now().timestamp())
        return {
            "span_id": str(span_id),
            "parent_span_id": str(parent_span_id),
            "span_name": span_name,
            "trace_id": trace_id,
            "request": request_payload,
            "start_time": start_time,
            "metadata": metadata,
        }

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

    def extract_tools(self, content: str) -> List[Dict[str, Any]]:
        tools_pattern = re.compile(r"(\w+)\((.*?)\) -> (.*?) - (.+)")
        tools_matches = tools_pattern.findall(content)
        tools = []
        for match in tools_matches:
            tool_name, params, return_type, description = match
            param_pattern = re.compile(r"(\w+): (.+?)(?:,|$)")
            param_matches = param_pattern.findall(params)
            {param: param_type for param, param_type in param_matches}
            tools.append(
                {
                    "name": tool_name,
                    "description": description,
                    "return_type": return_type,
                }
            )
        return tools

    def extract_response_format(self, content: str) -> List[str]:
        response_format_pattern = re.compile(
            r"Use the following format:\s*(.*?)\s*Begin!", re.DOTALL
        )
        response_format_match = response_format_pattern.search(content)
        if response_format_match:
            response_format_content = response_format_match.group(1)
            response_format_lines = [
                line.strip()
                for line in response_format_content.split("\n")
                if line.strip()
            ]
            return response_format_lines
        return []

    #  -----------------------------------------------------------------

    # ------ Event Transformers ------

    def on_llm_start_transformer(self, serialized, prompts, kwargs):
        try:
            result = {"messages": []}
            for entry in prompts:
                role, content = entry.split(": ", 1)
                tools = self.extract_tools(content)
                response_format = self.extract_response_format(content)
                example_question_pattern = re.compile(r"Question: (.+?)\n")
                example_question_match = example_question_pattern.search(content)
                example_question = (
                    example_question_match.group(1) if example_question_match else ""
                )
                content_before_format = content.split("Use the following format:")[
                    0
                ].strip()
                input_data = {
                    "role": role,
                    "content": content_before_format,
                    "tools": tools,
                    "response_format": {"structure": response_format},
                    "example_question": example_question,
                    "example_thought": "",
                }
                result["messages"].append(input_data)

            request = {}

            request["method"] = "POST"
            request["url"] = serialized.get("kwargs", "").get(
                "base_url", "chat/completions"
            )
            request["provider"] = serialized["id"][2]
            request["headers"] = serialized.get("kwargs", {}).get("default_headers", {})
            request["headers"].update({"provider": serialized["id"][2]})
            request["body"] = {"messages": result["messages"]}
            request["body"].update(kwargs.get("invocation_params", {}))
            return request
        except Exception:
            return {
                "serialized": serialized,
                "prompts": prompts,
                "invocation_params": kwargs,
            }

    def on_llm_end_transformer(self, response, kwargs):
        try:
            response_obj = {}
            usage = (response.llm_output or {}).get("token_usage", "")  # type: ignore[union-attr]

            response_obj["body"] = {
                "choices": [
                    {
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": response.generations[0][0].text,
                        },
                        "logprobs": response.generations[0][0].generation_info.get("logprobs", ""),  # type: ignore[union-attr] # noqa: E501
                        "finish_reason": response.generations[0][0].generation_info.get("finish_reason", ""),  # type: ignore[union-attr] # noqa: E501
                    }
                ]
            }
            response_obj["body"].update({"usage": usage})
            response_obj["body"].update({"id": str(kwargs.get("run_id", ""))})
            response_obj["body"].update({"created": int(time.time())})
            response_obj["body"].update({"model": (response.llm_output or {}).get("model_name", "")})  # type: ignore[union-attr] # noqa: E501
            response_obj["body"].update({"system_fingerprint": (response.llm_output or {}).get("system_fingerprint", "")})  # type: ignore[union-attr] # noqa: E501
            response_obj["headers"] = {}
            return response_obj
        except Exception:
            return {"response": response, "kwargs": kwargs}

    def on_chain_start_transformer(self, serialized, input, kwargs):
        try:
            name = kwargs["name"]
            return {
                "name": name,
                "input": json.dumps(input),
            }
        except Exception:
            return {"serialized": serialized, "input": input, "kwargs": kwargs}

    def on_chain_end_transformer(self, output):
        try:
            structured_data = {}

            # Define patterns and corresponding keys
            patterns = {
                r"Action:\s*(.*)": "action",
                r"Action Input:\s*(.*)": "action_input",
                r"Final Answer:\s*(.*)": "final_answer",
                r"Answer:\s*(.*)": "answer",
            }

            for key, value in output.items():
                for pattern, result_key in patterns.items():
                    matches = re.findall(pattern, value)
                    if matches:
                        structured_data[result_key] = matches[0].strip()
                    else:
                        structured_data[key] = value

            return {"output": structured_data}

        except Exception:
            return {"output": output}

    def on_text_transformer(self, text):
        try:
            return {"text": text}
        except Exception:
            return {"text": text}

    def on_chat_model_start_transformer(self, serialized, messages, kwargs):
        try:
            model = serialized["id"][-1]
            invocation_params = kwargs["invocation_params"]
            input_data = self.serialize(messages)
            message_obj = input_data[0][0]
            return {
                "model": model,
                "invocation_params": invocation_params,
                "messages": message_obj,
            }
        except Exception:
            return {"serialized": serialized, "messages": message_obj, "kwargs": kwargs}

    def on_agent_action_transformer(self, action):
        try:
            action = self.serialize(action)
            tool = action["tool"]
            tool_input = action["tool_input"]
            log = action["log"]
            return {"tool": tool, "tool_input": tool_input, "log": log}
        except Exception:
            return {"action": action}

    def on_agent_finish_transformer(self, finish):
        try:
            finish = self.serialize(finish)
            return_values = finish["return_values"]
            log = finish["log"]
            return {"return_values": return_values, "log": log}
        except Exception:
            return {"finish": finish}

    def on_tool_start_transformer(self, serialized, input_str, inputs):
        try:
            return {"serialized": serialized, "input_str": input_str, "inputs": inputs}
        except Exception:
            return {"serialized": serialized, "input_str": input_str, "inputs": inputs}

    def on_tool_end_transformer(self, output):
        try:
            return {"output": output}
        except Exception:
            return {"output": output}
