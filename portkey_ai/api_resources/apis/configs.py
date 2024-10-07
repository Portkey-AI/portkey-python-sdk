from typing import Any, Dict, Optional
from portkey_ai.api_resources.base_client import APIClient, AsyncAPIClient
from urllib.parse import urlencode
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.types.configs_type import (
    ConfigAddResponse,
    ConfigGetResponse,
    ConfigListResponse,
    ConfigUpdateResponse,
)
from portkey_ai.api_resources.utils import GenericResponse
from portkey_ai.api_resources.utils import PortkeyApiPaths


class Configs(APIResource):
    def __init__(self, client: APIClient) -> None:
        super().__init__(client)

    def add(
        self,
        *,
        name: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
        is_default: Optional[int] = None,
        workspace_id: Optional[str] = None,
    ) -> ConfigAddResponse:
        body = {
            "name": name,
            "config": config,
            "is_default": is_default,
            "workspace_id": workspace_id,
        }
        return self._post(
            f"{PortkeyApiPaths.CONFIG_API}",
            body=body,
            params=None,
            cast_to=ConfigAddResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def get(self, *, slug: Optional[str]) -> ConfigGetResponse:
        return self._get(
            f"{PortkeyApiPaths.CONFIG_API}/{slug}",
            params=None,
            body=None,
            cast_to=ConfigGetResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def list(
        self,
        *,
        workspace_id: Optional[str] = None,
    ) -> ConfigListResponse:
        query = {
            "workspace_id": workspace_id,
        }
        filtered_query = {k: v for k, v in query.items() if v is not None}
        query_string = urlencode(filtered_query)
        return self._get(
            f"{PortkeyApiPaths.CONFIG_API}?{query_string}",
            params=None,
            body=None,
            cast_to=ConfigListResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def update(
        self,
        *,
        slug: Optional[str] = None,
        name: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
        status: Optional[str] = None,
    ) -> ConfigUpdateResponse:
        body = {
            "slug": slug,
            "name": name,
            "config": config,
            "status": status,
        }
        return self._put(
            f"{PortkeyApiPaths.CONFIG_API}/{slug}",
            body=body,
            params=None,
            cast_to=ConfigUpdateResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def delete(
        self,
        *,
        config_id: Optional[str],
    ) -> Any:
        return self._delete(
            f"{PortkeyApiPaths.CONFIG_API}/{config_id}",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )


class AsyncConfigs(AsyncAPIResource):
    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)

    async def add(
        self,
        *,
        name: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
        is_default: Optional[int] = None,
        workspace_id: Optional[str] = None,
    ) -> ConfigAddResponse:
        body = {
            "name": name,
            "config": config,
            "is_default": is_default,
            "workspace_id": workspace_id,
        }
        return await self._post(
            f"{PortkeyApiPaths.CONFIG_API}",
            body=body,
            params=None,
            cast_to=ConfigAddResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def get(self, *, slug: Optional[str]) -> ConfigGetResponse:
        return await self._get(
            f"{PortkeyApiPaths.CONFIG_API}/{slug}",
            params=None,
            body=None,
            cast_to=ConfigGetResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def list(
        self,
        *,
        workspace_id: Optional[str] = None,
    ) -> ConfigListResponse:
        query = {
            "workspace_id": workspace_id,
        }
        filtered_query = {k: v for k, v in query.items() if v is not None}
        query_string = urlencode(filtered_query)
        return await self._get(
            f"{PortkeyApiPaths.CONFIG_API}?{query_string}",
            params=None,
            body=None,
            cast_to=ConfigListResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def update(
        self,
        *,
        slug: Optional[str] = None,
        name: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
        status: Optional[str] = None,
    ) -> ConfigUpdateResponse:
        body = {
            "slug": slug,
            "name": name,
            "config": config,
            "status": status,
        }
        return await self._put(
            f"{PortkeyApiPaths.CONFIG_API}/{slug}",
            body=body,
            params=None,
            cast_to=ConfigUpdateResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def delete(
        self,
        *,
        config_id: Optional[str],
    ) -> Any:
        return await self._delete(
            f"{PortkeyApiPaths.CONFIG_API}/{config_id}",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )
