from typing import Optional
from portkey_ai.api_resources.apis.api_resource import APIResource
from portkey_ai.api_resources.base_client import APIClient
from portkey_ai.api_resources.utils import PortkeyApiPaths, GenericResponse


class Embeddings(APIResource):
    def __init__(self, client: APIClient) -> None:
        super().__init__(client)

    def create(
        self,
        *,
        input: str,
        model: Optional[str] = None,
        dimensions: Optional[int] = None,
        encoding_format: Optional[str] = None,
        user: Optional[str] = None,
        **kwargs
    ) -> GenericResponse:
        body = {
            input=input,
            model=model,
            dimensions=dimensions,
            encoding_format=encoding_format,
            user=user,
            **kwargs,
        }

        return self._post(
            PortkeyApiPaths.EMBEDDING_API,
            body=body,
            params=None,
            cast_to=GenericResponse,
            stream_cls=None,
            stream=False,
            headers={},
        )