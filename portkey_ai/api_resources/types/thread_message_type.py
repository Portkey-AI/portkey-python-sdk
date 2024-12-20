import json
from typing import Dict, List, Optional, Union
import httpx

from portkey_ai.api_resources.types.assistant_type import ToolCodeInterpreter
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
    "Attachment",
    "AttachmentTool",
    "AttachmentToolAssistantToolsFileSearchTypeOnly",
    "IncompleteDetails",
    "ThreadMessageDeleted",
    "RefusalContentBlock",
    "ImageURL",
    "ImageURLContentBlock",
]


class IncompleteDetails(BaseModel, extra="allow"):
    reason: Optional[str] = None


class AttachmentToolAssistantToolsFileSearchTypeOnly(BaseModel, extra="allow"):
    type: Optional[str] = None


AttachmentTool = Union[
    ToolCodeInterpreter, AttachmentToolAssistantToolsFileSearchTypeOnly
]


class Attachment(BaseModel, extra="allow"):
    file_id: Optional[str] = None
    tools: Optional[List[AttachmentTool]] = None


class TextAnnotationFilePathFilePath(BaseModel, extra="allow"):
    file_id: Optional[str] = None


class TextAnnotationFileCitationFileCitation(BaseModel, extra="allow"):
    file_id: Optional[str] = None
    quote: Optional[str] = None


class TextAnnotationFilePath(BaseModel, extra="allow"):
    end_index: Optional[int] = None
    file_path: Optional[TextAnnotationFilePathFilePath]
    start_index: Optional[int] = None
    text: Optional[str] = None
    type: Optional[str] = None


class TextAnnotationFileCitation(BaseModel, extra="allow"):
    end_index: Optional[int] = None
    file_citation: Optional[TextAnnotationFileCitationFileCitation]
    start_index: Optional[int] = None
    text: Optional[str] = None
    type: Optional[str] = None


TextAnnotation = Union[TextAnnotationFileCitation, TextAnnotationFilePath]


class Text(BaseModel, extra="allow"):
    annotations: Optional[List[TextAnnotation]]
    value: Optional[str] = None


class RefusalContentBlock(BaseModel, extra="allow"):
    refusal: Optional[str] = None
    type: Optional[str] = None


class ImageURL(BaseModel, extra="allow"):
    url: Optional[str] = None
    detail: Optional[str] = None


class ImageURLContentBlock(BaseModel, extra="allow"):
    image_url: ImageURL
    type: Optional[str] = None


class MessageContentText(BaseModel, extra="allow"):
    text: Optional[Text]
    type: Optional[str] = None


class ImageFile(BaseModel, extra="allow"):
    file_id: Optional[str] = None
    detail: Optional[str] = None


class MessageContentImageFile(BaseModel, extra="allow"):
    image_file: Optional[ImageFile]
    type: Optional[str] = None


Content = Union[
    MessageContentImageFile,
    ImageURLContentBlock,
    MessageContentText,
    RefusalContentBlock,
]


class ThreadMessage(BaseModel, extra="allow"):
    id: Optional[str] = None
    assistant_id: Optional[str] = None
    content: Optional[List[Content]]
    created_at: Optional[int] = None
    file_ids: Optional[List[str]] = None
    metadata: Optional[object] = None
    object: Optional[str] = None
    role: Optional[str] = None
    run_id: Optional[str] = None
    thread_id: Optional[str] = None
    attachments: Optional[List[Attachment]] = None
    incomplete_at: Optional[int] = None
    incomplete_details: Optional[IncompleteDetails] = None
    completed_at: Optional[int] = None
    status: Optional[str] = None

    _headers: Optional[httpx.Headers] = PrivateAttr()

    def __str__(self):
        del self._headers
        return json.dumps(self.dict(), indent=4)

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)


class MessageList(BaseModel, extra="allow"):
    object: Optional[str] = None
    data: Optional[List[ThreadMessage]]
    first_id: Optional[str] = None
    last_id: Optional[str] = None
    has_more: Optional[bool] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def __str__(self):
        del self._headers
        return json.dumps(self.dict(), indent=4)

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)


class ThreadMessageDeleted(BaseModel, extra="allow"):
    id: Optional[str] = None
    deleted: Optional[bool] = None
    object: Optional[str] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def __str__(self):
        del self._headers
        return json.dumps(self.dict(), indent=4)

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)
