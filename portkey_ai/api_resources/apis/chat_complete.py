from __future__ import annotations

import json
from typing import Mapping, Optional, Union, overload, Literal, List
from portkey_ai.api_resources.base_client import APIClient, AsyncAPIClient
from portkey_ai.api_resources.client import AsyncPortkey, Portkey
from portkey_ai.api_resources.utils import (
    PortkeyApiPaths,
    Message,
    ChatCompletionChunk,
    ChatCompletions,
)

from portkey_ai.api_resources.streaming import AsyncStream, Stream
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource


__all__ = ["ChatCompletion", "AsyncChatCompletion"]


class ChatCompletion(APIResource):
    completions: Completions

    def __init__(self, client: APIClient) -> None:
        super().__init__(client)
        self.completions = Completions(client)


class AsyncChatCompletion(AsyncAPIResource):
    completions: AsyncCompletions

    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)
        self.completions = AsyncCompletions(client)


class Completions(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    @overload
    def create(
        self,
        *,
        messages: Optional[List[Message]] = None,
        config: Optional[Union[Mapping, str]] = None,
        stream: Literal[True],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        **kwargs,
    ) -> Stream[ChatCompletionChunk]:
        ...

    @overload
    def create(
        self,
        *,
        messages: Optional[List[Message]] = None,
        config: Optional[Union[Mapping, str]] = None,
        stream: Literal[False] = False,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        **kwargs,
    ) -> ChatCompletions:
        ...

    @overload
    def create(
        self,
        *,
        messages: Optional[List[Message]] = None,
        config: Optional[Union[Mapping, str]] = None,
        stream: bool = False,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        **kwargs,
    ) -> Union[ChatCompletions, Stream[ChatCompletionChunk]]:
        ...

    def create(
        self,
        **kwargs,
    ) -> Union[ChatCompletions, Stream[ChatCompletionChunk]]:

        if 'stream' in kwargs and kwargs['stream'] == True:
            final_responses = []
            response = self.openai_client.chat.completions.create(**kwargs)
            for chunk in response:
                finalResponse = {}
                finalResponse['id'] = chunk.id
                finalResponse['object'] = chunk.object
                finalResponse['created'] = chunk.created
                finalResponse['model'] = chunk.model
                finalResponse['choices'] = [{'index': chunk.choices[0].index,
                                             'delta': {
                                                 'role': chunk.choices[0].delta.role,
                                                 'content': chunk.choices[0].delta.content,
                                                 'tool_calls': chunk.choices[0].delta.tool_calls
                },
                    'logprobs': chunk.choices[0].logprobs,
                    'finish_reason': chunk.choices[0].finish_reason}]
                finalResponse['system_fingerprint'] = chunk.system_fingerprint
                final_responses.append(finalResponse)
            return final_responses
        elif 'stream' in kwargs and kwargs['stream'] == False:
            response = self.openai_client.with_raw_response.chat.completions.create(
                **kwargs)
            response = response.text
            return json.loads(response)
        else:
            response = self.openai_client.with_raw_response.chat.completions.create(
                **kwargs)
            response = response.text
            return json.loads(response)


    def _get_config_string(self, config: Union[Mapping, str]) -> str:
        return config if isinstance(config, str) else json.dumps(config)


class AsyncCompletions(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    @overload
    async def create(
        self,
        *,
        messages: Optional[List[Message]] = None,
        config: Optional[Union[Mapping, str]] = None,
        stream: Literal[True],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        **kwargs,
    ) -> AsyncStream[ChatCompletionChunk]:
        ...

    @overload
    async def create(
        self,
        *,
        messages: Optional[List[Message]] = None,
        config: Optional[Union[Mapping, str]] = None,
        stream: Literal[False] = False,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        **kwargs,
    ) -> ChatCompletions:
        ...

    @overload
    async def create(
        self,
        *,
        messages: Optional[List[Message]] = None,
        config: Optional[Union[Mapping, str]] = None,
        stream: bool = False,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        **kwargs,
    ) -> Union[ChatCompletions, AsyncStream[ChatCompletionChunk]]:
        ...

    async def create(
        self,
        **kwargs,
    ) -> Union[ChatCompletions, AsyncStream[ChatCompletionChunk]]:
        
        if 'stream' in kwargs and kwargs['stream'] == True:
            final_responses = []
            response = await self.openai_client.chat.completions.create(**kwargs)
            async for chunk in response:
                finalResponse = {}
                finalResponse['id'] = chunk.id
                finalResponse['object'] = chunk.object
                finalResponse['created'] = chunk.created
                finalResponse['model'] = chunk.model
                finalResponse['choices'] = [{'index': chunk.choices[0].index,
                                             'delta': {
                                                 'role': chunk.choices[0].delta.role,
                                                 'content': chunk.choices[0].delta.content,
                                                 'tool_calls': chunk.choices[0].delta.tool_calls
                },
                    'logprobs': chunk.choices[0].logprobs,
                    'finish_reason': chunk.choices[0].finish_reason}]
                finalResponse['system_fingerprint'] = chunk.system_fingerprint
                final_responses.append(finalResponse)
            return final_responses
        elif 'stream' in kwargs and kwargs['stream'] == False:
            response = await self.openai_client.with_raw_response.chat.completions.create(
                **kwargs)
            response = response.text
            return json.loads(response)
        else:
            response = await self.openai_client.with_raw_response.chat.completions.create(
                **kwargs)
            response = response.text
            return json.loads(response)

    def _get_config_string(self, config: Union[Mapping, str]) -> str:
        return config if isinstance(config, str) else json.dumps(config)
