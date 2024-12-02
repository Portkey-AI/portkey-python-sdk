import json
from typing import Any, Dict, List, Optional, Union
import httpx
from pydantic import BaseModel, PrivateAttr
from portkey_ai.api_resources.types.utils import parse_headers


class ConfigAddResponse(BaseModel, extra="allow"):
    id: Optional[str]
    version_id: Optional[str]
    slug: Optional[str]
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


class ConfigGetResponse(BaseModel, extra="allow"):
    id: Optional[str]
    organisation_id: Optional[str] = None
    config: Optional[Union[str, dict]]
    name: Optional[str]
    workspace_id: Optional[str]
    slug: Optional[str]
    is_default: Optional[int]
    status: Optional[str]
    owner_id: Optional[str]
    created_at: Optional[str]
    updated_by: Optional[str]
    last_updated_at: Optional[str]
    format: Optional[str]
    type: Optional[str]
    version_id: Optional[str]
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


class ConfigListResponse(BaseModel, extra="allow"):
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


class ConfigUpdateResponse(BaseModel, extra="allow"):
    version_id: Optional[str]
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
