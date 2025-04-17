import builtins
import json
from typing import Any, Dict, List, Literal, Optional
import httpx
from pydantic import BaseModel, PrivateAttr

from portkey_ai._vendor.openai.types.evals.runs.output_item_retrieve_response import (
    Sample,
)
from portkey_ai.api_resources.types.utils import parse_headers


class OutputItemRetrieveResponse(BaseModel, extra="allow"):
    id: Optional[str] = None
    created_at: Optional[int] = None
    datasource_item: Optional[Dict[str, object]] = None
    datasource_item_id: Optional[int] = None
    eval_id: Optional[str] = None
    object: Optional[Literal["eval.run.output_item"]] = None
    results: Optional[List[Dict[str, builtins.object]]] = None
    run_id: Optional[str] = None
    sample: Optional[Sample] = None
    status: Optional[str] = None
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


class OutputItemListResponse(BaseModel, extra="allow"):
    id: Optional[str] = None
    created_at: Optional[int] = None
    datasource_item: Optional[Dict[str, object]] = None
    datasource_item_id: Optional[int] = None
    eval_id: Optional[str] = None
    object: Optional[Literal["eval.run.output_item"]] = None
    results: Optional[List[Dict[str, builtins.object]]] = None
    run_id: Optional[str] = None
    sample: Optional[Sample] = None
    status: Optional[str] = None


class OutputItemListResponseList(BaseModel, extra="allow"):
    object: Optional[str] = None
    data: Optional[List[OutputItemListResponse]] = None
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
