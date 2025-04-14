from __future__ import annotations
from urllib.parse import urlencode
import warnings
from typing import Dict, List, Literal, Optional, Union, Mapping, Any, overload
from portkey_ai.api_resources.base_client import APIClient, AsyncAPIClient
from portkey_ai.api_resources.types.generation_type import (
    PromptCompletion,
    PromptCompletionChunk,
    PromptRender,
)
from portkey_ai.api_resources.utils import (
    PortkeyApiPaths,
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
        variables: Mapping[str, Any],
        stream: bool = False,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        **kwargs,
    ) -> PromptRender:
        """Prompt render Method"""
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
            cast_to=PromptRender,
            stream_cls=Stream[PromptRender],
            stream=False,
            headers={},
        )

    def create(
        self,
        *,
        name: str,
        collection_id: str,
        string: str,
        parameters: Dict[str, Any],
        virtual_key: Optional[str] = None,
        model: Optional[str] = None,
        functions: Optional[List[Any]] = None,
        tools: Optional[List[Any]] = None,
        tool_choice: Optional[Dict[str, Any]] = None,
        version_description: Optional[str] = None,
        template_metadata: Optional[Dict[str, Any]] = None,
    ) -> Any:
        body = {
            "name": name,
            "collection_id": collection_id,
            "string": string,
            "parameters": parameters,
            "virtual_key": virtual_key,
            "model": model,
            "functions": functions,
            "tools": tools,
            "tool_choice": tool_choice,
            "version_description": version_description,
            "template_metadata": template_metadata,
        }
        return self._post(
            f"{PortkeyApiPaths.PROMPTS_API}",
            body=body,
            params=None,
            cast_to=GenericResponse,
            stream_cls=None,
            stream=False,
            headers={},
        )

    def list(
        self,
        *,
        collection_id: Optional[str] = None,
        workspace_id: Optional[str] = None,
        current_page: Optional[int] = None,
        page_size: Optional[int] = None,
        search: Optional[str] = None,
    ) -> Any:
        query = {
            "collection_id": collection_id,
            "workspace_id": workspace_id,
            "current_page": current_page,
            "page_size": page_size,
            "search": search,
        }
        filtered_query = {k: v for k, v in query.items() if v is not None}
        query_string = urlencode(filtered_query)
        return self._get(
            f"{PortkeyApiPaths.PROMPTS_API}?{query_string}",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def retrieve(
        self,
        prompt_slug: str,
    ) -> Any:
        return self._get(
            f"{PortkeyApiPaths.PROMPTS_API}/{prompt_slug}",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def update(
        self,
        prompt_slug: str,
        *,
        name: Optional[str] = None,
        collection_id: Optional[str] = None,
        string: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None,
        virtual_key: Optional[str] = None,
        model: Optional[str] = None,
        functions: Optional[List[Any]] = None,
        tools: Optional[List[Any]] = None,
        tool_choice: Optional[Dict[str, Any]] = None,
        version_description: Optional[str] = None,
        template_metadata: Optional[Dict[str, Any]] = None,
    ) -> Any:
        body = {
            "name": name,
            "collection_id": collection_id,
            "string": string,
            "parameters": parameters,
            "virtual_key": virtual_key,
            "model": model,
            "functions": functions,
            "tools": tools,
            "tool_choice": tool_choice,
            "version_description": version_description,
            "template_metadata": template_metadata,
        }
        return self._put(
            f"{PortkeyApiPaths.PROMPTS_API}/{prompt_slug}",
            params=None,
            body=body,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def delete(
        self,
        prompt_slug: str,
    ) -> Any:
        return self._delete(
            f"{PortkeyApiPaths.PROMPTS_API}/{prompt_slug}",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def publish(
        self,
        prompt_slug: str,
        *,
        version: int,
    ) -> Any:
        body = {
            "version": version,
        }
        return self._put(
            f"{PortkeyApiPaths.PROMPTS_API}/{prompt_slug}/makeDefault",
            params=None,
            body=body,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
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
        variables: Mapping[str, Any],
        stream: bool = False,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        **kwargs,
    ) -> PromptRender:
        """Prompt render Method"""
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
            cast_to=PromptRender,
            stream=False,
            stream_cls=AsyncStream[PromptRender],
            headers={},
        )

    async def create(
        self,
        *,
        name: str,
        collection_id: str,
        string: str,
        parameters: Dict[str, Any],
        virtual_key: Optional[str] = None,
        model: Optional[str] = None,
        functions: Optional[List[Any]] = None,
        tools: Optional[List[Any]] = None,
        tool_choice: Optional[Dict[str, Any]] = None,
        version_description: Optional[str] = None,
        template_metadata: Optional[Dict[str, Any]] = None,
    ) -> Any:
        body = {
            "name": name,
            "collection_id": collection_id,
            "string": string,
            "parameters": parameters,
            "virtual_key": virtual_key,
            "model": model,
            "functions": functions,
            "tools": tools,
            "tool_choice": tool_choice,
            "version_description": version_description,
            "template_metadata": template_metadata,
        }
        return await self._post(
            f"{PortkeyApiPaths.PROMPTS_API}",
            body=body,
            params=None,
            cast_to=GenericResponse,
            stream_cls=None,
            stream=False,
            headers={},
        )

    async def list(
        self,
        *,
        collection_id: Optional[str] = None,
        workspace_id: Optional[str] = None,
        current_page: Optional[int] = None,
        page_size: Optional[int] = None,
        search: Optional[str] = None,
    ) -> Any:
        query = {
            "collection_id": collection_id,
            "workspace_id": workspace_id,
            "current_page": current_page,
            "page_size": page_size,
            "search": search,
        }
        filtered_query = {k: v for k, v in query.items() if v is not None}
        query_string = urlencode(filtered_query)
        return await self._get(
            f"{PortkeyApiPaths.PROMPTS_API}?{query_string}",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def retrieve(
        self,
        prompt_slug: str,
    ) -> Any:
        return await self._get(
            f"{PortkeyApiPaths.PROMPTS_API}/{prompt_slug}",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def update(
        self,
        prompt_slug: str,
        *,
        name: Optional[str] = None,
        collection_id: Optional[str] = None,
        string: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None,
        virtual_key: Optional[str] = None,
        model: Optional[str] = None,
        functions: Optional[List[Any]] = None,
        tools: Optional[List[Any]] = None,
        tool_choice: Optional[Dict[str, Any]] = None,
        version_description: Optional[str] = None,
        template_metadata: Optional[Dict[str, Any]] = None,
    ) -> Any:
        body = {
            "name": name,
            "collection_id": collection_id,
            "string": string,
            "parameters": parameters,
            "virtual_key": virtual_key,
            "model": model,
            "functions": functions,
            "tools": tools,
            "tool_choice": tool_choice,
            "version_description": version_description,
            "template_metadata": template_metadata,
        }
        return await self._put(
            f"{PortkeyApiPaths.PROMPTS_API}/{prompt_slug}",
            params=None,
            body=body,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def delete(
        self,
        prompt_slug: str,
    ) -> Any:
        return await self._delete(
            f"{PortkeyApiPaths.PROMPTS_API}/{prompt_slug}",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def publish(
        self,
        prompt_slug: str,
        *,
        version: int,
    ) -> Any:
        body = {
            "version": version,
        }
        return await self._put(
            f"{PortkeyApiPaths.PROMPTS_API}/{prompt_slug}/makeDefault",
            params=None,
            body=body,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
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
        extra_headers: Mapping[str, str] = {},
        **kwargs,
    ) -> Stream[PromptCompletionChunk]:
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
        extra_headers: Mapping[str, str] = {},
        **kwargs,
    ) -> PromptCompletion:
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
        extra_headers: Mapping[str, str] = {},
        **kwargs,
    ) -> Union[PromptCompletion, Stream[PromptCompletionChunk]]:
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
        extra_headers: Mapping[str, str] = {},
        **kwargs,
    ) -> Union[PromptCompletion, Stream[PromptCompletionChunk]]:
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
            cast_to=PromptCompletion,
            stream_cls=Stream[PromptCompletionChunk],
            stream=stream,
            headers=extra_headers,
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
        extra_headers: Mapping[str, str] = {},
        **kwargs,
    ) -> AsyncStream[PromptCompletionChunk]:
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
        extra_headers: Mapping[str, str] = {},
        **kwargs,
    ) -> PromptCompletion:
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
        extra_headers: Mapping[str, str] = {},
        **kwargs,
    ) -> Union[PromptCompletion, AsyncStream[PromptCompletionChunk]]:
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
        extra_headers: Mapping[str, str] = {},
        **kwargs,
    ) -> Union[PromptCompletion, AsyncStream[PromptCompletionChunk]]:
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
            cast_to=PromptCompletion,
            stream_cls=AsyncStream[PromptCompletionChunk],
            stream=stream,
            headers=extra_headers,
        )
