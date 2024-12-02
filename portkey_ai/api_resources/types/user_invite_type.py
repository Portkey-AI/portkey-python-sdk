import json
from typing import Any, Dict, List, Optional
import httpx
from pydantic import BaseModel, PrivateAttr
from portkey_ai.api_resources.types.utils import parse_headers


class UserRetrieveResponse(BaseModel, extra="allow"):
    object: Optional[str]
    id: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    role: Optional[str]
    email: Optional[str]
    created_at: Optional[str]
    last_updated_at: Optional[str]
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
    total: Optional[int]
    object: Optional[str]
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
    id: Optional[str]
    invite_link: Optional[str]
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
    object: Optional[str]
    id: Optional[str]
    email: Optional[str]
    role: Optional[str]
    created_at: Optional[str]
    expires_at: Optional[str]
    accepted_at: Optional[str]
    status: Optional[str]
    invited_by: Optional[str]
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
    object: Optional[str]
    total: Optional[int]
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
    id: Optional[str]
    slug: Optional[str]
    name: Optional[str]
    description: Optional[str]
    created_at: Optional[str]
    last_updated_at: Optional[str]
    defaults: Optional[Dict[str, Any]]
    users: Optional[List[Dict[str, str]]]
    object: Optional[str]
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
    object: Optional[str]
    id: Optional[str]
    slug: Optional[str]
    name: Optional[str]
    description: Optional[str]
    created_at: Optional[str]
    last_updated_at: Optional[str]
    defaults: Optional[Dict[str, Any]]
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
    total: Optional[int]
    object: Optional[str]
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
    id: Optional[str]
    slug: Optional[str]
    name: Optional[str]
    description: Optional[str]
    created_at: Optional[str]
    is_default: Optional[int]
    last_updated_at: Optional[str]
    defaults: Optional[Dict[str, Any]]
    object: Optional[str]
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
    first_name: Optional[str]
    last_name: Optional[str]
    org_role: Optional[str]
    role: Optional[str]
    created_at: Optional[str]
    last_updated_at: Optional[str]
    status: Optional[str]
    workspace_id: Optional[str]
    scopes: Optional[List[str]] = None
    settings: Optional[Any] = None
    object: Optional[str]
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
    total: Optional[int]
    object: Optional[str]
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
