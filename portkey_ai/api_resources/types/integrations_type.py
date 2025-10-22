import json
from typing import Any, Dict, List, Optional
import httpx
from pydantic import BaseModel, PrivateAttr
from portkey_ai.api_resources.types.utils import parse_headers


class IntegrationList(BaseModel, extra="allow"):
    id: Optional[str] = None
    slug: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    ai_provider_id: Optional[str] = None
    workspace_id: Optional[str] = None
    organisation_id: Optional[str] = None
    configurations: Optional[Dict[str, Any]] = None
    created_at: Optional[str] = None
    last_updated_at: Optional[str] = None
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


class IntegrationListResponse(BaseModel, extra="allow"):
    object: Optional[str] = None
    total: Optional[int] = None
    data: Optional[List[IntegrationList]] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


class IntegrationDetailResponse(BaseModel, extra="allow"):
    id: Optional[str] = None
    slug: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    ai_provider_id: Optional[str] = None
    workspace_id: Optional[str] = None
    configurations: Optional[Dict[str, Any]] = None
    created_at: Optional[str] = None
    last_updated_at: Optional[str] = None
    allow_all_models: Optional[bool] = None
    type: Optional[str] = None
    global_workspace_access: Optional[Dict[str, Any]] = None
    object: Optional[str] = None
    owner_id: Optional[str] = None
    status: Optional[str] = None
    masked_key: Optional[str] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


class IntegrationCreateResponse(BaseModel, extra="allow"):
    id: Optional[str] = None
    slug: Optional[str] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


class IntegrationModel(BaseModel, extra="allow"):
    slug: Optional[str] = None
    created_at: Optional[str] = None
    last_updated_at: Optional[str] = None
    enabled: Optional[bool] = None
    is_custom: Optional[bool] = None
    pricing_config: Optional[Dict[str, Any]] = None
    is_finetune: Optional[bool] = None
    base_model_slug: Optional[str] = None


class IntegrationModelsResponse(BaseModel, extra="allow"):
    models: Optional[List[IntegrationModel]] = None
    allow_all_models: Optional[bool] = None
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


class IntegrationWorkspace(BaseModel, extra="allow"):
    id: Optional[str] = None
    enabled: Optional[bool] = None
    usage_limits: Optional[Dict[str, Any]] = None
    rate_limits: Optional[Dict[str, Any]] = None
    created_at: Optional[str] = None
    last_updated_at: Optional[str] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


class IntegrationWorkspacesResponse(BaseModel, extra="allow"):
    object: Optional[str] = None
    total: Optional[int] = None
    data: Optional[List[IntegrationWorkspace]] = None
    global_workspace_access: Optional[Dict[str, Any]] = None
    workspaces: Optional[List[IntegrationWorkspace]] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default
