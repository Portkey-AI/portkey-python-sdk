from typing import Optional
from portkey.api_resources.apis.api_resource import APIResource
from portkey.api_resources.base_client import APIClient
from portkey.api_resources.utils import PortkeyApiPaths


class Embeddings(APIResource):
    def __init__(self, client: APIClient) -> None:
        super().__init__(client)

    def create(self, *, input: str, model: Optional[str] = None) -> dict:
        body = {"input": input, "model": model}
        return self._post(
            PortkeyApiPaths.EMBEDDING_API,
            body=body,
            params=None,
            cast_to=dict,
            stream_cls=None,
            stream=False,
            headers={},
        )
