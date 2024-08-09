from typing import Any, Union
from portkey_ai._vendor.openai.lib._parsing._completions import ResponseFormatT
from portkey_ai._vendor.openai.lib.streaming.chat._completions import (
    ChatCompletionStreamManager,
)
from portkey_ai._vendor.openai.types.chat.parsed_chat_completion import (
    ParsedChatCompletion,
)
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.client import AsyncPortkey, Portkey
from ..._vendor.openai._types import NotGiven, NOT_GIVEN


class BetaChat(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.completion = BetaCompletion(client)


class BetaCompletion(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    def parse(
        self,
        *,
        messages: Any,
        model: Union[str, Any] = "portkey-default",
        response_format: Union[type[ResponseFormatT], NotGiven] = NOT_GIVEN,
        tools: Union[Any, NotGiven] = NOT_GIVEN,
        **kwargs: Any,
    ) -> ParsedChatCompletion[ResponseFormatT]:
        response = self.openai_client.beta.chat.completions.parse(
            messages=messages,
            model=model,
            response_format=response_format,
            tools=tools,
            extra_body=kwargs,
        )
        return response

    def stream(
        self,
        *,
        messages: Any,
        model: Union[str, Any] = "portkey-default",
        response_format: Union[type[ResponseFormatT], NotGiven] = NOT_GIVEN,
        tools: Union[Any, NotGiven] = NOT_GIVEN,
        **kwargs: Any,
    ) -> ChatCompletionStreamManager[ResponseFormatT]:
        response = self.openai_client.beta.chat.completions.stream(
            messages=messages,
            model=model,
            response_format=response_format,
            tools=tools,
            extra_body=kwargs,
        )

        return response


class AsyncBetaChat(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.completion = AsyncBetaCompletion(client)


class AsyncBetaCompletion(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    async def parse(
        self,
        *,
        messages: Any,
        model: Union[str, Any] = "portkey-default",
        response_format: Union[type[ResponseFormatT], NotGiven] = NOT_GIVEN,
        tools: Union[Any, NotGiven] = NOT_GIVEN,
        **kwargs: Any,
    ) -> ParsedChatCompletion[ResponseFormatT]:
        response = await self.openai_client.beta.chat.completions.parse(
            messages=messages,
            model=model,
            response_format=response_format,
            tools=tools,
            extra_body=kwargs,
        )
        return response

    async def stream(
        self,
        *,
        messages: Any,
        model: Union[str, Any] = "portkey-default",
        response_format: Union[type[ResponseFormatT], NotGiven] = NOT_GIVEN,
        tools: Union[Any, NotGiven] = NOT_GIVEN,
        **kwargs: Any,
    ) -> Any:
        response = self.openai_client.beta.chat.completions.stream(
            messages=messages,
            model=model,
            response_format=response_format,
            tools=tools,
            extra_body=kwargs,
        )

        return response
