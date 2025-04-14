from typing import Any, Optional
from urllib.parse import urlencode
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.base_client import APIClient, AsyncAPIClient
from portkey_ai.api_resources.utils import GenericResponse, PortkeyApiPaths


class Labels(APIResource):
    def __init__(self, client: APIClient) -> None:
        super().__init__(client)

    def create(
        self,
        *,
        name: str,
        organization_id: Optional[str] = None,
        workspace_id: Optional[str] = None,
        description: Optional[str] = None,
        color_code: Optional[str] = None,
    ) -> Any:
        body = {
            "name": name,
            "organization_id": organization_id,
            "workspace_id": workspace_id,
            "description": description,
            "color_code": color_code,
        }
        return self._post(
            f"{PortkeyApiPaths.LABELS_API}",
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
        organization_id: Optional[str] = None,
        workspace_id: Optional[str] = None,
        current_page: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Any:
        query = {
            "organization_id": organization_id,
            "workspace_id": workspace_id,
            "current_page": current_page,
            "page_size": page_size,
        }
        filtered_query = {k: v for k, v in query.items() if v is not None}
        query_string = urlencode(filtered_query)
        return self._get(
            f"{PortkeyApiPaths.LABELS_API}?{query_string}",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def retrieve(
        self,
        label_id: str,
    ) -> Any:
        return self._get(
            f"{PortkeyApiPaths.LABELS_API}/{label_id}",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def update(
        self,
        label_id: str,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
        color_code: Optional[str] = None,
    ) -> Any:
        body = {
            "name": name,
            "description": description,
            "color_code": color_code,
        }
        return self._put(
            f"{PortkeyApiPaths.LABELS_API}/{label_id}",
            params=None,
            body=body,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def delete(
        self,
        label_id: str,
    ) -> Any:
        return self._delete(
            f"{PortkeyApiPaths.LABELS_API}/{label_id}",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )


class AsyncLabels(AsyncAPIResource):
    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)

    async def create(
        self,
        *,
        name: str,
        organization_id: Optional[str] = None,
        workspace_id: Optional[str] = None,
        description: Optional[str] = None,
        color_code: Optional[str] = None,
    ) -> Any:
        body = {
            "name": name,
            "organization_id": organization_id,
            "workspace_id": workspace_id,
            "description": description,
            "color_code": color_code,
        }
        return await self._post(
            f"{PortkeyApiPaths.LABELS_API}",
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
        organization_id: Optional[str] = None,
        workspace_id: Optional[str] = None,
        current_page: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Any:
        query = {
            "organization_id": organization_id,
            "workspace_id": workspace_id,
            "current_page": current_page,
            "page_size": page_size,
        }
        filtered_query = {k: v for k, v in query.items() if v is not None}
        query_string = urlencode(filtered_query)
        return await self._get(
            f"{PortkeyApiPaths.LABELS_API}?{query_string}",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def retrieve(
        self,
        label_id: str,
    ) -> Any:
        return await self._get(
            f"{PortkeyApiPaths.LABELS_API}/{label_id}",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def update(
        self,
        label_id: str,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
        color_code: Optional[str] = None,
    ) -> Any:
        body = {
            "name": name,
            "description": description,
            "color_code": color_code,
        }
        return await self._put(
            f"{PortkeyApiPaths.LABELS_API}/{label_id}",
            params=None,
            body=body,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def delete(
        self,
        label_id: str,
    ) -> Any:
        return await self._delete(
            f"{PortkeyApiPaths.LABELS_API}/{label_id}",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )
