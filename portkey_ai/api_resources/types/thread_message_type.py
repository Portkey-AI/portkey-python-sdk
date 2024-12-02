import json
from typing import Dict, List, Optional, Union
import httpx
from .utils import parse_headers
from pydantic import BaseModel, PrivateAttr

__all__ = [
    "ThreadMessage",
    "MessageList",
    "Content",
    "Text",
    "TextAnnotation",
    "TextAnnotationFileCitation",
    "TextAnnotationFileCitationFileCitation",
    "TextAnnotationFilePath",
    "TextAnnotationFilePathFilePath",
    "MessageContentImageFile",
    "ImageFile",
    "MessageContentText",
]


class TextAnnotationFilePathFilePath(BaseModel, extra="allow"):
    file_id: Optional[str]


class TextAnnotationFileCitationFileCitation(BaseModel, extra="allow"):
    file_id: Optional[str]
    quote: Optional[str]


class TextAnnotationFilePath(BaseModel, extra="allow"):
    end_index: Optional[int]
    file_path: Optional[TextAnnotationFilePathFilePath]
    start_index: Optional[int]
    text: Optional[str]
    type: Optional[str]


class TextAnnotationFileCitation(BaseModel, extra="allow"):
    end_index: Optional[int]
    file_citation: Optional[TextAnnotationFileCitationFileCitation]
    start_index: Optional[int]
    text: Optional[str]
    type: Optional[str]


TextAnnotation = Union[TextAnnotationFileCitation, TextAnnotationFilePath]


class Text(BaseModel, extra="allow"):
    annotations: Optional[List[TextAnnotation]]
    value: Optional[str]


class MessageContentText(BaseModel, extra="allow"):
    text: Optional[Text]
    type: Optional[str]


class ImageFile(BaseModel, extra="allow"):
    file_id: Optional[str]


class MessageContentImageFile(BaseModel, extra="allow"):
    image_file: Optional[ImageFile]
    type: Optional[str]


Content = Union[MessageContentImageFile, MessageContentText]


class ThreadMessage(BaseModel, extra="allow"):
    id: Optional[str]
    assistant_id: Optional[str] = None
    content: Optional[List[Content]]
    created_at: Optional[int]
    file_ids: Optional[List[str]] = None
    metadata: Optional[object] = None
    object: Optional[str]
    role: Optional[str]
    run_id: Optional[str] = None
    thread_id: Optional[str]
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def __str__(self):
        del self._headers
        return json.dumps(self.dict(), indent=4)

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)


class MessageList(BaseModel, extra="allow"):
    object: Optional[str]
    data: Optional[List[ThreadMessage]]
    first_id: Optional[str]
    last_id: Optional[str]
    has_more: Optional[bool]
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def __str__(self):
        del self._headers
        return json.dumps(self.dict(), indent=4)

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)


class ThreadMessageDeleted(BaseModel, extra="allow"):
    id: str
    deleted: bool
    object: str
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def __str__(self):
        del self._headers
        return json.dumps(self.dict(), indent=4)

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)
