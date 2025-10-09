import json
from typing import Dict, Literal, Optional, List
import httpx

from portkey_ai._vendor.openai.types.video_create_error import VideoCreateError
from portkey_ai._vendor.openai.types.video_model import VideoModel
from portkey_ai._vendor.openai.types.video_seconds import VideoSeconds
from portkey_ai._vendor.openai.types.video_size import VideoSize
from .utils import parse_headers
from typing import Any
from pydantic import BaseModel, PrivateAttr


class Video(BaseModel, extra="allow"):
    id: str
    completed_at: Optional[int] = None
    created_at: int
    error: Optional[VideoCreateError] = None
    expires_at: Optional[int] = None
    model: VideoModel
    object: Literal["video"]
    progress: int
    remixed_from_video_id: Optional[str] = None
    seconds: VideoSeconds
    size: VideoSize
    status: Literal["queued", "in_progress", "completed", "failed"]
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


class VideoList(BaseModel, extra="allow"):
    object: Optional[str] = None
    data: Optional[List[Video]] = None
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


class VideoDeleteResponse(BaseModel, extra="allow"):
    id: str
    deleted: bool
    object: Literal["video.deleted"]
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
