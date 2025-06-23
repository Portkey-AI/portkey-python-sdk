from typing import Any, Dict, List, Optional
from portkey_ai.api_resources.base_client import APIClient, AsyncAPIClient
from urllib.parse import urlencode
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
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
    ) -> GenericResponse:
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
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def list(
        self,
        *,
        organisation_id: Optional[str] = None,
        workspace_id: Optional[str] = None,
        current_page: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> GenericResponse:
        query = {
            "organisation_id": organisation_id,
            "workspace_id": workspace_id,
            "current_page": current_page,
            "page_size": page_size,
        }
        filtered_query = {k: v for k, v in query.items() if v is not None}
        query_string = urlencode(filtered_query)
        return self._get(
            f"{PortkeyApiPaths.INTEGRATIONS_API}?{query_string}",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def retrieve(self, *, integration_id: Optional[str]) -> Any:
        return self._get(
            f"{PortkeyApiPaths.INTEGRATIONS_API}/{integration_id}",
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
        integration_id: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        key: Optional[str] = None,
        configuration: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> GenericResponse:
        body = {
            "name": name,
            "description": description,
            "key": key,
            "configuration": configuration,
            **kwargs,
        }
        return self._put(
            f"{PortkeyApiPaths.INTEGRATIONS_API}/{integration_id}",
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
        integration_id: Optional[str],
    ) -> Any:
        return self._delete(
            f"{PortkeyApiPaths.INTEGRATIONS_API}/{integration_id}",
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
        provider_integration_id: Optional[str] = None,
    ) -> GenericResponse:
        return self._get(
            f"{PortkeyApiPaths.INTEGRATIONS_API}/{provider_integration_id}/workspaces",
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
        provider_integration_id: Optional[str] = None,
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
            f"{PortkeyApiPaths.INTEGRATIONS_API}/{provider_integration_id}/workspaces",
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
        provider_integration_id: Optional[str] = None,
    ) -> GenericResponse:
        return self._get(
            f"{PortkeyApiPaths.INTEGRATIONS_API}/{provider_integration_id}/models",
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
        provider_integration_id: Optional[str] = None,
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
            f"{PortkeyApiPaths.INTEGRATIONS_API}/{provider_integration_id}/models",
            body=body,
            params=None,
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
    ) -> GenericResponse:
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
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def list(
        self,
        *,
        organisation_id: Optional[str] = None,
        workspace_id: Optional[str] = None,
        current_page: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> GenericResponse:
        query = {
            "organisation_id": organisation_id,
            "workspace_id": workspace_id,
            "current_page": current_page,
            "page_size": page_size,
        }
        filtered_query = {k: v for k, v in query.items() if v is not None}
        query_string = urlencode(filtered_query)
        return await self._get(
            f"{PortkeyApiPaths.INTEGRATIONS_API}?{query_string}",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def retrieve(self, *, integration_id: Optional[str]) -> Any:
        return await self._get(
            f"{PortkeyApiPaths.INTEGRATIONS_API}/{integration_id}",
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
        integration_id: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        key: Optional[str] = None,
        configuration: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> GenericResponse:
        body = {
            "name": name,
            "description": description,
            "key": key,
            "configuration": configuration,
            **kwargs,
        }
        return await self._put(
            f"{PortkeyApiPaths.INTEGRATIONS_API}/{integration_id}",
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
        integration_id: Optional[str],
    ) -> Any:
        return await self._delete(
            f"{PortkeyApiPaths.INTEGRATIONS_API}/{integration_id}",
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
        provider_integration_id: Optional[str] = None,
    ) -> GenericResponse:
        return await self._get(
            f"{PortkeyApiPaths.INTEGRATIONS_API}/{provider_integration_id}/workspaces",
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
        provider_integration_id: Optional[str] = None,
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
            f"{PortkeyApiPaths.INTEGRATIONS_API}/{provider_integration_id}/workspaces",
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
        provider_integration_id: Optional[str] = None,
    ) -> GenericResponse:
        return await self._get(
            f"{PortkeyApiPaths.INTEGRATIONS_API}/{provider_integration_id}/models",
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
        provider_integration_id: Optional[str] = None,
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
            f"{PortkeyApiPaths.INTEGRATIONS_API}/{provider_integration_id}/models",
            body=body,
            params=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )
