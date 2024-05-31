import json
from typing import Dict, Optional, Union
import httpx

from portkey_ai.api_resources.types.chat_complete_type import (
    ChatCompletionMessage,
    Choice,
    StreamChoice,
    Usage,
)
from portkey_ai.api_resources.types.complete_type import Logprobs, TextChoice

from .utils import parse_headers
from typing import List, Any
from pydantic import BaseModel, PrivateAttr


class PromptCompletion(BaseModel):
    id: Optional[str] = None
    choices: Optional[List[Choice]] = None
    created: Optional[int] = None
    model: Optional[str] = None
    object: Optional[str] = None
    system_fingerprint: Optional[str] = None
    usage: Optional[Usage] = None
    index: Optional[int] = None
    text: Optional[str] = None
    logprobs: Optional[Logprobs] = None
    finish_reason: Optional[str] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)


class PromptCompletionChunk(BaseModel):
    id: Optional[str] = None
    object: Optional[str] = None
    created: Optional[int] = None
    model: Optional[str] = None
    provider: Optional[str] = None
    choices: Optional[Union[List[TextChoice], List[StreamChoice]]] = None

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


FunctionParameters = Dict[str, object]


class Function(BaseModel):
    name: Optional[str]
    description: Optional[str] = None
    parameters: Optional[FunctionParameters] = None


class Tool(BaseModel):
    function: Function
    type: Optional[str]


class PromptRenderData(BaseModel):
    messages: Optional[List[ChatCompletionMessage]] = None
    prompt: Optional[str] = None
    model: Optional[str] = None
    suffix: Optional[str] = None
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    top_k: Optional[int] = None
    top_p: Optional[float] = None
    n: Optional[int] = None
    stop_sequences: Optional[List[str]] = None
    timeout: Union[float, None] = None
    functions: Optional[List[Function]] = None
    function_call: Optional[Union[None, str, Function]] = None
    logprobs: Optional[bool] = None
    top_logprobs: Optional[int] = None
    echo: Optional[bool] = None
    stop: Optional[Union[str, List[str]]] = None
    presence_penalty: Optional[int] = None
    frequency_penalty: Optional[int] = None
    best_of: Optional[int] = None
    logit_bias: Optional[Dict[str, int]] = None
    user: Optional[str] = None
    organization: Optional[str] = None
    tool_choice: Optional[Union[None, str]] = None
    tools: Optional[List[Tool]] = None


class PromptRender(BaseModel):
    success: Optional[bool] = True
    data: PromptRenderData

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default
