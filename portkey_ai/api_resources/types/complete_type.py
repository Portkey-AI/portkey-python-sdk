import json
from typing import Dict, Optional
import httpx
from .utils import parse_headers
from typing import List, Any
from pydantic import BaseModel, PrivateAttr

__all__ = ["CompletionUsage", "Logprobs", "CompletionChoice", "TextCompletion"]


class CompletionUsage(BaseModel, extra="allow"):
    completion_tokens: Optional[int] = None
    prompt_tokens: Optional[int] = None
    total_tokens: Optional[int] = None


class Logprobs(BaseModel, extra="allow"):
    text_offset: Optional[List[int]] = None
    token_logprobs: Optional[List[Optional[float]]] = None
    tokens: Optional[List[str]] = None
    top_logprobs: Optional[List[Optional[Dict[str, float]]]] = None


class CompletionChoice(BaseModel, extra="allow"):
    finish_reason: Optional[str] = None
    index: Optional[int] = None
    logprobs: Optional[Logprobs] = None
    text: Optional[str] = None


class TextCompletion(BaseModel, extra="allow"):
    id: Optional[str] = None
    choices: List[CompletionChoice]
    created: Optional[int] = None
    model: Optional[str] = None
    object: Optional[str] = None
    system_fingerprint: Optional[str] = None
    usage: Optional[CompletionUsage] = None
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


class TextChoice(BaseModel, extra="allow"):
    index: Optional[int] = None
    text: Optional[str] = None
    logprobs: Optional[Logprobs] = None
    finish_reason: Optional[str] = None

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


class TextCompletionChunk(BaseModel, extra="allow"):
    id: Optional[str] = None
    object: Optional[str] = None
    created: Optional[int] = None
    model: Optional[str] = None
    provider: Optional[str] = None
    usage: Optional[CompletionUsage] = None
    choices: List[TextChoice]

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default
