from typing import TypeVar, Union

import httpx
from .streaming import Stream, AsyncStream
from .utils import ChatCompletionChunk, TextCompletionChunk, GenericResponse

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
