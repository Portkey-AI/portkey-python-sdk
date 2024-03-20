import json
from typing import Dict, Optional
import httpx
from portkey_ai.api_resources.utils import parse_headers
from typing import List, Any
from pydantic import BaseModel

__all__ = ["Model", "ModelDeleted", "ModelList"]

class Model(BaseModel):
    id: Optional[str]
    created: Optional[int]
    object: Optional[str]
    owned_by: Optional[str]
    _headers: Optional[httpx.Headers] = None

    def __str__(self):
        del self._headers
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)
    

class ModelList(BaseModel, extra="allow"):
    object: Optional[str]
    data: List[Model]
    _headers: Optional[httpx.Headers] = None

    def __str__(self):
        del self._headers
        return json.dumps(self.dict(), indent=4)

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)

class ModelDeleted(BaseModel):
    id: Optional[str]
    deleted: Optional[bool]
    object: Optional[str]
    _headers: Optional[httpx.Headers] = None

    def __str__(self):
        del self._headers
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)
