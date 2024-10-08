import json
from typing import Any, Dict, List, Optional
import httpx
from pydantic import BaseModel, PrivateAttr
from portkey_ai.api_resources.types.utils import parse_headers


class ApiKeyAddResponse(BaseModel):
    id: Optional[str]
    key: Optional[str]
    object: Optional[str]
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


class ApiKeyGetResponse(BaseModel):
    id: Optional[str]
    key: Optional[str]
    name: Optional[str]
    description: Optional[str]
    type: Optional[str]
    organisation_id: Optional[str]
    workspace_id: Optional[str]
    user_id: Optional[str]
    status: Optional[str]
    created_at: Optional[str]
    last_updated_at: Optional[str]
    creation_mode: Optional[str]
    rate_limits: Optional[List[Dict[str, Any]]]
    usage_limits: Optional[Dict[str, Any]]
    reset_usage: Optional[int]
    scopes: Optional[List[str]]
    defaults: Optional[Dict[str, Any]]
    object: Optional[str]
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


class ApiKeyListResponse(BaseModel):
    object: Optional[bool]
    total: Optional[int]
    data: Optional[List[Dict[str, Any]]]
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


class ApiKeyUpdateResponse(BaseModel):
    object: Optional[str]
    total: Optional[int]
    data: Optional[List[Dict[str, Any]]]
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default
