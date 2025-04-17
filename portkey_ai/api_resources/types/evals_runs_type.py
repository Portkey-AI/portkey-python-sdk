import json
from typing import List, Literal, Optional, Any, Dict
import httpx
from pydantic import BaseModel, PrivateAttr
from portkey_ai._vendor.openai.types.evals.eval_api_error import EvalAPIError
from portkey_ai._vendor.openai.types.evals.run_create_response import (
    DataSource,
    PerModelUsage,
    PerTestingCriteriaResult,
    ResultCounts,
)
from portkey_ai.api_resources.types.shared_types import Metadata
from portkey_ai.api_resources.types.utils import parse_headers


class RunCreateResponse(BaseModel, extra="allow"):
    id: Optional[str] = None
    created_at: Optional[int] = None
    data_source: Optional[DataSource] = None
    error: Optional[EvalAPIError] = None
    eval_id: Optional[str] = None
    metadata: Optional[Metadata] = None
    model: Optional[str] = None
    name: Optional[str] = None
    object: Optional[Literal["eval.run"]] = None
    per_model_usage: Optional[List[PerModelUsage]] = None
    per_testing_criteria_results: Optional[List[PerTestingCriteriaResult]] = None
    report_url: Optional[str] = None
    result_counts: Optional[ResultCounts] = None
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


class RunRetrieveResponse(BaseModel, extra="allow"):
    id: Optional[str] = None
    created_at: Optional[int] = None
    data_source: Optional[DataSource] = None
    error: Optional[EvalAPIError] = None
    eval_id: Optional[str] = None
    metadata: Optional[Metadata] = None
    model: Optional[str] = None
    name: Optional[str] = None
    object: Optional[Literal["eval.run"]] = None
    per_model_usage: Optional[List[PerModelUsage]] = None
    per_testing_criteria_results: Optional[List[PerTestingCriteriaResult]] = None
    report_url: Optional[str] = None
    result_counts: Optional[ResultCounts] = None
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


class RunList(BaseModel, extra="allow"):
    id: Optional[str] = None
    created_at: Optional[int] = None
    data_source: Optional[DataSource] = None
    error: Optional[EvalAPIError] = None
    eval_id: Optional[str] = None
    metadata: Optional[Metadata] = None
    model: Optional[str] = None
    name: Optional[str] = None
    object: Optional[Literal["eval.run"]] = None
    per_model_usage: Optional[List[PerModelUsage]] = None
    per_testing_criteria_results: Optional[List[PerTestingCriteriaResult]] = None
    report_url: Optional[str] = None
    result_counts: Optional[ResultCounts] = None
    status: Optional[str] = None


class RunListResponseList(BaseModel, extra="allow"):
    object: Optional[str] = None
    data: Optional[List[RunList]] = None
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


class RunDeleteResponse(BaseModel, extra="allow"):
    deleted: Optional[bool] = None
    object: Optional[str] = None
    run_id: Optional[str] = None
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


class RunCancelResponse(BaseModel, extra="allow"):
    id: Optional[str] = None
    created_at: Optional[int] = None
    data_source: Optional[DataSource] = None
    error: Optional[EvalAPIError] = None
    eval_id: Optional[str] = None
    metadata: Optional[Metadata] = None
    model: Optional[str] = None
    name: Optional[str] = None
    object: Optional[Literal["eval.run"]] = None
    per_model_usage: Optional[List[PerModelUsage]] = None
    per_testing_criteria_results: Optional[List[PerTestingCriteriaResult]] = None
    report_url: Optional[str] = None
    result_counts: Optional[ResultCounts] = None
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
