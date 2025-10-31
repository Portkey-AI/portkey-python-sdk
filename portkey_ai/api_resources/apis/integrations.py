from typing import Any, Dict, List, Literal, Optional, Union
from portkey_ai._vendor.openai import NOT_GIVEN, NotGiven
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
        name: Union[str, NotGiven] = NOT_GIVEN,
        description: Union[str, NotGiven] = NOT_GIVEN,
        key: Union[str, NotGiven] = NOT_GIVEN,
        ai_provider_id: Union[str, NotGiven] = NOT_GIVEN,
        workspace_id: Union[str, NotGiven] = NOT_GIVEN,
        slug: Union[str, NotGiven] = NOT_GIVEN,
        configurations: Union[Dict[str, Any], NotGiven] = NOT_GIVEN,
        **kwargs: Any,
    ) -> IntegrationCreateResponse:
        body = {
            "name": name,
            "description": description,
            "key": key,
            "ai_provider_id": ai_provider_id,
            "workspace_id": workspace_id,
            "slug": slug,
            "configurations": configurations,
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
        workspace_id: Union[str, NotGiven] = NOT_GIVEN,
        type: Union[Literal["workspace", "organisation", "all"], NotGiven] = NOT_GIVEN,
    ) -> IntegrationListResponse:
        query = {
            "current_page": current_page,
            "page_size": page_size,
            "workspace_id": workspace_id,
            "type": type,
        }
        filtered_query = {k: v for k, v in query.items() if v is not NOT_GIVEN}
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
        name: Union[str, NotGiven] = NOT_GIVEN,
        description: Union[str, NotGiven] = NOT_GIVEN,
        key: Union[str, NotGiven] = NOT_GIVEN,
        configurations: Union[Dict[str, Any], NotGiven] = NOT_GIVEN,
        **kwargs: Any,
    ) -> GenericResponse:
        body = {
            "name": name,
            "description": description,
            "key": key,
            "configurations": configurations,
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
        global_workspace_access: Union[Dict[str, Any], NotGiven] = NOT_GIVEN,
        override_existing_workspaces_access: Union[bool, NotGiven] = NOT_GIVEN,
        workspaces: Union[List[Dict[str, Any]], NotGiven] = NOT_GIVEN,
        **kwargs: Any,
    ) -> GenericResponse:
        body = {
            "global_workspace_access": global_workspace_access,
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
        allow_all_models: Union[bool, NotGiven] = NOT_GIVEN,
        models: Union[List[Dict[str, Any]], NotGiven] = NOT_GIVEN,
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
        filtered_query = {k: v for k, v in query.items() if v is not NOT_GIVEN}
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
        name: Union[str, NotGiven] = NOT_GIVEN,
        description: Union[str, NotGiven] = NOT_GIVEN,
        key: Union[str, NotGiven] = NOT_GIVEN,
        ai_provider_id: Union[str, NotGiven] = NOT_GIVEN,
        workspace_id: Union[str, NotGiven] = NOT_GIVEN,
        slug: Union[str, NotGiven] = NOT_GIVEN,
        configurations: Union[Dict[str, Any], NotGiven] = NOT_GIVEN,
        **kwargs: Any,
    ) -> IntegrationCreateResponse:
        body = {
            "name": name,
            "description": description,
            "key": key,
            "ai_provider_id": ai_provider_id,
            "workspace_id": workspace_id,
            "slug": slug,
            "configurations": configurations,
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
        workspace_id: Union[str, NotGiven] = NOT_GIVEN,
        type: Union[Literal["workspace", "organisation", "all"], NotGiven] = NOT_GIVEN,
    ) -> IntegrationListResponse:
        query = {
            "current_page": current_page,
            "page_size": page_size,
            "workspace_id": workspace_id,
            "type": type,
        }
        filtered_query = {k: v for k, v in query.items() if v is not NOT_GIVEN}
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
        name: Union[str, NotGiven] = NOT_GIVEN,
        description: Union[str, NotGiven] = NOT_GIVEN,
        key: Union[str, NotGiven] = NOT_GIVEN,
        configurations: Union[Dict[str, Any], NotGiven] = NOT_GIVEN,
        **kwargs: Any,
    ) -> GenericResponse:
        body = {
            "name": name,
            "description": description,
            "key": key,
            "configurations": configurations,
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
        global_workspace_access: Union[Dict[str, Any], NotGiven] = NOT_GIVEN,
        override_existing_workspaces_access: Union[bool, NotGiven] = NOT_GIVEN,
        workspaces: Union[List[Dict[str, Any]], NotGiven] = NOT_GIVEN,
        **kwargs: Any,
    ) -> GenericResponse:
        body = {
            "global_workspace_access": global_workspace_access,
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
        allow_all_models: Union[bool, NotGiven] = NOT_GIVEN,
        models: Union[List[Dict[str, Any]], NotGiven] = NOT_GIVEN,
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
        filtered_query = {k: v for k, v in query.items() if v is not NOT_GIVEN}
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
