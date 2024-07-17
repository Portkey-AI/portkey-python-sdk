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
        files = kwargs.pop("files", None)
        headers = kwargs.pop("headers", {})
        print(f"headers: {headers}")
        return self._post(
            url,
            body=kwargs,
            files=files,
            params=None,
            cast_to=GenericResponse,
            stream_cls=Stream[GenericResponse],
            stream=stream,
            headers=headers,
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
        files = kwargs.pop("files", None)
        return await self._post(
            url,
            body=kwargs,
            files=files,
            params=None,
            cast_to=GenericResponse,
            stream_cls=AsyncStream[GenericResponse],
            stream=stream,
            headers={},
        )
