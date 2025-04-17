import json
from typing import Any, Dict, List, Literal, Optional
import httpx
from pydantic import BaseModel, PrivateAttr
from portkey_ai._vendor.openai.types.eval_create_response import (
    DataSourceConfig,
    TestingCriterion,
)
from portkey_ai.api_resources.types.shared_types import Metadata
from portkey_ai.api_resources.types.utils import parse_headers


class EvalCreateResponse(BaseModel, extra="allow"):
    id: Optional[str] = None
    created_at: Optional[int] = None
    data_source_config: DataSourceConfig
    metadata: Optional[Metadata] = None
    name: Optional[str] = None
    object: Optional[Literal["eval"]] = None
    share_with_openai: Optional[bool] = None
    testing_criteria: Optional[List[TestingCriterion]] = None
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


class EvalRetrieveResponse(BaseModel, extra="allow"):
    id: Optional[str] = None
    created_at: Optional[int] = None
    data_source_config: Optional[DataSourceConfig] = None
    metadata: Optional[Metadata] = None
    name: Optional[str] = None
    object: Optional[Literal["eval"]] = None
    share_with_openai: Optional[bool] = None
    testing_criteria: Optional[List[TestingCriterion]] = None
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


class EvalUpdateResponse(BaseModel, extra="allow"):
    id: Optional[str] = None
    created_at: Optional[int] = None
    data_source_config: Optional[DataSourceConfig] = None
    metadata: Optional[Metadata] = None
    name: Optional[str] = None
    object: Optional[Literal["eval"]] = None
    share_with_openai: Optional[bool] = None
    testing_criteria: Optional[List[TestingCriterion]] = None
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


class EvalListResponse(BaseModel, extra="allow"):
    id: Optional[str] = None
    created_at: Optional[int] = None
    data_source_config: Optional[DataSourceConfig] = None
    metadata: Optional[Metadata] = None
    name: Optional[str] = None
    object: Optional[Literal["eval"]] = None
    share_with_openai: Optional[bool] = None
    testing_criteria: Optional[List[TestingCriterion]] = None


class EvalListResponseList(BaseModel, extra="allow"):
    object: Optional[str] = None
    data: Optional[List[EvalListResponse]] = None
    has_more: Optional[bool] = None
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


class EvalDeleteResponse(BaseModel, extra="allow"):
    deleted: Optional[bool] = None
    eval_id: Optional[str] = None
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
