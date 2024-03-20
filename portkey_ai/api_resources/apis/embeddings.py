import json
from typing import Optional
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.client import AsyncPortkey, Portkey
from portkey_ai.api_resources.types.embeddings_type import CreateEmbeddingResponse


class Embeddings(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    def create(
        self, *, input: str, model: Optional[str] = "portkey-default", **kwargs
    ) -> CreateEmbeddingResponse:
        response = self.openai_client.with_raw_response.embeddings.create(
            input=input, model=model, **kwargs  # type: ignore
        )

        data = CreateEmbeddingResponse(**json.loads(response.text))
        data._headers = response.headers

        return data


class AsyncEmbeddings(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    async def create(
        self, *, input: str, model: Optional[str] = "portkey-default", **kwargs
    ) -> CreateEmbeddingResponse:
        response = await self.openai_client.with_raw_response.embeddings.create(
            input=input, model=model, **kwargs  # type: ignore
        )
        data = CreateEmbeddingResponse(**json.loads(response.text))
        data._headers = response.headers

        return data
