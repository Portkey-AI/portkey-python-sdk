import json
from typing import Any, Dict, List, Literal, Optional
import httpx
from pydantic import BaseModel, PrivateAttr
from .utils import parse_headers


__all__ = [
    "ExpiresAfter",
    "ContainerCreateResponse",
    "ContainerRetrieveResponse",
    "ContainerListResponse",
]


class ExpiresAfter(BaseModel, extra="allow"):
    anchor: Optional[Literal["last_active_at"]] = None
    minutes: Optional[int] = None


class ContainerCreateResponse(BaseModel, extra="allow"):
    id: Optional[str] = None
    created_at: Optional[int] = None
    name: Optional[str] = None
    object: Optional[str] = None
    status: Optional[str] = None
    expires_after: Optional[ExpiresAfter] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def __str__(self):
        del self._headers
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)


class ContainerRetrieveResponse(BaseModel, extra="allow"):
    id: Optional[str] = None
    created_at: Optional[int] = None
    name: Optional[str] = None
    object: Optional[str] = None
    status: Optional[str] = None
    expires_after: Optional[ExpiresAfter] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def __str__(self):
        del self._headers
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)


class ContainerListResponse(BaseModel, extra="allow"):
    object: Optional[str] = None
    data: Optional[List[ContainerRetrieveResponse]] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def __str__(self):
        del self._headers
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)
