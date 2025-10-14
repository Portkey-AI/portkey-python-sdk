import json
from typing import Any, Literal, Optional, Union

import httpx
from portkey_ai._vendor.openai.types.video_model import VideoModel
from portkey_ai._vendor.openai.types.video_seconds import VideoSeconds
from portkey_ai._vendor.openai.types.video_size import VideoSize
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.client import AsyncPortkey, Portkey
from portkey_ai.api_resources.types.shared_types import Body, Headers, Query
from portkey_ai.api_resources.types.videos_type import (
    Video,
    VideoDeleteResponse,
    VideoList,
)
from ..._vendor.openai._types import FileTypes, NotGiven, Omit, not_given, omit


class Videos(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    def create(
        self,
        *,
        prompt: str,
        input_reference: Union[FileTypes, Omit] = omit,
        model: Union[VideoModel, Omit] = omit,
        seconds: Union[VideoSeconds, Omit] = omit,
        size: Union[VideoSize, Omit] = omit,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Union[Optional[float], httpx.Timeout, NotGiven] = not_given,
    ) -> Video:
        response = self.openai_client.with_raw_response.videos.create(
            prompt=prompt,
            input_reference=input_reference,
            model=model,
            seconds=seconds,
            size=size,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        data = Video(**json.loads(response.text))
        data._headers = response.headers

        return data

    def create_and_poll(
        self,
        *,
        prompt: str,
        input_reference: Union[FileTypes, Omit] = omit,
        model: Union[VideoModel, Omit] = omit,
        seconds: Union[VideoSeconds, Omit] = omit,
        size: Union[VideoSize, Omit] = omit,
        poll_interval_ms: Union[int, Omit] = omit,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Union[Optional[float], httpx.Timeout, NotGiven] = not_given,
    ) -> Video:
        response = self.openai_client.videos.create_and_poll(
            prompt=prompt,
            input_reference=input_reference,
            model=model,
            seconds=seconds,
            size=size,
            poll_interval_ms=poll_interval_ms,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return response  # type: ignore[return-value]

    def poll(
        self,
        video_id: str,
        *,
        poll_interval_ms: Union[int, Omit] = omit,
    ) -> Video:
        response = self.openai_client.videos.poll(
            video_id=video_id,
            poll_interval_ms=poll_interval_ms,
        )
        return response  # type: ignore[return-value]

    def retrieve(
        self,
        video_id: str,
        *,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Union[Optional[float], httpx.Timeout, NotGiven] = not_given,
    ) -> Video:
        response = self.openai_client.with_raw_response.videos.retrieve(
            video_id=video_id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        data = Video(**json.loads(response.text))
        data._headers = response.headers

        return data

    def list(
        self,
        *,
        after: Union[str, Omit] = omit,
        limit: Union[int, Omit] = omit,
        order: Union[Literal["asc", "desc"], Omit] = omit,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Union[Optional[float], httpx.Timeout, NotGiven] = not_given,
    ) -> VideoList:
        response = self.openai_client.with_raw_response.videos.list(
            after=after,
            limit=limit,
            order=order,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        data = VideoList(**json.loads(response.text))
        data._headers = response.headers
        return data

    def delete(
        self,
        video_id: str,
        *,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Union[Optional[float], httpx.Timeout, NotGiven] = not_given,
    ) -> VideoDeleteResponse:
        response = self.openai_client.with_raw_response.videos.delete(
            video_id=video_id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        data = VideoDeleteResponse(**json.loads(response.text))
        data._headers = response.headers
        return data

    def download_content(
        self,
        video_id: str,
        *,
        variant: Union[Literal["video", "thumbnail", "spritesheet"], Omit] = omit,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Union[Optional[float], httpx.Timeout, NotGiven] = not_given,
    ) -> Any:
        response = self.openai_client.videos.download_content(
            video_id=video_id,
            variant=variant,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return response

    def remix(
        self,
        video_id: str,
        *,
        prompt: str,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Union[Optional[float], httpx.Timeout, NotGiven] = not_given,
    ) -> Video:
        response = self.openai_client.with_raw_response.videos.remix(
            video_id=video_id,
            prompt=prompt,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        data = Video(**json.loads(response.text))
        data._headers = response.headers
        return data


class AsyncVideos(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    async def create(
        self,
        *,
        prompt: str,
        input_reference: Union[FileTypes, Omit] = omit,
        model: Union[VideoModel, Omit] = omit,
        seconds: Union[VideoSeconds, Omit] = omit,
        size: Union[VideoSize, Omit] = omit,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Union[Optional[float], httpx.Timeout, NotGiven] = not_given,
    ) -> Video:
        response = await self.openai_client.with_raw_response.videos.create(
            prompt=prompt,
            input_reference=input_reference,
            model=model,
            seconds=seconds,
            size=size,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        data = Video(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def create_and_poll(
        self,
        *,
        prompt: str,
        input_reference: Union[FileTypes, Omit] = omit,
        model: Union[VideoModel, Omit] = omit,
        seconds: Union[VideoSeconds, Omit] = omit,
        size: Union[VideoSize, Omit] = omit,
        poll_interval_ms: Union[int, Omit] = omit,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Union[Optional[float], httpx.Timeout, NotGiven] = not_given,
    ) -> Video:
        response = await self.openai_client.videos.create_and_poll(
            prompt=prompt,
            input_reference=input_reference,
            model=model,
            seconds=seconds,
            size=size,
            poll_interval_ms=poll_interval_ms,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return response  # type: ignore[return-value]

    async def poll(
        self,
        video_id: str,
        *,
        poll_interval_ms: Union[int, Omit] = omit,
    ) -> Video:
        response = await self.openai_client.videos.poll(
            video_id=video_id,
            poll_interval_ms=poll_interval_ms,
        )
        return response  # type: ignore[return-value]

    async def retrieve(
        self,
        video_id: str,
        *,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Union[Optional[float], httpx.Timeout, NotGiven] = not_given,
    ) -> Video:
        response = await self.openai_client.with_raw_response.videos.retrieve(
            video_id=video_id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        data = Video(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def list(
        self,
        *,
        after: Union[str, Omit] = omit,
        limit: Union[int, Omit] = omit,
        order: Union[Literal["asc", "desc"], Omit] = omit,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Union[Optional[float], httpx.Timeout, NotGiven] = not_given,
    ) -> VideoList:
        response = await self.openai_client.with_raw_response.videos.list(
            after=after,
            limit=limit,
            order=order,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        data = VideoList(**json.loads(response.text))
        data._headers = response.headers
        return data

    async def delete(
        self,
        video_id: str,
        *,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Union[Optional[float], httpx.Timeout, NotGiven] = not_given,
    ) -> VideoDeleteResponse:
        response = await self.openai_client.with_raw_response.videos.delete(
            video_id=video_id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        data = VideoDeleteResponse(**json.loads(response.text))
        data._headers = response.headers
        return data

    async def download_content(
        self,
        video_id: str,
        *,
        variant: Union[Literal["video", "thumbnail", "spritesheet"], Omit] = omit,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Union[Optional[float], httpx.Timeout, NotGiven] = not_given,
    ) -> Any:
        response = await self.openai_client.videos.download_content(
            video_id=video_id,
            variant=variant,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return response

    async def remix(
        self,
        video_id: str,
        *,
        prompt: str,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Union[Optional[float], httpx.Timeout, NotGiven] = not_given,
    ) -> Video:
        response = await self.openai_client.with_raw_response.videos.remix(
            video_id=video_id,
            prompt=prompt,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        data = Video(**json.loads(response.text))
        data._headers = response.headers
        return data
