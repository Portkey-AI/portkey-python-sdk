from typing import Any, Dict, List, Union
from portkey_ai._vendor.openai import NOT_GIVEN, NotGiven
from portkey_ai.api_resources.base_client import APIClient, AsyncAPIClient
from urllib.parse import urlencode
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.types.mcp_servers_type import (
    McpServerCreateResponse,
    McpServerRetrieveResponse,
    McpServerListResponse,
    McpServerUpdateResponse,
    McpServerDeleteResponse,
    McpServerTestResponse,
    McpServerTokensResponse,
    McpServerClientInfoResponse,
    McpServerCapabilitiesResponse,
    McpServerUserAccessResponse,
    McpServerUserAccessCheckResponse,
    McpServerMetadataResponse,
)
from portkey_ai.api_resources.utils import GenericResponse

MCP_SERVERS_API_PATH = "/mcp-servers"


class McpServerCapabilities(APIResource):
    """MCP Server Capabilities API."""

    def __init__(self, client: APIClient) -> None:
        super().__init__(client)

    def list(
        self,
        *,
        mcp_server_id: str,
    ) -> McpServerCapabilitiesResponse:
        """List capabilities for an MCP server."""
        return self._get(
            f"{MCP_SERVERS_API_PATH}/{mcp_server_id}/capabilities",
            params=None,
            body=None,
            cast_to=McpServerCapabilitiesResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def update(
        self,
        *,
        mcp_server_id: str,
        capabilities: List[Dict[str, Any]],
        **kwargs: Any,
    ) -> GenericResponse:
        """Update capabilities for an MCP server."""
        body = {
            "capabilities": capabilities,
            **kwargs,
        }
        return self._put(
            f"{MCP_SERVERS_API_PATH}/{mcp_server_id}/capabilities",
            body=body,
            params=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def sync(
        self,
        *,
        mcp_server_id: str,
        capabilities: Union[List[Dict[str, Any]], NotGiven] = NOT_GIVEN,
        **kwargs: Any,
    ) -> GenericResponse:
        """Sync capabilities for an MCP server."""
        body = {
            "capabilities": capabilities,
            **kwargs,
        }
        return self._post(
            f"{MCP_SERVERS_API_PATH}/{mcp_server_id}/capabilities/sync",
            body=body,
            params=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )


class McpServerUserAccess(APIResource):
    """MCP Server User Access API."""

    def __init__(self, client: APIClient) -> None:
        super().__init__(client)

    def check(
        self,
        *,
        mcp_server_id: str,
    ) -> McpServerUserAccessCheckResponse:
        """Check user access for an MCP server."""
        return self._get(
            f"{MCP_SERVERS_API_PATH}/{mcp_server_id}/user-access/check",
            params=None,
            body=None,
            cast_to=McpServerUserAccessCheckResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def list(
        self,
        *,
        mcp_server_id: str,
    ) -> McpServerUserAccessResponse:
        """List user access for an MCP server."""
        return self._get(
            f"{MCP_SERVERS_API_PATH}/{mcp_server_id}/user-access",
            params=None,
            body=None,
            cast_to=McpServerUserAccessResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def update(
        self,
        *,
        mcp_server_id: str,
        user_access: Union[List[Dict[str, Any]], NotGiven] = NOT_GIVEN,
        default_user_access: Union[Dict[str, Any], NotGiven] = NOT_GIVEN,
        **kwargs: Any,
    ) -> GenericResponse:
        """Update user access for an MCP server."""
        body = {
            "user_access": user_access,
            "default_user_access": default_user_access,
            **kwargs,
        }
        return self._put(
            f"{MCP_SERVERS_API_PATH}/{mcp_server_id}/user-access",
            body=body,
            params=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )


class McpServerMetadata(APIResource):
    """MCP Server Metadata API."""

    def __init__(self, client: APIClient) -> None:
        super().__init__(client)

    def retrieve(
        self,
        *,
        mcp_server_id: str,
    ) -> McpServerMetadataResponse:
        """Get metadata for an MCP server."""
        return self._get(
            f"{MCP_SERVERS_API_PATH}/{mcp_server_id}/metadata",
            params=None,
            body=None,
            cast_to=McpServerMetadataResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def sync(
        self,
        *,
        mcp_server_id: str,
        server_name: Union[str, NotGiven] = NOT_GIVEN,
        server_version: Union[str, NotGiven] = NOT_GIVEN,
        protocol_version: Union[str, NotGiven] = NOT_GIVEN,
        title: Union[str, NotGiven] = NOT_GIVEN,
        description: Union[str, NotGiven] = NOT_GIVEN,
        website_url: Union[str, NotGiven] = NOT_GIVEN,
        icons: Union[Dict[str, Any], NotGiven] = NOT_GIVEN,
        capability_flags: Union[Dict[str, Any], NotGiven] = NOT_GIVEN,
        instructions: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs: Any,
    ) -> GenericResponse:
        """Sync metadata for an MCP server."""
        body = {
            "server_name": server_name,
            "server_version": server_version,
            "protocol_version": protocol_version,
            "title": title,
            "description": description,
            "website_url": website_url,
            "icons": icons,
            "capability_flags": capability_flags,
            "instructions": instructions,
            **kwargs,
        }
        return self._post(
            f"{MCP_SERVERS_API_PATH}/{mcp_server_id}/metadata/sync",
            body=body,
            params=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )


class McpServers(APIResource):
    """MCP Servers API for managing MCP server configurations."""

    capabilities: McpServerCapabilities
    user_access: McpServerUserAccess
    metadata: McpServerMetadata

    def __init__(self, client: APIClient) -> None:
        super().__init__(client)
        self.capabilities = McpServerCapabilities(client)
        self.user_access = McpServerUserAccess(client)
        self.metadata = McpServerMetadata(client)

    def create(
        self,
        *,
        name: str,
        mcp_integration_id: str,
        description: Union[str, NotGiven] = NOT_GIVEN,
        workspace_id: Union[str, NotGiven] = NOT_GIVEN,
        slug: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs: Any,
    ) -> McpServerCreateResponse:
        """Create a new MCP server."""
        body = {
            "name": name,
            "mcp_integration_id": mcp_integration_id,
            "description": description,
            "workspace_id": workspace_id,
            "slug": slug,
            **kwargs,
        }
        return self._post(
            MCP_SERVERS_API_PATH,
            body=body,
            params=None,
            cast_to=McpServerCreateResponse,
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
        id: Union[str, NotGiven] = NOT_GIVEN,
        search: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs: Any,
    ) -> McpServerListResponse:
        """List MCP servers."""
        query = {
            "workspace_id": workspace_id,
            "current_page": current_page,
            "page_size": page_size,
            "id": id,
            "search": search,
            **kwargs,
        }
        filtered_query = {k: v for k, v in query.items() if v is not NOT_GIVEN}
        query_string = urlencode(filtered_query) if filtered_query else ""
        url = (
            f"{MCP_SERVERS_API_PATH}?{query_string}"
            if query_string
            else MCP_SERVERS_API_PATH
        )
        return self._get(
            url,
            params=None,
            body=None,
            cast_to=McpServerListResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def retrieve(
        self,
        *,
        mcp_server_id: str,
    ) -> McpServerRetrieveResponse:
        """Retrieve an MCP server by ID."""
        return self._get(
            f"{MCP_SERVERS_API_PATH}/{mcp_server_id}",
            params=None,
            body=None,
            cast_to=McpServerRetrieveResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def update(
        self,
        *,
        mcp_server_id: str,
        name: Union[str, NotGiven] = NOT_GIVEN,
        description: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs: Any,
    ) -> McpServerUpdateResponse:
        """Update an MCP server."""
        body = {
            "name": name,
            "description": description,
            **kwargs,
        }
        return self._put(
            f"{MCP_SERVERS_API_PATH}/{mcp_server_id}",
            body=body,
            params=None,
            cast_to=McpServerUpdateResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def delete(
        self,
        *,
        mcp_server_id: str,
    ) -> McpServerDeleteResponse:
        """Delete an MCP server."""
        return self._delete(
            f"{MCP_SERVERS_API_PATH}/{mcp_server_id}",
            params=None,
            body=None,
            cast_to=McpServerDeleteResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def test(
        self,
        *,
        mcp_server_id: str,
    ) -> McpServerTestResponse:
        """Test an MCP server connection."""
        return self._post(
            f"{MCP_SERVERS_API_PATH}/{mcp_server_id}/test",
            body=None,
            params=None,
            cast_to=McpServerTestResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def get_tokens(
        self,
        *,
        mcp_server_id: str,
    ) -> McpServerTokensResponse:
        """Get tokens for an MCP server."""
        return self._get(
            f"{MCP_SERVERS_API_PATH}/{mcp_server_id}/tokens",
            params=None,
            body=None,
            cast_to=McpServerTokensResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def update_tokens(
        self,
        *,
        mcp_server_id: str,
        access_token: str,
        refresh_token: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs: Any,
    ) -> GenericResponse:
        """Update tokens for an MCP server."""
        body = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            **kwargs,
        }
        return self._put(
            f"{MCP_SERVERS_API_PATH}/{mcp_server_id}/tokens",
            body=body,
            params=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def delete_tokens(
        self,
        *,
        mcp_server_id: str,
    ) -> GenericResponse:
        """Delete tokens for an MCP server."""
        return self._delete(
            f"{MCP_SERVERS_API_PATH}/{mcp_server_id}/tokens",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def get_client_info(
        self,
        *,
        mcp_server_id: str,
    ) -> McpServerClientInfoResponse:
        """Get client info for an MCP server."""
        return self._get(
            f"{MCP_SERVERS_API_PATH}/{mcp_server_id}/client-info",
            params=None,
            body=None,
            cast_to=McpServerClientInfoResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )


class AsyncMcpServerCapabilities(AsyncAPIResource):
    """Async MCP Server Capabilities API."""

    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)

    async def list(
        self,
        *,
        mcp_server_id: str,
    ) -> McpServerCapabilitiesResponse:
        """List capabilities for an MCP server."""
        return await self._get(
            f"{MCP_SERVERS_API_PATH}/{mcp_server_id}/capabilities",
            params=None,
            body=None,
            cast_to=McpServerCapabilitiesResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def update(
        self,
        *,
        mcp_server_id: str,
        capabilities: List[Dict[str, Any]],
        **kwargs: Any,
    ) -> GenericResponse:
        """Update capabilities for an MCP server."""
        body = {
            "capabilities": capabilities,
            **kwargs,
        }
        return await self._put(
            f"{MCP_SERVERS_API_PATH}/{mcp_server_id}/capabilities",
            body=body,
            params=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def sync(
        self,
        *,
        mcp_server_id: str,
        capabilities: Union[List[Dict[str, Any]], NotGiven] = NOT_GIVEN,
        **kwargs: Any,
    ) -> GenericResponse:
        """Sync capabilities for an MCP server."""
        body = {
            "capabilities": capabilities,
            **kwargs,
        }
        return await self._post(
            f"{MCP_SERVERS_API_PATH}/{mcp_server_id}/capabilities/sync",
            body=body,
            params=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )


class AsyncMcpServerUserAccess(AsyncAPIResource):
    """Async MCP Server User Access API."""

    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)

    async def check(
        self,
        *,
        mcp_server_id: str,
    ) -> McpServerUserAccessCheckResponse:
        """Check user access for an MCP server."""
        return await self._get(
            f"{MCP_SERVERS_API_PATH}/{mcp_server_id}/user-access/check",
            params=None,
            body=None,
            cast_to=McpServerUserAccessCheckResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def list(
        self,
        *,
        mcp_server_id: str,
    ) -> McpServerUserAccessResponse:
        """List user access for an MCP server."""
        return await self._get(
            f"{MCP_SERVERS_API_PATH}/{mcp_server_id}/user-access",
            params=None,
            body=None,
            cast_to=McpServerUserAccessResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def update(
        self,
        *,
        mcp_server_id: str,
        user_access: Union[List[Dict[str, Any]], NotGiven] = NOT_GIVEN,
        default_user_access: Union[Dict[str, Any], NotGiven] = NOT_GIVEN,
        **kwargs: Any,
    ) -> GenericResponse:
        """Update user access for an MCP server."""
        body = {
            "user_access": user_access,
            "default_user_access": default_user_access,
            **kwargs,
        }
        return await self._put(
            f"{MCP_SERVERS_API_PATH}/{mcp_server_id}/user-access",
            body=body,
            params=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )


class AsyncMcpServerMetadata(AsyncAPIResource):
    """Async MCP Server Metadata API."""

    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)

    async def retrieve(
        self,
        *,
        mcp_server_id: str,
    ) -> McpServerMetadataResponse:
        """Get metadata for an MCP server."""
        return await self._get(
            f"{MCP_SERVERS_API_PATH}/{mcp_server_id}/metadata",
            params=None,
            body=None,
            cast_to=McpServerMetadataResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def sync(
        self,
        *,
        mcp_server_id: str,
        server_name: Union[str, NotGiven] = NOT_GIVEN,
        server_version: Union[str, NotGiven] = NOT_GIVEN,
        protocol_version: Union[str, NotGiven] = NOT_GIVEN,
        title: Union[str, NotGiven] = NOT_GIVEN,
        description: Union[str, NotGiven] = NOT_GIVEN,
        website_url: Union[str, NotGiven] = NOT_GIVEN,
        icons: Union[Dict[str, Any], NotGiven] = NOT_GIVEN,
        capability_flags: Union[Dict[str, Any], NotGiven] = NOT_GIVEN,
        instructions: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs: Any,
    ) -> GenericResponse:
        """Sync metadata for an MCP server."""
        body = {
            "server_name": server_name,
            "server_version": server_version,
            "protocol_version": protocol_version,
            "title": title,
            "description": description,
            "website_url": website_url,
            "icons": icons,
            "capability_flags": capability_flags,
            "instructions": instructions,
            **kwargs,
        }
        return await self._post(
            f"{MCP_SERVERS_API_PATH}/{mcp_server_id}/metadata/sync",
            body=body,
            params=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )


class AsyncMcpServers(AsyncAPIResource):
    """Async MCP Servers API for managing MCP server configurations."""

    capabilities: AsyncMcpServerCapabilities
    user_access: AsyncMcpServerUserAccess
    metadata: AsyncMcpServerMetadata

    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)
        self.capabilities = AsyncMcpServerCapabilities(client)
        self.user_access = AsyncMcpServerUserAccess(client)
        self.metadata = AsyncMcpServerMetadata(client)

    async def create(
        self,
        *,
        name: str,
        mcp_integration_id: str,
        description: Union[str, NotGiven] = NOT_GIVEN,
        workspace_id: Union[str, NotGiven] = NOT_GIVEN,
        slug: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs: Any,
    ) -> McpServerCreateResponse:
        """Create a new MCP server."""
        body = {
            "name": name,
            "mcp_integration_id": mcp_integration_id,
            "description": description,
            "workspace_id": workspace_id,
            "slug": slug,
            **kwargs,
        }
        return await self._post(
            MCP_SERVERS_API_PATH,
            body=body,
            params=None,
            cast_to=McpServerCreateResponse,
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
        id: Union[str, NotGiven] = NOT_GIVEN,
        search: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs: Any,
    ) -> McpServerListResponse:
        """List MCP servers."""
        query = {
            "workspace_id": workspace_id,
            "current_page": current_page,
            "page_size": page_size,
            "id": id,
            "search": search,
            **kwargs,
        }
        filtered_query = {k: v for k, v in query.items() if v is not NOT_GIVEN}
        query_string = urlencode(filtered_query) if filtered_query else ""
        url = (
            f"{MCP_SERVERS_API_PATH}?{query_string}"
            if query_string
            else MCP_SERVERS_API_PATH
        )
        return await self._get(
            url,
            params=None,
            body=None,
            cast_to=McpServerListResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def retrieve(
        self,
        *,
        mcp_server_id: str,
    ) -> McpServerRetrieveResponse:
        """Retrieve an MCP server by ID."""
        return await self._get(
            f"{MCP_SERVERS_API_PATH}/{mcp_server_id}",
            params=None,
            body=None,
            cast_to=McpServerRetrieveResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def update(
        self,
        *,
        mcp_server_id: str,
        name: Union[str, NotGiven] = NOT_GIVEN,
        description: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs: Any,
    ) -> McpServerUpdateResponse:
        """Update an MCP server."""
        body = {
            "name": name,
            "description": description,
            **kwargs,
        }
        return await self._put(
            f"{MCP_SERVERS_API_PATH}/{mcp_server_id}",
            body=body,
            params=None,
            cast_to=McpServerUpdateResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def delete(
        self,
        *,
        mcp_server_id: str,
    ) -> McpServerDeleteResponse:
        """Delete an MCP server."""
        return await self._delete(
            f"{MCP_SERVERS_API_PATH}/{mcp_server_id}",
            params=None,
            body=None,
            cast_to=McpServerDeleteResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def test(
        self,
        *,
        mcp_server_id: str,
    ) -> McpServerTestResponse:
        """Test an MCP server connection."""
        return await self._post(
            f"{MCP_SERVERS_API_PATH}/{mcp_server_id}/test",
            body=None,
            params=None,
            cast_to=McpServerTestResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def get_tokens(
        self,
        *,
        mcp_server_id: str,
    ) -> McpServerTokensResponse:
        """Get tokens for an MCP server."""
        return await self._get(
            f"{MCP_SERVERS_API_PATH}/{mcp_server_id}/tokens",
            params=None,
            body=None,
            cast_to=McpServerTokensResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def update_tokens(
        self,
        *,
        mcp_server_id: str,
        access_token: str,
        refresh_token: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs: Any,
    ) -> GenericResponse:
        """Update tokens for an MCP server."""
        body = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            **kwargs,
        }
        return await self._put(
            f"{MCP_SERVERS_API_PATH}/{mcp_server_id}/tokens",
            body=body,
            params=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def delete_tokens(
        self,
        *,
        mcp_server_id: str,
    ) -> GenericResponse:
        """Delete tokens for an MCP server."""
        return await self._delete(
            f"{MCP_SERVERS_API_PATH}/{mcp_server_id}/tokens",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def get_client_info(
        self,
        *,
        mcp_server_id: str,
    ) -> McpServerClientInfoResponse:
        """Get client info for an MCP server."""
        return await self._get(
            f"{MCP_SERVERS_API_PATH}/{mcp_server_id}/client-info",
            params=None,
            body=None,
            cast_to=McpServerClientInfoResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )
