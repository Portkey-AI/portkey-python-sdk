from typing import Union, overload, Literal

from portkey_ai.api_resources.base_client import APIClient, AsyncAPIClient

from portkey_ai.api_resources.streaming import Stream, AsyncStream
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.utils import GenericResponse


class Post(APIResource):
    def __init__(self, client: APIClient) -> None:
        super().__init__(client)

    @overload
    def create(
        self,
        *,
        url: str,
        stream: Literal[True],
        **kwargs,
    ) -> Stream[GenericResponse]:
        ...

    @overload
    def create(
        self,
        *,
        url: str,
        stream: Literal[False] = False,
        **kwargs,
    ) -> GenericResponse:
        ...

    @overload
    def create(
        self,
        *,
        url: str,
        stream: bool = False,
        **kwargs,
    ) -> Union[GenericResponse, Stream[GenericResponse]]:
        ...

    def create(
        self,
        *,
        url: str,
        stream: bool = False,
        **kwargs,
    ) -> Union[GenericResponse, Stream[GenericResponse]]:
        return self._post(
            url,
            body=kwargs,
            params=None,
            cast_to=GenericResponse,
            stream_cls=Stream[GenericResponse],
            stream=stream,
            headers={},
        )


class AsyncPost(AsyncAPIResource):
    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)

    @overload
    async def create(
        self,
        *,
        url: str,
        stream: Literal[True],
        **kwargs,
    ) -> AsyncStream[GenericResponse]:
        ...

    @overload
    async def create(
        self,
        *,
        url: str,
        stream: Literal[False] = False,
        **kwargs,
    ) -> GenericResponse:
        ...

    @overload
    async def create(
        self,
        *,
        url: str,
        stream: bool = False,
        **kwargs,
    ) -> Union[GenericResponse, AsyncStream[GenericResponse]]:
        ...

    async def create(
        self,
        *,
        url: str,
        stream: bool = False,
        **kwargs,
    ) -> Union[GenericResponse, AsyncStream[GenericResponse]]:
        return await self._post(
            url,
            body=kwargs,
            params=None,
            cast_to=GenericResponse,
            stream_cls=AsyncStream[GenericResponse],
            stream=stream,
            headers={},
        )
