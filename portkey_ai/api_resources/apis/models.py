from typing import Any
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.client import AsyncPortkey, Portkey


class Models(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    def list(self, **kwargs) -> Any:
        response = self.openai_client.models.list(**kwargs)
        return response

    def retrieve(self, model, **kwargs) -> Any:
        response = self.openai_client.models.retrieve(model=model, **kwargs)
        return response

    def delete(self, model, **kwargs) -> Any:
        response = self.openai_client.models.delete(model=model, **kwargs)
        return response
    
class AsyncModels(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    async def list(self, **kwargs) -> Any:
        response = await self.openai_client.models.list(**kwargs)
        return response

    async def retrieve(self, model, **kwargs) -> Any:
        response = await self.openai_client.models.retrieve(model=model, **kwargs)
        return response

    async def delete(self, model, **kwargs) -> Any:
        response = await self.openai_client.models.delete(model=model, **kwargs)
        return response