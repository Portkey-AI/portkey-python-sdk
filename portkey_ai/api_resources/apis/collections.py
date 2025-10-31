from typing import Any, Union
from urllib.parse import urlencode
from portkey_ai._vendor.openai import NOT_GIVEN, NotGiven
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.base_client import APIClient, AsyncAPIClient
from portkey_ai.api_resources.utils import GenericResponse, PortkeyApiPaths


class Collections(APIResource):
    def __init__(self, client: APIClient) -> None:
        super().__init__(client)

    def create(
        self,
        name: str,
        workspace_id: Union[str, NotGiven] = NOT_GIVEN,
        parent_collection_id: Union[str, NotGiven] = NOT_GIVEN,
    ) -> Any:
        body = {
            "name": name,
            "workspace_id": workspace_id,
            "parent_collection_id": parent_collection_id,
        }
        return self._post(
            f"{PortkeyApiPaths.COLLECTIONS_API}",
            params=None,
            body=body,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def list(
        self,
        *,
        workspace_id: Union[str, NotGiven] = NOT_GIVEN,
        current_page: Union[int, NotGiven] = NOT_GIVEN,
        page_size: Union[int, NotGiven] = NOT_GIVEN,
        search: Union[str, NotGiven] = NOT_GIVEN,
    ) -> Any:
        query = {
            "workspace_id": workspace_id,
            "current_page": current_page,
            "page_size": page_size,
            "search": search,
        }
        filtered_query = {k: v for k, v in query.items() if v is not NOT_GIVEN}
        query_string = urlencode(filtered_query)
        return self._get(
            f"{PortkeyApiPaths.COLLECTIONS_API}?{query_string}",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def retrieve(
        self,
        collection_id: str,
    ) -> Any:
        return self._get(
            f"{PortkeyApiPaths.COLLECTIONS_API}/{collection_id}",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def update(
        self,
        collection_id: str,
        *,
        name: Union[str, NotGiven] = NOT_GIVEN,
    ) -> Any:
        body = {
            "name": name,
        }
        return self._put(
            f"{PortkeyApiPaths.COLLECTIONS_API}/{collection_id}",
            params=None,
            body=body,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def delete(
        self,
        collection_id: str,
    ) -> Any:
        return self._delete(
            f"{PortkeyApiPaths.COLLECTIONS_API}/{collection_id}",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )


class AsyncCollections(AsyncAPIResource):
    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)

    async def create(
        self,
        name: str,
        workspace_id: Union[str, NotGiven] = NOT_GIVEN,
        parent_collection_id: Union[str, NotGiven] = NOT_GIVEN,
    ) -> Any:
        body = {
            "name": name,
            "workspace_id": workspace_id,
            "parent_collection_id": parent_collection_id,
        }
        return await self._post(
            f"{PortkeyApiPaths.COLLECTIONS_API}",
            params=None,
            body=body,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def list(
        self,
        *,
        workspace_id: Union[str, NotGiven] = NOT_GIVEN,
        current_page: Union[int, NotGiven] = NOT_GIVEN,
        page_size: Union[int, NotGiven] = NOT_GIVEN,
        search: Union[str, NotGiven] = NOT_GIVEN,
    ) -> Any:
        query = {
            "workspace_id": workspace_id,
            "current_page": current_page,
            "page_size": page_size,
            "search": search,
        }
        filtered_query = {k: v for k, v in query.items() if v is not NOT_GIVEN}
        query_string = urlencode(filtered_query)
        return await self._get(
            f"{PortkeyApiPaths.COLLECTIONS_API}?{query_string}",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def retrieve(
        self,
        collection_id: str,
    ) -> Any:
        return await self._get(
            f"{PortkeyApiPaths.COLLECTIONS_API}/{collection_id}",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def update(
        self,
        collection_id: str,
        *,
        name: Union[str, NotGiven] = NOT_GIVEN,
    ) -> Any:
        body = {
            "name": name,
        }
        return await self._put(
            f"{PortkeyApiPaths.COLLECTIONS_API}/{collection_id}",
            params=None,
            body=body,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def delete(
        self,
        collection_id: str,
    ) -> Any:
        return await self._delete(
            f"{PortkeyApiPaths.COLLECTIONS_API}/{collection_id}",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )
