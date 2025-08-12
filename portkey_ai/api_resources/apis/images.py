import json
from typing import Literal, Optional, Union, Any
import typing
from portkey_ai._vendor.openai._streaming import AsyncStream, Stream
from portkey_ai._vendor.openai.types.image_gen_stream_event import ImageGenStreamEvent
from portkey_ai._vendor.openai.types.images_response import (
    ImagesResponse as OpenAIImagesResponse,
)
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.client import AsyncPortkey, Portkey
from portkey_ai.api_resources.types.image_type import ImagesResponse
from ..._vendor.openai._types import NotGiven, NOT_GIVEN
from typing_extensions import overload


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

    @overload
    def generate(
        self,
        *,
        prompt: str,
        background: Union[Optional[str], NotGiven] = NOT_GIVEN,
        model: Union[str, NotGiven] = NOT_GIVEN,
        moderation: Union[Optional[str], NotGiven] = NOT_GIVEN,
        n: Union[Optional[int], NotGiven] = NOT_GIVEN,
        output_compression: Union[Optional[int], NotGiven] = NOT_GIVEN,
        output_format: Union[Optional[str], NotGiven] = NOT_GIVEN,
        partial_images: Union[Optional[int], NotGiven] = NOT_GIVEN,
        quality: Union[Optional[str], NotGiven] = NOT_GIVEN,
        response_format: Union[Optional[str], NotGiven] = NOT_GIVEN,
        size: Union[Optional[str], NotGiven] = NOT_GIVEN,
        stream: Union[Optional[Literal[False]], NotGiven] = NOT_GIVEN,
        style: Union[Optional[str], NotGiven] = NOT_GIVEN,
        user: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs
    ) -> OpenAIImagesResponse:
        ...

    @overload
    def generate(
        self,
        *,
        prompt: str,
        stream: Literal[True],
        background: Union[Optional[str], NotGiven] = NOT_GIVEN,
        model: Union[str, NotGiven] = NOT_GIVEN,
        moderation: Union[Optional[str], NotGiven] = NOT_GIVEN,
        n: Union[Optional[int], NotGiven] = NOT_GIVEN,
        output_compression: Union[Optional[int], NotGiven] = NOT_GIVEN,
        output_format: Union[Optional[str], NotGiven] = NOT_GIVEN,
        partial_images: Union[Optional[int], NotGiven] = NOT_GIVEN,
        quality: Union[Optional[str], NotGiven] = NOT_GIVEN,
        response_format: Union[Optional[str], NotGiven] = NOT_GIVEN,
        size: Union[Optional[str], NotGiven] = NOT_GIVEN,
        style: Union[Optional[str], NotGiven] = NOT_GIVEN,
        user: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs
    ) -> Stream[ImageGenStreamEvent]:
        ...

    @overload
    def generate(
        self,
        *,
        prompt: str,
        stream: bool,
        background: Union[Optional[str], NotGiven] = NOT_GIVEN,
        model: Union[str, NotGiven] = NOT_GIVEN,
        moderation: Union[Optional[str], NotGiven] = NOT_GIVEN,
        n: Union[Optional[int], NotGiven] = NOT_GIVEN,
        output_compression: Union[Optional[int], NotGiven] = NOT_GIVEN,
        output_format: Union[Optional[str], NotGiven] = NOT_GIVEN,
        partial_images: Union[Optional[int], NotGiven] = NOT_GIVEN,
        quality: Union[Optional[str], NotGiven] = NOT_GIVEN,
        response_format: Union[Optional[str], NotGiven] = NOT_GIVEN,
        size: Union[Optional[str], NotGiven] = NOT_GIVEN,
        style: Union[Optional[str], NotGiven] = NOT_GIVEN,
        user: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs
    ) -> Union[OpenAIImagesResponse, Stream[ImageGenStreamEvent]]:
        ...

    def generate(
        self,
        *,
        prompt: str,
        background: Union[Optional[str], NotGiven] = NOT_GIVEN,
        model: Union[str, NotGiven] = NOT_GIVEN,
        moderation: Union[Optional[str], NotGiven] = NOT_GIVEN,
        n: Union[Optional[int], NotGiven] = NOT_GIVEN,
        output_compression: Union[Optional[int], NotGiven] = NOT_GIVEN,
        output_format: Union[Optional[str], NotGiven] = NOT_GIVEN,
        partial_images: Union[Optional[int], NotGiven] = NOT_GIVEN,
        quality: Union[Optional[str], NotGiven] = NOT_GIVEN,
        response_format: Union[Optional[str], NotGiven] = NOT_GIVEN,
        size: Union[Optional[str], NotGiven] = NOT_GIVEN,
        stream: Union[
            Optional[Union[Literal[False], Literal[True]]], NotGiven
        ] = NOT_GIVEN,
        style: Union[Optional[str], NotGiven] = NOT_GIVEN,
        user: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs
    ) -> Union[OpenAIImagesResponse, Stream[ImageGenStreamEvent]]:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)

        return self.openai_client.images.generate(  # type: ignore[misc]
            prompt=prompt,
            background=background,  # type: ignore[arg-type]
            model=model,
            moderation=moderation,  # type: ignore[arg-type]
            n=n,
            output_compression=output_compression,
            output_format=output_format,  # type: ignore[arg-type]
            partial_images=partial_images,
            quality=quality,  # type: ignore[arg-type]
            response_format=response_format,  # type: ignore[arg-type]
            size=size,  # type: ignore[arg-type]
            stream=stream,  # type: ignore[arg-type]
            style=style,  # type: ignore[arg-type]
            user=user,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )


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

    @overload
    async def generate(
        self,
        *,
        prompt: str,
        background: Union[Optional[str], NotGiven] = NOT_GIVEN,
        model: Union[str, NotGiven] = NOT_GIVEN,
        moderation: Union[Optional[str], NotGiven] = NOT_GIVEN,
        n: Union[Optional[int], NotGiven] = NOT_GIVEN,
        output_compression: Union[Optional[int], NotGiven] = NOT_GIVEN,
        output_format: Union[Optional[str], NotGiven] = NOT_GIVEN,
        partial_images: Union[Optional[int], NotGiven] = NOT_GIVEN,
        quality: Union[Optional[str], NotGiven] = NOT_GIVEN,
        response_format: Union[Optional[str], NotGiven] = NOT_GIVEN,
        size: Union[Optional[str], NotGiven] = NOT_GIVEN,
        stream: Union[Optional[Literal[False]], NotGiven] = NOT_GIVEN,
        style: Union[Optional[str], NotGiven] = NOT_GIVEN,
        user: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs
    ) -> OpenAIImagesResponse:
        ...

    @overload
    async def generate(
        self,
        *,
        prompt: str,
        stream: Literal[True],
        background: Union[Optional[str], NotGiven] = NOT_GIVEN,
        model: Union[str, NotGiven] = NOT_GIVEN,
        moderation: Union[Optional[str], NotGiven] = NOT_GIVEN,
        n: Union[Optional[int], NotGiven] = NOT_GIVEN,
        output_compression: Union[Optional[int], NotGiven] = NOT_GIVEN,
        output_format: Union[Optional[str], NotGiven] = NOT_GIVEN,
        partial_images: Union[Optional[int], NotGiven] = NOT_GIVEN,
        quality: Union[Optional[str], NotGiven] = NOT_GIVEN,
        response_format: Union[Optional[str], NotGiven] = NOT_GIVEN,
        size: Union[Optional[str], NotGiven] = NOT_GIVEN,
        style: Union[Optional[str], NotGiven] = NOT_GIVEN,
        user: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs
    ) -> AsyncStream[ImageGenStreamEvent]:
        ...

    @overload
    async def generate(
        self,
        *,
        prompt: str,
        stream: bool,
        background: Union[Optional[str], NotGiven] = NOT_GIVEN,
        model: Union[str, NotGiven] = NOT_GIVEN,
        moderation: Union[Optional[str], NotGiven] = NOT_GIVEN,
        n: Union[Optional[int], NotGiven] = NOT_GIVEN,
        output_compression: Union[Optional[int], NotGiven] = NOT_GIVEN,
        output_format: Union[Optional[str], NotGiven] = NOT_GIVEN,
        partial_images: Union[Optional[int], NotGiven] = NOT_GIVEN,
        quality: Union[Optional[str], NotGiven] = NOT_GIVEN,
        response_format: Union[Optional[str], NotGiven] = NOT_GIVEN,
        size: Union[Optional[str], NotGiven] = NOT_GIVEN,
        style: Union[Optional[str], NotGiven] = NOT_GIVEN,
        user: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs
    ) -> Union[OpenAIImagesResponse, AsyncStream[ImageGenStreamEvent]]:
        ...

    async def generate(
        self,
        *,
        prompt: str,
        background: Union[Optional[str], NotGiven] = NOT_GIVEN,
        model: Union[str, NotGiven] = NOT_GIVEN,
        moderation: Union[Optional[str], NotGiven] = NOT_GIVEN,
        n: Union[Optional[int], NotGiven] = NOT_GIVEN,
        output_compression: Union[Optional[int], NotGiven] = NOT_GIVEN,
        output_format: Union[Optional[str], NotGiven] = NOT_GIVEN,
        partial_images: Union[Optional[int], NotGiven] = NOT_GIVEN,
        quality: Union[Optional[str], NotGiven] = NOT_GIVEN,
        response_format: Union[Optional[str], NotGiven] = NOT_GIVEN,
        size: Union[Optional[str], NotGiven] = NOT_GIVEN,
        stream: Union[
            Optional[Union[Literal[False], Literal[True]]], NotGiven
        ] = NOT_GIVEN,
        style: Union[Optional[str], NotGiven] = NOT_GIVEN,
        user: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs
    ) -> Union[OpenAIImagesResponse, AsyncStream[ImageGenStreamEvent]]:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)

        return await self.openai_client.images.generate(  # type: ignore[misc]
            prompt=prompt,
            background=background,  # type: ignore[arg-type]
            model=model,
            moderation=moderation,  # type: ignore[arg-type]
            n=n,
            output_compression=output_compression,
            output_format=output_format,  # type: ignore[arg-type]
            partial_images=partial_images,
            quality=quality,  # type: ignore[arg-type]
            response_format=response_format,  # type: ignore[arg-type]
            size=size,  # type: ignore[arg-type]
            stream=stream,  # type: ignore[arg-type]
            style=style,  # type: ignore[arg-type]
            user=user,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
