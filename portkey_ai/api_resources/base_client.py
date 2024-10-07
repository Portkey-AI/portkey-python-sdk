from __future__ import annotations
import asyncio

import json
from types import TracebackType
from typing import (
    Dict,
    Any,
    List,
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
from .common_types import StreamT, AsyncStreamT
from .streaming import Stream, AsyncStream


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
        metadata: Union[Optional[dict[str, str]], str] = None,
        cache_namespace: Optional[str] = None,
        debug: Optional[bool] = None,
        cache_force_refresh: Optional[bool] = None,
        custom_host: Optional[str] = None,
        forward_headers: Optional[List[str]] = None,
        openai_project: Optional[str] = None,
        openai_organization: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        aws_access_key_id: Optional[str] = None,
        aws_session_token: Optional[str] = None,
        aws_region: Optional[str] = None,
        vertex_project_id: Optional[str] = None,
        vertex_region: Optional[str] = None,
        workers_ai_account_id: Optional[str] = None,
        azure_resource_name: Optional[str] = None,
        azure_deployment_id: Optional[str] = None,
        azure_api_version: Optional[str] = None,
        huggingface_base_url: Optional[str] = None,
        http_client: Optional[httpx.Client] = None,
        request_timeout: Optional[int] = None,
        strict_open_ai_compliance: Optional[bool] = None,
        anthropic_beta: Optional[str] = None,
        **kwargs,
    ) -> None:
        self.api_key = api_key or default_api_key()
        self.base_url = base_url or default_base_url()
        self.virtual_key = virtual_key
        self.config = config
        self.provider = provider
        self.trace_id = trace_id
        self.metadata = metadata
        self.debug = debug
        self.cache_force_refresh = cache_force_refresh
        self.custom_host = custom_host
        self.forward_headers = forward_headers
        self.openai_project = openai_project
        self.openai_organization = openai_organization
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_access_key_id = aws_access_key_id
        self.aws_session_token = aws_session_token
        self.aws_region = aws_region
        self.vertex_project_id = vertex_project_id
        self.vertex_region = vertex_region
        self.workers_ai_account_id = workers_ai_account_id
        self.azure_resource_name = azure_resource_name
        self.azure_deployment_id = azure_deployment_id
        self.azure_api_version = azure_api_version
        self.huggingface_base_url = huggingface_base_url
        self.cache_namespace = cache_namespace
        self.request_timeout = request_timeout
        self.strict_open_ai_compliance = strict_open_ai_compliance
        self.anthropic_beta = anthropic_beta
        self.kwargs = kwargs

        self.custom_headers = createHeaders(
            api_key=api_key,
            virtual_key=virtual_key,
            config=config,
            provider=provider,
            trace_id=trace_id,
            metadata=metadata,
            debug=debug,
            cache_force_refresh=cache_force_refresh,
            custom_host=custom_host,
            forward_headers=forward_headers,
            openai_project=openai_project,
            openai_organization=openai_organization,
            aws_secret_access_key=aws_secret_access_key,
            aws_access_key_id=aws_access_key_id,
            aws_session_token=aws_session_token,
            aws_region=aws_region,
            vertex_project_id=vertex_project_id,
            vertex_region=vertex_region,
            workers_ai_account_id=workers_ai_account_id,
            azure_resource_name=azure_resource_name,
            azure_deployment_id=azure_deployment_id,
            azure_api_version=azure_api_version,
            huggingface_base_url=huggingface_base_url,
            cache_namespace=cache_namespace,
            request_timeout=request_timeout,
            strict_open_ai_compliance=strict_open_ai_compliance,
            anthropic_beta=anthropic_beta,
            **kwargs,
        )

        self.allHeaders = self._build_headers(Options.construct())
        self._client = http_client or httpx.Client(
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
        body: Mapping[str, Any] = {},
        files: Any = None,
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
        body: Mapping[str, Any] = {},
        files: Any = None,
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
        body: Mapping[str, Any] = {},
        files: Any = None,
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
        body: Mapping[str, Any] = {},
        files: Any = None,
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
                files=files,
                stream=stream,
                params=params,
                headers=headers,
            )
        else:
            opts = self._construct(
                method="post",
                url=path,
                body=body,
                files=files,
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

    @overload
    def _put(
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
    def _put(
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
    def _put(
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

    def _put(
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
        opts = self._construct(
            method="put",
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

    @overload
    def _get(
        self,
        path: str,
        *,
        body: Mapping[str, Any],
        params: Mapping[str, str],
        headers: Mapping[str, str],
        cast_to: Type[ResponseT],
        stream: Literal[True],
        stream_cls: type[StreamT],
    ) -> StreamT:
        ...

    @overload
    def _get(
        self,
        path: str,
        *,
        body: Mapping[str, Any],
        params: Mapping[str, str],
        headers: Mapping[str, str],
        cast_to: Type[ResponseT],
        stream: Literal[False],
        stream_cls: type[StreamT],
    ) -> ResponseT:
        ...

    @overload
    def _get(
        self,
        path: str,
        *,
        body: Mapping[str, Any],
        params: Mapping[str, str],
        headers: Mapping[str, str],
        cast_to: Type[ResponseT],
        stream: bool,
        stream_cls: type[StreamT],
    ) -> Union[ResponseT, StreamT]:
        ...

    def _get(
        self,
        path: str,
        *,
        body: Mapping[str, Any],
        params: Mapping[str, str],
        headers: Mapping[str, str],
        cast_to: Type[ResponseT],
        stream: bool,
        stream_cls: type[StreamT],
    ) -> Union[ResponseT, StreamT]:
        opts = self._construct(
            method="get",
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

    @overload
    def _delete(
        self,
        path: str,
        *,
        body: Mapping[str, Any],
        params: Mapping[str, str],
        headers: Mapping[str, str],
        cast_to: Type[ResponseT],
        stream: Literal[True],
        stream_cls: type[StreamT],
    ) -> StreamT:
        ...

    @overload
    def _delete(
        self,
        path: str,
        *,
        body: Mapping[str, Any],
        params: Mapping[str, str],
        headers: Mapping[str, str],
        cast_to: Type[ResponseT],
        stream: Literal[False],
        stream_cls: type[StreamT],
    ) -> ResponseT:
        ...

    @overload
    def _delete(
        self,
        path: str,
        *,
        body: Mapping[str, Any],
        params: Mapping[str, str],
        headers: Mapping[str, str],
        cast_to: Type[ResponseT],
        stream: bool,
        stream_cls: type[StreamT],
    ) -> Union[ResponseT, StreamT]:
        ...

    def _delete(
        self,
        path: str,
        *,
        body: Mapping[str, Any],
        params: Mapping[str, str],
        headers: Mapping[str, str],
        cast_to: Type[ResponseT],
        stream: bool,
        stream_cls: type[StreamT],
    ) -> Union[ResponseT, StreamT]:
        opts = self._construct(
            method="delete",
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
        files: Any,
        stream: bool,
        params: Mapping[str, str],
        headers: Mapping[str, str],
    ) -> Options:
        opts = Options.construct()
        opts.method = method
        opts.url = url
        json_body = body
        opts.files = files
        opts.json_body = remove_empty_values(json_body)
        opts.headers = remove_empty_values(headers)
        return opts

    def _construct(
        self,
        *,
        method: str,
        url: str,
        body: Mapping[str, Any],
        files: Any = None,
        stream: bool,
        params: Mapping[str, str],
        headers: Mapping[str, str],
    ) -> Options:
        opts = Options.construct()
        opts.method = method
        opts.url = url
        opts.files = files
        if method != "get" or method != "delete":
            opts.json_body = remove_empty_values(body)
        opts.headers = remove_empty_values(headers)
        return opts

    @property
    def _default_headers(self) -> Mapping[str, str]:
        return {
            f"{PORTKEY_HEADER_PREFIX}api-key": self.api_key,
            f"{PORTKEY_HEADER_PREFIX}package-version": f"portkey-{VERSION}",
            f"{PORTKEY_HEADER_PREFIX}runtime": platform.python_implementation(),
            f"{PORTKEY_HEADER_PREFIX}runtime-version": platform.python_version(),
        }

    def _build_headers(self, options: Options) -> Dict[str, Any]:
        option_headers = options.headers or {}
        headers_dict = self._merge_mappings(
            self._default_headers, option_headers, self.custom_headers
        )
        return headers_dict

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
        if hasattr(self, "_client"):
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
            files=options.files,
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


class AsyncHttpxClientWrapper(httpx.AsyncClient):
    def __del__(self) -> None:
        try:
            asyncio.get_running_loop().create_task(self.aclose())
        except Exception:
            pass


class AsyncAPIClient:
    _client: httpx.AsyncClient
    _default_stream_cls: Union[type[AsyncStream[Any]], None] = None

    def __init__(
        self,
        *,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        virtual_key: Optional[str] = None,
        config: Optional[Union[Mapping, str]] = None,
        provider: Optional[str] = None,
        trace_id: Optional[str] = None,
        metadata: Union[Optional[dict[str, str]], str] = None,
        cache_namespace: Optional[str] = None,
        debug: Optional[bool] = None,
        cache_force_refresh: Optional[bool] = None,
        custom_host: Optional[str] = None,
        forward_headers: Optional[List[str]] = None,
        openai_project: Optional[str] = None,
        openai_organization: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        aws_access_key_id: Optional[str] = None,
        aws_session_token: Optional[str] = None,
        aws_region: Optional[str] = None,
        vertex_project_id: Optional[str] = None,
        vertex_region: Optional[str] = None,
        workers_ai_account_id: Optional[str] = None,
        azure_resource_name: Optional[str] = None,
        azure_deployment_id: Optional[str] = None,
        azure_api_version: Optional[str] = None,
        huggingface_base_url: Optional[str] = None,
        http_client: Optional[httpx.AsyncClient] = None,
        request_timeout: Optional[int] = None,
        strict_open_ai_compliance: Optional[bool] = None,
        anthropic_beta: Optional[str] = None,
        **kwargs,
    ) -> None:
        self.api_key = api_key or default_api_key()
        self.base_url = base_url or default_base_url()
        self.virtual_key = virtual_key
        self.config = config
        self.provider = provider
        self.trace_id = trace_id
        self.metadata = metadata
        self.debug = debug
        self.cache_force_refresh = cache_force_refresh
        self.custom_host = custom_host
        self.forward_headers = forward_headers
        self.openai_project = openai_project
        self.openai_organization = openai_organization
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_access_key_id = aws_access_key_id
        self.aws_session_token = aws_session_token
        self.aws_region = aws_region
        self.vertex_project_id = vertex_project_id
        self.vertex_region = vertex_region
        self.workers_ai_account_id = workers_ai_account_id
        self.azure_resource_name = azure_resource_name
        self.azure_deployment_id = azure_deployment_id
        self.azure_api_version = azure_api_version
        self.huggingface_base_url = huggingface_base_url
        self.cache_namespace = cache_namespace
        self.request_timeout = request_timeout
        self.strict_open_ai_compliance = strict_open_ai_compliance
        self.anthropic_beta = anthropic_beta
        self.kwargs = kwargs

        self.custom_headers = createHeaders(
            api_key=api_key,
            virtual_key=virtual_key,
            config=config,
            provider=provider,
            trace_id=trace_id,
            metadata=metadata,
            debug=debug,
            cache_force_refresh=cache_force_refresh,
            custom_host=custom_host,
            forward_headers=forward_headers,
            openai_project=openai_project,
            openai_organization=openai_organization,
            aws_secret_access_key=aws_secret_access_key,
            aws_access_key_id=aws_access_key_id,
            aws_session_token=aws_session_token,
            aws_region=aws_region,
            vertex_project_id=vertex_project_id,
            vertex_region=vertex_region,
            workers_ai_account_id=workers_ai_account_id,
            azure_resource_name=azure_resource_name,
            azure_deployment_id=azure_deployment_id,
            azure_api_version=azure_api_version,
            huggingface_base_url=huggingface_base_url,
            cache_namespace=cache_namespace,
            request_timeout=request_timeout,
            strict_open_ai_compliance=strict_open_ai_compliance,
            anthropic_beta=anthropic_beta,
            **kwargs,
        )

        self.allHeaders = self._build_headers(Options.construct())
        self._client = http_client or AsyncHttpxClientWrapper(
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
    async def _post(
        self,
        path: str,
        *,
        cast_to: Type[ResponseT],
        body: Mapping[str, Any],
        files: Any = None,
        stream: Literal[False],
        stream_cls: type[AsyncStreamT],
        params: Mapping[str, str],
        headers: Mapping[str, str],
    ) -> ResponseT:
        ...

    @overload
    async def _post(
        self,
        path: str,
        *,
        cast_to: Type[ResponseT],
        body: Mapping[str, Any],
        files: Any = None,
        stream: Literal[True],
        stream_cls: type[AsyncStreamT],
        params: Mapping[str, str],
        headers: Mapping[str, str],
    ) -> AsyncStreamT:
        ...

    @overload
    async def _post(
        self,
        path: str,
        *,
        cast_to: Type[ResponseT],
        body: Mapping[str, Any],
        files: Any = None,
        stream: bool,
        stream_cls: type[AsyncStreamT],
        params: Mapping[str, str],
        headers: Mapping[str, str],
    ) -> Union[ResponseT, AsyncStreamT]:
        ...

    async def _post(
        self,
        path: str,
        *,
        cast_to: Type[ResponseT],
        body: Mapping[str, Any],
        files: Any = None,
        stream: bool,
        stream_cls: type[AsyncStreamT],
        params: Mapping[str, str],
        headers: Mapping[str, str],
    ) -> Union[ResponseT, AsyncStreamT]:
        if path.endswith("/generate"):
            opts = await self._construct_generate_options(
                method="post",
                url=path,
                body=body,
                files=files,
                stream=stream,
                params=params,
                headers=headers,
            )
        else:
            opts = await self._construct(
                method="post",
                url=path,
                body=body,
                files=files,
                stream=stream,
                params=params,
                headers=headers,
            )

        res = await self._request(
            options=opts,
            stream=stream,
            cast_to=cast_to,
            stream_cls=stream_cls,
        )
        return res

    @overload
    async def _put(
        self,
        path: str,
        *,
        cast_to: Type[ResponseT],
        body: Mapping[str, Any],
        stream: Literal[False],
        stream_cls: type[AsyncStreamT],
        params: Mapping[str, str],
        headers: Mapping[str, str],
    ) -> ResponseT:
        ...

    @overload
    async def _put(
        self,
        path: str,
        *,
        cast_to: Type[ResponseT],
        body: Mapping[str, Any],
        stream: Literal[True],
        stream_cls: type[AsyncStreamT],
        params: Mapping[str, str],
        headers: Mapping[str, str],
    ) -> AsyncStreamT:
        ...

    @overload
    async def _put(
        self,
        path: str,
        *,
        cast_to: Type[ResponseT],
        body: Mapping[str, Any],
        stream: bool,
        stream_cls: type[AsyncStreamT],
        params: Mapping[str, str],
        headers: Mapping[str, str],
    ) -> Union[ResponseT, AsyncStreamT]:
        ...

    async def _put(
        self,
        path: str,
        *,
        cast_to: Type[ResponseT],
        body: Mapping[str, Any],
        stream: bool,
        stream_cls: type[AsyncStreamT],
        params: Mapping[str, str],
        headers: Mapping[str, str],
    ) -> Union[ResponseT, AsyncStreamT]:
        opts = await self._construct(
            method="put",
            url=path,
            body=body,
            stream=stream,
            params=params,
            headers=headers,
        )
        res = await self._request(
            options=opts,
            stream=stream,
            cast_to=cast_to,
            stream_cls=stream_cls,
        )
        return res

    @overload
    async def _get(
        self,
        path: str,
        *,
        body: Mapping[str, Any],
        params: Mapping[str, str],
        headers: Mapping[str, str],
        cast_to: Type[ResponseT],
        stream: Literal[True],
        stream_cls: type[AsyncStreamT],
    ) -> AsyncStreamT:
        ...

    @overload
    async def _get(
        self,
        path: str,
        *,
        body: Mapping[str, Any],
        params: Mapping[str, str],
        headers: Mapping[str, str],
        cast_to: Type[ResponseT],
        stream: Literal[False],
        stream_cls: type[AsyncStreamT],
    ) -> ResponseT:
        ...

    @overload
    async def _get(
        self,
        path: str,
        *,
        body: Mapping[str, Any],
        params: Mapping[str, str],
        headers: Mapping[str, str],
        cast_to: Type[ResponseT],
        stream: bool,
        stream_cls: type[AsyncStreamT],
    ) -> Union[ResponseT, AsyncStreamT]:
        ...

    async def _get(
        self,
        path: str,
        *,
        body: Mapping[str, Any],
        params: Mapping[str, str],
        headers: Mapping[str, str],
        cast_to: Type[ResponseT],
        stream: bool,
        stream_cls: type[AsyncStreamT],
    ) -> Union[ResponseT, AsyncStreamT]:
        opts = await self._construct(
            method="get",
            url=path,
            body=body,
            stream=stream,
            params=params,
            headers=headers,
        )
        res = await self._request(
            options=opts,
            stream=stream,
            cast_to=cast_to,
            stream_cls=stream_cls,
        )
        return res

    @overload
    async def _delete(
        self,
        path: str,
        *,
        body: Mapping[str, Any],
        params: Mapping[str, str],
        headers: Mapping[str, str],
        cast_to: Type[ResponseT],
        stream: Literal[True],
        stream_cls: type[AsyncStreamT],
    ) -> AsyncStreamT:
        ...

    @overload
    async def _delete(
        self,
        path: str,
        *,
        body: Mapping[str, Any],
        params: Mapping[str, str],
        headers: Mapping[str, str],
        cast_to: Type[ResponseT],
        stream: Literal[False],
        stream_cls: type[AsyncStreamT],
    ) -> ResponseT:
        ...

    @overload
    async def _delete(
        self,
        path: str,
        *,
        body: Mapping[str, Any],
        params: Mapping[str, str],
        headers: Mapping[str, str],
        cast_to: Type[ResponseT],
        stream: bool,
        stream_cls: type[AsyncStreamT],
    ) -> Union[ResponseT, AsyncStreamT]:
        ...

    async def _delete(
        self,
        path: str,
        *,
        body: Mapping[str, Any],
        params: Mapping[str, str],
        headers: Mapping[str, str],
        cast_to: Type[ResponseT],
        stream: bool,
        stream_cls: type[AsyncStreamT],
    ) -> Union[ResponseT, AsyncStreamT]:
        opts = await self._construct(
            method="delete",
            url=path,
            body=body,
            stream=stream,
            params=params,
            headers=headers,
        )
        res = await self._request(
            options=opts,
            stream=stream,
            cast_to=cast_to,
            stream_cls=stream_cls,
        )
        return res

    async def _construct_generate_options(
        self,
        *,
        method: str,
        url: str,
        body: Any,
        files: Any,
        stream: bool,
        params: Mapping[str, str],
        headers: Mapping[str, str],
    ) -> Options:
        opts = Options.construct()
        opts.method = method
        opts.url = url
        json_body = body
        opts.files = files
        opts.json_body = remove_empty_values(json_body)
        opts.headers = remove_empty_values(headers)
        return opts

    async def _construct(
        self,
        *,
        method: str,
        url: str,
        body: Mapping[str, Any],
        files: Any = None,
        stream: bool,
        params: Mapping[str, str],
        headers: Mapping[str, str],
    ) -> Options:
        opts = Options.construct()
        opts.method = method
        opts.url = url
        opts.files = files
        if method != "get" or method != "delete":
            opts.json_body = remove_empty_values(body)
        opts.headers = remove_empty_values(headers)
        return opts

    @property
    def _default_headers(self) -> Mapping[str, str]:
        return {
            f"{PORTKEY_HEADER_PREFIX}api-key": self.api_key,
            f"{PORTKEY_HEADER_PREFIX}package-version": f"portkey-{VERSION}",
            f"{PORTKEY_HEADER_PREFIX}runtime": platform.python_implementation(),
            f"{PORTKEY_HEADER_PREFIX}runtime-version": platform.python_version(),
        }

    def _build_headers(self, options: Options) -> Dict[str, Any]:
        option_headers = options.headers or {}
        headers_dict = self._merge_mappings(
            self._default_headers, option_headers, self.custom_headers
        )
        return headers_dict

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

    async def close(self) -> None:
        """Close the underlying HTTPX client.

        The client will *not* be usable after this.
        """
        if hasattr(self, "_client"):
            await self._client.aclose()

    async def __aenter__(self: Any) -> Any:
        return self

    async def __aexit__(
        self,
        exc_type: Optional[BaseException],
        exc: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        await self.close()

    async def _build_request(self, options: Options) -> httpx.Request:
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
    async def _request(
        self,
        *,
        options: Options,
        stream: Literal[False],
        cast_to: Type[ResponseT],
        stream_cls: Type[AsyncStreamT],
    ) -> ResponseT:
        ...

    @overload
    async def _request(
        self,
        *,
        options: Options,
        stream: Literal[True],
        cast_to: Type[ResponseT],
        stream_cls: Type[AsyncStreamT],
    ) -> AsyncStreamT:
        ...

    @overload
    async def _request(
        self,
        *,
        options: Options,
        stream: bool,
        cast_to: Type[ResponseT],
        stream_cls: Type[AsyncStreamT],
    ) -> Union[ResponseT, AsyncStreamT]:
        ...

    async def _request(
        self,
        *,
        options: Options,
        stream: bool,
        cast_to: Type[ResponseT],
        stream_cls: Type[AsyncStreamT],
    ) -> Union[ResponseT, AsyncStreamT]:
        request = await self._build_request(options)
        try:
            res = await self._client.send(request, auth=self.custom_auth, stream=stream)
            res.raise_for_status()
        except httpx.HTTPStatusError as err:  # 4xx and 5xx errors
            # If the response is streamed then we need to explicitly read the response
            # to completion before attempting to access the response text.
            await err.response.aread()
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
