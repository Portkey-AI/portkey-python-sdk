from typing import Optional, Union, overload, Literal
from portkey_ai.api_resources.base_client import APIClient
from portkey_ai.api_resources.utils import (
    PortkeyApiPaths,
    TextCompletion,
    TextCompletionChunk,
)

from portkey_ai.api_resources.streaming import Stream
from portkey_ai.api_resources.apis.api_resource import APIResource


class Completion(APIResource):
    def __init__(self, client: APIClient) -> None:
        super().__init__(client)

    @overload
    def create(
        self,
        *,
        prompt: Optional[str] = None,
        stream: Literal[True],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        **kwargs,
    ) -> Stream[TextCompletionChunk]:
        ...

    @overload
    def create(
        self,
        *,
        prompt: Optional[str] = None,
        stream: Literal[False] = False,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        **kwargs,
    ) -> TextCompletion:
        ...

    @overload
    def create(
        self,
        *,
        prompt: Optional[str] = None,
        stream: bool = False,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        **kwargs,
    ) -> Union[TextCompletion, Stream[TextCompletionChunk]]:
        ...

    def create(
        self,
        *,
        prompt: Optional[str] = None,
        stream: bool = False,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        **kwargs,
    ) -> Union[TextCompletion, Stream[TextCompletionChunk]]:
        body = dict(
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            top_k=top_k,
            top_p=top_p,
            stream=stream,
            **kwargs,
        )
        return self._post(
            PortkeyApiPaths.TEXT_COMPLETE_API,
            body=body,
            params=None,
            cast_to=TextCompletion,
            stream_cls=Stream[TextCompletionChunk],
            stream=stream,
            headers={},
        )
