from typing import Any
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.client import AsyncPortkey, Portkey


class Images(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    def generate(self, **kwargs) -> Any:
        response = self.openai_client.images.generate(**kwargs)
        return response

    def edit(self, **kwargs) -> Any:
        response = self.openai_client.images.edit(**kwargs)
        return response

    def create_variation(self, **kwargs) -> Any:
        response = self.openai_client.images.create_variation(**kwargs)
        return response


class AsyncImages(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    async def generate(self, **kwargs) -> Any:
        response = await self.openai_client.images.generate(**kwargs)
        return response

    async def edit(self, **kwargs) -> Any:
        response = await self.openai_client.images.edit(**kwargs)
        return response

    async def create_variation(self, **kwargs) -> Any:
        response = await self.openai_client.images.create_variation(**kwargs)
        return response
