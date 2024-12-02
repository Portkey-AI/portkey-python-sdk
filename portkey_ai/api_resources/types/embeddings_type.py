import json
from typing import Dict, Optional, Union
import httpx

from .utils import parse_headers
from typing import List, Any
from pydantic import BaseModel, PrivateAttr

__all__ = ["CreateEmbeddingResponse", "Usage", "Embedding"]


class Usage(BaseModel, extra="allow"):
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None


class Embedding(BaseModel, extra="allow"):
    embedding: Union[List[float], str]
    index: Optional[int] = None
    object: Optional[str] = None


class CreateEmbeddingResponse(BaseModel, extra="allow"):
    success: Optional[bool] = None
    warning: Optional[str] = None
    data: List[Embedding]
    model: Optional[str] = None
    object: Optional[str] = None
    usage: Usage
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
