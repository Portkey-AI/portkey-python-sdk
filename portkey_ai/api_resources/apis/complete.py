import json
from typing import Any, AsyncIterator, Iterator, Union
from portkey_ai.api_resources.client import AsyncPortkey, Portkey
from portkey_ai.api_resources.utils import (
    TextCompletion,
    TextCompletionChunk,
)

from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource


class Completion(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.client = client

    def stream_create(
        self, **kwargs
    ) -> Union[TextCompletion, Iterator[TextCompletionChunk]]:
        with self.openai_client.with_streaming_response.completions.create(
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
                    json_data = TextCompletionChunk(**json_data)
                    yield json_data
                else:
                    return ""

    def normal_create(self, **kwargs) -> TextCompletion:
        response = self.openai_client.with_raw_response.completions.create(**kwargs)
        json_response = json.loads(response.text)
        return TextCompletion(**json_response)

    def create(
        self,
        **kwargs,
    ) -> TextCompletion:
        if "stream" in kwargs and kwargs["stream"] is True:
            return self.stream_create(**kwargs)  # type: ignore
        elif "stream" in kwargs and kwargs["stream"] is False:
            return self.normal_create(**kwargs)
        else:
            return self.normal_create(**kwargs)


class AsyncCompletion(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    async def stream_create(
        self, **kwargs
    ) -> Union[TextCompletion, AsyncIterator[TextCompletionChunk]]:
        async with self.openai_client.with_streaming_response.completions.create(
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
                    json_data = TextCompletionChunk(**json_data)
                    yield json_data
                else:
                    pass

    async def normal_create(self, **kwargs) -> TextCompletion:
        response = await self.openai_client.with_raw_response.completions.create(
            **kwargs
        )
        json_response = json.loads(response.text)
        return TextCompletion(**json_response)

    async def create(
        self,
        **kwargs,
    ) -> Any:
        if "stream" in kwargs and kwargs["stream"] is True:
            return self.stream_create(**kwargs)  # type: ignore
        elif "stream" in kwargs and kwargs["stream"] is False:
            return await self.normal_create(**kwargs)
        else:
            return await self.normal_create(**kwargs)
