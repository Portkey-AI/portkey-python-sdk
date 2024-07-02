from enum import Enum
import json
import time
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from portkey_ai.api_resources.apis.logger import Logger
import re

try:
    from langchain_core.callbacks.base import BaseCallbackHandler
except ImportError:
    raise ImportError("Please pip install langchain-core to use PortkeyLangchain")


class PortkeyLangchain(BaseCallbackHandler):
    def __init__(
        self,
        api_key: str,
    ) -> None:
        super().__init__()
        self.startTimestamp: float = 0
        self.endTimestamp: float = 0

        self.api_key = api_key

        self.portkey_logger = Logger(api_key=api_key)

        self.log_object: Dict[str, Any] = {}
        self.prompt_records: Any = []

        self.request: Any = {}
        self.response: Any = {}

        # self.responseHeaders: Dict[str, Any] = {}
        self.responseBody: Any = None
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
        # print("on_llm_start")
        # print("on_llm_start: run_id: ", run_id)
        # print("on_llm_start: parent_run_id: ", parent_run_id)

        request_payload = self.on_llm_start_transformer(
            serialized, prompts, kwargs=kwargs
        )
        info_obj = self.start_event_information(
            run_id,
            parent_run_id,
            "llm_start",
            self.global_trace_id,
            request_payload,
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

        # print("on_chat_model_start")
        # print("on_chat_model_start: serialized: ", serialized)
        # print("on_chat_model_start: messages: ", messages)
        # print("on_chat_model_start: kwargs: ", kwargs)
        # print("on_chat_model_start: run_id: ", run_id)
        # print("on_chat_model_start: parent_run_id: ", parent_run_id)

        request_payload = self.on_chat_model_start_transformer(
            serialized, messages, kwargs=kwargs
        )
        info_obj = self.start_event_information(
            run_id,
            parent_run_id,
            "chat_model_start",
            self.global_trace_id,
            request_payload,
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
        # print("on_llm_end: ")
        # print(f"on_llm_end: run_id: {run_id}")
        # print(f"on_llm_end: parent_run_id: {parent_run_id}")

        response_payload = self.on_llm_end_transformer(response, kwargs=kwargs)
        self.event_map["llm_start_" + str(run_id)]["response"] = response_payload
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

        # print("on_chain_start: ")
        # print(f"on_chain_start: run_id: {run_id}")
        # print(f"on_chain_start: parent_run_id: {parent_run_id}")
        # print("on_chain_start: serialized: ", serialized)
        # print("on_chain_start: inputs: ", inputs)
        # print("on_chain_start: kwargs: ", kwargs)

        if parent_run_id is None:
            self.global_trace_id = str(uuid4())
            self.main_span_id = str(uuid4())

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
        )

        self.event_map["chain_start_" + str(run_id)] = info_obj
        # print(
        #     "on_chain_start: eventMap: ", self.event_map["chain_start_" + str(run_id)]
        # )
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
        # print("on_chain_end: ")
        # print(f"on_chain_end: run_id: {run_id}")
        # print(f"on_chain_end: parent_run_id: {parent_run_id}")

        response_payload = self.on_chain_end_transformer(outputs)

        self.event_map["chain_start_" + str(run_id)]["response"] = response_payload
        self.event_array.append(self.event_map["chain_start_" + str(run_id)])

        if parent_run_id is None:
            # print("END OF THE ENTIRE CHAIN")
            print("FINAL EVENT ARRAY: ", self.event_array)
            self.log_object = {"data": self.event_array}
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
        print("on_tool_start: ")
        # print(f"on_tool_start: run_id: {run_id}")
        # print(f"on_tool_start: parent_run_id: {parent_run_id}")
        request_payload = self.on_tool_start_transformer(serialized, input_str, inputs)
        info_obj = self.start_event_information(
            run_id,
            parent_run_id,
            "tool_start",
            self.global_trace_id,
            request_payload,
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
        # print("on_tool_end: ")
        # print(f"on_tool_end: run_id: {run_id}")
        # print(f"on_tool_end: parent_run_id: {parent_run_id}")
        response_payload = self.on_tool_end_transformer(output)
        self.event_map["tool_start_" + str(run_id)]["response"] = response_payload
        self.event_array.append(self.event_map["tool_start_" + str(run_id)])
        pass

    def on_text(  # Do we need to log this or not? This is just formatting of the text
        self,
        text: str,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> None:
        """Run on arbitrary text."""
        # print("on_text: ")
        # print(f"on_text: run_id: {run_id}")
        # print(f"on_text: parent_run_id: {parent_run_id}")

        parent_span_id = (
            self.main_span_id if parent_run_id is None else str(parent_run_id)
        )
        request_payload = self.on_text_transformer(text)
        info_obj = self.start_event_information(
            run_id, parent_span_id, "text", self.global_trace_id, request_payload
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
        # print("on_agent_action: ")
        # print(f"on_agent_action: run_id: {run_id}")
        # print(f"on_agent_action: parent_run_id: {parent_run_id}")

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
        # print("on_agent_finish: ")
        # print(f"on_agent_finish: run_id: {run_id}")
        # print(f"on_agent_finish: parent_run_id: {parent_run_id}")

        (self.main_span_id if parent_run_id is None else str(parent_run_id))
        response_payload = self.on_agent_finish_transformer(finish)
        self.event_map["agent_action_" + str(run_id)]["response"] = response_payload
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
        # print("on_retriever_start: ")
        # print(f"on_retriever_start: run_id: {run_id}")
        # print(f"on_retriever_start: parent_run_id: {parent_run_id}")
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
        # print("on_retriever_end: ")
        # print(f"on_retriever_end: run_id: {run_id}")
        # print(f"on_retriever_end: parent_run_id: {parent_run_id}")
        pass

    '''

    # def on_llm_new_token(
    #     self,
    #     token: str,
    #     *,
    #     chunk: Optional[Union[Any, Any]] = None,
    #     run_id: UUID,
    #     parent_run_id: Optional[UUID] = None,
    #     tags: Optional[List[str]] = None,
    #     **kwargs: Any,
    # ) -> None:
    #     """Run on new LLM token. Only available when streaming is enabled."""
    #     print("on_llm_new_token: ")
    #     print(f"on_llm_new_token: run_id: {run_id}")
    #     print(f"on_llm_new_token: parent_run_id: {parent_run_id}")
    #     pass

    # def on_retriever_error(
    #     self,
    #     error: BaseException,
    #     *,
    #     run_id: UUID,
    #     parent_run_id: Optional[UUID] = None,
    #     tags: Optional[List[str]] = None,
    #     **kwargs: Any,
    # ) -> None:
    #     """Run on retriever error."""
    #     print("on_retriever_error: ")
    #     print(f"on_retriever_error: run_id: {run_id}")
    #     print(f"on_retriever_error: parent_run_id: {parent_run_id}")
    #     pass

    # def on_llm_error(
    #     self,
    #     error: BaseException,
    #     *,
    #     run_id: UUID,
    #     parent_run_id: Optional[UUID] = None,
    #     tags: Optional[List[str]] = None,
    #     **kwargs: Any,
    # ) -> None:
    #     """Run when LLM errors.

    #     Args:
    #         error: The error that occurred.
    #         kwargs (Any): Additional keyword arguments.
    #             - response (Any): The response which was generated before
    #                 the error occurred.
    #     """
    #     print("on_llm_error: ")
    #     print(f"on_llm_error: run_id: {run_id}")
    #     print(f"on_llm_error: parent_run_id: {parent_run_id}")
    #     pass

    # def on_retry(
    #     self,
    #     retry_state: Any,
    #     *,
    #     run_id: UUID,
    #     parent_run_id: Optional[UUID] = None,
    #     **kwargs: Any,
    # ) -> Any:
    #     """Run on a retry event."""
    #     print("on_retry: ")
    #     # print(f"on_retry: run_id: {run_id}")
    #     # print(f"on_retry: parent_run_id: {parent_run_id}")
    #     pass

    # def on_tool_error(
    #     self,
    #     error: BaseException,
    #     *,
    #     run_id: UUID,
    #     parent_run_id: Optional[UUID] = None,
    #     tags: Optional[List[str]] = None,
    #     **kwargs: Any,
    # ) -> None:
    #     """Run when tool errors."""
    #     print("on_tool_error: ")
    #     print(f"on_tool_error: run_id: {run_id}")
    #     print(f"on_tool_error: parent_run_id: {parent_run_id}")
    #     pass

    # def on_chain_error(
    #     self,
    #     error: BaseException,
    #     *,
    #     run_id: UUID,
    #     parent_run_id: Optional[UUID] = None,
    #     tags: Optional[List[str]] = None,
    #     **kwargs: Any,
    # ) -> None:
    #     """Run when chain errors."""
    #     print("on_chain_error: ")
    #     print(f"on_chain_error: run_id: {run_id}")
    #     print(f"on_chain_error: parent_run_id: {parent_run_id}")
    #     pass

    '''

    #  -------------- Helpers ------------------------------------------
    def start_event_information(
        self, span_id, parent_span_id, span_name, trace_id, request_payload
    ):
        return {
            "span_id": str(span_id),
            "parent_span_id": str(parent_span_id),
            "span_name": span_name,
            "trace_id": trace_id,
            "request": request_payload,
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

    #  ----------------------------------------------------------------------------

    # ------ Event Transformers ------

    def on_llm_start_transformer(self, serialized, prompts, kwargs):
        # print("on_llm_start_transformer: serialized: ", serialized)
        # print("on_llm_start_transformer: prompts: ", prompts)
        # print("on_llm_start_transformer: kwargs: ", kwargs)

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

            # print("RESPONSE MESSAGES: ", result["messages"])

            # startTimestamp = float(datetime.now().timestamp())

            # streamingMode = kwargs.get("invocation_params", False).get("stream", False)

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
        except Exception as e:
            print("on_llm_start_transformer: Error: ", e)
            return {
                "serialized": serialized,
                "prompts": prompts,
                "invocation_params": kwargs,
            }

    def on_llm_end_transformer(self, response, kwargs):
        try:
            response_obj = {}
            # self.endTimestamp = float(datetime.now().timestamp())
            # responseTime = self.endTimestamp - self.startTimestamp
            usage = (response.llm_output or {}).get("token_usage", "")  # type: ignore[union-attr]

            # self.response["status"] = (
            #     200 if self.responseStatus == 0 else self.responseStatus
            # )

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
            # response["time"] = int(responseTime * 1000)
            response_obj["headers"] = {}
            # response["streamingMode"] = streamingMode
            return response_obj
        except Exception as e:
            print("on_llm_end_transformer: Error: ", e)
            return {"response": response, "kwargs": kwargs}

    def on_chain_start_transformer(self, serialized, input, kwargs):
        try:
            # print("on_chain_start_transformer: serialized: ", serialized)
            # print("on_chain_start_transformer: input: ", input)
            # print("on_chain_start_transformer: kwargs: ", kwargs)
            name = kwargs["name"]
            return {
                "name": name,
                "input": json.dumps(input),
            }
        except Exception as e:
            print("Error in on_chain_start_transformer:", str(e))
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

        except Exception as e:
            print("Error in on_chain_end_transformer:", str(e))
            return {"output": output}

    def on_text_transformer(self, text):
        try:
            # print("on_text_transformer: text: ", text)
            return {"text": text}
        except Exception as e:
            print("Error in on_text_transformer:", str(e))
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
        except Exception as e:
            print("Error in on_chat_model_start_transformer:", str(e))
            return {"serialized": serialized, "messages": message_obj, "kwargs": kwargs}

    def on_agent_action_transformer(self, action):
        try:
            action = self.serialize(action)
            tool = action["tool"]
            tool_input = action["tool_input"]
            log = action["log"]
            return {"tool": tool, "tool_input": tool_input, "log": log}
        except Exception as e:
            print("Error in on_agent_action_transformer:", str(e))
            return {"action": action}

    def on_agent_finish_transformer(self, finish):
        try:
            # print("on_agent_finish_transformer: finish: ", finish)
            finish = self.serialize(finish)
            return_values = finish["return_values"]
            log = finish["log"]
            return {"return_values": return_values, "log": log}
        except Exception as e:
            print("Error in on_agent_finish_transformer:", str(e))
            return {"finish": finish}

    def on_tool_start_transformer(self, serialized, input_str, inputs):
        try:
            return {"serialized": serialized, "input_str": input_str, "inputs": inputs}
        except Exception as e:
            print("Error in on_tool_start_transformer: ", str(e))
            return {"serialized": serialized, "input_str": input_str, "inputs": inputs}

    def on_tool_end_transformer(self, output):
        try:
            return {"output": output}
        except Exception as e:
            print("Error in on_tool_end_transformer: ", str(e))
            return {"output": output}


# flake8: noqa: E501
'''

    # def on_llm_start(
    #     self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    # ) -> None:
    #     print("on_llm_start: ")
    #     # for prompt in prompts:
    #     #     messages = prompt.split("\n")
    #     #     for message in messages:
    #     #         role, content = message.split(":", 1)
    #     #         self.prompt_records.append(
    #     #             {"role": role.lower(), "content": content.strip()}
    #     #         )

    #     # self.startTimestamp = float(datetime.now().timestamp())

    #     # self.streamingMode = kwargs.get("invocation_params", False).get("stream", False) # noqa: E501

    #     # self.request["method"] = "POST"
    #     # self.request["url"] = serialized.get("kwargs", "").get(
    #     #     "base_url", "chat/completions"
    #     # )
    #     # self.request["provider"] = serialized["id"][2]
    #     # self.request["headers"] = serialized.get("kwargs", {}).get(
    #     #     "default_headers", {}
    #     # )
    #     # self.request["headers"].update({"provider": serialized["id"][2]})
    #     # self.request["body"] = {"messages": self.prompt_records}
    #     # self.request["body"].update({**kwargs.get("invocation_params", {})})
    #     pass

    # def on_chain_start(
    #     self,
    #     serialized: Dict[str, Any],
    #     inputs: Dict[str, Any],
    #     **kwargs: Any,
    # ) -> None:
    #     """Run when chain starts running."""
    #     pass

    # def on_llm_end(self, response: Any, **kwargs: Any) -> None:
    #     # self.endTimestamp = float(datetime.now().timestamp())
    #     # responseTime = self.endTimestamp - self.startTimestamp

    #     # usage = (response.llm_output or {}).get("token_usage", "")  # type: ignore[union-attr] # noqa: E501

    #     # self.response["status"] = (
    #     #     200 if self.responseStatus == 0 else self.responseStatus
    #     # )
    #     # self.response["body"] = {
    #     #     "choices": [
    #     #         {
    #     #             "index": 0,
    #     #             "message": {
    #     #                 "role": "assistant",
    #     #                 "content": response.generations[0][0].text,
    #     #             },
    #     #             "logprobs": response.generations[0][0].generation_info.get("logprobs", ""),  # type: ignore[union-attr] # noqa: E501
    #     #             "finish_reason": response.generations[0][0].generation_info.get("finish_reason", ""),  # type: ignore[union-attr] # noqa: E501
    #     #         }
    #     #     ]
    #     # }
    #     # self.response["body"].update({"usage": usage})
    #     # self.response["body"].update({"id": str(kwargs.get("run_id", ""))})
    #     # self.response["body"].update({"created": int(time.time())})
    #     # self.response["body"].update({"model": (response.llm_output or {}).get("model_name", "")})  # type: ignore[union-attr] # noqa: E501
    #     # self.response["body"].update({"system_fingerprint": (response.llm_output or {}).get("system_fingerprint", "")})  # type: ignore[union-attr] # noqa: E501
    #     # self.response["time"] = int(responseTime * 1000)
    #     # self.response["headers"] = {}
    #     # self.response["streamingMode"] = self.streamingMode

    #     # self.log_object.update(
    #     #     {
    #     #         "request": self.request,
    #     #         "response": self.response,
    #     #     }
    #     # )

    #     # self.portkey_logger.log(log_object=self.log_object)
    #     pass

    # def on_chain_end(
    #     self,
    #     outputs: Dict[str, Any],
    #     **kwargs: Any,
    # ) -> None:
    #     """Run when chain ends running."""
    #     pass

    # def on_chain_error(self, error: BaseException, **kwargs: Any) -> None:
    #     # self.responseBody = error
    #     # self.responseStatus = error.status_code  # type: ignore[attr-defined]
    #     """Do nothing."""
    #     pass

    # def on_llm_error(self, error: BaseException, **kwargs: Any) -> None:
    #     # self.responseBody = error
    #     # self.responseStatus = error.status_code  # type: ignore[attr-defined]
    #     """Do nothing."""
    #     pass

    # def on_tool_error(self, error: BaseException, **kwargs: Any) -> None:
    #     # self.responseBody = error
    #     # self.responseStatus = error.status_code  # type: ignore[attr-defined]
    #     pass

    # def on_text(self, text: str, **kwargs: Any) -> None:
    #     pass

    # def on_agent_finish(self, finish: Any, **kwargs: Any) -> None:
    #     pass

    # def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
    #     # self.streamingMode = True
    #     """Do nothing."""
    #     pass

    # def on_tool_start(
    #     self,
    #     serialized: Dict[str, Any],
    #     input_str: str,
    #     **kwargs: Any,
    # ) -> None:
    #     pass

    # def on_agent_action(self, action: Any, **kwargs: Any) -> Any:
    #     """Do nothing."""
    #     pass

    # def on_tool_end(
    #     self,
    #     output: Any,
    #     observation_prefix: Optional[str] = None,
    #     llm_prefix: Optional[str] = None,
    #     **kwargs: Any,
    # ) -> None:
    #     pass

'''
