import json
from typing import Any, Dict, Optional
import httpx
from .utils import parse_headers
from pydantic import BaseModel, PrivateAttr


class Conversation(BaseModel, extra="allow"):
    id: Optional[str] = None
    created_at: Optional[int] = None
    metadata: Optional[object] = None
    object: Optional[str] = None
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


class ConversationDeletedResource(BaseModel, extra="allow"):
    id: Optional[str] = None
    deleted: Optional[bool] = None
    object: Optional[str] = None

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
