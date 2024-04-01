from datetime import datetime
from typing import Any, Dict, List, Optional
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult
from langchain_core.agents import AgentFinish, AgentAction

from portkey_ai.api_resources.apis.logger import Logger


class PortkeyCallbackHandler(BaseCallbackHandler):
    startTimestamp: int = 0
    endTimestamp: int = 0

    def __init__(
        self,
        api_key: str,
    ) -> None:
        super().__init__()

        self.api_key = api_key

        self.portkey_logger = Logger(api_key=api_key)

        # ------------------------------------------------
        self.log_object: Dict[str, Any] = {}
        self.prompt_records: List[str] = []
        self.usage_records: Any = {}
        self.prompt_tokens: int = 0
        self.completion_tokens: int = 0
        self.total_tokens: int = 0
        # ------------------------------------------------

        # ------------------------------------------------
        self.requestMethod: str = "POST"
        self.requestURL: str = ""
        self.requestHeaders: Dict[str, Any] = {}
        self.requestBody: Any = {}

        self.responseHeaders: Dict[str, Any] = {}  # Nowhere to get this from
        self.responseBody: Any = None
        self.responseStatus: int = 0
        self.responseTime: int = 0

        self.streamingMode: bool = False

        # ------------------------------------------------
        # self.config: Dict[str, Any] = {}
        # self.organisationConfig: Dict[str, Any] = {}
        # self.organisationDetails: Dict[str, Any] = {}
        # self.cacheStatus: str = None
        # self.retryCount: int = 0
        # self.portkeyHeaders: Dict[str, Any] = {}
        # ------------------------------------------------

        if not api_key:
            raise ValueError("Please provide an API key to use PortkeyCallbackHandler")

    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        print("on_llm_start serialized", serialized["id"][2])
        print("on_llm_start prompts", prompts)
        print("on_llm_start kwargs", kwargs)

        self.startTimestamp = int(datetime.now().timestamp())

        for prompt in prompts:
            self.prompt_records.append(prompt.replace("\n", " "))

        self.requestURL = serialized.get("kwargs", "").get("base_url", "")
        self.requestHeaders = serialized.get("kwargs", {}).get("default_headers", {})
        self.requestHeaders.update({"provider": serialized["id"][2]})

        self.requestBody = kwargs
        self.requestBody["prompts"] = self.prompt_records

        print("on_llm_start requestBody:", self.requestBody)

        self.streamingMode = kwargs.get("invocation_params", False).get("stream", False)

    def on_chain_start(
        self,
        serialized: Dict[str, Any],
        inputs: Dict[str, Any],
        **kwargs: Any,
    ) -> None:
        """Run when chain starts running."""
        self.requestBody = {**inputs, **kwargs}
        self.requestHeaders = (
            serialized.get("kwargs", {})
            .get("llm", {})
            .get("kwargs", {})
            .get("default_headers", {})
        )
        self.requestURL = (
            serialized.get("kwargs", "")
            .get("llm", "")
            .get("kwargs", "")
            .get("base_url", "")
        )

        self.startTimestamp = int(datetime.now().timestamp())
        print("on_chain_start inputs", inputs)
        print("on_chain_start kwargs", kwargs)
        print("on_chain_start serialized", serialized)

    # --------------------------------------------------------------------------------

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        print("on_llm_end response", response.generations)
        print("on_llm_end kwargs", kwargs)
        self.responseBody = response
        self.responseStatus = 200
        self.endTimestamp = int(datetime.now().timestamp())
        self.responseTime = self.endTimestamp - self.startTimestamp

        """This will handle all the token usage information from the LLM."""
        if response.llm_output and "token_usage" in response.llm_output:
            usage = response.llm_output["token_usage"]
            self.completion_tokens = usage.get("completion_tokens", 0)
            self.prompt_tokens = usage.get("prompt_tokens", 0)
            self.total_tokens = usage.get(
                "total_tokens", self.completion_tokens + self.prompt_tokens
            )
            self.usage_records["usage"] = usage
        """This will handle all the token usage information from the LLM."""

        self.log_object.update(
            {
                "requestMethod": self.requestMethod,
                "requestURL": self.requestURL,
                "requestHeaders": self.requestHeaders,
                "requestBody": self.requestBody,
                "responseHeaders": self.responseHeaders,
                "responseBody": self.responseBody,
                "responseStatus": self.responseStatus,
                "responseTime": self.responseTime,
                "streamingMode": self.streamingMode,
            }
        )

        print("on_llm_end log_object", {**self.log_object})

        self.portkey_logger.log(log_object=self.log_object)

    def on_chain_end(
        self,
        outputs: Dict[str, Any],
        **kwargs: Any,
    ) -> None:
        """Run when chain ends running."""
        print("on_chain_end outputs", outputs)
        self.responseBody = outputs
        self.responseStatus = 200
        self.endTimestamp = int(datetime.now().timestamp())
        self.responseTime = self.endTimestamp - self.startTimestamp

    # --------------------------------------------------------------------------------

    def on_chain_error(self, error: BaseException, **kwargs: Any) -> None:
        self.responseBody = error
        self.responseStatus = error.status_code  # type: ignore[attr-defined]
        print("on_chain_error error", error)
        print("on_chain_error kwargs", kwargs)
        """Do nothing."""
        pass

    def on_llm_error(self, error: BaseException, **kwargs: Any) -> None:
        self.responseBody = error
        self.responseStatus = error.status_code  # type: ignore[attr-defined]
        print("on_llm_error error", error)
        print("on_llm_error kwargs", kwargs)
        """Do nothing."""
        pass

    def on_tool_error(self, error: BaseException, **kwargs: Any) -> None:
        self.responseBody = error
        self.responseStatus = error.status_code  # type: ignore[attr-defined]
        pass

    # --------------------------------------------------------------------------------

    def on_text(self, text: str, **kwargs: Any) -> None:
        pass

    def on_agent_finish(self, finish: AgentFinish, **kwargs: Any) -> None:
        pass

    # --------------------------------------------------------------------------------

    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        self.streamingMode = True
        print("on_llm_new_token token", token)
        print("on_llm_new_token kwargs", kwargs)
        """Do nothing."""
        pass

    # --------------------------------------------------------------------------------

    def on_tool_start(
        self,
        serialized: Dict[str, Any],
        input_str: str,
        **kwargs: Any,
    ) -> None:
        print("on_tool_start input_str", input_str)
        print("on_tool_start serialized", serialized)
        print("on_tool_start kwargs", kwargs)

        pass

    def on_agent_action(self, action: AgentAction, **kwargs: Any) -> Any:
        print("on_agent_action action", action)
        print("on_agent_action kwargs", kwargs)
        """Do nothing."""
        pass

    def on_tool_end(
        self,
        output: Any,
        observation_prefix: Optional[str] = None,
        llm_prefix: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        print("on_tool_end output", output)
        print("on_tool_end observation_prefix", observation_prefix)
        print("on_tool_end llm_prefix", llm_prefix)
        print("on_tool_end kwargs", kwargs)
        pass


"""
winkychLogObject = {
            requestMethod: store.requestMethod,
            requestURL: store.proxyUrl,
            requestHeaders: store.requestHeadersWithoutPortkeyHeaders,
            requestBody: store.requestBody,

            responseHeaders: Object.fromEntries(store.response.headers),
            responseBody: {},
            responseStatus: store.responseStatus,
            responseTime: store.config.responseTime,
            config: {
                organisationConfig: { id: store.requestHeaders[globals.PORTKEY_CONFIG_HEADER], ...store.organisationConfig},
                organisationDetails: store.organisationDetails,
                cacheStatus: store.config.cacheStatus,
                retryCount: store.retryCount,
                isStreamingMode: store.streamingMode,
                portkeyHeaders: store.requestHeadersPortkey
            }
        }
"""
