from typing import Mapping
from portkey.api_resources.utils import get_portkey_header


class CreateHeaders:
    def __init__(self, **kwargs) -> None:  # type: ignore
        self.kwargs = kwargs

    def json(self) -> Mapping:
        headers = {}
        for k, v in self.kwargs.items():
            if k == "mode" and "proxy" not in v:
                v = f"proxy {v}"
            k = "-".join(k.split("_"))
            headers[get_portkey_header(k)] = v
        return headers
