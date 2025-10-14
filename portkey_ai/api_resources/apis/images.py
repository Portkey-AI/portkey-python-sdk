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
from ..._vendor.openai._types import FileTypes, Omit, omit
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
        n: Union[int, Omit] = omit,
        model: Union[str, Omit] = omit,
        response_format: Union[str, Omit] = omit,
        size: Union[str, Omit] = omit,
        user: Union[str, Omit] = omit,
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
        background: Union[Optional[str], Omit] = omit,
        input_fidelity: Union[Optional[str], Omit] = omit,
        mask: Union[FileTypes, Omit] = omit,
        model: Union[str, Omit] = omit,
        n: Union[Optional[int], Omit] = omit,
        output_compression: Union[Optional[int], Omit] = omit,
        output_format: Union[Optional[str], Omit] = omit,
        partial_images: Union[Optional[int], Omit] = omit,
        quality: Union[Optional[str], Omit] = omit,
        response_format: Union[Optional[str], Omit] = omit,
        size: Union[Optional[str], Omit] = omit,
        stream: Union[Optional[Literal[False]], Omit] = omit,
        user: Union[str, Omit] = omit,
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
        background: Union[Optional[str], Omit] = omit,
        input_fidelity: Union[Optional[str], Omit] = omit,
        mask: Union[FileTypes, Omit] = omit,
        model: Union[str, Omit] = omit,
        n: Union[Optional[int], Omit] = omit,
        output_compression: Union[Optional[int], Omit] = omit,
        output_format: Union[Optional[str], Omit] = omit,
        partial_images: Union[Optional[int], Omit] = omit,
        quality: Union[Optional[str], Omit] = omit,
        response_format: Union[Optional[str], Omit] = omit,
        size: Union[Optional[str], Omit] = omit,
        user: Union[str, Omit] = omit,
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
        background: Union[Optional[str], Omit] = omit,
        input_fidelity: Union[Optional[str], Omit] = omit,
        mask: Union[FileTypes, Omit] = omit,
        model: Union[str, Omit] = omit,
        n: Union[Optional[int], Omit] = omit,
        output_compression: Union[Optional[int], Omit] = omit,
        output_format: Union[Optional[str], Omit] = omit,
        partial_images: Union[Optional[int], Omit] = omit,
        quality: Union[Optional[str], Omit] = omit,
        response_format: Union[Optional[str], Omit] = omit,
        size: Union[Optional[str], Omit] = omit,
        user: Union[str, Omit] = omit,
        **kwargs
    ) -> Union[OpenAIImagesResponse, Stream[ImageEditStreamEvent], ImagesResponse]:
        ...

    def edit(
        self,
        *,
        image: Union[FileTypes, List[FileTypes]],
        prompt: str,
        background: Union[Optional[str], Omit] = omit,
        input_fidelity: Union[Optional[str], Omit] = omit,
        mask: Union[FileTypes, Omit] = omit,
        model: Union[str, Omit] = omit,
        n: Union[Optional[int], Omit] = omit,
        output_compression: Union[Optional[int], Omit] = omit,
        output_format: Union[Optional[str], Omit] = omit,
        partial_images: Union[Optional[int], Omit] = omit,
        quality: Union[Optional[str], Omit] = omit,
        response_format: Union[Optional[str], Omit] = omit,
        size: Union[Optional[str], Omit] = omit,
        stream: Union[Optional[Literal[False]], Literal[True], Omit] = omit,
        user: Union[str, Omit] = omit,
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
        background: Union[Optional[str], Omit] = omit,
        model: Union[str, Omit] = omit,
        moderation: Union[Optional[str], Omit] = omit,
        n: Union[Optional[int], Omit] = omit,
        output_compression: Union[Optional[int], Omit] = omit,
        output_format: Union[Optional[str], Omit] = omit,
        partial_images: Union[Optional[int], Omit] = omit,
        quality: Union[Optional[str], Omit] = omit,
        response_format: Union[Optional[str], Omit] = omit,
        size: Union[Optional[str], Omit] = omit,
        stream: Union[Optional[Literal[False]], Omit] = omit,
        style: Union[Optional[str], Omit] = omit,
        user: Union[str, Omit] = omit,
        **kwargs
    ) -> Union[OpenAIImagesResponse, ImagesResponse]:
        ...

    @overload
    def generate(
        self,
        *,
        prompt: str,
        stream: Literal[True],
        background: Union[Optional[str], Omit] = omit,
        model: Union[str, Omit] = omit,
        moderation: Union[Optional[str], Omit] = omit,
        n: Union[Optional[int], Omit] = omit,
        output_compression: Union[Optional[int], Omit] = omit,
        output_format: Union[Optional[str], Omit] = omit,
        partial_images: Union[Optional[int], Omit] = omit,
        quality: Union[Optional[str], Omit] = omit,
        response_format: Union[Optional[str], Omit] = omit,
        size: Union[Optional[str], Omit] = omit,
        style: Union[Optional[str], Omit] = omit,
        user: Union[str, Omit] = omit,
        **kwargs
    ) -> Stream[ImageGenStreamEvent]:
        ...

    @overload
    def generate(
        self,
        *,
        prompt: str,
        stream: bool,
        background: Union[Optional[str], Omit] = omit,
        model: Union[str, Omit] = omit,
        moderation: Union[Optional[str], Omit] = omit,
        n: Union[Optional[int], Omit] = omit,
        output_compression: Union[Optional[int], Omit] = omit,
        output_format: Union[Optional[str], Omit] = omit,
        partial_images: Union[Optional[int], Omit] = omit,
        quality: Union[Optional[str], Omit] = omit,
        response_format: Union[Optional[str], Omit] = omit,
        size: Union[Optional[str], Omit] = omit,
        style: Union[Optional[str], Omit] = omit,
        user: Union[str, Omit] = omit,
        **kwargs
    ) -> Union[OpenAIImagesResponse, Stream[ImageGenStreamEvent], ImagesResponse]:
        ...

    def generate(
        self,
        *,
        prompt: str,
        background: Union[Optional[str], Omit] = omit,
        model: Union[str, Omit] = omit,
        moderation: Union[Optional[str], Omit] = omit,
        n: Union[Optional[int], Omit] = omit,
        output_compression: Union[Optional[int], Omit] = omit,
        output_format: Union[Optional[str], Omit] = omit,
        partial_images: Union[Optional[int], Omit] = omit,
        quality: Union[Optional[str], Omit] = omit,
        response_format: Union[Optional[str], Omit] = omit,
        size: Union[Optional[str], Omit] = omit,
        stream: Union[Optional[Union[Literal[False], Literal[True]]], Omit] = omit,
        style: Union[Optional[str], Omit] = omit,
        user: Union[str, Omit] = omit,
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
        n: Union[int, Omit] = omit,
        response_format: Union[str, Omit] = omit,
        size: Union[str, Omit] = omit,
        user: Union[str, Omit] = omit,
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
        background: Union[Optional[str], Omit] = omit,
        input_fidelity: Union[Optional[str], Omit] = omit,
        mask: Union[FileTypes, Omit] = omit,
        model: Union[str, Omit] = omit,
        n: Union[Optional[int], Omit] = omit,
        output_compression: Union[Optional[int], Omit] = omit,
        output_format: Union[Optional[str], Omit] = omit,
        partial_images: Union[Optional[int], Omit] = omit,
        quality: Union[Optional[str], Omit] = omit,
        response_format: Union[Optional[str], Omit] = omit,
        size: Union[Optional[str], Omit] = omit,
        stream: Union[Optional[Literal[False]], Omit] = omit,
        user: Union[str, Omit] = omit,
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
        background: Union[Optional[str], Omit] = omit,
        input_fidelity: Union[Optional[str], Omit] = omit,
        mask: Union[FileTypes, Omit] = omit,
        model: Union[str, Omit] = omit,
        n: Union[Optional[int], Omit] = omit,
        output_compression: Union[Optional[int], Omit] = omit,
        output_format: Union[Optional[str], Omit] = omit,
        partial_images: Union[Optional[int], Omit] = omit,
        quality: Union[Optional[str], Omit] = omit,
        response_format: Union[Optional[str], Omit] = omit,
        size: Union[Optional[str], Omit] = omit,
        user: Union[str, Omit] = omit,
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
        background: Union[Optional[str], Omit] = omit,
        input_fidelity: Union[Optional[str], Omit] = omit,
        mask: Union[FileTypes, Omit] = omit,
        model: Union[str, Omit] = omit,
        n: Union[Optional[int], Omit] = omit,
        output_compression: Union[Optional[int], Omit] = omit,
        output_format: Union[Optional[str], Omit] = omit,
        partial_images: Union[Optional[int], Omit] = omit,
        quality: Union[Optional[str], Omit] = omit,
        response_format: Union[Optional[str], Omit] = omit,
        size: Union[Optional[str], Omit] = omit,
        user: Union[str, Omit] = omit,
        **kwargs
    ) -> Union[OpenAIImagesResponse, AsyncStream[ImageEditStreamEvent], ImagesResponse]:
        ...

    async def edit(
        self,
        *,
        image: Union[FileTypes, List[FileTypes]],
        prompt: str,
        background: Union[Optional[str], Omit] = omit,
        input_fidelity: Union[Optional[str], Omit] = omit,
        mask: Union[FileTypes, Omit] = omit,
        model: Union[str, Omit] = omit,
        n: Union[Optional[int], Omit] = omit,
        output_compression: Union[Optional[int], Omit] = omit,
        output_format: Union[Optional[str], Omit] = omit,
        partial_images: Union[Optional[int], Omit] = omit,
        quality: Union[Optional[str], Omit] = omit,
        response_format: Union[Optional[str], Omit] = omit,
        size: Union[Optional[str], Omit] = omit,
        stream: Union[Optional[Literal[False]], Literal[True], Omit] = omit,
        user: Union[str, Omit] = omit,
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
        background: Union[Optional[str], Omit] = omit,
        model: Union[str, Omit] = omit,
        moderation: Union[Optional[str], Omit] = omit,
        n: Union[Optional[int], Omit] = omit,
        output_compression: Union[Optional[int], Omit] = omit,
        output_format: Union[Optional[str], Omit] = omit,
        partial_images: Union[Optional[int], Omit] = omit,
        quality: Union[Optional[str], Omit] = omit,
        response_format: Union[Optional[str], Omit] = omit,
        size: Union[Optional[str], Omit] = omit,
        stream: Union[Optional[Literal[False]], Omit] = omit,
        style: Union[Optional[str], Omit] = omit,
        user: Union[str, Omit] = omit,
        **kwargs
    ) -> Union[OpenAIImagesResponse, ImagesResponse]:
        ...

    @overload
    async def generate(
        self,
        *,
        prompt: str,
        stream: Literal[True],
        background: Union[Optional[str], Omit] = omit,
        model: Union[str, Omit] = omit,
        moderation: Union[Optional[str], Omit] = omit,
        n: Union[Optional[int], Omit] = omit,
        output_compression: Union[Optional[int], Omit] = omit,
        output_format: Union[Optional[str], Omit] = omit,
        partial_images: Union[Optional[int], Omit] = omit,
        quality: Union[Optional[str], Omit] = omit,
        response_format: Union[Optional[str], Omit] = omit,
        size: Union[Optional[str], Omit] = omit,
        style: Union[Optional[str], Omit] = omit,
        user: Union[str, Omit] = omit,
        **kwargs
    ) -> AsyncStream[ImageGenStreamEvent]:
        ...

    @overload
    async def generate(
        self,
        *,
        prompt: str,
        stream: bool,
        background: Union[Optional[str], Omit] = omit,
        model: Union[str, Omit] = omit,
        moderation: Union[Optional[str], Omit] = omit,
        n: Union[Optional[int], Omit] = omit,
        output_compression: Union[Optional[int], Omit] = omit,
        output_format: Union[Optional[str], Omit] = omit,
        partial_images: Union[Optional[int], Omit] = omit,
        quality: Union[Optional[str], Omit] = omit,
        response_format: Union[Optional[str], Omit] = omit,
        size: Union[Optional[str], Omit] = omit,
        style: Union[Optional[str], Omit] = omit,
        user: Union[str, Omit] = omit,
        **kwargs
    ) -> Union[OpenAIImagesResponse, AsyncStream[ImageGenStreamEvent], ImagesResponse]:
        ...

    async def generate(
        self,
        *,
        prompt: str,
        background: Union[Optional[str], Omit] = omit,
        model: Union[str, Omit] = omit,
        moderation: Union[Optional[str], Omit] = omit,
        n: Union[Optional[int], Omit] = omit,
        output_compression: Union[Optional[int], Omit] = omit,
        output_format: Union[Optional[str], Omit] = omit,
        partial_images: Union[Optional[int], Omit] = omit,
        quality: Union[Optional[str], Omit] = omit,
        response_format: Union[Optional[str], Omit] = omit,
        size: Union[Optional[str], Omit] = omit,
        stream: Union[Optional[Union[Literal[False], Literal[True]]], Omit] = omit,
        style: Union[Optional[str], Omit] = omit,
        user: Union[str, Omit] = omit,
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
