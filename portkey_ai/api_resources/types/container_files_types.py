import json
from typing import Any, Dict, List, Optional
import httpx
from pydantic import BaseModel, PrivateAttr
from .utils import parse_headers

__all__ = [
    "FileCreateResponse",
    "FileRetrieveResponse",
    "FileListResponse",
]


class FileCreateResponse(BaseModel, extra="allow"):
    id: Optional[str] = None
    bytes: Optional[int] = None
    container_id: Optional[str] = None
    created_at: Optional[int] = None
    object: Optional[str] = None
    path: Optional[str] = None
    source: Optional[str] = None
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


class FileRetrieveResponse(BaseModel, extra="allow"):
    id: Optional[str] = None
    bytes: Optional[int] = None
    container_id: Optional[str] = None
    created_at: Optional[int] = None
    object: Optional[str] = None
    path: Optional[str] = None
    source: Optional[str] = None
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


class FileListResponse(BaseModel, extra="allow"):
    object: Optional[str] = None
    data: Optional[List[FileRetrieveResponse]] = None
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
