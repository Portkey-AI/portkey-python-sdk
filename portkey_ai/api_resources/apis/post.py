from typing import Any, Dict, Union

from portkey_ai.api_resources.base_client import APIClient

from portkey_ai.api_resources.streaming import Stream
from portkey_ai.api_resources.apis.api_resource import APIResource


class Post(APIResource):
    def __init__(self, client: APIClient) -> None:
        super().__init__(client)

    def create(
        self,
        *,
        url: str,
        **kwargs,
    ) -> Union[Dict[str, Any], Stream[Dict[str, Any]]]:
        return self._post(
            url,
            body=kwargs,
            params=None,
            cast_to=dict,
            stream_cls=Stream[dict],
            stream=False,
            headers={},
        )
