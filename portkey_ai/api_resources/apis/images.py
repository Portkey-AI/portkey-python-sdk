from typing import Any
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.client import AsyncPortkey, Portkey


class Images(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    def generate(self, prompt: str, **kwargs) -> Any:
        response = self.openai_client.images.generate(prompt=prompt, **kwargs)
        return response

    def edit(self, prompt: str, image, **kwargs) -> Any:
        response = self.openai_client.images.edit(prompt=prompt, image=image, **kwargs)
        return response

    def create_variation(self, image, **kwargs) -> Any:
        response = self.openai_client.images.create_variation(image=image, **kwargs)
        return response


class AsyncImages(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    async def generate(self, prompt: str, **kwargs) -> Any:
        response = await self.openai_client.images.generate(prompt=prompt, **kwargs)
        return response

    async def edit(self, prompt: str, image, **kwargs) -> Any:
        response = await self.openai_client.images.edit(
            prompt=prompt, image=image, **kwargs
        )
        return response

    async def create_variation(self, image, **kwargs) -> Any:
        response = await self.openai_client.images.create_variation(
            image=image, **kwargs
        )
        return response
