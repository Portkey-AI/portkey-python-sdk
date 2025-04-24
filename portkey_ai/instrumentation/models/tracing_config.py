from typing import List, Union
from pydantic import BaseModel


# we use regex if include_pattern is not empty


class MethodConfig(BaseModel):
    name: Union[str, None] = None
    pattern: Union[str, None] = None
    args: Union[str, None] = None
    result: Union[str, None] = None


class ClassConfig(BaseModel):
    pattern: Union[str, None] = None
    name: Union[str, None] = None
    methods: List[MethodConfig] = []


# module name can be a specific file or directory, both cases are supported
class ModuleConfig(BaseModel):
    name: str
    classes: List[ClassConfig] = []
    methods: List[MethodConfig] = []


class TracingConfig(BaseModel):
    name: str
    min_version: str
    modules: List[ModuleConfig] = []


__all__ = ["TracingConfig"]
