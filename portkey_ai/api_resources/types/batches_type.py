import json
import builtins
from typing import Dict, Optional
import httpx
from .utils import parse_headers
from typing import List, Any
from pydantic import BaseModel, PrivateAttr
from openai.types.batch_error import BatchError
from openai.types.batch_request_counts import BatchRequestCounts

__all__ = ["Batch", "BatchList", "Errors"]


class Errors(BaseModel):
    data: Optional[List[BatchError]] = None

    object: Optional[str] = None
    """The object type, which is always `list`."""


class Batch(BaseModel):
    id: str
    completion_window: str
    created_at: int
    endpoint: str
    input_file_id: str
    object: str
    status: str
    cancelled_at: Optional[int] = None
    cancelling_at: Optional[int] = None
    completed_at: Optional[int] = None
    error_file_id: Optional[str] = None
    errors: Optional[Errors] = None
    expired_at: Optional[int] = None
    expires_at: Optional[int] = None
    failed_at: Optional[int] = None
    finalizing_at: Optional[int] = None
    in_progress_at: Optional[int] = None
    metadata: Optional[builtins.object] = None
    output_file_id: Optional[str] = None
    request_counts: Optional[BatchRequestCounts] = None
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


class BatchList(BaseModel):
    object: Optional[str] = None
    data: Optional[List[Batch]] = None
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
