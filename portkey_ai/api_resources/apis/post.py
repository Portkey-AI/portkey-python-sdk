from typing import Union, overload, Literal

from portkey_ai.api_resources.base_client import APIClient

from portkey_ai.api_resources.streaming import Stream
from portkey_ai.api_resources.apis.api_resource import APIResource
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
            cast_to=dict,
            stream_cls=Stream[GenericResponse],
            stream=stream,
            headers={},
        )
