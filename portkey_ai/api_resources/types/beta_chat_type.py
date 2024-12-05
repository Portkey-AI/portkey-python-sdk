from typing import Optional, TypeVar, List, Any
import json
from pydantic import BaseModel
from .chat_complete_type import (
    ChatCompletions,
    Choice,
    ChatCompletionMessage,
    ChatCompletionMessageToolCall,
    FunctionCall,
)

__all__ = [
    "ParsedChatCompletion",
    "ParsedChoice",
    "ParsedChatCompletionMessage",
    "ParsedFunction",
    "ParsedFunctionToolCall",
]

ContentType = TypeVar("ContentType")


class ParsedFunction(FunctionCall, BaseModel, extra="allow"):
    parsed_arguments: Optional[Any] = None


class ParsedFunctionToolCall(ChatCompletionMessageToolCall, BaseModel, extra="allow"):
    function: ParsedFunction


class ParsedChatCompletionMessage(ChatCompletionMessage, BaseModel, extra="allow"):
    parsed: Optional[Any] = None
    tool_calls: Optional[List[ParsedFunctionToolCall]] = None  # type: ignore[assignment]


class ParsedChoice(Choice, BaseModel, extra="allow"):
    message: ParsedChatCompletionMessage


class ParsedChatCompletion(ChatCompletions, BaseModel, extra="allow"):
    choices: List[ParsedChoice]  # type: ignore[assignment]

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default
