import json
from typing import Union
import typing
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.client import AsyncPortkey, Portkey
from portkey_ai.api_resources.types.image_type import ImagesResponse
from openai._types import NotGiven, NOT_GIVEN


class Images(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    @typing.no_type_check
    def generate(
        self,
        *,
        prompt: str,
        model: Union[str, NotGiven] = NOT_GIVEN,
        n: Union[int, NotGiven] = NOT_GIVEN,
        quality: Union[str, NotGiven] = NOT_GIVEN,
        response_format: Union[str, NotGiven] = NOT_GIVEN,
        size: Union[str, NotGiven] = NOT_GIVEN,
        user: Union[str, NotGiven] = NOT_GIVEN,
        style: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs
    ) -> ImagesResponse:
        response = self.openai_client.with_raw_response.images.generate(
            prompt=prompt,
            model=model,
            n=n,
            quality=quality,
            response_format=response_format,
            size=size,
            user=user,
            style=style,
            **kwargs
        )
        data = ImagesResponse(**json.loads(response.text))
        data._headers = response.headers

        return data

    def edit(self, prompt: str, image, **kwargs) -> ImagesResponse:
        response = self.openai_client.with_raw_response.images.edit(
            prompt=prompt, image=image, **kwargs
        )
        data = ImagesResponse(**json.loads(response.text))
        data._headers = response.headers

        return data

    def create_variation(self, image, **kwargs) -> ImagesResponse:
        response = self.openai_client.with_raw_response.images.create_variation(
            image=image, **kwargs
        )
        data = ImagesResponse(**json.loads(response.text))
        data._headers = response.headers

        return data


class AsyncImages(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    @typing.no_type_check
    async def generate(
        self,
        *,
        prompt: str,
        model: Union[str, NotGiven] = NOT_GIVEN,
        n: Union[int, NotGiven] = NOT_GIVEN,
        quality: Union[str, NotGiven] = NOT_GIVEN,
        response_format: Union[str, NotGiven] = NOT_GIVEN,
        size: Union[str, NotGiven] = NOT_GIVEN,
        user: Union[str, NotGiven] = NOT_GIVEN,
        style: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs
    ) -> ImagesResponse:
        response = await self.openai_client.with_raw_response.images.generate(
            prompt=prompt,
            model=model,
            n=n,
            quality=quality,
            response_format=response_format,
            size=size,
            user=user,
            style=style,
            **kwargs
        )
        data = ImagesResponse(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def edit(self, prompt: str, image, **kwargs) -> ImagesResponse:
        response = await self.openai_client.with_raw_response.images.edit(
            prompt=prompt, image=image, **kwargs
        )
        data = ImagesResponse(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def create_variation(self, image, **kwargs) -> ImagesResponse:
        response = await self.openai_client.with_raw_response.images.create_variation(
            image=image, **kwargs
        )
        data = ImagesResponse(**json.loads(response.text))
        data._headers = response.headers

        return data
