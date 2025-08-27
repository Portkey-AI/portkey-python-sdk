from typing import Any, Dict, List, Literal, Optional
from portkey_ai.api_resources.base_client import APIClient, AsyncAPIClient
from urllib.parse import urlencode
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.types.integrations_type import (
    IntegrationListResponse,
    IntegrationDetailResponse,
    IntegrationCreateResponse,
    IntegrationModelsResponse,
    IntegrationWorkspacesResponse,
)
from portkey_ai.api_resources.utils import GenericResponse
from portkey_ai.api_resources.utils import PortkeyApiPaths


class Integrations(APIResource):
    def __init__(self, client: APIClient) -> None:
        super().__init__(client)
        self.workspaces = IntegrationsWorkspaces(client)
        self.models = IntegrationsModels(client)

    def create(
        self,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
        key: Optional[str] = None,
        ai_provider_id: Optional[str] = None,
        workspace_id: Optional[str] = None,
        slug: Optional[str] = None,
        organisation_id: Optional[str] = None,
        note: Optional[str] = None,
        configuration: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> IntegrationCreateResponse:
        body = {
            "name": name,
            "description": description,
            "key": key,
            "ai_provider_id": ai_provider_id,
            "workspace_id": workspace_id,
            "slug": slug,
            "organisation_id": organisation_id,
            "note": note,
            "configuration": configuration,
            **kwargs,
        }
        return self._post(
            f"{PortkeyApiPaths.INTEGRATIONS_API}",
            body=body,
            params=None,
            cast_to=IntegrationCreateResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def list(
        self,
        *,
        current_page: Optional[int] = 0,
        page_size: Optional[int] = 100,
        workspace_id: Optional[str] = None,
        type: Optional[Literal["workspace", "organisation", "all"]] = None,
    ) -> IntegrationListResponse:
        query = {
            "current_page": current_page,
            "page_size": page_size,
            "workspace_id": workspace_id,
            "type": type,
        }
        filtered_query = {k: v for k, v in query.items() if v is not None}
        query_string = urlencode(filtered_query)
        return self._get(
            f"{PortkeyApiPaths.INTEGRATIONS_API}?{query_string}",
            params=None,
            body=None,
            cast_to=IntegrationListResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def retrieve(self, *, slug: str) -> IntegrationDetailResponse:
        return self._get(
            f"{PortkeyApiPaths.INTEGRATIONS_API}/{slug}",
            params=None,
            body=None,
            cast_to=IntegrationDetailResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def update(
        self,
        *,
        slug: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        key: Optional[str] = None,
        configuration: Optional[Dict[str, Any]] = None,
        note: Optional[str] = None,
        **kwargs: Any,
    ) -> GenericResponse:
        body = {
            "name": name,
            "description": description,
            "key": key,
            "configuration": configuration,
            "note": note,
            **kwargs,
        }
        return self._put(
            f"{PortkeyApiPaths.INTEGRATIONS_API}/{slug}",
            body=body,
            params=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def delete(
        self,
        *,
        slug: str,
    ) -> GenericResponse:
        return self._delete(
            f"{PortkeyApiPaths.INTEGRATIONS_API}/{slug}",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )


class IntegrationsWorkspaces(APIResource):
    def __init__(self, client: APIClient) -> None:
        super().__init__(client)

    def list(
        self,
        *,
        slug: str,
    ) -> IntegrationWorkspacesResponse:
        return self._get(
            f"{PortkeyApiPaths.INTEGRATIONS_API}/{slug}/workspaces",
            params=None,
            body=None,
            cast_to=IntegrationWorkspacesResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def update(
        self,
        *,
        slug: str,
        global_workspace_access: Optional[Dict[str, Any]] = None,
        workspace_ids: Optional[List[str]] = None,
        override_existing_workspaces_access: Optional[bool] = None,
        workspaces: Optional[List[Dict[str, Any]]] = None,
        **kwargs: Any,
    ) -> GenericResponse:
        body = {
            "global_workspace_access": global_workspace_access,
            "workspace_ids": workspace_ids,
            "override_existing_workspaces_access": override_existing_workspaces_access,
            "workspaces": workspaces,
            **kwargs,
        }
        return self._put(
            f"{PortkeyApiPaths.INTEGRATIONS_API}/{slug}/workspaces",
            body=body,
            params=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )


class IntegrationsModels(APIResource):
    def __init__(self, client: APIClient) -> None:
        super().__init__(client)

    def list(
        self,
        *,
        slug: str,
    ) -> IntegrationModelsResponse:
        return self._get(
            f"{PortkeyApiPaths.INTEGRATIONS_API}/{slug}/models",
            params=None,
            body=None,
            cast_to=IntegrationModelsResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def update(
        self,
        *,
        slug: str,
        allow_all_models: Optional[bool] = None,
        models: Optional[List[Dict[str, Any]]] = None,
        **kwargs: Any,
    ) -> GenericResponse:
        body = {
            "allow_all_models": allow_all_models,
            "models": models,
            **kwargs,
        }
        return self._put(
            f"{PortkeyApiPaths.INTEGRATIONS_API}/{slug}/models",
            body=body,
            params=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def delete(
        self,
        *,
        slug: str,
        slugs: str,
    ) -> GenericResponse:
        query = {
            "slugs": slugs,
        }
        filtered_query = {k: v for k, v in query.items() if v is not None}
        query_string = urlencode(filtered_query)
        return self._delete(
            f"{PortkeyApiPaths.INTEGRATIONS_API}/{slug}/models?{query_string}",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )


class AsyncIntegrations(AsyncAPIResource):
    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)
        self.workspaces = AsyncIntegrationsWorkspaces(client)
        self.models = AsyncIntegrationsModels(client)

    async def create(
        self,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
        key: Optional[str] = None,
        ai_provider_id: Optional[str] = None,
        workspace_id: Optional[str] = None,
        slug: Optional[str] = None,
        organisation_id: Optional[str] = None,
        note: Optional[str] = None,
        configuration: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> IntegrationCreateResponse:
        body = {
            "name": name,
            "description": description,
            "key": key,
            "ai_provider_id": ai_provider_id,
            "workspace_id": workspace_id,
            "slug": slug,
            "organisation_id": organisation_id,
            "note": note,
            "configuration": configuration,
            **kwargs,
        }
        return await self._post(
            f"{PortkeyApiPaths.INTEGRATIONS_API}",
            body=body,
            params=None,
            cast_to=IntegrationCreateResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def list(
        self,
        *,
        current_page: Optional[int] = 0,
        page_size: Optional[int] = 100,
        workspace_id: Optional[str] = None,
        type: Optional[Literal["workspace", "organisation", "all"]] = None,
    ) -> IntegrationListResponse:
        query = {
            "current_page": current_page,
            "page_size": page_size,
            "workspace_id": workspace_id,
            "type": type,
        }
        filtered_query = {k: v for k, v in query.items() if v is not None}
        query_string = urlencode(filtered_query)
        return await self._get(
            f"{PortkeyApiPaths.INTEGRATIONS_API}?{query_string}",
            params=None,
            body=None,
            cast_to=IntegrationListResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def retrieve(self, *, slug: str) -> IntegrationDetailResponse:
        return await self._get(
            f"{PortkeyApiPaths.INTEGRATIONS_API}/{slug}",
            params=None,
            body=None,
            cast_to=IntegrationDetailResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def update(
        self,
        *,
        slug: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        key: Optional[str] = None,
        configuration: Optional[Dict[str, Any]] = None,
        note: Optional[str] = None,
        **kwargs: Any,
    ) -> GenericResponse:
        body = {
            "name": name,
            "description": description,
            "key": key,
            "configuration": configuration,
            "note": note,
            **kwargs,
        }
        return await self._put(
            f"{PortkeyApiPaths.INTEGRATIONS_API}/{slug}",
            body=body,
            params=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def delete(
        self,
        *,
        slug: str,
    ) -> GenericResponse:
        return await self._delete(
            f"{PortkeyApiPaths.INTEGRATIONS_API}/{slug}",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )


class AsyncIntegrationsWorkspaces(AsyncAPIResource):
    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)

    async def list(
        self,
        *,
        slug: str,
    ) -> IntegrationWorkspacesResponse:
        return await self._get(
            f"{PortkeyApiPaths.INTEGRATIONS_API}/{slug}/workspaces",
            params=None,
            body=None,
            cast_to=IntegrationWorkspacesResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def update(
        self,
        *,
        slug: str,
        global_workspace_access: Optional[Dict[str, Any]] = None,
        workspace_ids: Optional[List[str]] = None,
        override_existing_workspaces_access: Optional[bool] = None,
        workspaces: Optional[List[Dict[str, Any]]] = None,
        **kwargs: Any,
    ) -> GenericResponse:
        body = {
            "global_workspace_access": global_workspace_access,
            "workspace_ids": workspace_ids,
            "override_existing_workspaces_access": override_existing_workspaces_access,
            "workspaces": workspaces,
            **kwargs,
        }
        return await self._put(
            f"{PortkeyApiPaths.INTEGRATIONS_API}/{slug}/workspaces",
            body=body,
            params=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )


class AsyncIntegrationsModels(AsyncAPIResource):
    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)

    async def list(
        self,
        *,
        slug: str,
    ) -> IntegrationModelsResponse:
        return await self._get(
            f"{PortkeyApiPaths.INTEGRATIONS_API}/{slug}/models",
            params=None,
            body=None,
            cast_to=IntegrationModelsResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def update(
        self,
        *,
        slug: str,
        allow_all_models: Optional[bool] = None,
        models: Optional[List[Dict[str, Any]]] = None,
        **kwargs: Any,
    ) -> GenericResponse:
        body = {
            "allow_all_models": allow_all_models,
            "models": models,
            **kwargs,
        }
        return await self._put(
            f"{PortkeyApiPaths.INTEGRATIONS_API}/{slug}/models",
            body=body,
            params=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def delete(
        self,
        *,
        slug: str,
        slugs: str,
    ) -> GenericResponse:
        query = {
            "slugs": slugs,
        }
        filtered_query = {k: v for k, v in query.items() if v is not None}
        query_string = urlencode(filtered_query)
        return await self._delete(
            f"{PortkeyApiPaths.INTEGRATIONS_API}/{slug}/models?{query_string}",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )
