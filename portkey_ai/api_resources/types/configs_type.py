import json
from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class ConfigAddResponse(BaseModel):
    id: Optional[str]
    version_id: Optional[str]
    slug: Optional[str]
    object: Optional[str]

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


class ConfigGetResponse(BaseModel):
    id: Optional[str]
    name: Optional[str]
    workspace_id: Optional[str]
    slug: Optional[str]
    organization_id: Optional[str]
    is_default: Optional[int]
    status: Optional[str]
    owner_id: Optional[str]
    created_at: Optional[str]
    updated_by: Optional[str]
    last_updated_at: Optional[str]
    config: Optional[Dict[str, Any]]
    format: Optional[str]
    type: Optional[str]
    version_id: Optional[str]
    object: Optional[str]

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


class ConfigListResponse(BaseModel):
    object: Optional[bool]
    total: Optional[int]
    data: Optional[List[Dict[str, Any]]]

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


class ConfigUpdateResponse(BaseModel):
    version_id: Optional[str]
    object: Optional[str]

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default
