import json
from typing import Dict, Optional, Union
import httpx

from portkey_ai.api_resources.types.chat_complete_type import (
    Choice,
    StreamChoice,
    Usage,
)
from portkey_ai.api_resources.types.complete_type import Logprobs, TextChoice

from .utils import parse_headers
from typing import List, Any
from pydantic import BaseModel


class PromptCreate(BaseModel):
    id: Optional[str]
    choices: List[Choice]
    created: Optional[int]
    model: Optional[str]
    object: Optional[str]
    system_fingerprint: Optional[str] = None
    usage: Optional[Usage] = None
    index: Optional[int] = None
    text: Optional[str] = None
    logprobs: Optional[Logprobs] = None
    finish_reason: Optional[str] = None
    _headers: Optional[httpx.Headers] = None

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)


class PromptCreateChunk(BaseModel):
    id: Optional[str] = None
    object: Optional[str] = None
    created: Optional[int] = None
    model: Optional[str] = None
    provider: Optional[str] = None
    choices: Optional[Union[List[TextChoice], List[StreamChoice]]]

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default
