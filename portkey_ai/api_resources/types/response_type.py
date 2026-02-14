import json
from typing import Any, Dict, List, Literal, Optional
import httpx
from pydantic import BaseModel, PrivateAttr

from portkey_ai._vendor.openai.types.responses.response import ToolChoice
from portkey_ai._vendor.openai.types.responses.response_output_item import (
    ResponseOutputItem,
)
from portkey_ai._vendor.openai.types.responses.response_status import ResponseStatus
from portkey_ai._vendor.openai.types.responses.response_text_config import (
    ResponseTextConfig,
)
from portkey_ai._vendor.openai.types.responses.response_usage import ResponseUsage
from portkey_ai._vendor.openai.types.responses.tool import Tool
from portkey_ai._vendor.openai.types.shared.reasoning import Reasoning
from portkey_ai.api_resources.types.shared_types import Metadata
from portkey_ai.api_resources.types.utils import parse_headers


class CompactedResponse(BaseModel, extra="allow"):
    id: str
    """The unique identifier for the compacted response."""

    created_at: int
    """Unix timestamp (in seconds) when the compacted conversation was created."""

    object: Literal["response.compaction"]
    """The object type. Always `response.compaction`."""

    output: List[ResponseOutputItem]
    """The compacted list of output items."""

    usage: ResponseUsage
    """Token accounting for the compaction pass."""

    _headers: Optional[httpx.Headers] = PrivateAttr()

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)


class ResponseError(BaseModel, extra="allow"):
    code: Literal[
        "server_error",
        "rate_limit_exceeded",
        "invalid_prompt",
        "vector_store_timeout",
        "invalid_image",
        "invalid_image_format",
        "invalid_base64_image",
        "invalid_image_url",
        "image_too_large",
        "image_too_small",
        "image_parse_error",
        "image_content_policy_violation",
        "invalid_image_mode",
        "image_file_too_large",
        "unsupported_image_media_type",
        "empty_image_file",
        "failed_to_download_image",
        "image_file_not_found",
    ]
    """The error code for the response."""

    message: str
    """A human-readable description of the error."""


class IncompleteDetails(BaseModel, extra="allow"):
    reason: Optional[Literal["max_output_tokens", "content_filter"]] = None


class Response(BaseModel, extra="allow"):
    id: str
    created_at: float
    error: Optional[ResponseError] = None
    incomplete_details: Optional[IncompleteDetails] = None
    instructions: Optional[str] = None
    metadata: Optional[Metadata] = None
    model: Optional[str] = None
    object: Literal["response"]
    output: List[ResponseOutputItem]
    parallel_tool_calls: bool
    temperature: Optional[float] = None
    tool_choice: ToolChoice
    tools: List[Tool]
    top_p: Optional[float] = None
    max_output_tokens: Optional[int] = None
    previous_response_id: Optional[str] = None
    reasoning: Optional[Reasoning] = None
    status: Optional[ResponseStatus] = None
    text: Optional[ResponseTextConfig] = None
    truncation: Optional[Literal["auto", "disabled"]] = None
    usage: Optional[ResponseUsage] = None
    user: Optional[str] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    @property
    def output_text(self) -> str:
        texts: List[str] = []
        for output in self.output:
            if output.type == "message":
                for content in output.content:
                    if content.type == "output_text":
                        texts.append(content.text)

        return "".join(texts)

    def __str__(self):
        del self._headers
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)
