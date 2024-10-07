import json
from typing import Dict, Literal, Optional
import httpx

from portkey_ai._vendor.openai.types.file_object import FileObject
from .utils import parse_headers
from pydantic import BaseModel, PrivateAttr


class Upload(BaseModel, extra="allow"):
    id: Optional[str]
    bytes: Optional[int]
    created_at: Optional[int]
    expires_at: Optional[int]
    filename: Optional[str]
    object: Optional[Literal["upload"]]
    purpose: Optional[str]
    status: Optional[Literal["pending", "completed", "cancelled", "expired"]]
    file: Optional[FileObject] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def __str__(self):
        del self._headers
        return json.dumps(self.dict(), indent=4)

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)


class UploadPart(BaseModel, extra="allow"):
    id: Optional[str]
    created_at: Optional[int]
    object: Optional[Literal["upload.part"]]
    upload_id: Optional[str]
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def __str__(self):
        del self._headers
        return json.dumps(self.dict(), indent=4)

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)
