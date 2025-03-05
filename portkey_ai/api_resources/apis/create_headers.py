from typing import Mapping
import json
from portkey_ai.api_resources.utils import get_portkey_header

__all__ = ["createHeaders"]


class CreateHeaders:
    def __init__(self, **kwargs) -> None:  # type: ignore
        self.kwargs = kwargs

    def json(self) -> Mapping:
        headers = {}
        forward_headers = self.kwargs.get("forward_headers", [])
        # Logic to accept both _ and - in forward_headers for devex
        if forward_headers:
            forward_headers = [
                "-".join(header.split("_")) for header in forward_headers
            ]
        for k, v in self.kwargs.items():
            # logic for boolean type headers
            if isinstance(v, bool):
                v = str(v).lower()
            if k == "mode" and "proxy" not in v:
                v = f"proxy {v}"
            k = "-".join(k.split("_"))
            if isinstance(v, Mapping):
                v = json.dumps(v)
            if v:
                if k.lower() != "authorization":
                    if forward_headers and k in forward_headers:
                        headers[k] = str(v)
                    else:
                        headers[get_portkey_header(k)] = str(v)
                else:
                    # Logic to add Bearer only if it is not present.
                    # Else it would be added everytime a request is made
                    if v.startswith("Bearer "):
                        headers[k] = v
                    else:
                        headers[k] = str("Bearer " + v)

                # logic for List of str to comma separated string
                if k == "forward-headers":
                    headers[get_portkey_header(k)] = ",".join(v)
        print("headers", headers)
        return headers


def createHeaders(**kwargs):
    return CreateHeaders(**kwargs).json()
