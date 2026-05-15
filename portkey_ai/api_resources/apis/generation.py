from __future__ import annotations
from urllib.parse import urlencode
import warnings
from typing import Dict, List, Literal, Union, Mapping, Any, overload
from portkey_ai._vendor.openai import NOT_GIVEN, NotGiven
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
        config: Union[Mapping, str, NotGiven] = NOT_GIVEN,
        variables: Union[Mapping[str, Any], NotGiven] = NOT_GIVEN,
    ) -> Union[GenericResponse, Stream[GenericResponse]]:
        warning_message = "This API has been deprecated. Please use the Prompt API for the saved prompt."  # noqa: E501
        warnings.warn(
            warning_message,
            DeprecationWarning,
            stacklevel=2,
        )
        if config is NOT_GIVEN:
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
        config: Union[Mapping, str, NotGiven] = NOT_GIVEN,
        variables: Union[Mapping[str, Any], NotGiven] = NOT_GIVEN,
    ) -> Union[GenericResponse, AsyncStream[GenericResponse]]:
        warning_message = "This API has been deprecated. Please use the Prompt API for the saved prompt."  # noqa: E501
        warnings.warn(
            warning_message,
            DeprecationWarning,
            stacklevel=2,
        )
        if config is NOT_GIVEN:
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
        self.versions = PromptVersions(client)
        self.partials = PromptPartials(client)

    def render(
        self,
        *,
        prompt_id: str,
        variables: Mapping[str, Any],
        stream: bool = False,
        temperature: Union[float, NotGiven] = NOT_GIVEN,
        max_tokens: Union[int, NotGiven] = NOT_GIVEN,
        top_k: Union[int, NotGiven] = NOT_GIVEN,
        top_p: Union[float, NotGiven] = NOT_GIVEN,
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
        virtual_key: Union[str, NotGiven] = NOT_GIVEN,
        model: Union[str, NotGiven] = NOT_GIVEN,
        functions: Union[List[Any], NotGiven] = NOT_GIVEN,
        tools: Union[List[Any], NotGiven] = NOT_GIVEN,
        tool_choice: Union[Dict[str, Any], NotGiven] = NOT_GIVEN,
        version_description: Union[str, NotGiven] = NOT_GIVEN,
        template_metadata: Union[Dict[str, Any], NotGiven] = NOT_GIVEN,
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
        collection_id: Union[str, NotGiven] = NOT_GIVEN,
        workspace_id: Union[str, NotGiven] = NOT_GIVEN,
        current_page: Union[int, NotGiven] = NOT_GIVEN,
        page_size: Union[int, NotGiven] = NOT_GIVEN,
        search: Union[str, NotGiven] = NOT_GIVEN,
    ) -> Any:
        query = {
            "collection_id": collection_id,
            "workspace_id": workspace_id,
            "current_page": current_page,
            "page_size": page_size,
            "search": search,
        }
        filtered_query = {k: v for k, v in query.items() if v is not NOT_GIVEN}
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

    def list_versions(
        self,
        prompt_slug: str,
    ) -> Any:
        return self._get(
            f"{PortkeyApiPaths.PROMPTS_API}/{prompt_slug}/versions",
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
        name: Union[str, NotGiven] = NOT_GIVEN,
        collection_id: Union[str, NotGiven] = NOT_GIVEN,
        string: Union[str, NotGiven] = NOT_GIVEN,
        parameters: Union[Dict[str, Any], NotGiven] = NOT_GIVEN,
        virtual_key: Union[str, NotGiven] = NOT_GIVEN,
        model: Union[str, NotGiven] = NOT_GIVEN,
        functions: Union[List[Any], NotGiven] = NOT_GIVEN,
        tools: Union[List[Any], NotGiven] = NOT_GIVEN,
        tool_choice: Union[Dict[str, Any], NotGiven] = NOT_GIVEN,
        version_description: Union[str, NotGiven] = NOT_GIVEN,
        template_metadata: Union[Dict[str, Any], NotGiven] = NOT_GIVEN,
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
        self.versions = AsyncPromptVersions(client)
        self.partials = AsyncPromptPartials(client)

    async def render(
        self,
        *,
        prompt_id: str,
        variables: Mapping[str, Any],
        stream: bool = False,
        temperature: Union[float, NotGiven] = NOT_GIVEN,
        max_tokens: Union[int, NotGiven] = NOT_GIVEN,
        top_k: Union[int, NotGiven] = NOT_GIVEN,
        top_p: Union[float, NotGiven] = NOT_GIVEN,
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
        virtual_key: Union[str, NotGiven] = NOT_GIVEN,
        model: Union[str, NotGiven] = NOT_GIVEN,
        functions: Union[List[Any], NotGiven] = NOT_GIVEN,
        tools: Union[List[Any], NotGiven] = NOT_GIVEN,
        tool_choice: Union[Dict[str, Any], NotGiven] = NOT_GIVEN,
        version_description: Union[str, NotGiven] = NOT_GIVEN,
        template_metadata: Union[Dict[str, Any], NotGiven] = NOT_GIVEN,
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
        collection_id: Union[str, NotGiven] = NOT_GIVEN,
        workspace_id: Union[str, NotGiven] = NOT_GIVEN,
        current_page: Union[int, NotGiven] = NOT_GIVEN,
        page_size: Union[int, NotGiven] = NOT_GIVEN,
        search: Union[str, NotGiven] = NOT_GIVEN,
    ) -> Any:
        query = {
            "collection_id": collection_id,
            "workspace_id": workspace_id,
            "current_page": current_page,
            "page_size": page_size,
            "search": search,
        }
        filtered_query = {k: v for k, v in query.items() if v is not NOT_GIVEN}
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
    
    async def list_versions(
        self,
        prompt_slug: str,
    ) -> Any:
        return await self._get(
            f"{PortkeyApiPaths.PROMPTS_API}/{prompt_slug}/versions",
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
        name: Union[str, NotGiven] = NOT_GIVEN,
        collection_id: Union[str, NotGiven] = NOT_GIVEN,
        string: Union[str, NotGiven] = NOT_GIVEN,
        parameters: Union[Dict[str, Any], NotGiven] = NOT_GIVEN,
        virtual_key: Union[str, NotGiven] = NOT_GIVEN,
        model: Union[str, NotGiven] = NOT_GIVEN,
        functions: Union[List[Any], NotGiven] = NOT_GIVEN,
        tools: Union[List[Any], NotGiven] = NOT_GIVEN,
        tool_choice: Union[Dict[str, Any], NotGiven] = NOT_GIVEN,
        version_description: Union[str, NotGiven] = NOT_GIVEN,
        template_metadata: Union[Dict[str, Any], NotGiven] = NOT_GIVEN,
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
        variables: Union[Mapping[str, Any], NotGiven] = NOT_GIVEN,
        config: Union[Mapping, str, NotGiven] = NOT_GIVEN,
        stream: Literal[True],
        temperature: Union[float, NotGiven] = NOT_GIVEN,
        max_tokens: Union[int, NotGiven] = NOT_GIVEN,
        top_k: Union[int, NotGiven] = NOT_GIVEN,
        top_p: Union[float, NotGiven] = NOT_GIVEN,
        extra_headers: Mapping[str, str] = {},
        **kwargs,
    ) -> Stream[PromptCompletionChunk]:
        ...

    @overload
    def create(
        self,
        *,
        prompt_id: str,
        variables: Union[Mapping[str, Any], NotGiven] = NOT_GIVEN,
        config: Union[Mapping, str, NotGiven] = NOT_GIVEN,
        stream: Literal[False] = False,
        temperature: Union[float, NotGiven] = NOT_GIVEN,
        max_tokens: Union[int, NotGiven] = NOT_GIVEN,
        top_k: Union[int, NotGiven] = NOT_GIVEN,
        top_p: Union[float, NotGiven] = NOT_GIVEN,
        extra_headers: Mapping[str, str] = {},
        **kwargs,
    ) -> PromptCompletion:
        ...

    @overload
    def create(
        self,
        *,
        prompt_id: str,
        variables: Union[Mapping[str, Any], NotGiven] = NOT_GIVEN,
        config: Union[Mapping, str, NotGiven] = NOT_GIVEN,
        stream: bool = False,
        temperature: Union[float, NotGiven] = NOT_GIVEN,
        max_tokens: Union[int, NotGiven] = NOT_GIVEN,
        top_k: Union[int, NotGiven] = NOT_GIVEN,
        top_p: Union[float, NotGiven] = NOT_GIVEN,
        extra_headers: Mapping[str, str] = {},
        **kwargs,
    ) -> Union[PromptCompletion, Stream[PromptCompletionChunk]]:
        ...

    def create(
        self,
        *,
        prompt_id: str,
        variables: Union[Mapping[str, Any], NotGiven] = NOT_GIVEN,
        config: Union[Mapping, str, NotGiven] = NOT_GIVEN,
        stream: bool = False,
        temperature: Union[float, NotGiven] = NOT_GIVEN,
        max_tokens: Union[int, NotGiven] = NOT_GIVEN,
        top_k: Union[int, NotGiven] = NOT_GIVEN,
        top_p: Union[float, NotGiven] = NOT_GIVEN,
        extra_headers: Mapping[str, str] = {},
        **kwargs,
    ) -> Union[PromptCompletion, Stream[PromptCompletionChunk]]:
        """Prompt completions Method"""
        if config is NOT_GIVEN:
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
        variables: Union[Mapping[str, Any], NotGiven] = NOT_GIVEN,
        config: Union[Mapping, str, NotGiven] = NOT_GIVEN,
        stream: Literal[True],
        temperature: Union[float, NotGiven] = NOT_GIVEN,
        max_tokens: Union[int, NotGiven] = NOT_GIVEN,
        top_k: Union[int, NotGiven] = NOT_GIVEN,
        top_p: Union[float, NotGiven] = NOT_GIVEN,
        extra_headers: Mapping[str, str] = {},
        **kwargs,
    ) -> AsyncStream[PromptCompletionChunk]:
        ...

    @overload
    async def create(
        self,
        *,
        prompt_id: str,
        variables: Union[Mapping[str, Any], NotGiven] = NOT_GIVEN,
        config: Union[Mapping, str, NotGiven] = NOT_GIVEN,
        stream: Literal[False] = False,
        temperature: Union[float, NotGiven] = NOT_GIVEN,
        max_tokens: Union[int, NotGiven] = NOT_GIVEN,
        top_k: Union[int, NotGiven] = NOT_GIVEN,
        top_p: Union[float, NotGiven] = NOT_GIVEN,
        extra_headers: Mapping[str, str] = {},
        **kwargs,
    ) -> PromptCompletion:
        ...

    @overload
    async def create(
        self,
        *,
        prompt_id: str,
        variables: Union[Mapping[str, Any], NotGiven] = NOT_GIVEN,
        config: Union[Mapping, str, NotGiven] = NOT_GIVEN,
        stream: bool = False,
        temperature: Union[float, NotGiven] = NOT_GIVEN,
        max_tokens: Union[int, NotGiven] = NOT_GIVEN,
        top_k: Union[int, NotGiven] = NOT_GIVEN,
        top_p: Union[float, NotGiven] = NOT_GIVEN,
        extra_headers: Mapping[str, str] = {},
        **kwargs,
    ) -> Union[PromptCompletion, AsyncStream[PromptCompletionChunk]]:
        ...

    async def create(
        self,
        *,
        prompt_id: str,
        variables: Union[Mapping[str, Any], NotGiven] = NOT_GIVEN,
        config: Union[Mapping, str, NotGiven] = NOT_GIVEN,
        stream: bool = False,
        temperature: Union[float, NotGiven] = NOT_GIVEN,
        max_tokens: Union[int, NotGiven] = NOT_GIVEN,
        top_k: Union[int, NotGiven] = NOT_GIVEN,
        top_p: Union[float, NotGiven] = NOT_GIVEN,
        extra_headers: Mapping[str, str] = {},
        **kwargs,
    ) -> Union[PromptCompletion, AsyncStream[PromptCompletionChunk]]:
        """Prompt completions Method"""
        if config is NOT_GIVEN:
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


class PromptVersions(APIResource):
    def __init__(self, client: APIClient) -> None:
        super().__init__(client)

    def list(
        self,
        prompt_slug: str,
    ) -> Any:
        return self._get(
            f"{PortkeyApiPaths.PROMPTS_API}/{prompt_slug}/versions",
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
        version_id: str,
    ) -> Any:
        return self._get(
            f"{PortkeyApiPaths.PROMPTS_API}/{prompt_slug}/versions/{version_id}",
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
        version_id: str,
        *,
        label_id: Union[str, NotGiven] = NOT_GIVEN,
    ) -> Any:
        body = {
            "label_id": label_id,
        }
        return self._put(
            f"{PortkeyApiPaths.PROMPTS_API}/{prompt_slug}/versions/{version_id}",
            params=None,
            body=body,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )


class AsyncPromptVersions(AsyncAPIResource):
    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)

    async def list(
        self,
        prompt_slug: str,
    ) -> Any:
        return await self._get(
            f"{PortkeyApiPaths.PROMPTS_API}/{prompt_slug}/versions",
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
        version_id: str,
    ) -> Any:
        return await self._get(
            f"{PortkeyApiPaths.PROMPTS_API}/{prompt_slug}/versions/{version_id}",
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
        version_id: str,
        *,
        label_id: Union[str, NotGiven] = NOT_GIVEN,
    ) -> Any:
        body = {
            "label_id": label_id,
        }
        return await self._put(
            f"{PortkeyApiPaths.PROMPTS_API}/{prompt_slug}/versions/{version_id}",
            params=None,
            body=body,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )


class PromptPartials(APIResource):
    def __init__(self, client: APIClient) -> None:
        super().__init__(client)
        self.versions = PromptPartialVersions(client)

    def create(
        self,
        *,
        name: str,
        string: str,
        workspace_id: Union[str, NotGiven] = NOT_GIVEN,
        version_description: Union[str, NotGiven] = NOT_GIVEN,
    ) -> Any:
        body = {
            "name": name,
            "string": string,
            "workspace_id": workspace_id,
            "version_description": version_description,
        }
        return self._post(
            f"{PortkeyApiPaths.PROMPTS_PARTIALS_API}",
            body=body,
            params=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def list(
        self,
        *,
        collection_id: Union[str, NotGiven] = NOT_GIVEN,
    ) -> Any:
        query = {
            "collection_id": collection_id,
        }
        filtered_query = {k: v for k, v in query.items() if v is not NOT_GIVEN}
        query_string = urlencode(filtered_query)
        return self._get(
            f"{PortkeyApiPaths.PROMPTS_PARTIALS_API}?{query_string}",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def retrieve(
        self,
        partial_slug: str,
    ) -> Any:
        return self._get(
            f"{PortkeyApiPaths.PROMPTS_PARTIALS_API}/{partial_slug}",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def update(
        self,
        partial_slug: str,
        *,
        name: Union[str, NotGiven] = NOT_GIVEN,
        string: Union[str, NotGiven] = NOT_GIVEN,
        description: Union[str, NotGiven] = NOT_GIVEN,
        status: Union[str, NotGiven] = NOT_GIVEN,
    ) -> Any:
        body = {
            "name": name,
            "string": string,
            "description": description,
            "status": status,
        }
        return self._put(
            f"{PortkeyApiPaths.PROMPTS_PARTIALS_API}/{partial_slug}",
            params=None,
            body=body,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def delete(
        self,
        partial_slug: str,
    ) -> Any:
        return self._delete(
            f"{PortkeyApiPaths.PROMPTS_PARTIALS_API}/{partial_slug}",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def publish(
        self,
        partial_slug: str,
        *,
        version: int,
    ) -> Any:
        body = {
            "version": version,
        }
        return self._put(
            f"{PortkeyApiPaths.PROMPTS_PARTIALS_API}/{partial_slug}/makeDefault",
            params=None,
            body=body,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )


class AsyncPromptPartials(AsyncAPIResource):
    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)
        self.versions = AsyncPromptPartialVersions(client)

    async def create(
        self,
        *,
        name: str,
        string: str,
        workspace_id: Union[str, NotGiven] = NOT_GIVEN,
        version_description: Union[str, NotGiven] = NOT_GIVEN,
    ) -> Any:
        body = {
            "name": name,
            "string": string,
            "workspace_id": workspace_id,
            "version_description": version_description,
        }
        return await self._post(
            f"{PortkeyApiPaths.PROMPTS_PARTIALS_API}",
            body=body,
            params=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def list(
        self,
        *,
        collection_id: Union[str, NotGiven] = NOT_GIVEN,
    ) -> Any:
        query = {
            "collection_id": collection_id,
        }
        filtered_query = {k: v for k, v in query.items() if v is not NOT_GIVEN}
        query_string = urlencode(filtered_query)
        return await self._get(
            f"{PortkeyApiPaths.PROMPTS_PARTIALS_API}?{query_string}",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def retrieve(
        self,
        partial_slug: str,
    ) -> Any:
        return await self._get(
            f"{PortkeyApiPaths.PROMPTS_PARTIALS_API}/{partial_slug}",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def update(
        self,
        partial_slug: str,
        *,
        name: Union[str, NotGiven] = NOT_GIVEN,
        string: Union[str, NotGiven] = NOT_GIVEN,
        description: Union[str, NotGiven] = NOT_GIVEN,
        status: Union[str, NotGiven] = NOT_GIVEN,
    ) -> Any:
        body = {
            "name": name,
            "string": string,
            "description": description,
            "status": status,
        }
        return await self._put(
            f"{PortkeyApiPaths.PROMPTS_PARTIALS_API}/{partial_slug}",
            params=None,
            body=body,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def delete(
        self,
        partial_slug: str,
    ) -> Any:
        return await self._delete(
            f"{PortkeyApiPaths.PROMPTS_PARTIALS_API}/{partial_slug}",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def publish(
        self,
        partial_slug: str,
        *,
        version: int,
    ) -> Any:
        body = {
            "version": version,
        }
        return await self._put(
            f"{PortkeyApiPaths.PROMPTS_PARTIALS_API}/{partial_slug}/makeDefault",
            params=None,
            body=body,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )


class PromptPartialVersions(APIResource):
    def __init__(self, client: APIClient) -> None:
        super().__init__(client)

    def list(
        self,
        partial_slug: str,
    ) -> Any:
        return self._get(
            f"{PortkeyApiPaths.PROMPTS_PARTIALS_API}/{partial_slug}/versions",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )


class AsyncPromptPartialVersions(AsyncAPIResource):
    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)

    async def list(
        self,
        partial_slug: str,
    ) -> Any:
        return await self._get(
            f"{PortkeyApiPaths.PROMPTS_PARTIALS_API}/{partial_slug}/versions",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )
