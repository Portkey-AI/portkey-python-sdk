import json
from typing import Any, Dict, List, Optional
import httpx
from pydantic import BaseModel, PrivateAttr
from portkey_ai.api_resources.types.utils import parse_headers


class Provider(BaseModel, extra="allow"):
    id: Optional[str] = None
    slug: Optional[str] = None
    name: Optional[str] = None
    note: Optional[str] = None
    integration_id: Optional[str] = None
    workspace_id: Optional[str] = None
    usage_limits: Optional[Dict[str, Any]] = None
    rate_limits: Optional[Dict[str, Any]] = None
    expires_at: Optional[str] = None
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


class ProviderListResponse(BaseModel, extra="allow"):
    object: Optional[str] = None
    total: Optional[int] = None
    data: Optional[List[Provider]] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


class ProviderDetailResponse(BaseModel, extra="allow"):
    id: Optional[str] = None
    slug: Optional[str] = None
    name: Optional[str] = None
    note: Optional[str] = None
    integration_id: Optional[str] = None
    workspace_id: Optional[str] = None
    usage_limits: Optional[Dict[str, Any]] = None
    rate_limits: Optional[List[Any]] = None
    expires_at: Optional[str] = None
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


class ProviderCreateResponse(BaseModel, extra="allow"):
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


class ProviderUpdateResponse(BaseModel, extra="allow"):
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
