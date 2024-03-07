from __future__ import annotations

import json
from typing import (
    Any,
    AsyncIterator,
    Iterable,
    Iterator,
    Mapping,
    Optional,
    Union,
)
from portkey_ai.api_resources.client import AsyncPortkey, Portkey
from portkey_ai.api_resources.utils import (
    ChatCompletionChunk,
    ChatCompletions,
)

from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource


__all__ = ["ChatCompletion", "AsyncChatCompletion"]


class ChatCompletion(APIResource):
    completions: Completions

    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.completions = Completions(client)


class AsyncChatCompletion(AsyncAPIResource):
    completions: AsyncCompletions

    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.completions = AsyncCompletions(client)


class Completions(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    def stream_create(
        self, model, messages, **kwargs
    ) -> Union[ChatCompletions, Iterator[ChatCompletionChunk]]:
        with self.openai_client.with_streaming_response.chat.completions.create(
            model=model, messages=messages, **kwargs
        ) as response:
            for line in response.iter_lines():
                json_string = line.replace("data: ", "")
                json_string = json_string.strip().rstrip("\n")
                if json_string == "":
                    continue
                elif json_string == "[DONE]":
                    break
                elif json_string != "":
                    json_data = json.loads(json_string)
                    json_data = ChatCompletionChunk(**json_data)
                    yield json_data
                else:
                    return ""

    def normal_create(self, model, messages, **kwargs) -> ChatCompletions:
        response = self.openai_client.with_raw_response.chat.completions.create(
            model=model, messages=messages, **kwargs
        )
        json_response = json.loads(response.text)
        return ChatCompletions(**json_response)

    def create(
        self,
        *,
        model: Optional[str] = None,
        messages: Iterable[Any],
        **kwargs,
    ) -> ChatCompletions:
        if "stream" in kwargs and kwargs["stream"] is True:
            return self.stream_create(model=model, messages=messages, **kwargs)  # type: ignore
        elif "stream" in kwargs and kwargs["stream"] is False:
            return self.normal_create(model=model, messages=messages, **kwargs)
        else:
            return self.normal_create(model=model, messages=messages, **kwargs)


class AsyncCompletions(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    async def stream_create(
        self, model, messages, **kwargs
    ) -> Union[ChatCompletions, AsyncIterator[ChatCompletionChunk]]:  # type: ignore
        async with self.openai_client.with_streaming_response.chat.completions.create(
            model=model, messages=messages, **kwargs
        ) as response:
            async for line in response.iter_lines():
                json_string = line.replace("data: ", "")
                json_string = json_string.strip().rstrip("\n")
                if json_string == "":
                    continue
                elif json_string == "[DONE]":
                    break
                elif json_string != "":
                    json_data = json.loads(json_string)
                    json_data = ChatCompletionChunk(**json_data)
                    yield json_data
                else:
                    pass

    async def normal_create(self, model, messages, **kwargs) -> ChatCompletions:
        response = await self.openai_client.with_raw_response.chat.completions.create(
            model=model, messages=messages, **kwargs
        )
        json_response = json.loads(response.text)
        return ChatCompletions(**json_response)

    async def create(
        self,
        *,
        model: Optional[str] = None,
        messages: Iterable[Any],
        **kwargs,
    ) -> ChatCompletions:
        if "stream" in kwargs and kwargs["stream"] is True:
            return self.stream_create(model=model, messages=messages, **kwargs)  # type: ignore
        elif "stream" in kwargs and kwargs["stream"] is False:
            return await self.normal_create(model=model, messages=messages, **kwargs)
        else:
            return await self.normal_create(model=model, messages=messages, **kwargs)

    def _get_config_string(self, config: Union[Mapping, str]) -> str:
        return config if isinstance(config, str) else json.dumps(config)
