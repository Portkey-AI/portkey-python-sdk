import json
from typing import Dict, Optional
import httpx
from .utils import parse_headers
from typing import List, Any
from pydantic import BaseModel, PrivateAttr
from ..._vendor.openai.types.moderation import Moderation


__all__ = ["ModerationCreateResponse"]


class ModerationCreateResponse(BaseModel, extra="allow"):
    id: Optional[str] = None
    model: Optional[str] = None
    results: Optional[List[Moderation]] = None
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
