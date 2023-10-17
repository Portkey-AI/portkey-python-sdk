import typing
from typing import Any
import httpx
from httpx import Request, Response
from httpx._client import (
    UseClientDefault,
    USE_CLIENT_DEFAULT,
)
from httpx._types import (
    AuthTypes,
    CookieTypes,
    HeaderTypes,
    QueryParamTypes,
    RequestContent,
    RequestData,
    RequestExtensions,
    RequestFiles,
    TimeoutTypes,
    URLTypes,
)
from portkey.tracer.handlers.utils import intitiate_tracing


class ClientHandler(httpx.Client):
    def build_request(
        self,
        method: str,
        url: URLTypes,
        *,
        content: typing.Optional[RequestContent] = None,
        data: typing.Optional[RequestData] = None,
        files: typing.Optional[RequestFiles] = None,
        json: typing.Optional[typing.Any] = None,
        params: typing.Optional[QueryParamTypes] = None,
        headers: typing.Optional[HeaderTypes] = None,
        cookies: typing.Optional[CookieTypes] = None,
        timeout: typing.Union[TimeoutTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
        extensions: typing.Optional[RequestExtensions] = None,
    ) -> Request:
        url, headers = intitiate_tracing(method, f"{self.base_url}{url}", headers)  # type: ignore
        return super().build_request(
            method,
            url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            extensions=extensions,
        )
