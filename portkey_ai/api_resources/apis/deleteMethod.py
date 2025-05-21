from typing import Any, Optional
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.base_client import APIClient, AsyncAPIClient


class DeleteMethod(APIResource):
    def __init__(self, client: APIClient) -> None:
        super().__init__(client)

    def create(
        self,
        path: str,
        headers: Optional[dict[str, str]] = {},
        cast_to: Optional[Any] = None,
    ):
        return self._delete(
            path=path,
            body={},
            params={},
            headers=headers,
            cast_to=cast_to,
            stream=False,
            stream_cls=None,
        )


class AsyncDeleteMethod(AsyncAPIResource):
    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)

    async def create(
        self,
        path: str,
        headers: Optional[dict[str, str]] = {},
        cast_to: Optional[Any] = None,
    ):
        return await self._delete(
            path=path,
            body={},
            params={},
            headers=headers,
            cast_to=cast_to,
            stream=False,
            stream_cls=None,
        )
