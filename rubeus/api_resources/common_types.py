from typing import TypeVar, Any
from .streaming import Stream

StreamT = TypeVar(
    "StreamT",
    bound=Stream[Any],
)
