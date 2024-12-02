import json
from typing import Any, Dict, List, Optional
import httpx
from pydantic import BaseModel, PrivateAttr
from portkey_ai.api_resources.types.utils import parse_headers


class UserRetrieveResponse(BaseModel, extra="allow"):
    object: Optional[str] = None
    id: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[str] = None
    email: Optional[str] = None
    created_at: Optional[str] = None
    last_updated_at: Optional[str] = None
    workspace_ids: Optional[List[str]] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


class UserRetrieveAllResponse(BaseModel, extra="allow"):
    total: Optional[int] = None
    object: Optional[str] = None
    data: Optional[List[UserRetrieveResponse]]
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


class UserInviteResponse(BaseModel, extra="allow"):
    id: Optional[str] = None
    invite_link: Optional[str] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


class UserInviteRetrieveResponse(BaseModel, extra="allow"):
    object: Optional[str] = None
    id: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None
    created_at: Optional[str] = None
    expires_at: Optional[str] = None
    accepted_at: Optional[str] = None
    status: Optional[str] = None
    invited_by: Optional[str] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


class UserInviteRetrieveAllResponse(BaseModel, extra="allow"):
    object: Optional[str] = None
    total: Optional[int] = None
    data: Optional[List[UserInviteRetrieveResponse]]
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


class WorkspacesAddResponse(BaseModel, extra="allow"):
    id: Optional[str] = None
    slug: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    created_at: Optional[str] = None
    last_updated_at: Optional[str] = None
    defaults: Optional[Dict[str, Any]] = None
    users: Optional[List[Dict[str, str]]] = None
    object: Optional[str] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


class WorkspacesGetResponse(BaseModel, extra="allow"):
    object: Optional[str] = None
    id: Optional[str] = None
    slug: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    created_at: Optional[str] = None
    last_updated_at: Optional[str] = None
    defaults: Optional[Dict[str, Any]] = None
    is_default: Optional[int] = None
    users: Optional[List[Dict[str, Any]]] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


class WorkspacesListResponse(BaseModel, extra="allow"):
    total: Optional[int] = None
    object: Optional[str] = None
    data: Optional[List[WorkspacesGetResponse]]
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


class WorkspacesUpdateResponse(BaseModel, extra="allow"):
    id: Optional[str] = None
    slug: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    created_at: Optional[str] = None
    is_default: Optional[int] = None
    last_updated_at: Optional[str] = None
    defaults: Optional[Dict[str, Any]] = None
    object: Optional[str] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


class WorkspaceMemberGetResponse(BaseModel, extra="allow"):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    org_role: Optional[str] = None
    role: Optional[str] = None
    created_at: Optional[str] = None
    last_updated_at: Optional[str] = None
    status: Optional[str] = None
    workspace_id: Optional[str] = None
    scopes: Optional[List[str]] = None
    settings: Optional[Any] = None
    object: Optional[str] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


class WorkspaceMemberListResponse(BaseModel, extra="allow"):
    total: Optional[int] = None
    object: Optional[str] = None
    data: Optional[List[WorkspaceMemberGetResponse]]
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)

    def __str__(self):
        return json.dumps(self.dict(), indent=4, default=str)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default
