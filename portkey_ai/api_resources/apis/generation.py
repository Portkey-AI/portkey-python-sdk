from __future__ import annotations
import warnings
from typing import Literal, Optional, Union, Mapping, Any, overload
from portkey_ai.api_resources.base_client import APIClient, AsyncAPIClient
from portkey_ai.api_resources.utils import (
    retrieve_config,
    GenericResponse,
)

from portkey_ai.api_resources.streaming import AsyncStream, Stream
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource


class Generations(APIResource):
    def __init__(self, client: APIClient) -> None:
        super().__init__(client)

    def create(
        self,
        *,
        prompt_id: str,
        config: Optional[Union[Mapping, str]] = None,
        variables: Optional[Mapping[str, Any]] = None,
    ) -> Union[GenericResponse, Stream[GenericResponse]]:
        warning_message = "This API has been deprecated. Please use the Prompt API for the saved prompt."  # noqa: E501
        warnings.warn(
            warning_message,
            DeprecationWarning,
            stacklevel=2,
        )
        if config is None:
            config = retrieve_config()
        body = {"variables": variables}
        response = self._post(
            f"/v1/prompts/{prompt_id}/generate",
            body=body,
            mode=None,
            params=None,
            cast_to=GenericResponse,
            stream_cls=Stream[GenericResponse],
            stream=False,
        )
        response["warning"] = warning_message
        return response


class AsyncGenerations(AsyncAPIResource):
    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)

    async def create(
        self,
        *,
        prompt_id: str,
        config: Optional[Union[Mapping, str]] = None,
        variables: Optional[Mapping[str, Any]] = None,
    ) -> Union[GenericResponse, AsyncStream[GenericResponse]]:
        warning_message = "This API has been deprecated. Please use the Prompt API for the saved prompt."  # noqa: E501
        warnings.warn(
            warning_message,
            DeprecationWarning,
            stacklevel=2,
        )
        if config is None:
            config = retrieve_config()
        body = {"variables": variables}
        response = await self._post(
            f"/v1/prompts/{prompt_id}/generate",
            body=body,
            mode=None,
            params=None,
            cast_to=GenericResponse,
            stream_cls=AsyncStream[GenericResponse],
            stream=False,
        )
        response["warning"] = warning_message
        return response


class Prompts(APIResource):
    completions: Completions

    def __init__(self, client: APIClient) -> None:
        super().__init__(client)
        self.completions = Completions(client)

    def render(
        self,
        *,
        prompt_id: str,
        variables: Optional[Mapping[str, Any]] = None,
        config: Optional[Union[Mapping, str]] = None,
        stream: bool = False,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        **kwargs,
    ) -> Union[GenericResponse, Stream[GenericResponse]]:
        """Prompt render Method"""
        if config is None:
            config = retrieve_config()
        body = {
            "variables": variables,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_k": top_k,
            "top_p": top_p,
            "stream": stream,
            **kwargs,
        }
        return self._post(
            f"/prompts/{prompt_id}/render",
            body=body,
            params=None,
            cast_to=GenericResponse,
            stream_cls=Stream[GenericResponse],
            stream=stream,
            headers={},
        )


class AsyncPrompts(AsyncAPIResource):
    completions: AsyncCompletions

    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)
        self.completions = AsyncCompletions(client)

    async def render(
        self,
        *,
        prompt_id: str,
        variables: Optional[Mapping[str, Any]] = None,
        config: Optional[Union[Mapping, str]] = None,
        stream: bool = False,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        **kwargs,
    ) -> Union[GenericResponse, AsyncStream[GenericResponse]]:
        """Prompt render Method"""
        if config is None:
            config = retrieve_config()
        body = {
            "variables": variables,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_k": top_k,
            "top_p": top_p,
            "stream": stream,
            **kwargs,
        }
        return await self._post(
            f"/prompts/{prompt_id}/render",
            body=body,
            params=None,
            cast_to=GenericResponse,
            stream_cls=AsyncStream[GenericResponse],
            stream=stream,
            headers={},
        )


class Completions(APIResource):
    def __init__(self, client: APIClient) -> None:
        super().__init__(client)

    @overload
    def create(
        self,
        *,
        prompt_id: str,
        variables: Optional[Mapping[str, Any]] = None,
        config: Optional[Union[Mapping, str]] = None,
        stream: Literal[True],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        **kwargs,
    ) -> Stream[GenericResponse]:
        ...

    @overload
    def create(
        self,
        *,
        prompt_id: str,
        variables: Optional[Mapping[str, Any]] = None,
        config: Optional[Union[Mapping, str]] = None,
        stream: Literal[False] = False,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        **kwargs,
    ) -> GenericResponse:
        ...

    @overload
    def create(
        self,
        *,
        prompt_id: str,
        variables: Optional[Mapping[str, Any]] = None,
        config: Optional[Union[Mapping, str]] = None,
        stream: bool = False,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        **kwargs,
    ) -> Union[GenericResponse, Stream[GenericResponse]]:
        ...

    def create(
        self,
        *,
        prompt_id: str,
        variables: Optional[Mapping[str, Any]] = None,
        config: Optional[Union[Mapping, str]] = None,
        stream: bool = False,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        **kwargs,
    ) -> Union[GenericResponse, Stream[GenericResponse]]:
        """Prompt completions Method"""
        if config is None:
            config = retrieve_config()
        body = {
            "variables": variables,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_k": top_k,
            "top_p": top_p,
            "stream": stream,
            **kwargs,
        }
        return self._post(
            f"/prompts/{prompt_id}/completions",
            body=body,
            params=None,
            cast_to=GenericResponse,
            stream_cls=Stream[GenericResponse],
            stream=stream,
            headers={},
        )


class AsyncCompletions(AsyncAPIResource):
    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)

    @overload
    async def create(
        self,
        *,
        prompt_id: str,
        variables: Optional[Mapping[str, Any]] = None,
        config: Optional[Union[Mapping, str]] = None,
        stream: Literal[True],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        **kwargs,
    ) -> AsyncStream[GenericResponse]:
        ...

    @overload
    async def create(
        self,
        *,
        prompt_id: str,
        variables: Optional[Mapping[str, Any]] = None,
        config: Optional[Union[Mapping, str]] = None,
        stream: Literal[False] = False,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        **kwargs,
    ) -> GenericResponse:
        ...

    @overload
    async def create(
        self,
        *,
        prompt_id: str,
        variables: Optional[Mapping[str, Any]] = None,
        config: Optional[Union[Mapping, str]] = None,
        stream: bool = False,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        **kwargs,
    ) -> Union[GenericResponse, AsyncStream[GenericResponse]]:
        ...

    async def create(
        self,
        *,
        prompt_id: str,
        variables: Optional[Mapping[str, Any]] = None,
        config: Optional[Union[Mapping, str]] = None,
        stream: bool = False,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        **kwargs,
    ) -> Union[GenericResponse, AsyncStream[GenericResponse]]:
        """Prompt completions Method"""
        if config is None:
            config = retrieve_config()
        body = {
            "variables": variables,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_k": top_k,
            "top_p": top_p,
            "stream": stream,
            **kwargs,
        }
        return await self._post(
            f"/prompts/{prompt_id}/completions",
            body=body,
            params=None,
            cast_to=GenericResponse,
            stream_cls=AsyncStream[GenericResponse],
            stream=stream,
            headers={},
        )
