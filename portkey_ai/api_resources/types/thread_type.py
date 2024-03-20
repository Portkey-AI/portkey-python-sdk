import json
from typing import Dict, Optional
import httpx
from .utils import parse_headers
from pydantic import BaseModel


__all__ = ["Thread", "ThreadDeleted"]


class Thread(BaseModel, extra="allow"):
    id: Optional[str]
    created_at: Optional[int]
    metadata: Optional[object] = None
    object: Optional[str]
    _headers: Optional[httpx.Headers] = None

    def __str__(self):
        del self._headers
        return json.dumps(self.dict(), indent=4)

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)


class ThreadDeleted(BaseModel, extra="allow"):
    id: Optional[str]
    object: Optional[str]
    deleted: Optional[bool]
    _headers: Optional[httpx.Headers] = None

    def __str__(self):
        del self._headers
        return json.dumps(self.dict(), indent=4)

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)
