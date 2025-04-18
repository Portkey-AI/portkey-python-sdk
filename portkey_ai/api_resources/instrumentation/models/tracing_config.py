from typing import List, Optional
from pydantic import BaseModel, ConfigDict


# we use regex if include_pattern is not empty


class MethodConfig(BaseModel):
    name: str | None = None
    pattern: str | None = None


class ClassConfig(BaseModel):
    pattern: str | None = None
    name: str | None = None
    methods: List[MethodConfig] = []


# module name can be a specific file or directory, both cases are supported
class ModuleConfig(BaseModel):
    name: str
    classes: List[ClassConfig] = []
    methods: List[MethodConfig] = []


class TracingConfig(BaseModel):
    name: str
    min_version: Optional[str] = None
    modules: List[ModuleConfig] = []


__all__ = ["TracingConfig"]
