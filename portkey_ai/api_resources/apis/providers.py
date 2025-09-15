from typing import Any, Dict, Optional
from portkey_ai.api_resources.base_client import APIClient, AsyncAPIClient
from urllib.parse import urlencode
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.types.providers_type import (
    ProviderListResponse,
    ProviderDetailResponse,
    ProviderCreateResponse,
    ProviderUpdateResponse,
)
from portkey_ai.api_resources.utils import GenericResponse
from portkey_ai.api_resources.utils import PortkeyApiPaths


class Providers(APIResource):
    def __init__(self, client: APIClient) -> None:
        super().__init__(client)

    def create(
        self,
        *,
        name: str,
        integration_id: str,
        workspace_id: Optional[str] = None,
        slug: Optional[str] = None,
        note: Optional[str] = None,
        usage_limits: Optional[Dict[str, Any]] = None,
        rate_limits: Optional[Dict[str, Any]] = None,
        expires_at: Optional[str] = None,
        **kwargs: Any,
    ) -> ProviderCreateResponse:
        body = {
            "name": name,
            "integration_id": integration_id,
            "workspace_id": workspace_id,
            "slug": slug,
            "note": note,
            "usage_limits": usage_limits,
            "rate_limits": rate_limits,
            "expires_at": expires_at,
            **kwargs,
        }
        return self._post(
            f"{PortkeyApiPaths.PROVIDERS_API}",
            body=body,
            params=None,
            cast_to=ProviderCreateResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def list(
        self,
        *,
        current_page: Optional[int] = 0,
        page_size: Optional[int] = 50,
        workspace_id: Optional[str] = None,
    ) -> ProviderListResponse:
        query = {
            "current_page": current_page,
            "page_size": page_size,
            "workspace_id": workspace_id,
        }
        filtered_query = {k: v for k, v in query.items() if v is not None}
        query_string = urlencode(filtered_query)
        return self._get(
            f"{PortkeyApiPaths.PROVIDERS_API}?{query_string}",
            params=None,
            body=None,
            cast_to=ProviderListResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def retrieve(
        self,
        *,
        slug: str,
        workspace_id: Optional[str] = None,
    ) -> ProviderDetailResponse:
        query = {
            "workspace_id": workspace_id,
        }
        filtered_query = {k: v for k, v in query.items() if v is not None}
        query_string = urlencode(filtered_query)
        path = f"{PortkeyApiPaths.PROVIDERS_API}/{slug}"
        if query_string:
            path = f"{path}?{query_string}"
        return self._get(
            path,
            params=None,
            body=None,
            cast_to=ProviderDetailResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def update(
        self,
        *,
        slug: str,
        workspace_id: Optional[str] = None,
        name: Optional[str] = None,
        note: Optional[str] = None,
        usage_limits: Optional[Dict[str, Any]] = None,
        rate_limits: Optional[Dict[str, Any]] = None,
        expires_at: Optional[str] = None,
        reset_usage: Optional[bool] = None,
        **kwargs: Any,
    ) -> ProviderUpdateResponse:
        body = {
            "name": name,
            "note": note,
            "usage_limits": usage_limits,
            "rate_limits": rate_limits,
            "expires_at": expires_at,
            "reset_usage": reset_usage,
            **kwargs,
        }
        query = {
            "workspace_id": workspace_id,
        }
        filtered_query = {k: v for k, v in query.items() if v is not None}
        query_string = urlencode(filtered_query)
        path = f"{PortkeyApiPaths.PROVIDERS_API}/{slug}"
        if query_string:
            path = f"{path}?{query_string}"
        return self._put(
            path,
            body=body,
            params=None,
            cast_to=ProviderUpdateResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def delete(
        self,
        *,
        slug: str,
        workspace_id: Optional[str] = None,
    ) -> GenericResponse:
        query = {
            "workspace_id": workspace_id,
        }
        filtered_query = {k: v for k, v in query.items() if v is not None}
        query_string = urlencode(filtered_query)
        path = f"{PortkeyApiPaths.PROVIDERS_API}/{slug}"
        if query_string:
            path = f"{path}?{query_string}"
        return self._delete(
            path,
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )


class AsyncProviders(AsyncAPIResource):
    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)

    async def create(
        self,
        *,
        name: str,
        integration_id: str,
        workspace_id: Optional[str] = None,
        slug: Optional[str] = None,
        note: Optional[str] = None,
        usage_limits: Optional[Dict[str, Any]] = None,
        rate_limits: Optional[Dict[str, Any]] = None,
        expires_at: Optional[str] = None,
        **kwargs: Any,
    ) -> ProviderCreateResponse:
        body = {
            "name": name,
            "integration_id": integration_id,
            "workspace_id": workspace_id,
            "slug": slug,
            "note": note,
            "usage_limits": usage_limits,
            "rate_limits": rate_limits,
            "expires_at": expires_at,
            **kwargs,
        }
        return await self._post(
            f"{PortkeyApiPaths.PROVIDERS_API}",
            body=body,
            params=None,
            cast_to=ProviderCreateResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def list(
        self,
        *,
        current_page: Optional[int] = 0,
        page_size: Optional[int] = 50,
        workspace_id: Optional[str] = None,
    ) -> ProviderListResponse:
        query = {
            "current_page": current_page,
            "page_size": page_size,
            "workspace_id": workspace_id,
        }
        filtered_query = {k: v for k, v in query.items() if v is not None}
        query_string = urlencode(filtered_query)
        return await self._get(
            f"{PortkeyApiPaths.PROVIDERS_API}?{query_string}",
            params=None,
            body=None,
            cast_to=ProviderListResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def retrieve(
        self,
        *,
        slug: str,
        workspace_id: Optional[str] = None,
    ) -> ProviderDetailResponse:
        query = {
            "workspace_id": workspace_id,
        }
        filtered_query = {k: v for k, v in query.items() if v is not None}
        query_string = urlencode(filtered_query)
        path = f"{PortkeyApiPaths.PROVIDERS_API}/{slug}"
        if query_string:
            path = f"{path}?{query_string}"
        return await self._get(
            path,
            params=None,
            body=None,
            cast_to=ProviderDetailResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def update(
        self,
        *,
        slug: str,
        workspace_id: Optional[str] = None,
        name: Optional[str] = None,
        note: Optional[str] = None,
        usage_limits: Optional[Dict[str, Any]] = None,
        rate_limits: Optional[Dict[str, Any]] = None,
        expires_at: Optional[str] = None,
        reset_usage: Optional[bool] = None,
        **kwargs: Any,
    ) -> ProviderUpdateResponse:
        body = {
            "name": name,
            "note": note,
            "usage_limits": usage_limits,
            "rate_limits": rate_limits,
            "expires_at": expires_at,
            "reset_usage": reset_usage,
            **kwargs,
        }
        query = {
            "workspace_id": workspace_id,
        }
        filtered_query = {k: v for k, v in query.items() if v is not None}
        query_string = urlencode(filtered_query)
        path = f"{PortkeyApiPaths.PROVIDERS_API}/{slug}"
        if query_string:
            path = f"{path}?{query_string}"
        return await self._put(
            path,
            body=body,
            params=None,
            cast_to=ProviderUpdateResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def delete(
        self,
        *,
        slug: str,
        workspace_id: Optional[str] = None,
    ) -> GenericResponse:
        query = {
            "workspace_id": workspace_id,
        }
        filtered_query = {k: v for k, v in query.items() if v is not None}
        query_string = urlencode(filtered_query)
        path = f"{PortkeyApiPaths.PROVIDERS_API}/{slug}"
        if query_string:
            path = f"{path}?{query_string}"
        return await self._delete(
            path,
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )
