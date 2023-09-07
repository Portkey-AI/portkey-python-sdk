from __future__ import annotations

import json
from types import TracebackType
from typing import (
    Dict,
    Any,
    Union,
    Mapping,
    cast,
    List,
    Optional,
    Type,
    overload,
    Literal,
)
import httpx
import platform
from .global_constants import PORTKEY_HEADER_PREFIX
from .utils import (
    remove_empty_values,
    Body,
    Options,
    RequestConfig,
    OverrideParams,
    ProviderOptions,
    PortkeyResponse,
    Params,
)
from .exceptions import (
    APIStatusError,
    APITimeoutError,
    APIConnectionError,
)
from portkey.version import VERSION
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
    ) -> None:
        self.api_key = api_key or default_api_key()
        self.base_url = base_url or default_base_url()
        self._client = httpx.Client(
            base_url=self.base_url,
            headers={"Accept": "application/json"},
        )

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
    def post(
        self,
        path: str,
        *,
        body: List[Body],
        mode: str,
        cast_to: Type[ResponseT],
        stream: Literal[True],
        stream_cls: type[StreamT],
        params: Params,
    ) -> StreamT:
        ...

    @overload
    def post(
        self,
        path: str,
        *,
        body: List[Body],
        mode: str,
        cast_to: Type[ResponseT],
        stream: Literal[False],
        stream_cls: type[StreamT],
        params: Params,
    ) -> ResponseT:
        ...

    @overload
    def post(
        self,
        path: str,
        *,
        body: List[Body],
        mode: str,
        cast_to: Type[ResponseT],
        stream: bool,
        stream_cls: type[StreamT],
        params: Params,
    ) -> Union[ResponseT, StreamT]:
        ...

    def post(
        self,
        path: str,
        *,
        body: List[Body],
        mode: str,
        cast_to: Type[ResponseT],
        stream: bool,
        stream_cls: type[StreamT],
        params: Params,
    ) -> Union[ResponseT, StreamT]:
        body = cast(List[Body], body)
        opts = self._construct(
            method="post", url=path, body=body, mode=mode, stream=stream, params=params
        )
        res = self._request(
            options=opts,
            stream=stream,
            cast_to=cast_to,
            stream_cls=stream_cls,
        )
        return res

    def _construct(
        self,
        *,
        method: str,
        url: str,
        body: List[Body],
        mode: str,
        stream: bool,
        params: Params,
    ) -> Options:
        opts = Options.construct()
        opts.method = method
        opts.url = url
        params_dict = {} if params is None else params.dict()
        json_body = {
            "config": self._config(mode, body).dict(),
            "params": {**params_dict, "stream": stream},
        }
        opts.json_body = remove_empty_values(json_body)
        opts.headers = None
        return opts

    def _config(self, mode: str, body: List[Body]) -> RequestConfig:
        config = RequestConfig(mode=mode, options=[])
        for i in body:
            item = i.dict()
            override_params = cast(OverrideParams, i.dict())
            options = ProviderOptions(
                virtualKey=item.get("virtual_key"),
                provider=item.get("provider"),
                apiKey=item.get("api_key"),
                weight=item.get("weight"),
                retry=item.get("retry"),
                override_params=override_params,
            )
            config.options.append(options)
        return config

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
        custom_headers = options.headers or {}
        headers_dict = self._merge_mappings(self._default_headers, custom_headers)
        headers = httpx.Headers(headers_dict)
        return headers

    def _merge_mappings(
        self,
        obj1: Mapping[str, Any],
        obj2: Mapping[str, Any],
    ) -> Dict[str, Any]:
        """Merge two mappings of the given type
        In cases with duplicate keys the second mapping takes precedence.
        """
        return {**obj1, **obj2}

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
        stream_cls: Union[type[StreamT], None] = None,
    ) -> ResponseT:
        ...

    @overload
    def _request(
        self,
        *,
        options: Options,
        stream: Literal[True],
        cast_to: Type[ResponseT],
        stream_cls: Union[type[StreamT], None] = None,
    ) -> StreamT:
        ...

    @overload
    def _request(
        self,
        *,
        options: Options,
        stream: bool,
        cast_to: Type[ResponseT],
        stream_cls: Union[type[StreamT], None] = None,
    ) -> Union[ResponseT, StreamT]:
        ...

    def _request(
        self,
        *,
        options: Options,
        stream: bool,
        cast_to: Type[ResponseT],
        stream_cls: Union[type[StreamT], None] = None,
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
        if stream:
            stream_cls = stream_cls or cast(
                "Union[type[StreamT], None]", self._default_stream_cls
            )
            if stream_cls is None:
                raise MissingStreamClassError()
            stream_response = stream_cls(response=res)
            return stream_response
        response = cast(
            ResponseT,
            PortkeyResponse.construct(**res.json(), raw_body=res.json()),
        )
        return response

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
