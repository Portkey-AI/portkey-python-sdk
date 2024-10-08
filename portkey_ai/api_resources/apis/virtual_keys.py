from typing import Any, Dict, List, Optional
from portkey_ai.api_resources.base_client import APIClient, AsyncAPIClient
from urllib.parse import urlencode
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.types.virtual_keys_type import (
    VirtualKeysListReponse,
    VirtualKeysUpdateResponse,
    VirtualKeysAddResponse,
)
from portkey_ai.api_resources.utils import GenericResponse
from portkey_ai.api_resources.utils import PortkeyApiPaths


class VirtualKeys(APIResource):
    def __init__(self, client: APIClient) -> None:
        super().__init__(client)

    def create(
        self,
        *,
        name: Optional[str] = None,
        provider: Optional[str] = None,
        key: Optional[str] = None,
        note: Optional[str] = None,
        apiVersion: Optional[str] = None,
        resourceName: Optional[str] = None,
        deploymentName: Optional[str] = None,
        workspace_id: Optional[str] = None,
        usage_limits: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> VirtualKeysAddResponse:
        body = {
            "name": name,
            "provider": provider,
            "key": key,
            "note": note,
            "apiVersion": apiVersion,
            "resourceName": resourceName,
            "deploymentName": deploymentName,
            "workspace_id": workspace_id,
            "usage_limits": usage_limits,
            **kwargs,
        }
        return self._post(
            f"{PortkeyApiPaths.VIRTUAL_KEYS_API}",
            body=body,
            params=None,
            cast_to=VirtualKeysAddResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def list(
        self,
        *,
        workspace_id: Optional[str] = None,
    ) -> VirtualKeysListReponse:
        query = {"workspace_id": workspace_id}
        filtered_query = {k: v for k, v in query.items() if v is not None}
        query_string = urlencode(filtered_query)
        return self._get(
            f"{PortkeyApiPaths.VIRTUAL_KEYS_API}?{query_string}",
            params=None,
            body=None,
            cast_to=VirtualKeysListReponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def retrieve(self, *, slug: Optional[str]) -> Any:
        return self._get(
            f"{PortkeyApiPaths.VIRTUAL_KEYS_API}/{slug}",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def update(
        self,
        *,
        slug: Optional[str] = None,
        name: Optional[str] = None,
        key: Optional[str] = None,
        note: Optional[str] = None,
        usage_limits: Optional[Dict[str, Any]] = None,
        rate_limits: Optional[List[Dict[str, Any]]] = None,
        **kwargs: Any,
    ) -> VirtualKeysUpdateResponse:
        body = {
            "name": name,
            "key": key,
            "note": note,
            "usage_limits": usage_limits,
            "rate_limits": rate_limits,
            **kwargs,
        }
        return self._put(
            f"{PortkeyApiPaths.VIRTUAL_KEYS_API}/{slug}",
            body=body,
            params=None,
            cast_to=VirtualKeysUpdateResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def delete(
        self,
        *,
        slug: Optional[str],
    ) -> Any:
        return self._delete(
            f"{PortkeyApiPaths.VIRTUAL_KEYS_API}/{slug}",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )


class AsyncVirtualKeys(AsyncAPIResource):
    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)

    async def create(
        self,
        *,
        name: Optional[str] = None,
        provider: Optional[str] = None,
        key: Optional[str] = None,
        note: Optional[str] = None,
        apiVersion: Optional[str] = None,
        resourceName: Optional[str] = None,
        deploymentName: Optional[str] = None,
        workspace_id: Optional[str] = None,
        usage_limits: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> VirtualKeysAddResponse:
        body = {
            "name": name,
            "provider": provider,
            "key": key,
            "note": note,
            "apiVersion": apiVersion,
            "resourceName": resourceName,
            "deploymentName": deploymentName,
            "workspace_id": workspace_id,
            "usage_limits": usage_limits,
            **kwargs,
        }
        return await self._post(
            f"{PortkeyApiPaths.VIRTUAL_KEYS_API}",
            body=body,
            params=None,
            cast_to=VirtualKeysAddResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def list(
        self,
        *,
        workspace_id: Optional[str] = None,
    ) -> VirtualKeysListReponse:
        query = {"workspace_id": workspace_id}
        filtered_query = {k: v for k, v in query.items() if v is not None}
        query_string = urlencode(filtered_query)
        return await self._get(
            f"{PortkeyApiPaths.VIRTUAL_KEYS_API}?{query_string}",
            params=None,
            body=None,
            cast_to=VirtualKeysListReponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def retrieve(self, *, slug: Optional[str]) -> Any:
        return await self._get(
            f"{PortkeyApiPaths.VIRTUAL_KEYS_API}/{slug}",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def update(
        self,
        *,
        slug: Optional[str] = None,
        name: Optional[str] = None,
        key: Optional[str] = None,
        note: Optional[str] = None,
        usage_limits: Optional[Dict[str, Any]] = None,
        rate_limits: Optional[List[Dict[str, Any]]] = None,
        **kwargs: Any,
    ) -> VirtualKeysUpdateResponse:
        body = {
            "name": name,
            "key": key,
            "note": note,
            "usage_limits": usage_limits,
            "rate_limits": rate_limits,
            **kwargs,
        }
        return await self._put(
            f"{PortkeyApiPaths.VIRTUAL_KEYS_API}/{slug}",
            body=body,
            params=None,
            cast_to=VirtualKeysUpdateResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def delete(
        self,
        *,
        slug: Optional[str],
    ) -> Any:
        return await self._delete(
            f"{PortkeyApiPaths.VIRTUAL_KEYS_API}/{slug}",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )
