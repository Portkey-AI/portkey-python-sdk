from typing import List, Optional, Union
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
    name: Union[str, None] = None
    classes: List[ClassConfig] = []
    methods: List[MethodConfig] = []


class TracingConfig(BaseModel):
    name: Union[str, None] = None
    min_version: Union[str, None] = None
    modules: List[ModuleConfig] = []


__all__ = ["TracingConfig"]
