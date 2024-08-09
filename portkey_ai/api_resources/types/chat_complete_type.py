import json
from typing import Dict, Iterable, Optional, Union
import httpx
from .utils import parse_headers
from typing import List, Any
from pydantic import BaseModel, PrivateAttr

__all__ = [
    "ChatCompletions",
    "ChatCompletionMessage",
    "ChatCompletionMessageToolCall",
    "FunctionCall",
    "TopLogprob",
    "ChatCompletionTokenLogprob",
    "ChoiceLogprobs",
    "Choice",
    "Usage",
    "DeltaToolCall",
    "Delta",
    "StreamChoice",
    "ChatCompletionChunk",
    "ChoiceLogprobs",
]


class TopLogprob(BaseModel, extra="allow"):
    token: Optional[str]
    bytes: Optional[List[int]] = None
    logprob: Optional[float]


class ChatCompletionTokenLogprob(BaseModel, extra="allow"):
    token: Optional[str]
    bytes: Optional[List[int]] = None
    logprob: Optional[float]
    top_logprobs: Optional[List[TopLogprob]]


class ChoiceLogprobs(BaseModel, extra="allow"):
    content: Optional[List[ChatCompletionTokenLogprob]] = None
    refusal: Optional[List[ChatCompletionTokenLogprob]] = None


class Usage(BaseModel, extra="allow"):
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None


class DeltaToolCallFunction(BaseModel, extra="allow"):
    arguments: Optional[str] = None
    name: Optional[str] = None


class DeltaToolCall(BaseModel, extra="allow"):
    index: Optional[int]
    id: Optional[str] = None
    function: Optional[DeltaToolCallFunction] = None
    type: Optional[str] = None


class Delta(BaseModel, extra="allow"):
    role: Optional[str] = None
    content: Optional[str] = ""
    tool_calls: Optional[List[DeltaToolCall]] = None
    refusal: Optional[str] = None


class StreamChoice(BaseModel, extra="allow"):
    index: Optional[int] = None
    delta: Optional[Delta]
    finish_reason: Optional[str] = None
    logprobs: Optional[ChoiceLogprobs] = None

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default

    def __getitem__(self, key):
        return getattr(self, key, None)


class FunctionCall(BaseModel, extra="allow"):
    arguments: Optional[str]
    name: Optional[str]


class ChatCompletionMessageToolCall(BaseModel, extra="allow"):
    id: Optional[str]
    function: Optional[FunctionCall]
    type: Optional[str]


class ChatCompletionMessage(BaseModel, extra="allow"):
    content: Optional[Union[str, Iterable[Any]]] = None
    role: Optional[str]
    function_call: Optional[FunctionCall] = None
    tool_calls: Optional[List[ChatCompletionMessageToolCall]] = None


class Choice(BaseModel, extra="allow"):
    finish_reason: Optional[str]
    index: Optional[int]
    logprobs: Optional[ChoiceLogprobs] = None
    message: Optional[ChatCompletionMessage]


class ChatCompletions(BaseModel, extra="allow"):
    id: Optional[str]
    choices: Optional[List[Choice]]
    created: Optional[int]
    model: Optional[str]
    object: Optional[str]
    system_fingerprint: Optional[str] = None
    usage: Optional[Usage] = None
    service_tier: Optional[str] = None
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


class ChatCompletionChunk(BaseModel, extra="allow"):
    id: Optional[str] = None
    object: Optional[str] = None
    created: Optional[int] = None
    model: Optional[str] = None
    choices: Optional[List[StreamChoice]]
    service_tier: Optional[str] = None

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default
