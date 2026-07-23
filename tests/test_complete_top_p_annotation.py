import inspect
import typing

from portkey_ai import AsyncCompletion, Completion


def test_completion_top_p_is_typed_as_float():
    annotation = inspect.signature(Completion.create).parameters["top_p"].annotation
    args = typing.get_args(annotation)
    assert float in args
    assert bool not in args


def test_async_completion_top_p_is_typed_as_float():
    annotation = (
        inspect.signature(AsyncCompletion.create).parameters["top_p"].annotation
    )
    args = typing.get_args(annotation)
    assert float in args
    assert bool not in args
