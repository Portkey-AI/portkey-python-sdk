from __future__ import annotations

import json
from typing import (
    AsyncIterator,
    Iterator,
    Mapping,
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
        self, **kwargs
    ) -> Union[ChatCompletions, Iterator[ChatCompletionChunk]]:
        with self.openai_client.with_streaming_response.chat.completions.create(
            **kwargs
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

    def normal_create(self, **kwargs) -> ChatCompletions:
        response = self.openai_client.with_raw_response.chat.completions.create(
            **kwargs
        )
        json_response = json.loads(response.text)
        return ChatCompletions(**json_response)

    def create(
        self,
        **kwargs,
    ) -> ChatCompletions:
        if "stream" in kwargs and kwargs["stream"] is True:
            return self.stream_create(**kwargs)  # type: ignore
        elif "stream" in kwargs and kwargs["stream"] is False:
            return self.normal_create(**kwargs)
        else:
            return self.normal_create(**kwargs)

    # def create(
    #     self,
    #     **kwargs
    # ) -> Union[ChatCompletions, Iterator[ChatCompletionChunk]]:
    #     print("Res kw:", kwargs)
    #     if 'stream' in kwargs and kwargs['stream'] == True:
    #         with self.openai_client.with_streaming_response.chat.
    # completions.create(**kwargs) as response:
    #             for line in response.iter_lines():
    #                 json_string = line.replace('data: ', '')
    #                 json_string = json_string.strip().rstrip('\n')
    #                 if json_string == '':
    #                     continue
    #                 elif json_string == '[DONE]':
    #                     break
    #                 else:
    #                     json_data = json.loads(json_string)
    #                     json_data = ChatCompletionChunk(**json_data)
    #                     yield json_data
    #     elif 'stream' in kwargs and kwargs['stream'] == False:
    #         response = self.openai_client.with_raw_response.chat.completions.create(
    #             **kwargs)
    #         print("Res Stream:", response)
    #         response = response.text
    #         return json.loads(response)
    #     else:
    #         response = self.openai_client.with_raw_response.chat.completions.create(
    #             **kwargs)
    #         print("Res:", response)
    #         response = response.text
    #         response = json.loads(response)
    #         response = ChatCompletions(**response)
    #         return response

    # @overload
    # def create(
    #     self,
    #     *,
    #     messages: Optional[List[Message]] = None,
    #     config: Optional[Union[Mapping, str]] = None,
    #     stream: Literal[True],
    #     temperature: Optional[float] = None,
    #     max_tokens: Optional[int] = None,
    #     top_k: Optional[int] = None,
    #     top_p: Optional[float] = None,
    #     **kwargs,
    # ) -> Stream[ChatCompletionChunk]:
    #     ...

    # @overload
    # def create(
    #     self,
    #     *,
    #     messages: Optional[List[Message]] = None,
    #     config: Optional[Union[Mapping, str]] = None,
    #     stream: bool = False,
    #     temperature: Optional[float] = None,
    #     max_tokens: Optional[int] = None,
    #     top_k: Optional[int] = None,
    #     top_p: Optional[float] = None,
    #     **kwargs,
    # ) -> Union[ChatCompletions, Iterator[ChatCompletionChunk]]:
    #     ...

    # def create(
    #     self,
    #     **kwargs
    # ) -> Union[ChatCompletions, Stream[ChatCompletionChunk]]:

    #     print("Res kw:", kwargs)
    #     if 'stream' in kwargs and kwargs['stream'] == True:
    #         print("Res kwwww:", kwargs)
    #         with self.openai_client.with_streaming_response.
    # chat.completions.create(**kwargs) as response:
    #             for line in response.iter_lines():
    #                 json_string = line.replace('data: ', '')
    #                 json_string = json_string.strip().rstrip('\n')
    #                 if json_string == '':
    #                     continue
    #                 elif json_string == '[DONE]':
    #                     break
    #                 elif json_string!= '':
    #                     json_data = json.loads(json_string)
    #                     json_data = ChatCompletionChunk(**json_data)
    #                     yield json_data
    #                 else:
    #                     return ""

    #     if 'stream' in kwargs and kwargs['stream'] == False:
    #         response = self.openai_client.with_raw_response.chat.completions.create(
    #             **kwargs)
    #         print("REs Stream:", response.text)
    #         json_response = json.loads(response.text)
    #         return ChatCompletions(**json_response)
    #         response = response.text
    #         return json.loads(response)
    #     elif 'stream' not in kwargs:
    #         response = self.openai_client.with_raw_response.chat.completions.create(
    #             **kwargs)
    #         print("REssss:", response)
    #         json_response = json.loads(response.text)
    #         print("TYPE:", type(ChatCompletions(**json_response)))
    #         # response = response.text
    #         # return json.loads(response)
    #         return ChatCompletions(**json_response)
    #     else:
    #         return "Streaming not requested"

    # def _get_config_string(self, config: Union[Mapping, str]) -> str:
    #     return config if isinstance(config, str) else json.dumps(config)


class AsyncCompletions(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    async def stream_create(
        self, **kwargs
    ) -> Union[ChatCompletions, AsyncIterator[ChatCompletionChunk]]:  # type: ignore
        async with self.openai_client.with_streaming_response.chat.completions.create(
            **kwargs
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

    async def normal_create(self, **kwargs) -> ChatCompletions:
        response = await self.openai_client.with_raw_response.chat.completions.create(
            **kwargs
        )
        json_response = json.loads(response.text)
        return ChatCompletions(**json_response)

    async def create(
        self,
        **kwargs,
    ) -> ChatCompletions:
        if "stream" in kwargs and kwargs["stream"] is True:
            return self.stream_create(**kwargs)  # type: ignore
        elif "stream" in kwargs and kwargs["stream"] is False:
            return await self.normal_create(**kwargs)
        else:
            return await self.normal_create(**kwargs)

    # @overload
    # async def create(
    #     self,
    #     *,
    #     messages: Optional[List[Message]] = None,
    #     config: Optional[Union[Mapping, str]] = None,
    #     stream: Literal[True],
    #     temperature: Optional[float] = None,
    #     max_tokens: Optional[int] = None,
    #     top_k: Optional[int] = None,
    #     top_p: Optional[float] = None,
    #     **kwargs,
    # ) -> AsyncStream[ChatCompletionChunk]:
    #     ...

    # @overload
    # async def create(
    #     self,
    #     *,
    #     messages: Optional[List[Message]] = None,
    #     config: Optional[Union[Mapping, str]] = None,
    #     stream: Literal[False] = False,
    #     temperature: Optional[float] = None,
    #     max_tokens: Optional[int] = None,
    #     top_k: Optional[int] = None,
    #     top_p: Optional[float] = None,
    #     **kwargs,
    # ) -> ChatCompletions:
    #     ...

    # @overload
    # async def create(
    #     self,
    #     *,
    #     messages: Optional[List[Message]] = None,
    #     config: Optional[Union[Mapping, str]] = None,
    #     stream: bool = False,
    #     temperature: Optional[float] = None,
    #     max_tokens: Optional[int] = None,
    #     top_k: Optional[int] = None,
    #     top_p: Optional[float] = None,
    #     **kwargs,
    # ) -> Union[ChatCompletions, AsyncStream[ChatCompletionChunk]]:
    #     ...

    # async def create(
    #     self,
    #     **kwargs,
    # ) -> Union[ChatCompletions, AsyncStream[ChatCompletionChunk]]:

    #     if 'stream' in kwargs and kwargs['stream'] == True:
    #         final_responses = []
    #         response = await self.openai_client.chat.completions.create(**kwargs)
    #         async for chunk in response:
    #             finalResponse = {}
    #             finalResponse['id'] = chunk.id
    #             finalResponse['object'] = chunk.object
    #             finalResponse['created'] = chunk.created
    #             finalResponse['model'] = chunk.model
    #             finalResponse['choices'] =
    # [{'index': chunk.choices[0].index,
    #   'delta': {
    #       'role': chunk.choices[0].delta.role,
    #       'content': chunk.choices[0].delta.content,
    #       'tool_calls': chunk.choices[0].delta.tool_calls            },
    #                 'logprobs': chunk.choices[0].logprobs,
    #                 'finish_reason': chunk.choices[0].finish_reason}]
    #             finalResponse['system_fingerprint'] = chunk.system_fingerprint
    #             final_responses.append(finalResponse)
    #         return final_responses
    #     elif 'stream' in kwargs and kwargs['stream'] == False:
    #         response = await self.openai_client.with_raw_response.
    # chat.completions.create(
    #             **kwargs)
    #         response = response.text
    #         return json.loads(response)
    #     else:
    #         response = await self.openai_client.with_raw_response.
    # chat.completions.create(
    #             **kwargs)
    #         response = response.text
    #         return json.loads(response)

    def _get_config_string(self, config: Union[Mapping, str]) -> str:
        return config if isinstance(config, str) else json.dumps(config)
