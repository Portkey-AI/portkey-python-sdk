from __future__ import annotations

import json
from types import TracebackType
from typing import (
    Dict,
    Any,
    Union,
    Mapping,
    cast,
    Optional,
    Type,
    overload,
    Literal,
    get_args,
)
import httpx
import platform

from portkey_ai.api_resources.apis.create_headers import createHeaders
from .global_constants import PORTKEY_HEADER_PREFIX
from .utils import remove_empty_values, Options
from .exceptions import (
    APIStatusError,
    APITimeoutError,
    APIConnectionError,
)
from portkey_ai.version import VERSION
from .utils import ResponseT, make_status_error, default_api_key, default_base_url
from .common_types import StreamT
from .streaming import Stream


class MissingStreamClassError(TypeError):
    def __init__(self) -> None:
        super().__init__(
            "The `stream` argument was set to `True` but the `stream_cls` argument was\
            not given",
        )


class APIClient:
    _client: httpx.Client
    _default_stream_cls: Union[type[Stream[Any]], None] = None

    def __init__(
        self,
        *,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        virtual_key: Optional[str] = None,
        config: Optional[Union[Mapping, str]] = None,
        provider: Optional[str] = None,
        trace_id: Optional[str] = None,
        metadata: Optional[str] = None,
        **kwargs,
    ) -> None:
        self.api_key = api_key or default_api_key()
        self.base_url = base_url or default_base_url()
        self.virtual_key = virtual_key
        self.config = config
        self.provider = provider
        self.trace_id = trace_id
        self.metadata = metadata
        self.kwargs = kwargs

        self.custom_headers = createHeaders(
            virtual_key=virtual_key,
            config=config,
            provider=provider,
            trace_id=trace_id,
            metadata=metadata,
            **kwargs,
        )
        self._client = httpx.Client(
            base_url=self.base_url,
            headers={
                "Accept": "application/json",
            },
        )

        self.response_headers: httpx.Headers | None = None

    def _serialize_header_values(
        self, headers: Optional[Mapping[str, Any]]
    ) -> Dict[str, str]:
        if headers is None:
            return {}
        return {
            f"{PORTKEY_HEADER_PREFIX}{k}": json.dumps(v)
            if isinstance(v, (dict, list))
            else str(v)
            for k, v in headers.items()
        }

    @property
    def custom_auth(self) -> Optional[httpx.Auth]:
        return None

    @overload
    def _post(
        self,
        path: str,
        *,
        body: Mapping[str, Any],
        cast_to: Type[ResponseT],
        stream: Literal[True],
        stream_cls: type[StreamT],
        params: Mapping[str, str],
        headers: Mapping[str, str],
    ) -> StreamT:
        ...

    @overload
    def _post(
        self,
        path: str,
        *,
        body: Mapping[str, Any],
        cast_to: Type[ResponseT],
        stream: Literal[False],
        stream_cls: type[StreamT],
        params: Mapping[str, str],
        headers: Mapping[str, str],
    ) -> ResponseT:
        ...

    @overload
    def _post(
        self,
        path: str,
        *,
        body: Mapping[str, Any],
        cast_to: Type[ResponseT],
        stream: bool,
        stream_cls: type[StreamT],
        params: Mapping[str, str],
        headers: Mapping[str, str],
    ) -> Union[ResponseT, StreamT]:
        ...

    def _post(
        self,
        path: str,
        *,
        body: Mapping[str, Any],
        cast_to: Type[ResponseT],
        stream: bool,
        stream_cls: type[StreamT],
        params: Mapping[str, str],
        headers: Mapping[str, str],
    ) -> Union[ResponseT, StreamT]:
        if path.endswith("/generate"):
            opts = self._construct_generate_options(
                method="post",
                url=path,
                body=body,
                stream=stream,
                params=params,
                headers=headers,
            )
        else:
            opts = self._construct(
                method="post",
                url=path,
                body=body,
                stream=stream,
                params=params,
                headers=headers,
            )

        res = self._request(
            options=opts,
            stream=stream,
            cast_to=cast_to,
            stream_cls=stream_cls,
        )
        return res

    def _construct_generate_options(
        self,
        *,
        method: str,
        url: str,
        body: Any,
        stream: bool,
        params: Mapping[str, str],
        headers: Mapping[str, str],
    ) -> Options:
        opts = Options.construct()
        opts.method = method
        opts.url = url
        json_body = body
        opts.json_body = remove_empty_values(json_body)
        opts.headers = remove_empty_values(headers)
        return opts

    def _construct(
        self,
        *,
        method: str,
        url: str,
        body: Mapping[str, Any],
        stream: bool,
        params: Mapping[str, str],
        headers: Mapping[str, str],
    ) -> Options:
        opts = Options.construct()
        opts.method = method
        opts.url = url
        opts.json_body = remove_empty_values(body)
        opts.headers = remove_empty_values(headers)
        return opts

    @property
    def _default_headers(self) -> Mapping[str, str]:
        return {
            "Content-Type": "application/json",
            f"{PORTKEY_HEADER_PREFIX}api-key": self.api_key,
            f"{PORTKEY_HEADER_PREFIX}package-version": f"portkey-{VERSION}",
            f"{PORTKEY_HEADER_PREFIX}runtime": platform.python_implementation(),
            f"{PORTKEY_HEADER_PREFIX}runtime-version": platform.python_version(),
        }

    def _build_headers(self, options: Options) -> httpx.Headers:
        option_headers = options.headers or {}
        headers_dict = self._merge_mappings(
            self._default_headers, option_headers, self.custom_headers
        )
        headers = httpx.Headers(headers_dict)
        return headers

    def _merge_mappings(
        self,
        *args,
    ) -> Dict[str, Any]:
        """Merge two mappings of the given type
        In cases with duplicate keys the second mapping takes precedence.
        """
        mapped_headers = {}
        for i in args:
            mapped_headers.update(i)
        return mapped_headers

    def is_closed(self) -> bool:
        return self._client.is_closed

    def close(self) -> None:
        """Close the underlying HTTPX client.

        The client will *not* be usable after this.
        """
        self._client.close()

    def __enter__(self: Any) -> Any:
        return self

    def __exit__(
        self,
        exc_type: Optional[BaseException],
        exc: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        self.close()

    def _build_request(self, options: Options) -> httpx.Request:
        headers = self._build_headers(options)
        params = options.params
        json_body = options.json_body
        request = self._client.build_request(
            method=options.method,
            url=options.url,
            headers=headers,
            params=params,
            json=json_body,
            timeout=options.timeout,
        )
        return request

    @overload
    def _request(
        self,
        *,
        options: Options,
        stream: Literal[False],
        cast_to: Type[ResponseT],
        stream_cls: Type[StreamT],
    ) -> ResponseT:
        ...

    @overload
    def _request(
        self,
        *,
        options: Options,
        stream: Literal[True],
        cast_to: Type[ResponseT],
        stream_cls: Type[StreamT],
    ) -> StreamT:
        ...

    @overload
    def _request(
        self,
        *,
        options: Options,
        stream: bool,
        cast_to: Type[ResponseT],
        stream_cls: Type[StreamT],
    ) -> Union[ResponseT, StreamT]:
        ...

    def _request(
        self,
        *,
        options: Options,
        stream: bool,
        cast_to: Type[ResponseT],
        stream_cls: Type[StreamT],
    ) -> Union[ResponseT, StreamT]:
        request = self._build_request(options)
        try:
            res = self._client.send(request, auth=self.custom_auth, stream=stream)
            res.raise_for_status()
        except httpx.HTTPStatusError as err:  # 4xx and 5xx errors
            # If the response is streamed then we need to explicitly read the response
            # to completion before attempting to access the response text.
            err.response.read()
            raise self._make_status_error_from_response(request, err.response) from None
        except httpx.TimeoutException as err:
            raise APITimeoutError(request=request) from err
        except Exception as err:
            raise APIConnectionError(request=request) from err

        self.response_headers = res.headers
        if stream or res.headers["content-type"] == "text/event-stream":
            if stream_cls is None:
                raise MissingStreamClassError()
            stream_response = stream_cls(
                response=res, cast_to=self._extract_stream_chunk_type(stream_cls)
            )
            return stream_response

        response = (
            cast(
                ResponseT,
                cast_to(**res.json()),
            )
            if not isinstance(cast_to, httpx.Response)
            else cast(ResponseT, res)
        )
        response._headers = res.headers  # type: ignore
        return response

    def _extract_stream_chunk_type(self, stream_cls: Type) -> type:
        args = get_args(stream_cls)
        if not args:
            raise TypeError(
                f"Expected stream_cls to have been given a generic type argument, e.g. \
                    Stream[Foo] but received {stream_cls}",
            )
        return cast(type, args[0])

    def _make_status_error_from_response(
        self,
        request: httpx.Request,
        response: httpx.Response,
    ) -> APIStatusError:
        err_text = response.text.strip()
        body = err_text

        try:
            body = json.loads(err_text)["error"]["message"]
            err_msg = f"Error code: {response.status_code} - {body}"
        except Exception:
            err_msg = err_text or f"Error code: {response.status_code}"

        return make_status_error(err_msg, body=body, request=request, response=response)
