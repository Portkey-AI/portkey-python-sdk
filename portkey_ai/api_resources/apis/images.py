import json
from typing import List, Literal, Optional, Union
import typing
from portkey_ai._vendor.openai._streaming import AsyncStream, Stream
from portkey_ai._vendor.openai.types.image_edit_stream_event import ImageEditStreamEvent
from portkey_ai._vendor.openai.types.image_gen_stream_event import ImageGenStreamEvent
from portkey_ai._vendor.openai.types.images_response import (
    ImagesResponse as OpenAIImagesResponse,
)
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.client import AsyncPortkey, Portkey
from portkey_ai.api_resources.types.image_type import ImagesResponse
from ..._vendor.openai._types import FileTypes, NotGiven, NOT_GIVEN
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

    @overload
    def edit(
        self,
        *,
        image: Union[FileTypes, List[FileTypes]],
        prompt: str,
        background: Union[Optional[str], NotGiven] = NOT_GIVEN,
        input_fidelity: Union[Optional[str], NotGiven] = NOT_GIVEN,
        mask: Union[FileTypes, NotGiven] = NOT_GIVEN,
        model: Union[str, NotGiven] = NOT_GIVEN,
        n: Union[Optional[int], NotGiven] = NOT_GIVEN,
        output_compression: Union[Optional[int], NotGiven] = NOT_GIVEN,
        output_format: Union[Optional[str], NotGiven] = NOT_GIVEN,
        partial_images: Union[Optional[int], NotGiven] = NOT_GIVEN,
        quality: Union[Optional[str], NotGiven] = NOT_GIVEN,
        response_format: Union[Optional[str], NotGiven] = NOT_GIVEN,
        size: Union[Optional[str], NotGiven] = NOT_GIVEN,
        stream: Union[Optional[Literal[False]], NotGiven] = NOT_GIVEN,
        user: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs
    ) -> Union[OpenAIImagesResponse, ImagesResponse]:
        ...

    @overload
    def edit(
        self,
        *,
        image: Union[FileTypes, List[FileTypes]],
        prompt: str,
        stream: Literal[True],
        background: Union[Optional[str], NotGiven] = NOT_GIVEN,
        input_fidelity: Union[Optional[str], NotGiven] = NOT_GIVEN,
        mask: Union[FileTypes, NotGiven] = NOT_GIVEN,
        model: Union[str, NotGiven] = NOT_GIVEN,
        n: Union[Optional[int], NotGiven] = NOT_GIVEN,
        output_compression: Union[Optional[int], NotGiven] = NOT_GIVEN,
        output_format: Union[Optional[str], NotGiven] = NOT_GIVEN,
        partial_images: Union[Optional[int], NotGiven] = NOT_GIVEN,
        quality: Union[Optional[str], NotGiven] = NOT_GIVEN,
        response_format: Union[Optional[str], NotGiven] = NOT_GIVEN,
        size: Union[Optional[str], NotGiven] = NOT_GIVEN,
        user: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs
    ) -> Stream[ImageEditStreamEvent]:
        ...

    @overload
    def edit(
        self,
        *,
        image: Union[FileTypes, List[FileTypes]],
        prompt: str,
        stream: bool,
        background: Union[Optional[str], NotGiven] = NOT_GIVEN,
        input_fidelity: Union[Optional[str], NotGiven] = NOT_GIVEN,
        mask: Union[FileTypes, NotGiven] = NOT_GIVEN,
        model: Union[str, NotGiven] = NOT_GIVEN,
        n: Union[Optional[int], NotGiven] = NOT_GIVEN,
        output_compression: Union[Optional[int], NotGiven] = NOT_GIVEN,
        output_format: Union[Optional[str], NotGiven] = NOT_GIVEN,
        partial_images: Union[Optional[int], NotGiven] = NOT_GIVEN,
        quality: Union[Optional[str], NotGiven] = NOT_GIVEN,
        response_format: Union[Optional[str], NotGiven] = NOT_GIVEN,
        size: Union[Optional[str], NotGiven] = NOT_GIVEN,
        user: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs
    ) -> Union[OpenAIImagesResponse, Stream[ImageEditStreamEvent], ImagesResponse]:
        ...

    def edit(
        self,
        *,
        image: Union[FileTypes, List[FileTypes]],
        prompt: str,
        background: Union[Optional[str], NotGiven] = NOT_GIVEN,
        input_fidelity: Union[Optional[str], NotGiven] = NOT_GIVEN,
        mask: Union[FileTypes, NotGiven] = NOT_GIVEN,
        model: Union[str, NotGiven] = NOT_GIVEN,
        n: Union[Optional[int], NotGiven] = NOT_GIVEN,
        output_compression: Union[Optional[int], NotGiven] = NOT_GIVEN,
        output_format: Union[Optional[str], NotGiven] = NOT_GIVEN,
        partial_images: Union[Optional[int], NotGiven] = NOT_GIVEN,
        quality: Union[Optional[str], NotGiven] = NOT_GIVEN,
        response_format: Union[Optional[str], NotGiven] = NOT_GIVEN,
        size: Union[Optional[str], NotGiven] = NOT_GIVEN,
        stream: Union[Optional[Literal[False]], Literal[True], NotGiven] = NOT_GIVEN,
        user: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs
    ) -> Union[OpenAIImagesResponse, Stream[ImageEditStreamEvent], ImagesResponse]:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)

        if stream:
            return self.openai_client.images.edit(  # type: ignore[misc]
                image=image,
                prompt=prompt,
                background=background,  # type: ignore[arg-type]
                input_fidelity=input_fidelity,  # type: ignore[arg-type]
                mask=mask,
                model=model,
                n=n,
                output_compression=output_compression,
                output_format=output_format,  # type: ignore[arg-type]
                partial_images=partial_images,
                quality=quality,  # type: ignore[arg-type]
                response_format=response_format,  # type: ignore[arg-type]
                size=size,  # type: ignore[arg-type]
                stream=stream,  # type: ignore[arg-type]
                user=user,
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            )
        else:
            response = self.openai_client.with_raw_response.images.edit(  # type: ignore[misc]
                image=image,
                prompt=prompt,
                background=background,  # type: ignore[arg-type]
                input_fidelity=input_fidelity,  # type: ignore[arg-type]
                mask=mask,
                model=model,
                n=n,
                output_compression=output_compression,
                output_format=output_format,  # type: ignore[arg-type]
                partial_images=partial_images,
                quality=quality,  # type: ignore[arg-type]
                response_format=response_format,  # type: ignore[arg-type]
                size=size,  # type: ignore[arg-type]
                user=user,
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
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
    ) -> Union[OpenAIImagesResponse, ImagesResponse]:
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
    ) -> Union[OpenAIImagesResponse, Stream[ImageGenStreamEvent], ImagesResponse]:
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
    ) -> Union[OpenAIImagesResponse, Stream[ImageGenStreamEvent], ImagesResponse]:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)

        if stream:
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
        else:
            response = self.openai_client.with_raw_response.images.generate(  # type: ignore[misc]
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
                style=style,  # type: ignore[arg-type]
                user=user,
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
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

    @overload
    async def edit(
        self,
        *,
        image: Union[FileTypes, List[FileTypes]],
        prompt: str,
        background: Union[Optional[str], NotGiven] = NOT_GIVEN,
        input_fidelity: Union[Optional[str], NotGiven] = NOT_GIVEN,
        mask: Union[FileTypes, NotGiven] = NOT_GIVEN,
        model: Union[str, NotGiven] = NOT_GIVEN,
        n: Union[Optional[int], NotGiven] = NOT_GIVEN,
        output_compression: Union[Optional[int], NotGiven] = NOT_GIVEN,
        output_format: Union[Optional[str], NotGiven] = NOT_GIVEN,
        partial_images: Union[Optional[int], NotGiven] = NOT_GIVEN,
        quality: Union[Optional[str], NotGiven] = NOT_GIVEN,
        response_format: Union[Optional[str], NotGiven] = NOT_GIVEN,
        size: Union[Optional[str], NotGiven] = NOT_GIVEN,
        stream: Union[Optional[Literal[False]], NotGiven] = NOT_GIVEN,
        user: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs
    ) -> Union[OpenAIImagesResponse, ImagesResponse]:
        ...

    @overload
    async def edit(
        self,
        *,
        image: Union[FileTypes, List[FileTypes]],
        prompt: str,
        stream: Literal[True],
        background: Union[Optional[str], NotGiven] = NOT_GIVEN,
        input_fidelity: Union[Optional[str], NotGiven] = NOT_GIVEN,
        mask: Union[FileTypes, NotGiven] = NOT_GIVEN,
        model: Union[str, NotGiven] = NOT_GIVEN,
        n: Union[Optional[int], NotGiven] = NOT_GIVEN,
        output_compression: Union[Optional[int], NotGiven] = NOT_GIVEN,
        output_format: Union[Optional[str], NotGiven] = NOT_GIVEN,
        partial_images: Union[Optional[int], NotGiven] = NOT_GIVEN,
        quality: Union[Optional[str], NotGiven] = NOT_GIVEN,
        response_format: Union[Optional[str], NotGiven] = NOT_GIVEN,
        size: Union[Optional[str], NotGiven] = NOT_GIVEN,
        user: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs
    ) -> AsyncStream[ImageEditStreamEvent]:
        ...

    @overload
    async def edit(
        self,
        *,
        image: Union[FileTypes, List[FileTypes]],
        prompt: str,
        stream: bool,
        background: Union[Optional[str], NotGiven] = NOT_GIVEN,
        input_fidelity: Union[Optional[str], NotGiven] = NOT_GIVEN,
        mask: Union[FileTypes, NotGiven] = NOT_GIVEN,
        model: Union[str, NotGiven] = NOT_GIVEN,
        n: Union[Optional[int], NotGiven] = NOT_GIVEN,
        output_compression: Union[Optional[int], NotGiven] = NOT_GIVEN,
        output_format: Union[Optional[str], NotGiven] = NOT_GIVEN,
        partial_images: Union[Optional[int], NotGiven] = NOT_GIVEN,
        quality: Union[Optional[str], NotGiven] = NOT_GIVEN,
        response_format: Union[Optional[str], NotGiven] = NOT_GIVEN,
        size: Union[Optional[str], NotGiven] = NOT_GIVEN,
        user: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs
    ) -> Union[OpenAIImagesResponse, AsyncStream[ImageEditStreamEvent], ImagesResponse]:
        ...

    async def edit(
        self,
        *,
        image: Union[FileTypes, List[FileTypes]],
        prompt: str,
        background: Union[Optional[str], NotGiven] = NOT_GIVEN,
        input_fidelity: Union[Optional[str], NotGiven] = NOT_GIVEN,
        mask: Union[FileTypes, NotGiven] = NOT_GIVEN,
        model: Union[str, NotGiven] = NOT_GIVEN,
        n: Union[Optional[int], NotGiven] = NOT_GIVEN,
        output_compression: Union[Optional[int], NotGiven] = NOT_GIVEN,
        output_format: Union[Optional[str], NotGiven] = NOT_GIVEN,
        partial_images: Union[Optional[int], NotGiven] = NOT_GIVEN,
        quality: Union[Optional[str], NotGiven] = NOT_GIVEN,
        response_format: Union[Optional[str], NotGiven] = NOT_GIVEN,
        size: Union[Optional[str], NotGiven] = NOT_GIVEN,
        stream: Union[Optional[Literal[False]], Literal[True], NotGiven] = NOT_GIVEN,
        user: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs
    ) -> Union[OpenAIImagesResponse, AsyncStream[ImageEditStreamEvent], ImagesResponse]:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)

        if stream:
            return await self.openai_client.images.edit(  # type: ignore[misc]
                image=image,
                prompt=prompt,
                background=background,  # type: ignore[arg-type]
                input_fidelity=input_fidelity,  # type: ignore[arg-type]
                mask=mask,
                model=model,
                n=n,
                output_compression=output_compression,
                output_format=output_format,  # type: ignore[arg-type]
                partial_images=partial_images,
                quality=quality,  # type: ignore[arg-type]
                response_format=response_format,  # type: ignore[arg-type]
                size=size,  # type: ignore[arg-type]
                stream=stream,  # type: ignore[arg-type]
                user=user,
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            )
        else:
            response = await self.openai_client.with_raw_response.images.edit(  # type: ignore[misc]
                image=image,
                prompt=prompt,
                background=background,  # type: ignore[arg-type]
                input_fidelity=input_fidelity,  # type: ignore[arg-type]
                mask=mask,
                model=model,
                n=n,
                output_compression=output_compression,
                output_format=output_format,  # type: ignore[arg-type]
                partial_images=partial_images,
                quality=quality,  # type: ignore[arg-type]
                response_format=response_format,  # type: ignore[arg-type]
                size=size,  # type: ignore[arg-type]
                user=user,
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
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
    ) -> Union[OpenAIImagesResponse, ImagesResponse]:
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
    ) -> Union[OpenAIImagesResponse, AsyncStream[ImageGenStreamEvent], ImagesResponse]:
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
    ) -> Union[OpenAIImagesResponse, AsyncStream[ImageGenStreamEvent], ImagesResponse]:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)

        if stream:
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
        else:
            response = await self.openai_client.with_raw_response.images.generate(  # type: ignore[misc]
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
                style=style,  # type: ignore[arg-type]
                user=user,
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            )
            data = ImagesResponse(**json.loads(response.text))
            data._headers = response.headers

            return data
