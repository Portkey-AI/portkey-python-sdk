from typing import Mapping
import json
from portkey_ai.api_resources.utils import get_portkey_header

__all__ = ["createHeaders"]


class CreateHeaders:
    def __init__(self, **kwargs) -> None:  # type: ignore
        self.kwargs = kwargs

    def json(self) -> Mapping:
        headers = {}
        for k, v in self.kwargs.items():
            if k == "mode" and "proxy" not in v:
                v = f"proxy {v}"
            k = "-".join(k.split("_"))
            if isinstance(v, Mapping):
                v = json.dumps(v)
            if v:
                if k.lower() != "authorization":
                    headers[get_portkey_header(k)] = str(v)
                else:
                    headers[k] = str(v)
        return headers


def createHeaders(**kwargs):
    return CreateHeaders(**kwargs).json()
