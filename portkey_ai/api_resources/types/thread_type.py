import json
from typing import Dict, Optional
import httpx
from .utils import parse_headers
from pydantic import BaseModel, PrivateAttr


__all__ = ["Thread", "ThreadDeleted"]


class Thread(BaseModel, extra="allow"):
    id: Optional[str] = None
    created_at: Optional[int] = None
    metadata: Optional[object] = None
    object: Optional[str] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def __str__(self):
        del self._headers
        return json.dumps(self.dict(), indent=4)

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)


class ThreadDeleted(BaseModel, extra="allow"):
    id: Optional[str] = None
    object: Optional[str] = None
    deleted: Optional[bool] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def __str__(self):
        del self._headers
        return json.dumps(self.dict(), indent=4)

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)
