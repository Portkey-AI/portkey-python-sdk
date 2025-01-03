import json
from typing import Dict, List, Optional
import httpx
from .utils import parse_headers
from typing import Any
from pydantic import BaseModel, PrivateAttr

__all__ = ["Transcription", "Translation"]


class TranscriptionSegment(BaseModel, extra="allow"):
    id: Optional[int] = None
    avg_logprob: Optional[float] = None
    compression_ratio: Optional[float] = None
    end: Optional[float] = None
    no_speech_prob: Optional[float] = None
    seek: Optional[int] = None
    start: Optional[float] = None
    temperature: Optional[float] = None
    text: Optional[str] = None
    tokens: Optional[List[int]] = None


class TranscriptionWord(BaseModel, extra="allow"):
    start: Optional[float] = None
    end: Optional[float] = None
    word: Optional[str] = None


class TranscriptionVerbose(BaseModel, extra="allow"):
    duration: Optional[str] = None
    language: Optional[str] = None
    text: Optional[str] = None
    segments: Optional[List[TranscriptionSegment]] = None
    words: Optional[List[TranscriptionWord]] = None
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


class Transcription(BaseModel, extra="allow"):
    text: Optional[str] = None
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


class TranslationVerbose(BaseModel, extra="allow"):
    duration: Optional[str] = None
    language: Optional[str] = None
    text: Optional[str] = None
    segments: Optional[List[TranscriptionSegment]] = None
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


class Translation(BaseModel, extra="allow"):
    text: Optional[str] = None
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
