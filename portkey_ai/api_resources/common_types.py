from typing import TypeVar, Union

import httpx

from portkey_ai.api_resources.types.generation_type import PromptCompletionChunk
from .streaming import Stream, AsyncStream
from .utils import GenericResponse
from .types.chat_complete_type import ChatCompletionChunk
from .types.complete_type import TextCompletionChunk

StreamT = TypeVar(
    "StreamT",
    bound=Stream[
        Union[
            ChatCompletionChunk,
            TextCompletionChunk,
            GenericResponse,
            PromptCompletionChunk,
            httpx.Response,
        ]
    ],
)

AsyncStreamT = TypeVar(
    "AsyncStreamT",
    bound=AsyncStream[
        Union[
            ChatCompletionChunk,
            TextCompletionChunk,
            GenericResponse,
            PromptCompletionChunk,
            httpx.Response,
        ]
    ],
)
