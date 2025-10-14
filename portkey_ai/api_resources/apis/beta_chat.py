from typing import Any, Dict, List, Union
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.client import AsyncPortkey, Portkey
from portkey_ai.api_resources.types.beta_chat_type import ParsedChatCompletion
from ..._vendor.openai._types import Omit, omit


class BetaChat(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.completions = BetaCompletions(client)


class BetaCompletions(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    def parse(
        self,
        *,
        messages: Any,
        model: Union[str, Any] = "portkey-default",
        response_format: Union[Any, Omit] = omit,
        tools: Union[Any, Omit] = omit,
        audio: Union[Any, Omit] = omit,
        max_completion_tokens: Union[int, Omit] = omit,
        metadata: Union[Dict[str, str], Omit] = omit,
        modalities: Union[List[Any], Omit] = omit,
        prediction: Union[Any, Omit] = omit,
        reasoning_effort: Union[Any, Omit] = omit,
        store: Union[bool, Omit] = omit,
        **kwargs: Any,
    ) -> ParsedChatCompletion:
        response = self.openai_client.beta.chat.completions.parse(
            messages=messages,
            model=model,
            response_format=response_format,
            tools=tools,
            audio=audio,
            max_completion_tokens=max_completion_tokens,
            metadata=metadata,
            modalities=modalities,
            prediction=prediction,
            reasoning_effort=reasoning_effort,
            store=store,
            extra_body=kwargs,
        )
        return response  # type: ignore [return-value]

    def stream(
        self,
        *,
        messages: Any,
        model: Union[str, Any] = "portkey-default",
        response_format: Union[Any, Omit] = omit,
        tools: Union[Any, Omit] = omit,
        audio: Union[Any, Omit] = omit,
        max_completion_tokens: Union[int, Omit] = omit,
        metadata: Union[Dict[str, str], Omit] = omit,
        modalities: Union[List[Any], Omit] = omit,
        prediction: Union[Any, Omit] = omit,
        reasoning_effort: Union[Any, Omit] = omit,
        store: Union[bool, Omit] = omit,
        **kwargs: Any,
    ) -> Any:
        with self.openai_client.beta.chat.completions.stream(
            messages=messages,
            model=model,
            response_format=response_format,
            tools=tools,
            audio=audio,
            max_completion_tokens=max_completion_tokens,
            metadata=metadata,
            modalities=modalities,
            prediction=prediction,
            reasoning_effort=reasoning_effort,
            store=store,
            extra_body=kwargs,
        ) as stream:
            for event in stream:
                if event.type == "content.delta":
                    continue
                elif event.type == "content.done":
                    break
                elif event.type == "chunk":
                    json_data = event.model_dump_json()
                    yield json_data
                else:
                    return ""


class AsyncBetaChat(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.completions = AsyncBetaCompletions(client)


class AsyncBetaCompletions(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    async def parse(
        self,
        *,
        messages: Any,
        model: Union[str, Any] = "portkey-default",
        response_format: Union[Any, Omit] = omit,
        tools: Union[Any, Omit] = omit,
        audio: Union[Any, Omit] = omit,
        max_completion_tokens: Union[int, Omit] = omit,
        metadata: Union[Dict[str, str], Omit] = omit,
        modalities: Union[List[Any], Omit] = omit,
        prediction: Union[Any, Omit] = omit,
        reasoning_effort: Union[Any, Omit] = omit,
        store: Union[bool, Omit] = omit,
        **kwargs: Any,
    ) -> ParsedChatCompletion:
        response = await self.openai_client.beta.chat.completions.parse(
            messages=messages,
            model=model,
            response_format=response_format,
            tools=tools,
            audio=audio,
            max_completion_tokens=max_completion_tokens,
            metadata=metadata,
            modalities=modalities,
            prediction=prediction,
            reasoning_effort=reasoning_effort,
            store=store,
            extra_body=kwargs,
        )
        return response  # type: ignore [return-value]

    async def stream(
        self,
        *,
        messages: Any,
        model: Union[str, Any] = "portkey-default",
        response_format: Union[Any, Omit] = omit,
        tools: Union[Any, Omit] = omit,
        audio: Union[Any, Omit] = omit,
        max_completion_tokens: Union[int, Omit] = omit,
        metadata: Union[Dict[str, str], Omit] = omit,
        modalities: Union[List[Any], Omit] = omit,
        prediction: Union[Any, Omit] = omit,
        reasoning_effort: Union[Any, Omit] = omit,
        store: Union[bool, Omit] = omit,
        **kwargs: Any,
    ) -> Any:
        async with self.openai_client.beta.chat.completions.stream(
            messages=messages,
            model=model,
            response_format=response_format,
            tools=tools,
            audio=audio,
            max_completion_tokens=max_completion_tokens,
            metadata=metadata,
            modalities=modalities,
            prediction=prediction,
            reasoning_effort=reasoning_effort,
            store=store,
            extra_body=kwargs,
        ) as stream:
            async for event in stream:
                if event.type == "content.delta":
                    continue
                elif event.type == "content.done":
                    break
                elif event.type == "chunk":
                    json_data = event.model_dump_json()
                    yield json_data
                else:
                    pass
