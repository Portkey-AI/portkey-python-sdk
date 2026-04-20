import json
from typing import Any, Dict, List, Literal, Optional

import httpx
from pydantic import BaseModel, PrivateAttr

from .utils import parse_headers

__all__ = [
    "Skill",
    "SkillDeleted",
    "SkillList",
    "SkillVersion",
    "SkillVersionDeleted",
    "SkillVersionList",
]


class Skill(BaseModel, extra="allow"):
    id: str
    created_at: int
    default_version: str
    description: str
    latest_version: str
    name: str
    object: Literal["skill"]
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


class SkillDeleted(BaseModel, extra="allow"):
    id: str
    deleted: bool
    object: Literal["skill.deleted"]
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


class SkillList(BaseModel, extra="allow"):
    object: Optional[str] = None
    data: Optional[List[Skill]] = None
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


class SkillVersion(BaseModel, extra="allow"):
    id: str
    created_at: int
    description: str
    name: str
    object: Literal["skill.version"]
    skill_id: str
    version: str
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


class SkillVersionDeleted(BaseModel, extra="allow"):
    id: str
    deleted: bool
    object: Literal["skill.version.deleted"]
    version: str
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


class SkillVersionList(BaseModel, extra="allow"):
    object: Optional[str] = None
    data: Optional[List[SkillVersion]] = None
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
