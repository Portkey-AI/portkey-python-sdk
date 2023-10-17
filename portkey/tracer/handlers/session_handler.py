import requests
from requests.models import Response
from portkey.tracer.handlers.utils import intitiate_tracing


class SessionHandler(requests.Session):
    def request(
        self,
        method: str | bytes,
        url: str | bytes,
        params=None,
        data=None,
        headers=None,
        cookies=None,
        files=None,
        auth=None,
        timeout=None,
        allow_redirects: bool = True,
        proxies=None,
        hooks=None,
        stream=None,
        verify=None,
        cert=None,
        json=None,
    ) -> Response:
        url, headers = intitiate_tracing(method, url, headers)  # type: ignore
        return super().request(
            method,
            url,
            params,
            data,
            headers,
            cookies,
            files,
            auth,
            timeout,
            allow_redirects,
            proxies,
            hooks,
            stream,
            verify,
            cert,
            json,
        )
