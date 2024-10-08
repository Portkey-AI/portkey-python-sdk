import json
from typing import Any, Dict, List, Optional
import httpx
from pydantic import BaseModel, PrivateAttr
from portkey_ai.api_resources.types.utils import parse_headers

class VirtualKeysAddResponse(BaseModel):
    id: Optional[str]
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
    
class VirtualKeysGetResponse(BaseModel):
    id: Optional[str]
    ai_provider_name: Optional[str]
    model_config: Optional[Dict[str,Any]]
    masked_api_key: Optional[str]
    slug: Optional[str]
    name: Optional[str]
    usage_limits: Optional[Dict[str, Any]]
    status: Optional[str]
    note: Optional[str]
    created_at: Optional[str]
    rate_limits: Optional[List[Dict[str, Any]]]
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

class VirtualKeysListReponse(BaseModel):
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

class VirtualKeysUpdateResponse(BaseModel):
    id: Optional[str]
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