import json
from typing import Dict, List, Literal, Optional
import httpx

from portkey_ai._vendor.openai.types.beta.chatkit.chat_session_chatkit_configuration import (
    ChatSessionChatKitConfiguration,
)
from portkey_ai._vendor.openai.types.beta.chatkit.chat_session_rate_limits import (
    ChatSessionRateLimits,
)
from portkey_ai._vendor.openai.types.beta.chatkit.chat_session_status import (
    ChatSessionStatus,
)
from portkey_ai._vendor.openai.types.beta.chatkit.chatkit_thread import Status
from portkey_ai._vendor.openai.types.beta.chatkit_workflow import ChatKitWorkflow
from .utils import parse_headers
from typing import Any
from pydantic import BaseModel, PrivateAttr


class ChatSession(BaseModel, extra="allow"):
    id: str
    chatkit_configuration: ChatSessionChatKitConfiguration
    client_secret: str
    expires_at: int
    max_requests_per_1_minute: int
    object: Literal["chatkit.session"]
    rate_limits: ChatSessionRateLimits
    status: ChatSessionStatus
    user: str
    workflow: ChatKitWorkflow
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


class ChatKitThread(BaseModel, extra="allow"):
    id: str
    created_at: int
    object: Literal["chatkit.thread"]
    status: Status
    title: Optional[str] = None
    user: str
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


class ChatKitThreadList(BaseModel, extra="allow"):
    object: Literal["list"]
    data: List[ChatKitThread]
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


class ThreadDeleteResponse(BaseModel, extra="allow"):
    id: str
    deleted: bool
    object: Literal["chatkit.thread.deleted"]
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
