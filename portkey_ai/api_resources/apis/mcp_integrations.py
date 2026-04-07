from typing import Any, Dict, List, Literal, Union
from portkey_ai._vendor.openai import NOT_GIVEN, NotGiven
from portkey_ai.api_resources.base_client import APIClient, AsyncAPIClient
from urllib.parse import urlencode
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.types.mcp_type import (
    McpIntegrationCreateResponse,
    McpIntegrationRetrieveResponse,
    McpIntegrationListResponse,
    McpIntegrationUpdateResponse,
    McpIntegrationDeleteResponse,
    McpIntegrationSyncResponse,
    McpIntegrationTestResponse,
    McpIntegrationWorkspacesResponse,
    McpIntegrationCapabilitiesResponse,
    McpIntegrationMetadataResponse,
)
from portkey_ai.api_resources.utils import GenericResponse

MCP_INTEGRATIONS_API_PATH = "/mcp-integrations"


class McpIntegrationWorkspaces(APIResource):
    """MCP Integration Workspaces API."""

    def __init__(self, client: APIClient) -> None:
        super().__init__(client)

    def list(
        self,
        *,
        mcp_integration_id: str,
    ) -> McpIntegrationWorkspacesResponse:
        """List workspaces for an MCP integration."""
        return self._get(
            f"{MCP_INTEGRATIONS_API_PATH}/{mcp_integration_id}/workspaces",
            params=None,
            body=None,
            cast_to=McpIntegrationWorkspacesResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def update(
        self,
        *,
        mcp_integration_id: str,
        workspaces: Union[List[Dict[str, Any]], NotGiven] = NOT_GIVEN,
        global_workspace_access: Union[Dict[str, Any], NotGiven] = NOT_GIVEN,
        **kwargs: Any,
    ) -> GenericResponse:
        """Update workspaces for an MCP integration."""
        body = {
            "workspaces": workspaces,
            "global_workspace_access": global_workspace_access,
            **kwargs,
        }
        return self._put(
            f"{MCP_INTEGRATIONS_API_PATH}/{mcp_integration_id}/workspaces",
            body=body,
            params=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )


class McpIntegrationCapabilities(APIResource):
    """MCP Integration Capabilities API."""

    def __init__(self, client: APIClient) -> None:
        super().__init__(client)

    def list(
        self,
        *,
        mcp_integration_id: str,
    ) -> McpIntegrationCapabilitiesResponse:
        """List capabilities for an MCP integration."""
        return self._get(
            f"{MCP_INTEGRATIONS_API_PATH}/{mcp_integration_id}/capabilities",
            params=None,
            body=None,
            cast_to=McpIntegrationCapabilitiesResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def update(
        self,
        *,
        mcp_integration_id: str,
        capabilities: List[Dict[str, Any]],
        **kwargs: Any,
    ) -> GenericResponse:
        """Update capabilities for an MCP integration."""
        body = {
            "capabilities": capabilities,
            **kwargs,
        }
        return self._put(
            f"{MCP_INTEGRATIONS_API_PATH}/{mcp_integration_id}/capabilities",
            body=body,
            params=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )


class McpIntegrationMetadata(APIResource):
    """MCP Integration Metadata API."""

    def __init__(self, client: APIClient) -> None:
        super().__init__(client)

    def retrieve(
        self,
        *,
        mcp_integration_id: str,
    ) -> McpIntegrationMetadataResponse:
        """Get metadata for an MCP integration."""
        return self._get(
            f"{MCP_INTEGRATIONS_API_PATH}/{mcp_integration_id}/metadata",
            params=None,
            body=None,
            cast_to=McpIntegrationMetadataResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )


class McpIntegrations(APIResource):
    """MCP Integrations API for managing MCP integration configurations."""

    workspaces: McpIntegrationWorkspaces
    capabilities: McpIntegrationCapabilities
    metadata: McpIntegrationMetadata

    def __init__(self, client: APIClient) -> None:
        super().__init__(client)
        self.workspaces = McpIntegrationWorkspaces(client)
        self.capabilities = McpIntegrationCapabilities(client)
        self.metadata = McpIntegrationMetadata(client)

    def create(
        self,
        *,
        name: str,
        url: str,
        auth_type: Literal["oauth_auto", "oauth_client_credentials", "headers", "none"],
        transport: Literal["http", "sse"],
        description: Union[str, NotGiven] = NOT_GIVEN,
        workspace_id: Union[str, NotGiven] = NOT_GIVEN,
        organisation_id: Union[str, NotGiven] = NOT_GIVEN,
        configurations: Union[Dict[str, Any], NotGiven] = NOT_GIVEN,
        **kwargs: Any,
    ) -> McpIntegrationCreateResponse:
        """Create a new MCP integration."""
        body = {
            "name": name,
            "url": url,
            "auth_type": auth_type,
            "transport": transport,
            "description": description,
            "workspace_id": workspace_id,
            "organisation_id": organisation_id,
            "configurations": configurations,
            **kwargs,
        }
        return self._post(
            MCP_INTEGRATIONS_API_PATH,
            body=body,
            params=None,
            cast_to=McpIntegrationCreateResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def list(
        self,
        *,
        organisation_id: Union[str, NotGiven] = NOT_GIVEN,
        type: Union[Literal["workspace", "organisation", "all"], NotGiven] = NOT_GIVEN,
        workspace_id: Union[str, NotGiven] = NOT_GIVEN,
        current_page: Union[int, NotGiven] = NOT_GIVEN,
        page_size: Union[int, NotGiven] = NOT_GIVEN,
        search: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs: Any,
    ) -> McpIntegrationListResponse:
        """List MCP integrations."""
        query = {
            "organisation_id": organisation_id,
            "type": type,
            "workspace_id": workspace_id,
            "current_page": current_page,
            "page_size": page_size,
            "search": search,
            **kwargs,
        }
        filtered_query = {k: v for k, v in query.items() if v is not NOT_GIVEN}
        query_string = urlencode(filtered_query) if filtered_query else ""
        url = (
            f"{MCP_INTEGRATIONS_API_PATH}?{query_string}"
            if query_string
            else MCP_INTEGRATIONS_API_PATH
        )
        return self._get(
            url,
            params=None,
            body=None,
            cast_to=McpIntegrationListResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def retrieve(
        self,
        *,
        mcp_integration_id: str,
    ) -> McpIntegrationRetrieveResponse:
        """Retrieve an MCP integration by ID."""
        return self._get(
            f"{MCP_INTEGRATIONS_API_PATH}/{mcp_integration_id}",
            params=None,
            body=None,
            cast_to=McpIntegrationRetrieveResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def update(
        self,
        *,
        mcp_integration_id: str,
        name: Union[str, NotGiven] = NOT_GIVEN,
        description: Union[str, NotGiven] = NOT_GIVEN,
        configurations: Union[Dict[str, Any], NotGiven] = NOT_GIVEN,
        url: Union[str, NotGiven] = NOT_GIVEN,
        auth_type: Union[
            Literal["oauth_auto", "oauth_client_credentials", "headers", "none"],
            NotGiven,
        ] = NOT_GIVEN,
        transport: Union[Literal["http", "sse"], NotGiven] = NOT_GIVEN,
        **kwargs: Any,
    ) -> McpIntegrationUpdateResponse:
        """Update an MCP integration."""
        body = {
            "name": name,
            "description": description,
            "configurations": configurations,
            "url": url,
            "auth_type": auth_type,
            "transport": transport,
            **kwargs,
        }
        return self._put(
            f"{MCP_INTEGRATIONS_API_PATH}/{mcp_integration_id}",
            body=body,
            params=None,
            cast_to=McpIntegrationUpdateResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def delete(
        self,
        *,
        mcp_integration_id: str,
    ) -> McpIntegrationDeleteResponse:
        """Delete an MCP integration."""
        return self._delete(
            f"{MCP_INTEGRATIONS_API_PATH}/{mcp_integration_id}",
            params=None,
            body=None,
            cast_to=McpIntegrationDeleteResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def sync(
        self,
        *,
        mcp_integration_id: str,
        server_info: Union[Dict[str, Any], NotGiven] = NOT_GIVEN,
        capabilities: Union[List[Dict[str, Any]], NotGiven] = NOT_GIVEN,
        **kwargs: Any,
    ) -> McpIntegrationSyncResponse:
        """Sync an MCP integration."""
        body = {
            "server_info": server_info,
            "capabilities": capabilities,
            **kwargs,
        }
        return self._post(
            f"{MCP_INTEGRATIONS_API_PATH}/{mcp_integration_id}/sync",
            body=body,
            params=None,
            cast_to=McpIntegrationSyncResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def test(
        self,
        *,
        mcp_integration_id: str,
    ) -> McpIntegrationTestResponse:
        """Test an MCP integration connection."""
        return self._post(
            f"{MCP_INTEGRATIONS_API_PATH}/{mcp_integration_id}/test",
            body=None,
            params=None,
            cast_to=McpIntegrationTestResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )


class AsyncMcpIntegrationWorkspaces(AsyncAPIResource):
    """Async MCP Integration Workspaces API."""

    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)

    async def list(
        self,
        *,
        mcp_integration_id: str,
    ) -> McpIntegrationWorkspacesResponse:
        """List workspaces for an MCP integration."""
        return await self._get(
            f"{MCP_INTEGRATIONS_API_PATH}/{mcp_integration_id}/workspaces",
            params=None,
            body=None,
            cast_to=McpIntegrationWorkspacesResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def update(
        self,
        *,
        mcp_integration_id: str,
        workspaces: Union[List[Dict[str, Any]], NotGiven] = NOT_GIVEN,
        global_workspace_access: Union[Dict[str, Any], NotGiven] = NOT_GIVEN,
        **kwargs: Any,
    ) -> GenericResponse:
        """Update workspaces for an MCP integration."""
        body = {
            "workspaces": workspaces,
            "global_workspace_access": global_workspace_access,
            **kwargs,
        }
        return await self._put(
            f"{MCP_INTEGRATIONS_API_PATH}/{mcp_integration_id}/workspaces",
            body=body,
            params=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )


class AsyncMcpIntegrationCapabilities(AsyncAPIResource):
    """Async MCP Integration Capabilities API."""

    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)

    async def list(
        self,
        *,
        mcp_integration_id: str,
    ) -> McpIntegrationCapabilitiesResponse:
        """List capabilities for an MCP integration."""
        return await self._get(
            f"{MCP_INTEGRATIONS_API_PATH}/{mcp_integration_id}/capabilities",
            params=None,
            body=None,
            cast_to=McpIntegrationCapabilitiesResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def update(
        self,
        *,
        mcp_integration_id: str,
        capabilities: List[Dict[str, Any]],
        **kwargs: Any,
    ) -> GenericResponse:
        """Update capabilities for an MCP integration."""
        body = {
            "capabilities": capabilities,
            **kwargs,
        }
        return await self._put(
            f"{MCP_INTEGRATIONS_API_PATH}/{mcp_integration_id}/capabilities",
            body=body,
            params=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )


class AsyncMcpIntegrationMetadata(AsyncAPIResource):
    """Async MCP Integration Metadata API."""

    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)

    async def retrieve(
        self,
        *,
        mcp_integration_id: str,
    ) -> McpIntegrationMetadataResponse:
        """Get metadata for an MCP integration."""
        return await self._get(
            f"{MCP_INTEGRATIONS_API_PATH}/{mcp_integration_id}/metadata",
            params=None,
            body=None,
            cast_to=McpIntegrationMetadataResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )


class AsyncMcpIntegrations(AsyncAPIResource):
    """Async MCP Integrations API for managing MCP integration configurations."""

    workspaces: AsyncMcpIntegrationWorkspaces
    capabilities: AsyncMcpIntegrationCapabilities
    metadata: AsyncMcpIntegrationMetadata

    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)
        self.workspaces = AsyncMcpIntegrationWorkspaces(client)
        self.capabilities = AsyncMcpIntegrationCapabilities(client)
        self.metadata = AsyncMcpIntegrationMetadata(client)

    async def create(
        self,
        *,
        name: str,
        url: str,
        auth_type: Literal["oauth_auto", "oauth_client_credentials", "headers", "none"],
        transport: Literal["http", "sse"],
        description: Union[str, NotGiven] = NOT_GIVEN,
        workspace_id: Union[str, NotGiven] = NOT_GIVEN,
        organisation_id: Union[str, NotGiven] = NOT_GIVEN,
        configurations: Union[Dict[str, Any], NotGiven] = NOT_GIVEN,
        **kwargs: Any,
    ) -> McpIntegrationCreateResponse:
        """Create a new MCP integration."""
        body = {
            "name": name,
            "url": url,
            "auth_type": auth_type,
            "transport": transport,
            "description": description,
            "workspace_id": workspace_id,
            "organisation_id": organisation_id,
            "configurations": configurations,
            **kwargs,
        }
        return await self._post(
            MCP_INTEGRATIONS_API_PATH,
            body=body,
            params=None,
            cast_to=McpIntegrationCreateResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def list(
        self,
        *,
        organisation_id: Union[str, NotGiven] = NOT_GIVEN,
        type: Union[Literal["workspace", "organisation", "all"], NotGiven] = NOT_GIVEN,
        workspace_id: Union[str, NotGiven] = NOT_GIVEN,
        current_page: Union[int, NotGiven] = NOT_GIVEN,
        page_size: Union[int, NotGiven] = NOT_GIVEN,
        search: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs: Any,
    ) -> McpIntegrationListResponse:
        """List MCP integrations."""
        query = {
            "organisation_id": organisation_id,
            "type": type,
            "workspace_id": workspace_id,
            "current_page": current_page,
            "page_size": page_size,
            "search": search,
            **kwargs,
        }
        filtered_query = {k: v for k, v in query.items() if v is not NOT_GIVEN}
        query_string = urlencode(filtered_query) if filtered_query else ""
        url = (
            f"{MCP_INTEGRATIONS_API_PATH}?{query_string}"
            if query_string
            else MCP_INTEGRATIONS_API_PATH
        )
        return await self._get(
            url,
            params=None,
            body=None,
            cast_to=McpIntegrationListResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def retrieve(
        self,
        *,
        mcp_integration_id: str,
    ) -> McpIntegrationRetrieveResponse:
        """Retrieve an MCP integration by ID."""
        return await self._get(
            f"{MCP_INTEGRATIONS_API_PATH}/{mcp_integration_id}",
            params=None,
            body=None,
            cast_to=McpIntegrationRetrieveResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def update(
        self,
        *,
        mcp_integration_id: str,
        name: Union[str, NotGiven] = NOT_GIVEN,
        description: Union[str, NotGiven] = NOT_GIVEN,
        configurations: Union[Dict[str, Any], NotGiven] = NOT_GIVEN,
        url: Union[str, NotGiven] = NOT_GIVEN,
        auth_type: Union[
            Literal["oauth_auto", "oauth_client_credentials", "headers", "none"],
            NotGiven,
        ] = NOT_GIVEN,
        transport: Union[Literal["http", "sse"], NotGiven] = NOT_GIVEN,
        **kwargs: Any,
    ) -> McpIntegrationUpdateResponse:
        """Update an MCP integration."""
        body = {
            "name": name,
            "description": description,
            "configurations": configurations,
            "url": url,
            "auth_type": auth_type,
            "transport": transport,
            **kwargs,
        }
        return await self._put(
            f"{MCP_INTEGRATIONS_API_PATH}/{mcp_integration_id}",
            body=body,
            params=None,
            cast_to=McpIntegrationUpdateResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def delete(
        self,
        *,
        mcp_integration_id: str,
    ) -> McpIntegrationDeleteResponse:
        """Delete an MCP integration."""
        return await self._delete(
            f"{MCP_INTEGRATIONS_API_PATH}/{mcp_integration_id}",
            params=None,
            body=None,
            cast_to=McpIntegrationDeleteResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def sync(
        self,
        *,
        mcp_integration_id: str,
        server_info: Union[Dict[str, Any], NotGiven] = NOT_GIVEN,
        capabilities: Union[List[Dict[str, Any]], NotGiven] = NOT_GIVEN,
        **kwargs: Any,
    ) -> McpIntegrationSyncResponse:
        """Sync an MCP integration."""
        body = {
            "server_info": server_info,
            "capabilities": capabilities,
            **kwargs,
        }
        return await self._post(
            f"{MCP_INTEGRATIONS_API_PATH}/{mcp_integration_id}/sync",
            body=body,
            params=None,
            cast_to=McpIntegrationSyncResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def test(
        self,
        *,
        mcp_integration_id: str,
    ) -> McpIntegrationTestResponse:
        """Test an MCP integration connection."""
        return await self._post(
            f"{MCP_INTEGRATIONS_API_PATH}/{mcp_integration_id}/test",
            body=None,
            params=None,
            cast_to=McpIntegrationTestResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )
