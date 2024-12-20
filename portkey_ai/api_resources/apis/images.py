import json
from typing import Union, Any
import typing
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.client import AsyncPortkey, Portkey
from portkey_ai.api_resources.types.image_type import ImagesResponse
from ..._vendor.openai._types import NotGiven, NOT_GIVEN


class Images(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    @typing.no_type_check
    def create_variation(
        self,
        *,
        image,
        n: Union[int, NotGiven] = NOT_GIVEN,
        model: Union[str, NotGiven] = NOT_GIVEN,
        response_format: Union[str, NotGiven] = NOT_GIVEN,
        size: Union[str, NotGiven] = NOT_GIVEN,
        user: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs
    ) -> ImagesResponse:
        response = self.openai_client.with_raw_response.images.create_variation(
            image=image,
            n=n,
            model=model,
            response_format=response_format,
            size=size,
            user=user,
            extra_body=kwargs,
        )
        data = ImagesResponse(**json.loads(response.text))
        data._headers = response.headers

        return data

    @typing.no_type_check
    def edit(
        self,
        *,
        prompt: str,
        image,
        mask: Union[Any, NotGiven] = NOT_GIVEN,
        model: Union[str, NotGiven] = NOT_GIVEN,
        n: Union[int, NotGiven] = NOT_GIVEN,
        response_format: Union[str, NotGiven] = NOT_GIVEN,
        size: Union[str, NotGiven] = NOT_GIVEN,
        user: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs
    ) -> ImagesResponse:
        response = self.openai_client.with_raw_response.images.edit(
            prompt=prompt,
            image=image,
            mask=mask,
            model=model,
            n=n,
            response_format=response_format,
            size=size,
            user=user,
            extra_body=kwargs,
        )
        data = ImagesResponse(**json.loads(response.text))
        data._headers = response.headers

        return data

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
            style=style,
            user=user,
            extra_body=kwargs,
        )
        data = ImagesResponse(**json.loads(response.text))
        data._headers = response.headers

        return data


class AsyncImages(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    @typing.no_type_check
    async def create_variation(
        self,
        *,
        image,
        n: Union[int, NotGiven] = NOT_GIVEN,
        response_format: Union[str, NotGiven] = NOT_GIVEN,
        size: Union[str, NotGiven] = NOT_GIVEN,
        user: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs
    ) -> ImagesResponse:
        response = await self.openai_client.with_raw_response.images.create_variation(
            image=image,
            n=n,
            response_format=response_format,
            size=size,
            user=user,
            extra_body=kwargs,
        )
        data = ImagesResponse(**json.loads(response.text))
        data._headers = response.headers

        return data

    @typing.no_type_check
    async def edit(
        self,
        *,
        prompt: str,
        image,
        mask: Union[Any, NotGiven] = NOT_GIVEN,
        model: Union[str, NotGiven] = NOT_GIVEN,
        n: Union[int, NotGiven] = NOT_GIVEN,
        response_format: Union[str, NotGiven] = NOT_GIVEN,
        size: Union[str, NotGiven] = NOT_GIVEN,
        user: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs
    ) -> ImagesResponse:
        response = await self.openai_client.with_raw_response.images.edit(
            prompt=prompt,
            image=image,
            mask=mask,
            model=model,
            n=n,
            response_format=response_format,
            size=size,
            user=user,
            extra_body=kwargs,
        )
        data = ImagesResponse(**json.loads(response.text))
        data._headers = response.headers

        return data

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
            style=style,
            user=user,
            extra_body=kwargs,
        )
        data = ImagesResponse(**json.loads(response.text))
        data._headers = response.headers

        return data
