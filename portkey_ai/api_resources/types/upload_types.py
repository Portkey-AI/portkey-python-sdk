import json
from typing import Dict, Literal, Optional
import httpx

from .utils import parse_headers
from pydantic import BaseModel, PrivateAttr


class FileObject(BaseModel, extra="allow"):
    id: Optional[str] = None
    bytes: Optional[int] = None
    created_at: Optional[int] = None
    filename: Optional[str] = None
    object: Optional[str] = None
    purpose: Optional[str] = None
    status: Optional[str] = None
    status_details: Optional[str] = None


class Upload(BaseModel, extra="allow"):
    id: Optional[str] = None
    bytes: Optional[int] = None
    created_at: Optional[int] = None
    expires_at: Optional[int] = None
    filename: Optional[str] = None
    object: Optional[Literal["upload"]] = None
    purpose: Optional[str] = None
    status: Optional[Literal["pending", "completed", "cancelled", "expired"]] = None
    file: Optional[FileObject] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def __str__(self):
        del self._headers
        return json.dumps(self.dict(), indent=4)

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)


class UploadPart(BaseModel, extra="allow"):
    id: Optional[str] = None
    created_at: Optional[int] = None
    object: Optional[Literal["upload.part"]] = None
    upload_id: Optional[str] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def __str__(self):
        del self._headers
        return json.dumps(self.dict(), indent=4)

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)
