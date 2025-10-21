import json
from typing import Any, Dict, List, Optional
import httpx
from pydantic import BaseModel, PrivateAttr
from portkey_ai.api_resources.types.utils import parse_headers


class GuardrailSummary(BaseModel, extra="allow"):
    id: Optional[str] = None
    name: Optional[str] = None
    slug: Optional[str] = None
    organisation_id: Optional[str] = None
    workspace_id: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[str] = None
    last_updated_at: Optional[str] = None
    owner_id: Optional[str] = None
    updated_by: Optional[str] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


class GuardrailListResponse(BaseModel, extra="allow"):
    data: Optional[List[GuardrailSummary]] = None
    total: Optional[int] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


class GuardrailDetailResponse(BaseModel, extra="allow"):
    id: Optional[str] = None
    name: Optional[str] = None
    slug: Optional[str] = None
    organisation_id: Optional[str] = None
    workspace_id: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[str] = None
    last_updated_at: Optional[str] = None
    owner_id: Optional[str] = None
    updated_by: Optional[str] = None
    checks: Optional[List[Dict[str, Any]]] = None
    actions: Optional[Dict[str, Any]] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


class GuardrailCreateResponse(BaseModel, extra="allow"):
    id: Optional[str] = None
    slug: Optional[str] = None
    version_id: Optional[str] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


class GuardrailUpdateResponse(BaseModel, extra="allow"):
    id: Optional[str] = None
    slug: Optional[str] = None
    version_id: Optional[str] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default
