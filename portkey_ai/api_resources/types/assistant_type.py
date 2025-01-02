import json
from typing import Dict, Optional, Union
import httpx
from .utils import parse_headers
from typing import List, Any
from pydantic import BaseModel, PrivateAttr

__all__ = [
    "Assistant",
    "AssistantList",
    "AssistantDeleted",
    "ToolCodeInterpreter",
    "ToolRetrieval",
    "ToolFunction",
    "AssistantTool",
    "FunctionDefinition",
    "FunctionParameters",
    "FileSearch",
    "FileSearchTool",
]


class FileSearch(BaseModel, extra="allow"):
    max_num_results: Optional[int] = None


class FileSearchTool(BaseModel, extra="allow"):
    type: Optional[str] = None
    file_search: Optional[FileSearch] = None


FunctionParameters = Dict[str, object]


class FunctionDefinition(BaseModel, extra="allow"):
    name: Optional[str] = None
    description: Optional[str] = None
    parameters: Optional[FunctionParameters] = None
    strict: Optional[bool] = None


class ToolCodeInterpreter(BaseModel, extra="allow"):
    type: Optional[str] = None


class ToolRetrieval(BaseModel, extra="allow"):
    type: Optional[str] = None


class ToolFunction(BaseModel, extra="allow"):
    type: Optional[str] = None
    function: Optional[FunctionDefinition] = None


AssistantTool = Union[ToolCodeInterpreter, ToolRetrieval, ToolFunction, FileSearchTool]


class Assistant(BaseModel, extra="allow"):
    id: Optional[str] = None
    created_at: Optional[int] = None
    description: Optional[str] = None
    file_ids: Optional[List[str]] = None
    instructions: Optional[str] = None
    metadata: Optional[object] = None
    model: Optional[str] = None
    name: Optional[str] = None
    object: Optional[str] = None
    tools: Optional[List[AssistantTool]] = None
    response_format: Optional[Any] = None
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


class AssistantList(BaseModel, extra="allow"):
    object: Optional[str] = None
    data: Optional[List[Assistant]] = None
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


class AssistantDeleted(BaseModel, extra="allow"):
    id: Optional[str] = None
    object: Optional[str] = None
    deleted: Optional[bool] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def __str__(self):
        del self._headers
        return json.dumps(self.dict(), indent=4)

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)
