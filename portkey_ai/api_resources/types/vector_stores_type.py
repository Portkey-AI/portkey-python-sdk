import json
from typing import Dict, List, Optional, Union
from typing_extensions import Annotated, TypeAlias
import httpx

from portkey_ai._vendor.openai._utils._transform import PropertyInfo
from portkey_ai._vendor.openai.types.beta.vector_stores.vector_store_file import (
    ChunkingStrategyOther,
    ChunkingStrategyStatic,
)
from .utils import parse_headers
from pydantic import BaseModel, PrivateAttr

__all__ = [
    "LastError",
    "ExpiresAfter",
    "VectorStore",
    "VectorStoreList",
    "VectorStoreDeleted",
    "VectorStoreFile",
    "VectorStoreFileList",
    "VectorStoreFileDeleted",
    "FileCounts",
    "VectorStoreFileBatch",
]


class FileCounts(BaseModel, extra="allow"):
    cancelled: int
    completed: int
    failed: int
    in_progress: int
    total: int


class ExpiresAfter(BaseModel, extra="allow"):
    anchor: str
    days: int


class VectorStore(BaseModel, extra="allow"):
    id: str
    created_at: int
    file_counts: FileCounts
    last_active_at: Optional[int] = None
    metadata: Optional[object] = None
    name: str
    object: str
    status: str
    usage_bytes: int
    expires_after: Optional[ExpiresAfter] = None
    expires_at: Optional[int] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def __str__(self):
        del self._headers
        return json.dumps(self.dict(), indent=4)

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)


class VectorStoreList(BaseModel, extra="allow"):
    data: List[VectorStore]
    object: str
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def __str__(self):
        del self._headers
        return json.dumps(self.dict(), indent=4)

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)


class VectorStoreDeleted(BaseModel, extra="allow"):
    id: str
    deleted: bool
    object: str
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def __str__(self):
        del self._headers
        return json.dumps(self.dict(), indent=4)

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)


class LastError(BaseModel, extra="allow"):
    code: str
    message: str


ChunkingStrategy: TypeAlias = Annotated[
    Union[ChunkingStrategyStatic, ChunkingStrategyOther],
    PropertyInfo(discriminator="type"),
]


class VectorStoreFile(BaseModel, extra="allow"):
    id: str
    created_at: int
    last_error: Optional[LastError] = None
    object: str
    status: str
    usage_bytes: int
    vector_store_id: str
    chunking_strategy: Optional[ChunkingStrategy] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def __str__(self):
        del self._headers
        return json.dumps(self.dict(), indent=4)

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)


class VectorStoreFileList(BaseModel, extra="allow"):
    data: List[VectorStoreFile]
    object: str
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def __str__(self):
        del self._headers
        return json.dumps(self.dict(), indent=4)

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)


class VectorStoreFileDeleted(BaseModel, extra="allow"):
    id: str
    deleted: bool
    object: str
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def __str__(self):
        del self._headers
        return json.dumps(self.dict(), indent=4)

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)


class VectorStoreFileBatch(BaseModel, extra="allow"):
    id: str
    created_at: int
    file_counts: FileCounts
    object: str
    status: str
    vector_store_id: str
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def __str__(self):
        del self._headers
        return json.dumps(self.dict(), indent=4)

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)
