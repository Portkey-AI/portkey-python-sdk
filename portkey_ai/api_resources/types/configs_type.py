import json
from typing import Any, Dict, List, Optional, Union
import httpx
from pydantic import BaseModel, PrivateAttr
from portkey_ai.api_resources.types.utils import parse_headers


class ConfigAddResponse(BaseModel, extra="allow"):
    id: Optional[str] = None
    version_id: Optional[str] = None
    slug: Optional[str] = None
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


class ConfigGetResponse(BaseModel, extra="allow"):
    id: Optional[str] = None
    organisation_id: Optional[str] = None
    config: Optional[Union[str, dict]] = None
    name: Optional[str] = None
    workspace_id: Optional[str] = None
    slug: Optional[str] = None
    is_default: Optional[int] = None
    status: Optional[str] = None
    owner_id: Optional[str] = None
    created_at: Optional[str] = None
    updated_by: Optional[str] = None
    last_updated_at: Optional[str] = None
    format: Optional[str] = None
    type: Optional[str] = None
    version_id: Optional[str] = None
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


class ConfigListResponse(BaseModel, extra="allow"):
    object: Optional[str] = None
    total: Optional[int] = None
    data: Optional[List[Dict[str, Any]]] = None

    _headers: Optional[httpx.Headers] = PrivateAttr()

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


class ConfigUpdateResponse(BaseModel, extra="allow"):
    version_id: Optional[str] = None
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
