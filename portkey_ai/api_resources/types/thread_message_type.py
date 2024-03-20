import json
from typing import Dict, List, Optional, Union
import httpx
from portkey_ai.api_resources.utils import parse_headers
from pydantic import BaseModel

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


class TextAnnotationFilePathFilePath(BaseModel):
    file_id: Optional[str]


class TextAnnotationFileCitationFileCitation(BaseModel):
    file_id: Optional[str]
    quote: Optional[str]


class TextAnnotationFilePath(BaseModel):
    end_index: Optional[int]
    file_path: Optional[TextAnnotationFilePathFilePath]
    start_index: Optional[int]
    text: Optional[str]
    type: Optional[str]


class TextAnnotationFileCitation(BaseModel):
    end_index: Optional[int]
    file_citation: Optional[TextAnnotationFileCitationFileCitation]
    start_index: Optional[int]
    text: Optional[str]
    type: Optional[str]


TextAnnotation = Union[TextAnnotationFileCitation, TextAnnotationFilePath]


class Text(BaseModel):
    annotations: Optional[List[TextAnnotation]]
    value: Optional[str]


class MessageContentText(BaseModel):
    text: Optional[Text]
    type: Optional[str]


class ImageFile(BaseModel):
    file_id: Optional[str]


class MessageContentImageFile(BaseModel):
    image_file: Optional[ImageFile]
    type: Optional[str]


Content = Union[MessageContentImageFile, MessageContentText]


class ThreadMessage(BaseModel, extra="allow"):
    id: Optional[str]
    assistant_id: Optional[str] = None
    content: Optional[List[Content]]
    created_at: Optional[int]
    file_ids: Optional[List[str]]
    metadata: Optional[object] = None
    object: Optional[str]
    role: Optional[str]
    run_id: Optional[str] = None
    thread_id: Optional[str]
    _headers: Optional[httpx.Headers] = None

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
    _headers: Optional[httpx.Headers] = None

    def __str__(self):
        del self._headers
        return json.dumps(self.dict(), indent=4)

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)


class MessageFile(BaseModel, extra="allow"):
    id: Optional[str]
    object: Optional[str]
    created_at: Optional[int]
    message_id: Optional[str]
    _headers: Optional[httpx.Headers] = None

    def __str__(self):
        del self._headers
        return json.dumps(self.dict(), indent=4)

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)
