from typing import TypeVar, Union

import httpx
from .streaming import Stream, AsyncStream
from .utils import GenericResponse
from .types.chat_complete_type import ChatCompletionChunk
from .types.complete_type import TextCompletionChunk

StreamT = TypeVar(
    "StreamT",
    bound=Stream[
        Union[ChatCompletionChunk, TextCompletionChunk, GenericResponse, httpx.Response]
    ],
)

AsyncStreamT = TypeVar(
    "AsyncStreamT",
    bound=AsyncStream[
        Union[ChatCompletionChunk, TextCompletionChunk, GenericResponse, httpx.Response]
    ],
)
