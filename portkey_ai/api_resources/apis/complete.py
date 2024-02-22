import json
from typing import AsyncIterator, Iterator, Optional, Union, overload, Literal
from portkey_ai.api_resources.base_client import APIClient, AsyncAPIClient
from portkey_ai.api_resources.client import AsyncPortkey, Portkey
from portkey_ai.api_resources.utils import (
    PortkeyApiPaths,
    TextCompletion,
    TextCompletionChunk,
)

from portkey_ai.api_resources.streaming import AsyncStream, Stream
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource


class Completion(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.client = client

    def stream_create(self,**kwargs) -> Union[TextCompletion, Iterator[TextCompletionChunk]]:
        with self.openai_client.with_streaming_response.completions.create(**kwargs) as response:
            for line in response.iter_lines():
                json_string = line.replace('data: ', '')
                json_string = json_string.strip().rstrip('\n')
                if json_string == '':
                    continue
                elif json_string == '[DONE]':
                    break
                elif json_string!= '':
                    json_data = json.loads(json_string)
                    json_data = TextCompletionChunk(**json_data)
                    yield json_data
                else:
                    return ""
    
    def normal_create(self, **kwargs) -> TextCompletion:
        response = self.openai_client.with_raw_response.completions.create(
                **kwargs)
        json_response = json.loads(response.text)
        return TextCompletion(**json_response)
    
    def create(
        self,
        **kwargs,
    ) -> TextCompletion:
        
        if 'stream' in kwargs and kwargs['stream'] == True:
            return (self.stream_create(**kwargs))
        elif 'stream' in kwargs and kwargs['stream'] == False:
            return (self.normal_create(**kwargs))
        else:
            return (self.normal_create(**kwargs))

    # @overload
    # def create(
    #     self,
    #     *,
    #     prompt: Optional[str] = None,
    #     stream: Literal[True],
    #     temperature: Optional[float] = None,
    #     max_tokens: Optional[int] = None,
    #     top_k: Optional[int] = None,
    #     top_p: Optional[float] = None,
    #     **kwargs,
    # ) -> Stream[TextCompletionChunk]:
    #     ...

    # @overload
    # def create(
    #     self,
    #     *,
    #     prompt: Optional[str] = None,
    #     stream: Literal[False] = False,
    #     temperature: Optional[float] = None,
    #     max_tokens: Optional[int] = None,
    #     top_k: Optional[int] = None,
    #     top_p: Optional[float] = None,
    #     **kwargs,
    # ) -> TextCompletion:
    #     ...

    # @overload
    # def create(
    #     self,
    #     *,
    #     prompt: Optional[str] = None,
    #     stream: bool = False,
    #     temperature: Optional[float] = None,
    #     max_tokens: Optional[int] = None,
    #     top_k: Optional[int] = None,
    #     top_p: Optional[float] = None,
    #     **kwargs,
    # ) -> Union[TextCompletion, Stream[TextCompletionChunk]]:
    #     ...

    # def create(
    #     self,
    #     **kwargs,
    # ) -> Union[TextCompletion, Stream[TextCompletionChunk]]:
        
    #     if 'stream' in kwargs and kwargs['stream'] == True:
    #         final_responses = []
    #         response = self.openai_client.completions.create(**kwargs)
    #         for chunk in response:
    #             finalResponse = {}
    #             finalResponse['id'] = chunk.id
    #             finalResponse['object'] = chunk.object
    #             finalResponse['created'] = chunk.created
    #             finalResponse['model'] = chunk.model
    #             finalResponse['choices'] = [{'index': chunk.choices[0].index,
    #                                         'text': chunk.choices[0].text,
    #                                         'logprobs': chunk.choices[0].logprobs,
    #                                         'finish_reason': chunk.choices[0].finish_reason}]
    #             final_responses.append(finalResponse)
    #         return final_responses
    #     elif 'stream' in kwargs and kwargs['stream'] == False:
    #         response = self.openai_client.with_raw_response.completions.create(**kwargs)
    #         response = response
    #         return json.loads(response)
    #     else:
    #         response = self.openai_client.with_raw_response.completions.create(**kwargs)
    #         response = response.text
    #         return json.loads(response)


class AsyncCompletion(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
    
    async def stream_create(self,**kwargs) -> Union[TextCompletion, AsyncIterator[TextCompletionChunk]]:
        async with self.openai_client.with_streaming_response.completions.create(**kwargs) as response:
            async for line in response.iter_lines():
                json_string = line.replace('data: ', '')
                json_string = json_string.strip().rstrip('\n')
                if json_string == '':
                    continue
                elif json_string == '[DONE]':
                    break
                elif json_string!= '':
                    json_data = json.loads(json_string)
                    json_data = TextCompletionChunk(**json_data)
                    yield json_data
                else:
                    pass
    
    async def normal_create(self, **kwargs) -> TextCompletion:
        response = await self.openai_client.with_raw_response.completions.create(
                **kwargs)
        json_response = json.loads(response.text)
        return TextCompletion(**json_response)
    
    async def create(
        self,
        **kwargs,
    ) -> TextCompletion:
        
        if 'stream' in kwargs and kwargs['stream'] == True:
            return (self.stream_create(**kwargs))
        elif 'stream' in kwargs and kwargs['stream'] == False:
            return await (self.normal_create(**kwargs))
        else:
            return await (self.normal_create(**kwargs))

    # @overload
    # async def create(
    #     self,
    #     *,
    #     prompt: Optional[str] = None,
    #     stream: Literal[True],
    #     temperature: Optional[float] = None,
    #     max_tokens: Optional[int] = None,
    #     top_k: Optional[int] = None,
    #     top_p: Optional[float] = None,
    #     **kwargs,
    # ) -> AsyncStream[TextCompletionChunk]:
    #     ...

    # @overload
    # async def create(
    #     self,
    #     *,
    #     prompt: Optional[str] = None,
    #     stream: Literal[False] = False,
    #     temperature: Optional[float] = None,
    #     max_tokens: Optional[int] = None,
    #     top_k: Optional[int] = None,
    #     top_p: Optional[float] = None,
    #     **kwargs,
    # ) -> TextCompletion:
    #     ...

    # @overload
    # async def create(
    #     self,
    #     *,
    #     prompt: Optional[str] = None,
    #     stream: bool = False,
    #     temperature: Optional[float] = None,
    #     max_tokens: Optional[int] = None,
    #     top_k: Optional[int] = None,
    #     top_p: Optional[float] = None,
    #     **kwargs,
    # ) -> Union[TextCompletion, AsyncStream[TextCompletionChunk]]:
    #     ...

    # async def create(
    #     self,
    #     **kwargs,
    # ) -> Union[TextCompletion, AsyncStream[TextCompletionChunk]]:

    #     if 'stream' in kwargs and kwargs['stream'] == True:
    #         final_responses = []
    #         response = await self.openai_client.completions.create(**kwargs)
    #         async for chunk in response:
    #             finalResponse = {}
    #             finalResponse['id'] = chunk.id
    #             finalResponse['object'] = chunk.object
    #             finalResponse['created'] = chunk.created
    #             finalResponse['model'] = chunk.model
    #             finalResponse['choices'] = [{'index': chunk.choices[0].index,
    #                                         'text': chunk.choices[0].text,
    #                                         'logprobs': chunk.choices[0].logprobs,
    #                                         'finish_reason': chunk.choices[0].finish_reason}]
    #             final_responses.append(finalResponse)
    #         return final_responses
    #     elif 'stream' in kwargs and kwargs['stream'] == False:
    #         response = await self.openai_client.with_raw_response.completions.create(**kwargs)
    #         response = response.text
    #         return json.loads(response)
    #     else:
    #         response = await self.openai_client.with_raw_response.completions.create(**kwargs)
    #         response = response.text
    #         return json.loads(response)
