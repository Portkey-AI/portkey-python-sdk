from __future__ import annotations
import json
from typing import Any, Iterator, AsyncIterator, Generic, cast, Union, Type
import httpx
from .utils import (
    ResponseT,
    make_status_error,
)
from types import TracebackType
from typing_extensions import Self


class ServerSentEvent:
    def __init__(
        self,
        *,
        event: Union[str, None] = None,
        data: Union[str, None] = None,
        id: Union[str, None] = None,
        retry: Union[int, None] = None,
    ) -> None:
        if data is None:
            data = ""

        self._id = id
        self._data = data
        self._event = event or None
        self._retry = retry

    @property
    def event(self) -> Union[str, None]:
        return self._event

    @property
    def id(self) -> Union[str, None]:
        return self._id

    @property
    def retry(self) -> Union[int, None]:
        return self._retry

    @property
    def data(self) -> str:
        return self._data

    def json(self) -> Any:
        return json.loads(self.data)

    def __repr__(self) -> str:
        return f"ServerSentEvent(event={self.event}, data={self.data}, id={self.id},\
            retry={self.retry})"


class SSEDecoder:
    _data: list[str]
    _event: Union[str, None]
    _retry: Union[int, None]
    _last_event_id: Union[str, None]

    def __init__(self) -> None:
        self._event = None
        self._data = []
        self._last_event_id = None
        self._retry = None

    def iter(self, iterator: Iterator[str]) -> Iterator[ServerSentEvent]:
        """Given an iterator that yields lines, iterate over it & yield every
        event encountered
        """
        for line in iterator:
            line = line.rstrip("\n")
            sse = self.decode(line)
            if sse is not None:
                yield sse

    async def aiter(
        self, iterator: AsyncIterator[str]
    ) -> AsyncIterator[ServerSentEvent]:
        """Given an async iterator that yields lines,
        iterate over it & yield every event encountered"""
        async for line in iterator:
            line = line.rstrip("\n")
            sse = self.decode(line)
            if sse is not None:
                yield sse

    def decode(self, line: str) -> Union[ServerSentEvent, None]:
        # See: https://html.spec.whatwg.org/multipage/server-sent-events.html#event-stream-interpretation  # noqa: E501

        if not line:
            if (
                not self._event
                and not self._data
                and not self._last_event_id
                and self._retry is None
            ):
                return None

            sse = ServerSentEvent(
                event=self._event,
                data="\n".join(self._data),
                id=self._last_event_id,
                retry=self._retry,
            )

            # NOTE: as per the SSE spec, do not reset last_event_id.
            self._event = None
            self._data = []
            self._retry = None

            return sse

        if line.startswith(":"):
            return None

        fieldname, _, value = line.partition(":")

        if value.startswith(" "):
            value = value[1:]

        if fieldname == "event":
            self._event = value
        elif fieldname == "data":
            self._data.append(value)
        elif fieldname == "id":
            if "\0" in value:
                pass
            else:
                self._last_event_id = value
        elif fieldname == "retry":
            try:
                self._retry = int(value)
            except (TypeError, ValueError):
                pass
        else:
            pass  # Field is ignored.

        return None


class Stream(Generic[ResponseT]):
    """Provides the core interface to iterate over a synchronous stream response."""

    response: httpx.Response

    def __init__(self, *, response: httpx.Response, cast_to: Type[ResponseT]) -> None:
        self._cast_to = cast_to
        self.response = response
        self._decoder = SSEDecoder()
        self._iterator = self.__stream__()

    def __next__(self) -> ResponseT:
        return self._iterator.__next__()

    def __iter__(self) -> Iterator[ResponseT]:
        for item in self._iterator:
            yield item

    def _iter_events(self) -> Iterator[ServerSentEvent]:
        yield from self._decoder.iter(self.response.iter_lines())

    def __stream__(self) -> Iterator[ResponseT]:
        response = self.response
        for sse in self._iter_events():
            if sse.data.startswith("[DONE]"):
                break
            if sse.event is None:
                yield cast(ResponseT, self._cast_to(**sse.json())) if not isinstance(
                    self._cast_to, httpx.Response
                ) else cast(ResponseT, sse)

            if sse.event == "ping":
                continue

            if sse.event == "error":
                body = sse.data

                try:
                    body = sse.json()
                    err_msg = f"{body}"
                except Exception:
                    err_msg = sse.data or f"Error code: {response.status_code}"

                raise make_status_error(
                    err_msg,
                    body=body,
                    response=self.response,
                    request=self.response.request,
                )

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.close()

    def close(self) -> None:
        self.response.close()


class AsyncStream(Generic[ResponseT]):
    """Provides the core interface to iterate over a asynchronous stream response."""

    response: httpx.Response

    def __init__(self, *, response: httpx.Response, cast_to: Type[ResponseT]) -> None:
        self._cast_to = cast_to
        self.response = response
        self._decoder = SSEDecoder()
        self._iterator = self.__stream__()

    async def __anext__(self) -> ResponseT:
        return await self._iterator.__anext__()

    async def __aiter__(self) -> AsyncIterator[ResponseT]:
        async for item in self._iterator:
            yield item

    async def _iter_events(self) -> AsyncIterator[ServerSentEvent]:
        async for sse in self._decoder.aiter(self.response.aiter_lines()):
            yield sse

    async def __stream__(self) -> AsyncIterator[ResponseT]:
        response = self.response

        async for sse in self._iter_events():
            if sse.data.startswith("[DONE]"):
                break
            if sse.event is None:
                yield cast(ResponseT, self._cast_to(**sse.json())) if not isinstance(
                    self._cast_to, httpx.Response
                ) else cast(ResponseT, sse)

            if sse.event == "ping":
                continue

            if sse.event == "error":
                body = sse.data

                try:
                    body = sse.json()
                    err_msg = f"{body}"
                except Exception:
                    err_msg = sse.data or f"Error code: {response.status_code}"

                raise make_status_error(
                    err_msg,
                    body=body,
                    response=self.response,
                    request=self.response.request,
                )

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.close()

    async def close(self) -> None:
        await self.response.aclose()
