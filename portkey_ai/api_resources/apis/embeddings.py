import json
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.base_client import APIClient, AsyncAPIClient
from portkey_ai.api_resources.client import AsyncPortkey, Portkey
from portkey_ai.api_resources.utils import PortkeyApiPaths, GenericResponse


class Embeddings(APIResource):

    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    def create(
        self,
        **kwargs
    ) -> GenericResponse:
        
        response = self.openai_client.with_raw_response.embeddings.create(**kwargs)
        response = response.text
        return json.loads(response)


class AsyncEmbeddings(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    async def create(
        self,
        **kwargs
    ) -> GenericResponse:
        
        response = await self.openai_client.with_raw_response.embeddings.create(**kwargs)
        response = response.text
        return json.loads(response)
