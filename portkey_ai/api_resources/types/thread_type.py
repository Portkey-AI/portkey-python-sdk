import json
from typing import Dict, List, Optional
import httpx
from .utils import parse_headers
from pydantic import BaseModel, PrivateAttr


__all__ = [
    "Thread",
    "ThreadDeleted",
    "ToolResources",
    "ToolResourcesCodeInterpreter",
    "ToolResourcesFileSearch",
]


class ToolResourcesCodeInterpreter(BaseModel, extra="allow"):
    file_ids: Optional[List[str]] = None


class ToolResourcesFileSearch(BaseModel, extra="allow"):
    vector_store_ids: Optional[List[str]] = None


class ToolResources(BaseModel, extra="allow"):
    code_interpreter: Optional[ToolResourcesCodeInterpreter] = None

    file_search: Optional[ToolResourcesFileSearch] = None


class Thread(BaseModel, extra="allow"):
    id: Optional[str] = None
    created_at: Optional[int] = None
    metadata: Optional[object] = None
    object: Optional[str] = None
    tool_resources: Optional[ToolResources] = None
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
