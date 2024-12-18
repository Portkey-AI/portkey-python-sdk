import json
from typing import Any, Dict, List, Optional, Union
import httpx
from pydantic import BaseModel, PrivateAttr
from portkey_ai.api_resources.types.utils import parse_headers

__all__ = [
    "SessionCreateResponse",
    "ClientSecret",
    "InputAudioTranscription",
    "Tool",
    "TurnDetection",
]


class ClientSecret(BaseModel, extra="allow"):
    expires_at: Optional[int] = None
    value: Optional[str] = None


class InputAudioTranscription(BaseModel, extra="allow"):
    model: Optional[str] = None


class Tool(BaseModel, extra="allow"):
    description: Optional[str] = None
    name: Optional[str] = None
    parameters: Optional[object] = None
    type: Optional[str] = None


class TurnDetection(BaseModel, extra="allow"):
    prefix_padding_ms: Optional[int] = None
    silence_duration_ms: Optional[int] = None
    threshold: Optional[float] = None
    type: Optional[str] = None


class SessionCreateResponse(BaseModel, extra="allow"):
    client_secret: Optional[ClientSecret] = None
    input_audio_format: Optional[str] = None
    input_audio_transcription: Optional[InputAudioTranscription] = None
    instructions: Optional[str] = None
    max_response_output_tokens: Union[int, str, None] = None
    modalities: Optional[List[str]] = None
    output_audio_format: Optional[str] = None
    temperature: Optional[float] = None
    tool_choice: Optional[str] = None
    tools: Optional[List[Tool]] = None
    turn_detection: Optional[TurnDetection] = None
    voice: Optional[str] = None

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
