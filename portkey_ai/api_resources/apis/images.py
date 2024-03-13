import json
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.client import AsyncPortkey, Portkey
from portkey_ai.api_resources.utils import ImageResponse


class Images(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    def generate(self, prompt: str, **kwargs) -> ImageResponse:
        response = self.openai_client.with_raw_response.images.generate(
            prompt=prompt, **kwargs
        )
        data = ImageResponse(**json.loads(response.text))
        data._headers = response.headers

        return data

    def edit(self, prompt: str, image, **kwargs) -> ImageResponse:
        response = self.openai_client.with_raw_response.images.edit(
            prompt=prompt, image=image, **kwargs
        )
        data = ImageResponse(**json.loads(response.text))
        data._headers = response.headers

        return data

    def create_variation(self, image, **kwargs) -> ImageResponse:
        response = self.openai_client.with_raw_response.images.create_variation(
            image=image, **kwargs
        )
        data = ImageResponse(**json.loads(response.text))
        data._headers = response.headers

        return data


class AsyncImages(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    async def generate(self, prompt: str, **kwargs) -> ImageResponse:
        response = await self.openai_client.with_raw_response.images.generate(
            prompt=prompt, **kwargs
        )
        data = ImageResponse(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def edit(self, prompt: str, image, **kwargs) -> ImageResponse:
        response = await self.openai_client.with_raw_response.images.edit(
            prompt=prompt, image=image, **kwargs
        )
        data = ImageResponse(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def create_variation(self, image, **kwargs) -> ImageResponse:
        response = await self.openai_client.with_raw_response.images.create_variation(
            image=image, **kwargs
        )
        data = ImageResponse(**json.loads(response.text))
        data._headers = response.headers

        return data
