import json
from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class UserRetrieveResponse(BaseModel):
    object: Optional[str]
    id: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    role: Optional[str]
    email: Optional[str]
    created_at: Optional[str]
    last_updated_at: Optional[str]
    workspace_ids: Optional[List[str]]

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


class UserRetrieveAllResponse(BaseModel):
    total: Optional[int]
    object: Optional[str]
    data: Optional[List[UserRetrieveResponse]]

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


class UserInviteResponse(BaseModel):
    id: Optional[str]
    invite_link: Optional[str]

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


class UserInviteRetrieveResponse(BaseModel):
    object: Optional[str]
    id: Optional[str]
    email: Optional[str]
    role: Optional[str]
    created_at: Optional[str]
    expires_at: Optional[str]
    accepted_at: Optional[str]
    status: Optional[str]
    invited_by: Optional[str]

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


class UserInviteRetrieveAllResponse(BaseModel):
    object: Optional[str]
    total: Optional[int]
    data: Optional[List[UserInviteRetrieveResponse]]

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


class WorkspacesAddResponse(BaseModel):
    id: Optional[str]
    slug: Optional[str]
    name: Optional[str]
    description: Optional[str]
    created_at: Optional[str]
    last_updated_at: Optional[str]
    defaults: Optional[Dict[str, Any]]
    users: Optional[List[Dict[str, str]]]
    object: Optional[str]

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


class WorkspacesGetResponse(BaseModel):
    id: Optional[str]
    slug: Optional[str]
    name: Optional[str]
    description: Optional[str]
    created_at: Optional[str]
    last_updated_at: Optional[str]
    defaults: Optional[Dict[str, Any]]
    users: Optional[List[Dict[str, Any]]]

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


class WorkspacesListResponse(BaseModel):
    total: Optional[int]
    object: Optional[str]
    data: Optional[List[WorkspacesGetResponse]]

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


class WorkspacesUpdateResponse(BaseModel):
    id: Optional[str]
    slug: Optional[str]
    name: Optional[str]
    description: Optional[str]
    created_at: Optional[str]
    is_default: Optional[int]
    last_updated_at: Optional[str]
    defaults: Optional[Dict[str, Any]]
    object: Optional[str]

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


class WorkspaceMemberGetResponse(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    org_role: Optional[str]
    role: Optional[str]
    created_at: Optional[str]
    last_updated_at: Optional[str]
    status: Optional[str]
    workspace_id: Optional[str]
    scopes: Optional[List[str]]
    settings: Optional[Dict[str, Any]]
    object: Optional[str]

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


class WorkspaceMemberListResponse(BaseModel):
    total: Optional[int]
    object: Optional[str]
    data: Optional[List[WorkspaceMemberGetResponse]]

    def __str__(self):
        return json.dumps(self.dict(), indent=4, default=str)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default
