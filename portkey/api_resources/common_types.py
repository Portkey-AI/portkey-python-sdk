from typing import TypeVar, Union, Any
from .streaming import Stream
from .utils import ChatCompletionChunk, TextCompletionChunk, GenericResponse

StreamT = TypeVar(
    "StreamT",
    bound=Stream[Union[ChatCompletionChunk, TextCompletionChunk, GenericResponse]],
)
