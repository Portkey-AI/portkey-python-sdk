from __future__ import annotations

import json
from typing import (
    Any,
    AsyncIterator,
    Dict,
    Iterable,
    Iterator,
    List,
    Literal,
    Mapping,
    Optional,
    Union,
)

import httpx
from portkey_ai._vendor.openai.types.chat.parsed_chat_completion import (
    ParsedChatCompletion,
)
from portkey_ai.api_resources.client import AsyncPortkey, Portkey
from portkey_ai.api_resources.types.chat_complete_type import (
    ChatCompletionChunk,
    ChatCompletionDeleted,
    ChatCompletionList,
    ChatCompletionStoreMessageList,
    ChatCompletions,
)

from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.types.shared_types import Headers, Metadata, Query
from portkey_ai.api_resources.utils import Body
from ..._vendor.openai._types import NOT_GIVEN, NotGiven, Omit, omit

__all__ = ["ChatCompletion", "AsyncChatCompletion"]


class ChatCompletion(APIResource):
    completions: Completions

    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.completions = Completions(client)


class AsyncChatCompletion(AsyncAPIResource):
    completions: AsyncCompletions

    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.completions = AsyncCompletions(client)


class Completions(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.messages = ChatCompletionsMessages(client)

    def stream_create(  # type: ignore[return]
        self,
        model,
        messages,
        stream,
        temperature,
        max_tokens,
        top_p,
        audio,
        max_completion_tokens,
        metadata,
        modalities,
        prediction,
        reasoning_effort,
        store,
        **kwargs,
    ) -> Union[ChatCompletions, Iterator[ChatCompletionChunk]]:
        extra_headers = kwargs.get("extra_headers", {})
        with self.openai_client.with_streaming_response.chat.completions.create(
            model=model,
            messages=messages,
            stream=stream,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            audio=audio,
            max_completion_tokens=max_completion_tokens,
            metadata=metadata,
            modalities=modalities,
            prediction=prediction,
            reasoning_effort=reasoning_effort,
            store=store,
            extra_headers=extra_headers,
            extra_body=kwargs,
        ) as response:
            for line in response.iter_lines():
                json_string = line.replace("data: ", "")
                json_string = json_string.strip().rstrip("\n")
                if json_string == "":
                    continue
                if json_string.startswith(":"):
                    continue
                elif json_string == "[DONE]":
                    break
                elif json_string != "":
                    json_data = json.loads(json_string)
                    json_data = ChatCompletionChunk(**json_data)
                    yield json_data
                else:
                    return ""

    def normal_create(
        self,
        model,
        messages,
        stream,
        temperature,
        max_tokens,
        top_p,
        audio,
        max_completion_tokens,
        metadata,
        modalities,
        prediction,
        reasoning_effort,
        store,
        **kwargs,
    ) -> ChatCompletions:
        extra_headers = kwargs.get("extra_headers", {})
        response = self.openai_client.with_raw_response.chat.completions.create(
            model=model,
            messages=messages,
            stream=stream,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            audio=audio,
            max_completion_tokens=max_completion_tokens,
            metadata=metadata,
            modalities=modalities,
            prediction=prediction,
            reasoning_effort=reasoning_effort,
            store=store,
            extra_headers=extra_headers,
            extra_body=kwargs,
        )
        data = ChatCompletions(**json.loads(response.text))
        data._headers = response.headers
        return data

    def create(
        self,
        *,
        model: Optional[str] = "portkey-default",
        messages: Iterable[Any],
        stream: Union[bool, Omit] = omit,
        temperature: Union[float, Omit] = omit,
        max_tokens: Union[int, Omit] = omit,
        top_p: Union[float, Omit] = omit,
        audio: Optional[Any] = omit,
        max_completion_tokens: Union[int, Omit] = omit,
        metadata: Union[Dict[str, str], Omit] = omit,
        modalities: Union[List[Any], Omit] = omit,
        prediction: Union[Any, Omit] = omit,
        reasoning_effort: Union[Any, Omit] = omit,
        store: Union[Optional[bool], Omit] = omit,
        **kwargs,
    ) -> Union[ChatCompletions, Iterator[ChatCompletionChunk]]:
        if stream is True:
            return self.stream_create(
                model=model,
                messages=messages,
                stream=stream,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                audio=audio,
                max_completion_tokens=max_completion_tokens,
                metadata=metadata,
                modalities=modalities,
                prediction=prediction,
                reasoning_effort=reasoning_effort,
                store=store,
                **kwargs,
            )
        else:
            return self.normal_create(
                model=model,
                messages=messages,
                stream=stream,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                audio=audio,
                max_completion_tokens=max_completion_tokens,
                metadata=metadata,
                modalities=modalities,
                prediction=prediction,
                reasoning_effort=reasoning_effort,
                store=store,
                **kwargs,
            )

    def retrieve(
        self,
        completion_id: str,
    ) -> ChatCompletions:
        if not completion_id:
            raise ValueError(
                "Expected a non-empty value for `completion_id` but received "
                f"{completion_id!r}"
            )
        response = self.openai_client.with_raw_response.chat.completions.retrieve(
            completion_id=completion_id
        )
        data = ChatCompletions(**json.loads(response.text))
        data._headers = response.headers

        return data

    def update(
        self,
        completion_id: str,
        *,
        metadata: Optional[Metadata] = None,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Optional[float | httpx.Timeout | None | NotGiven] = NOT_GIVEN,
    ) -> ChatCompletions:
        if not completion_id:
            raise ValueError(
                "Expected a non-empty value for `completion_id` but received "
                f"{completion_id!r}"
            )
        response = self.openai_client.with_raw_response.chat.completions.update(
            completion_id=completion_id,
            metadata=metadata,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        data = ChatCompletions(**json.loads(response.text))
        data._headers = response.headers

        return data

    def list(
        self,
        *,
        after: Union[str, Omit] = omit,
        limit: Union[int, Omit] = omit,
        metadata: Union[Metadata, Omit] = omit,
        model: Union[str, Omit] = omit,
        order: Union[Literal["asc", "desc"], Omit] = omit,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Optional[float | httpx.Timeout | None | NotGiven] = NOT_GIVEN,
    ) -> ChatCompletionList:
        response = self.openai_client.with_raw_response.chat.completions.list(
            after=after,
            limit=limit,
            metadata=metadata,
            model=model,
            order=order,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        data = ChatCompletionList(**json.loads(response.text))
        data._headers = response.headers

        return data

    def delete(
        self,
        completion_id: str,
        *,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Optional[float | httpx.Timeout | None | NotGiven] = NOT_GIVEN,
    ) -> ChatCompletionDeleted:
        if not completion_id:
            raise ValueError(
                "Expected a non-empty value for `completion_id` but received "
                f"{completion_id!r}"
            )
        response = self.openai_client.with_raw_response.chat.completions.delete(
            completion_id=completion_id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        data = ChatCompletionDeleted(**json.loads(response.text))
        data._headers = response.headers

        return data

    def parse(
        self,
        *,
        messages: Iterable[Any],
        model: Optional[str] = "portkey-default",
        audio: Union[Optional[Any], Omit] = omit,
        response_format: Union[Any, Omit] = omit,
        frequency_penalty: Union[Optional[float], Omit] = omit,
        function_call: Union[Any, Omit] = omit,
        functions: Union[Iterable[Any], Omit] = omit,
        logit_bias: Union[Optional[Dict[str, int]], Omit] = omit,
        logprobs: Union[Optional[bool], Omit] = omit,
        max_completion_tokens: Union[Optional[int], Omit] = omit,
        max_tokens: Union[Optional[int], Omit] = omit,
        metadata: Union[Optional[Metadata], Omit] = omit,
        modalities: Union[Optional[List[Any]], Omit] = omit,
        n: Union[Optional[int], Omit] = omit,
        parallel_tool_calls: Union[bool, Omit] = omit,
        prediction: Union[Any, Omit] = omit,
        presence_penalty: Union[Optional[float], Omit] = omit,
        prompt_cache_key: Union[str, Omit] = omit,
        reasoning_effort: Union[Any, Omit] = omit,
        safety_identifier: Union[str, Omit] = omit,
        seed: Union[Optional[int], Omit] = omit,
        service_tier: Union[
            Literal["auto", "default", "flex", "scale", "priority"], Omit
        ] = omit,
        stop: Union[Optional[str], List[str], None] | Omit = omit,
        store: Union[Optional[bool], Omit] = omit,
        stream_options: Union[Any, Omit] = omit,
        temperature: Union[Optional[float], Omit] = omit,
        tool_choice: Union[Any, Omit] = omit,
        tools: Union[Iterable[Any], Omit] = omit,
        top_logprobs: Union[Optional[int], Omit] = omit,
        top_p: Union[Optional[float], Omit] = omit,
        user: Union[str, Omit] = omit,
        verbosity: Union[Literal["low", "medium", "high"], Omit] = omit,
        web_search_options: Union[Any, Omit] = omit,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
    ) -> ParsedChatCompletion:
        response = self.openai_client.chat.completions.parse(
            messages=messages,
            model=model,  # type: ignore[arg-type]
            audio=audio,
            response_format=response_format,
            frequency_penalty=frequency_penalty,
            function_call=function_call,
            functions=functions,
            logit_bias=logit_bias,
            logprobs=logprobs,
            max_completion_tokens=max_completion_tokens,
            max_tokens=max_tokens,
            metadata=metadata,
            modalities=modalities,
            n=n,
            parallel_tool_calls=parallel_tool_calls,
            prediction=prediction,
            presence_penalty=presence_penalty,
            prompt_cache_key=prompt_cache_key,
            reasoning_effort=reasoning_effort,
            safety_identifier=safety_identifier,
            seed=seed,
            service_tier=service_tier,
            stop=stop,
            store=store,
            stream_options=stream_options,
            temperature=temperature,
            tool_choice=tool_choice,
            tools=tools,
            top_logprobs=top_logprobs,
            top_p=top_p,
            user=user,
            verbosity=verbosity,
            web_search_options=web_search_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
        )
        return response

    def stream(
        self,
        *,
        messages: Iterable[Any],
        model: Optional[str] = "portkey-default",
        audio: Union[Optional[Any], Omit] = omit,
        response_format: Union[Any, Omit] = omit,
        frequency_penalty: Union[Optional[float], Omit] = omit,
        function_call: Union[Any, Omit] = omit,
        functions: Union[Iterable[Any], Omit] = omit,
        logit_bias: Union[Optional[Dict[str, int]], Omit] = omit,
        logprobs: Union[Optional[bool], Omit] = omit,
        max_completion_tokens: Union[Optional[int], Omit] = omit,
        max_tokens: Union[Optional[int], Omit] = omit,
        metadata: Union[Optional[Metadata], Omit] = omit,
        modalities: Union[Optional[List[Any]], Omit] = omit,
        n: Union[Optional[int], Omit] = omit,
        parallel_tool_calls: Union[bool, Omit] = omit,
        prediction: Union[Any, Omit] = omit,
        presence_penalty: Union[Optional[float], Omit] = omit,
        prompt_cache_key: Union[str, Omit] = omit,
        reasoning_effort: Union[Any, Omit] = omit,
        safety_identifier: Union[str, Omit] = omit,
        seed: Union[Optional[int], Omit] = omit,
        service_tier: Union[
            Literal["auto", "default", "flex", "scale", "priority"], Omit
        ] = omit,
        stop: Union[Optional[str], List[str], None] | Omit = omit,
        store: Union[Optional[bool], Omit] = omit,
        stream_options: Union[Any, Omit] = omit,
        temperature: Union[Optional[float], Omit] = omit,
        tool_choice: Union[Any, Omit] = omit,
        tools: Union[Iterable[Any], Omit] = omit,
        top_logprobs: Union[Optional[int], Omit] = omit,
        top_p: Union[Optional[float], Omit] = omit,
        user: Union[str, Omit] = omit,
        verbosity: Union[Literal["low", "medium", "high"], Omit] = omit,
        web_search_options: Union[Any, Omit] = omit,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
    ) -> Any:
        return self.openai_client.chat.completions.stream(
            messages=messages,
            model=model,  # type: ignore[arg-type]
            audio=audio,
            response_format=response_format,
            frequency_penalty=frequency_penalty,
            function_call=function_call,
            functions=functions,
            logit_bias=logit_bias,
            logprobs=logprobs,
            max_completion_tokens=max_completion_tokens,
            max_tokens=max_tokens,
            metadata=metadata,
            modalities=modalities,
            n=n,
            parallel_tool_calls=parallel_tool_calls,
            prediction=prediction,
            presence_penalty=presence_penalty,
            prompt_cache_key=prompt_cache_key,
            reasoning_effort=reasoning_effort,
            safety_identifier=safety_identifier,
            seed=seed,
            service_tier=service_tier,
            stop=stop,
            store=store,
            stream_options=stream_options,
            temperature=temperature,
            tool_choice=tool_choice,
            tools=tools,
            top_logprobs=top_logprobs,
            top_p=top_p,
            user=user,
            verbosity=verbosity,
            web_search_options=web_search_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
        )


class AsyncCompletions(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.messages = AsyncChatCompletionsMessages(client)

    async def stream_create(
        self,
        model,
        messages,
        stream,
        temperature,
        max_tokens,
        top_p,
        audio,
        max_completion_tokens,
        metadata,
        modalities,
        prediction,
        reasoning_effort,
        store,
        **kwargs,
    ) -> Union[ChatCompletions, AsyncIterator[ChatCompletionChunk]]:
        extra_headers = kwargs.get("extra_headers", {})
        async with self.openai_client.with_streaming_response.chat.completions.create(
            model=model,
            messages=messages,
            stream=stream,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            audio=audio,
            max_completion_tokens=max_completion_tokens,
            metadata=metadata,
            modalities=modalities,
            prediction=prediction,
            reasoning_effort=reasoning_effort,
            store=store,
            extra_headers=extra_headers,
            extra_body=kwargs,
        ) as response:
            async for line in response.iter_lines():
                json_string = line.replace("data: ", "")
                json_string = json_string.strip().rstrip("\n")
                if json_string == "":
                    continue
                if json_string.startswith(":"):
                    continue
                elif json_string == "[DONE]":
                    break
                elif json_string != "":
                    json_data = json.loads(json_string)
                    json_data = ChatCompletionChunk(**json_data)
                    yield json_data
                else:
                    pass

    async def normal_create(
        self,
        model,
        messages,
        stream,
        temperature,
        max_tokens,
        top_p,
        audio,
        max_completion_tokens,
        metadata,
        modalities,
        prediction,
        reasoning_effort,
        store,
        **kwargs,
    ) -> ChatCompletions:
        extra_headers = kwargs.get("extra_headers", {})
        response = await self.openai_client.with_raw_response.chat.completions.create(
            model=model,
            messages=messages,
            stream=stream,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            audio=audio,
            max_completion_tokens=max_completion_tokens,
            metadata=metadata,
            modalities=modalities,
            prediction=prediction,
            reasoning_effort=reasoning_effort,
            store=store,
            extra_headers=extra_headers,
            extra_body=kwargs,
        )
        data = ChatCompletions(**json.loads(response.text))
        data._headers = response.headers
        return data

    async def create(
        self,
        *,
        model: Optional[str] = "portkey-default",
        messages: Iterable[Any],
        stream: Union[bool, Omit] = omit,
        temperature: Union[float, Omit] = omit,
        max_tokens: Union[int, Omit] = omit,
        top_p: Union[float, Omit] = omit,
        audio: Optional[Any] = omit,
        max_completion_tokens: Union[int, Omit] = omit,
        metadata: Union[Dict[str, str], Omit] = omit,
        modalities: Union[List[Any], Omit] = omit,
        prediction: Union[Any, Omit] = omit,
        reasoning_effort: Union[Any, Omit] = omit,
        store: Union[Optional[bool], Omit] = omit,
        **kwargs,
    ) -> Union[ChatCompletions, AsyncIterator[ChatCompletionChunk]]:
        if stream is True:
            return self.stream_create(
                model=model,
                messages=messages,
                stream=stream,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                audio=audio,
                max_completion_tokens=max_completion_tokens,
                metadata=metadata,
                modalities=modalities,
                prediction=prediction,
                reasoning_effort=reasoning_effort,
                store=store,
                **kwargs,
            )
        else:
            return await self.normal_create(
                model=model,
                messages=messages,
                stream=stream,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                audio=audio,
                max_completion_tokens=max_completion_tokens,
                metadata=metadata,
                modalities=modalities,
                prediction=prediction,
                reasoning_effort=reasoning_effort,
                store=store,
                **kwargs,
            )

    async def retrieve(
        self,
        completion_id: str,
    ) -> ChatCompletions:
        response = await self.openai_client.with_raw_response.chat.completions.retrieve(
            completion_id=completion_id
        )
        data = ChatCompletions(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def update(
        self,
        completion_id: str,
        *,
        metadata: Optional[Metadata] = None,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Optional[float | httpx.Timeout | None | NotGiven] = NOT_GIVEN,
    ) -> ChatCompletions:
        if not completion_id:
            raise ValueError(
                "Expected a non-empty value for `completion_id` but received "
                f"{completion_id!r}"
            )
        response = await self.openai_client.with_raw_response.chat.completions.update(
            completion_id=completion_id,
            metadata=metadata,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        data = ChatCompletions(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def list(
        self,
        *,
        after: Union[str, Omit] = omit,
        limit: Union[int, Omit] = omit,
        metadata: Union[Metadata, Omit] = omit,
        model: Union[str, Omit] = omit,
        order: Union[Literal["asc", "desc"], Omit] = omit,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Optional[float | httpx.Timeout | None | NotGiven] = NOT_GIVEN,
    ) -> ChatCompletionList:
        response = await self.openai_client.with_raw_response.chat.completions.list(
            after=after,
            limit=limit,
            metadata=metadata,
            model=model,
            order=order,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        data = ChatCompletionList(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def delete(
        self,
        completion_id: str,
        *,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Optional[float | httpx.Timeout | None | NotGiven] = NOT_GIVEN,
    ) -> ChatCompletionDeleted:
        if not completion_id:
            raise ValueError(
                "Expected a non-empty value for `completion_id` but received "
                f"{completion_id!r}"
            )
        response = await self.openai_client.with_raw_response.chat.completions.delete(
            completion_id=completion_id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        data = ChatCompletionDeleted(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def parse(
        self,
        *,
        messages: Iterable[Any],
        model: Optional[str] = "portkey-default",
        audio: Union[Optional[Any], Omit] = omit,
        response_format: Union[Any, Omit] = omit,
        frequency_penalty: Union[Optional[float], Omit] = omit,
        function_call: Union[Any, Omit] = omit,
        functions: Union[Iterable[Any], Omit] = omit,
        logit_bias: Union[Optional[Dict[str, int]], Omit] = omit,
        logprobs: Union[Optional[bool], Omit] = omit,
        max_completion_tokens: Union[Optional[int], Omit] = omit,
        max_tokens: Union[Optional[int], Omit] = omit,
        metadata: Union[Optional[Metadata], Omit] = omit,
        modalities: Union[Optional[List[Any]], Omit] = omit,
        n: Union[Optional[int], Omit] = omit,
        parallel_tool_calls: Union[bool, Omit] = omit,
        prediction: Union[Any, Omit] = omit,
        presence_penalty: Union[Optional[float], Omit] = omit,
        prompt_cache_key: Union[str, Omit] = omit,
        reasoning_effort: Union[Any, Omit] = omit,
        safety_identifier: Union[str, Omit] = omit,
        seed: Union[Optional[int], Omit] = omit,
        service_tier: Union[
            Literal["auto", "default", "flex", "scale", "priority"], Omit
        ] = omit,
        stop: Union[Optional[str], List[str], None] | Omit = omit,
        store: Union[Optional[bool], Omit] = omit,
        stream_options: Union[Any, Omit] = omit,
        temperature: Union[Optional[float], Omit] = omit,
        tool_choice: Union[Any, Omit] = omit,
        tools: Union[Iterable[Any], Omit] = omit,
        top_logprobs: Union[Optional[int], Omit] = omit,
        top_p: Union[Optional[float], Omit] = omit,
        user: Union[str, Omit] = omit,
        verbosity: Union[Literal["low", "medium", "high"], Omit] = omit,
        web_search_options: Union[Any, Omit] = omit,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
    ) -> ParsedChatCompletion:
        response = await self.openai_client.chat.completions.parse(
            messages=messages,
            model=model,  # type: ignore[arg-type]
            audio=audio,
            response_format=response_format,
            frequency_penalty=frequency_penalty,
            function_call=function_call,
            functions=functions,
            logit_bias=logit_bias,
            logprobs=logprobs,
            max_completion_tokens=max_completion_tokens,
            max_tokens=max_tokens,
            metadata=metadata,
            modalities=modalities,
            n=n,
            parallel_tool_calls=parallel_tool_calls,
            prediction=prediction,
            presence_penalty=presence_penalty,
            prompt_cache_key=prompt_cache_key,
            reasoning_effort=reasoning_effort,
            safety_identifier=safety_identifier,
            seed=seed,
            service_tier=service_tier,
            stop=stop,
            store=store,
            stream_options=stream_options,
            temperature=temperature,
            tool_choice=tool_choice,
            tools=tools,
            top_logprobs=top_logprobs,
            top_p=top_p,
            user=user,
            verbosity=verbosity,
            web_search_options=web_search_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
        )
        return response

    def stream(
        self,
        *,
        messages: Iterable[Any],
        model: Optional[str] = "portkey-default",
        audio: Union[Optional[Any], Omit] = omit,
        response_format: Union[Any, Omit] = omit,
        frequency_penalty: Union[Optional[float], Omit] = omit,
        function_call: Union[Any, Omit] = omit,
        functions: Union[Iterable[Any], Omit] = omit,
        logit_bias: Union[Optional[Dict[str, int]], Omit] = omit,
        logprobs: Union[Optional[bool], Omit] = omit,
        max_completion_tokens: Union[Optional[int], Omit] = omit,
        max_tokens: Union[Optional[int], Omit] = omit,
        metadata: Union[Optional[Metadata], Omit] = omit,
        modalities: Union[Optional[List[Any]], Omit] = omit,
        n: Union[Optional[int], Omit] = omit,
        parallel_tool_calls: Union[bool, Omit] = omit,
        prediction: Union[Any, Omit] = omit,
        presence_penalty: Union[Optional[float], Omit] = omit,
        prompt_cache_key: Union[str, Omit] = omit,
        reasoning_effort: Union[Any, Omit] = omit,
        safety_identifier: Union[str, Omit] = omit,
        seed: Union[Optional[int], Omit] = omit,
        service_tier: Union[
            Literal["auto", "default", "flex", "scale", "priority"], Omit
        ] = omit,
        stop: Union[Optional[str], List[str], None] | Omit = omit,
        store: Union[Optional[bool], Omit] = omit,
        stream_options: Union[Any, Omit] = omit,
        temperature: Union[Optional[float], Omit] = omit,
        tool_choice: Union[Any, Omit] = omit,
        tools: Union[Iterable[Any], Omit] = omit,
        top_logprobs: Union[Optional[int], Omit] = omit,
        top_p: Union[Optional[float], Omit] = omit,
        user: Union[str, Omit] = omit,
        verbosity: Union[Literal["low", "medium", "high"], Omit] = omit,
        web_search_options: Union[Any, Omit] = omit,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
    ) -> Any:
        return self.openai_client.chat.completions.stream(
            messages=messages,
            model=model,  # type: ignore[arg-type]
            audio=audio,
            response_format=response_format,
            frequency_penalty=frequency_penalty,
            function_call=function_call,
            functions=functions,
            logit_bias=logit_bias,
            logprobs=logprobs,
            max_completion_tokens=max_completion_tokens,
            max_tokens=max_tokens,
            metadata=metadata,
            modalities=modalities,
            n=n,
            parallel_tool_calls=parallel_tool_calls,
            prediction=prediction,
            presence_penalty=presence_penalty,
            prompt_cache_key=prompt_cache_key,
            reasoning_effort=reasoning_effort,
            safety_identifier=safety_identifier,
            seed=seed,
            service_tier=service_tier,
            stop=stop,
            store=store,
            stream_options=stream_options,
            temperature=temperature,
            tool_choice=tool_choice,
            tools=tools,
            top_logprobs=top_logprobs,
            top_p=top_p,
            user=user,
            verbosity=verbosity,
            web_search_options=web_search_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
        )

    def _get_config_string(self, config: Union[Mapping, str]) -> str:
        return config if isinstance(config, str) else json.dumps(config)


class ChatCompletionsMessages(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    def list(
        self,
        completion_id: str,
        *,
        after: Union[str, Omit] = omit,
        limit: Union[int, Omit] = omit,
        order: Union[Literal["asc", "desc"], Omit] = omit,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Optional[float | httpx.Timeout | None | NotGiven] = NOT_GIVEN,
    ) -> ChatCompletionStoreMessageList:
        if not completion_id:
            raise ValueError(
                "Expected a non-empty value for `completion_id` but received "
                f"{completion_id!r}"
            )
        response = self.openai_client.with_raw_response.chat.completions.messages.list(
            completion_id=completion_id,
            after=after,
            limit=limit,
            order=order,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        data = ChatCompletionStoreMessageList(**json.loads(response.text))
        data._headers = response.headers

        return data


class AsyncChatCompletionsMessages(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    async def list(
        self,
        completion_id: str,
        *,
        after: Union[str, Omit] = omit,
        limit: Union[int, Omit] = omit,
        order: Union[Literal["asc", "desc"], Omit] = omit,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Optional[float | httpx.Timeout | None | NotGiven] = NOT_GIVEN,
    ) -> ChatCompletionStoreMessageList:
        if not completion_id:
            raise ValueError(
                "Expected a non-empty value for `completion_id` but received "
                f"{completion_id!r}"
            )
        response = (
            await self.openai_client.with_raw_response.chat.completions.messages.list(
                completion_id=completion_id,
                after=after,
                limit=limit,
                order=order,
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            )
        )
        data = ChatCompletionStoreMessageList(**json.loads(response.text))
        data._headers = response.headers

        return data
