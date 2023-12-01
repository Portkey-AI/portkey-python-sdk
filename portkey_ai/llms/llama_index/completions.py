from portkey_ai import Message, Portkey
from typing import TYPE_CHECKING, Optional, Union, List, Any, Mapping, cast, Sequence
from portkey_ai.api_resources.utils import PortkeyResponse

from portkey_ai.llms.llama_index.utils import (
    IMPORT_ERROR_MESSAGE,
    is_chat_model,
    modelname_to_contextsize,
)

if TYPE_CHECKING:
    from llama_index.llms.base import (
        ChatMessage,
        ChatResponse,
        ChatResponseGen,
        CompletionResponse,
        CompletionResponseGen,
        LLMMetadata,
        llm_chat_callback,
        llm_completion_callback,
    )

try:
    from llama_index.llms.custom import CustomLLM
    from llama_index.bridge.pydantic import PrivateAttr
except ImportError as exc:
    raise ImportError(IMPORT_ERROR_MESSAGE) from exc


class PortkeyLLM(CustomLLM):
    """_summary_.

    Args:
        LLM (_type_): _description_
    """

    _client: Any = PrivateAttr()
    model: str = ""

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        virtual_key: Optional[str] = None,
        config: Optional[Union[Mapping, str]] = None,
    ) -> None:
        """
        Initialize a Portkey instance.

        Args:
            api_key (Optional[str]): The API key to authenticate with Portkey.
            base_url (Optional[str]): The Base url to the self hosted rubeus \
                (the opensource version of portkey) or any other self hosted server.
        """
        super().__init__(
            base_url=base_url,
            api_key=api_key,
        )
        self._client = Portkey(
            api_key=api_key, base_url=base_url, virtual_key=virtual_key, config=config
        )
        self.model = ""

    @property
    def metadata(self) -> LLMMetadata:
        """LLM metadata."""
        try:
            from llama_index.llms.base import (
                LLMMetadata,
            )
        except ImportError as exc:
            raise ImportError(IMPORT_ERROR_MESSAGE) from exc
        return LLMMetadata(
            _context_window=modelname_to_contextsize(self.model),
            is_chat_model=is_chat_model(self.model),
            model_name=self.model,
        )

    @llm_completion_callback()
    def complete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        """Completion endpoint for LLM."""
        complete_fn = self._complete
        return complete_fn(prompt, **kwargs)

    @llm_chat_callback()
    def chat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        chat_fn = self._chat
        return chat_fn(messages, **kwargs)

    @llm_completion_callback()
    def stream_complete(self, prompt: str, **kwargs: Any) -> CompletionResponseGen:
        """Completion endpoint for LLM."""
        complete_fn = self._stream_complete
        return complete_fn(prompt, **kwargs)

    @llm_chat_callback()
    def stream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        stream_chat_fn = self._stream_chat
        return stream_chat_fn(messages, **kwargs)

    def _chat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        _messages = cast(
            List[Message],
            [{"role": i.role.value, "content": i.content} for i in messages],
        )
        response = self._client.chat.completions.create(messages=_messages, **kwargs)
        self.model = self._get_model(response)

        message = response.choices[0].message
        return ChatResponse(message=message, raw=response)

    def _complete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        response = self._client.completions.create(prompt=prompt, **kwargs)
        text = response.choices[0].text
        return CompletionResponse(text=text, raw=response)

    def _stream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        _messages = cast(
            List[Message],
            [{"role": i.role.value, "content": i.content} for i in messages],
        )
        response = self._client.chat.completions.create(
            messages=_messages, stream=True, **kwargs
        )

        def gen() -> ChatResponseGen:
            content = ""
            function_call: Optional[dict] = {}
            for resp in response:
                if resp.choices is None:
                    continue
                delta = resp.choices[0].delta
                role = delta.get("role", "assistant")
                content_delta = delta.get("content", "") or ""
                content += content_delta

                function_call_delta = delta.get("function_call", None)
                if function_call_delta is not None:
                    if function_call is None:
                        function_call = function_call_delta
                        # ensure we do not add a blank function call
                        if (
                            function_call
                            and function_call.get("function_name", "") is None
                        ):
                            del function_call["function_name"]
                    else:
                        function_call["arguments"] += function_call_delta["arguments"]

                additional_kwargs = {}
                if function_call is not None:
                    additional_kwargs["function_call"] = function_call

                yield ChatResponse(
                    message=ChatMessage(
                        role=role,
                        content=content,
                        additional_kwargs=additional_kwargs,
                    ),
                    delta=content_delta,
                    raw=resp,
                )

        return gen()

    def _stream_complete(self, prompt: str, **kwargs: Any) -> CompletionResponseGen:
        response = self._client.completions.create(prompt=prompt, stream=True, **kwargs)

        def gen() -> CompletionResponseGen:
            text = ""
            for resp in response:
                delta = resp.choices[0].text or ""
                text += delta
                yield CompletionResponse(
                    delta=delta,
                    text=text,
                    raw=resp,
                )

        return gen()

    @property
    def _is_chat_model(self) -> bool:
        """Check if a given model is a chat-based language model.

        Returns:
            bool: True if the provided model is a chat-based language model,
            False otherwise.
        """
        return is_chat_model(self.model or "")

    def _get_model(self, response: PortkeyResponse) -> str:
        return response.model
