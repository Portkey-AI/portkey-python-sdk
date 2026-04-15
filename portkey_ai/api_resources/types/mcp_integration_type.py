import json
from typing import Any, Dict, List, Optional
import httpx
from pydantic import BaseModel, PrivateAttr
from portkey_ai.api_resources.types.utils import parse_headers


class McpIntegrationCreateResponse(BaseModel, extra="allow"):
    """Response type for MCP integration creation."""

    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    auth_type: Optional[str] = None
    transport: Optional[str] = None
    workspace_id: Optional[str] = None
    organisation_id: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    object: Optional[str] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


class McpIntegrationRetrieveResponse(BaseModel, extra="allow"):
    """Response type for MCP integration retrieval."""

    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    auth_type: Optional[str] = None
    transport: Optional[str] = None
    workspace_id: Optional[str] = None
    organisation_id: Optional[str] = None
    configurations: Optional[Dict[str, Any]] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    object: Optional[str] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


class McpIntegrationListResponse(BaseModel, extra="allow"):
    """Response type for MCP integration list."""

    data: Optional[List[Dict[str, Any]]] = None
    total: Optional[int] = None
    object: Optional[str] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


class McpIntegrationUpdateResponse(BaseModel, extra="allow"):
    """Response type for MCP integration update."""

    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    auth_type: Optional[str] = None
    transport: Optional[str] = None
    updated_at: Optional[str] = None
    object: Optional[str] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


class McpIntegrationDeleteResponse(BaseModel, extra="allow"):
    """Response type for MCP integration deletion."""

    success: Optional[bool] = None
    message: Optional[str] = None
    object: Optional[str] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


class McpIntegrationSyncResponse(BaseModel, extra="allow"):
    """Response type for MCP integration sync."""

    success: Optional[bool] = None
    message: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    object: Optional[str] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


class McpIntegrationTestResponse(BaseModel, extra="allow"):
    """Response type for MCP integration test."""

    success: Optional[bool] = None
    message: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    object: Optional[str] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


class McpIntegrationWorkspacesResponse(BaseModel, extra="allow"):
    """Response type for MCP integration workspaces."""

    workspaces: Optional[List[Dict[str, Any]]] = None
    global_workspace_access: Optional[Dict[str, Any]] = None
    object: Optional[str] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


class McpIntegrationCapabilitiesResponse(BaseModel, extra="allow"):
    """Response type for MCP integration capabilities."""

    data: Optional[List[Dict[str, Any]]] = None
    object: Optional[str] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


class McpIntegrationMetadataResponse(BaseModel, extra="allow"):
    """Response type for MCP integration metadata."""

    server_name: Optional[str] = None
    server_version: Optional[str] = None
    protocol_version: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    website_url: Optional[str] = None
    icons: Optional[Dict[str, Any]] = None
    capability_flags: Optional[Dict[str, Any]] = None
    instructions: Optional[str] = None
    object: Optional[str] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default
