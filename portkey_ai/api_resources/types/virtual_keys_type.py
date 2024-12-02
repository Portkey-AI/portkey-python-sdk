import json
from typing import Any, Dict, List, Optional
import httpx
from pydantic import BaseModel, PrivateAttr
from portkey_ai.api_resources.types.utils import parse_headers


class VirtualKeysAddResponse(BaseModel, extra="allow"):
    id: Optional[str] = None
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


class VirtualKeysListReponse(BaseModel, extra="allow"):
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


class VirtualKeysUpdateResponse(BaseModel, extra="allow"):
    id: Optional[str] = None
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
