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
    cancelled: Optional[int] = None
    completed: Optional[int] = None
    failed: Optional[int] = None
    in_progress: Optional[int] = None
    total: Optional[int] = None


class ExpiresAfter(BaseModel, extra="allow"):
    anchor: Optional[str] = None
    days: Optional[int] = None


class VectorStore(BaseModel, extra="allow"):
    id: Optional[str] = None
    created_at: Optional[int] = None
    file_counts: FileCounts
    last_active_at: Optional[int] = None
    metadata: Optional[object] = None
    name: Optional[str] = None
    object: Optional[str] = None
    status: Optional[str] = None
    usage_bytes: Optional[int] = None
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
    object: Optional[str] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def __str__(self):
        del self._headers
        return json.dumps(self.dict(), indent=4)

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)


class VectorStoreDeleted(BaseModel, extra="allow"):
    id: Optional[str] = None
    deleted: Optional[bool] = None
    object: Optional[str] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def __str__(self):
        del self._headers
        return json.dumps(self.dict(), indent=4)

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)


class LastError(BaseModel, extra="allow"):
    code: Optional[str] = None
    message: Optional[str] = None


ChunkingStrategy: TypeAlias = Annotated[
    Union[ChunkingStrategyStatic, ChunkingStrategyOther],
    PropertyInfo(discriminator="type"),
]


class VectorStoreFile(BaseModel, extra="allow"):
    id: Optional[str] = None
    created_at: Optional[int] = None
    last_error: Optional[LastError] = None
    object: Optional[str] = None
    status: Optional[str] = None
    usage_bytes: Optional[int] = None
    vector_store_id: Optional[str] = None
    chunking_strategy: Optional[ChunkingStrategy] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def __str__(self):
        del self._headers
        return json.dumps(self.dict(), indent=4)

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)


class VectorStoreFileList(BaseModel, extra="allow"):
    data: List[VectorStoreFile]
    object: Optional[str] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def __str__(self):
        del self._headers
        return json.dumps(self.dict(), indent=4)

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)


class VectorStoreFileDeleted(BaseModel, extra="allow"):
    id: Optional[str] = None
    deleted: Optional[bool] = None
    object: Optional[str] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def __str__(self):
        del self._headers
        return json.dumps(self.dict(), indent=4)

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)


class VectorStoreFileBatch(BaseModel, extra="allow"):
    id: Optional[str] = None
    created_at: Optional[int] = None
    file_counts: FileCounts
    object: Optional[str] = None
    status: Optional[str] = None
    vector_store_id: Optional[str] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def __str__(self):
        del self._headers
        return json.dumps(self.dict(), indent=4)

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)
