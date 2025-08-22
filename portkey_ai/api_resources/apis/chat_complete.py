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
from ..._vendor.openai._types import NotGiven, NOT_GIVEN

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
        stream: Union[bool, NotGiven] = NOT_GIVEN,
        temperature: Union[float, NotGiven] = NOT_GIVEN,
        max_tokens: Union[int, NotGiven] = NOT_GIVEN,
        top_p: Union[float, NotGiven] = NOT_GIVEN,
        audio: Optional[Any] = NOT_GIVEN,
        max_completion_tokens: Union[int, NotGiven] = NOT_GIVEN,
        metadata: Union[Dict[str, str], NotGiven] = NOT_GIVEN,
        modalities: Union[List[Any], NotGiven] = NOT_GIVEN,
        prediction: Union[Any, NotGiven] = NOT_GIVEN,
        reasoning_effort: Union[Any, NotGiven] = NOT_GIVEN,
        store: Union[Optional[bool], NotGiven] = NOT_GIVEN,
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
        after: Union[str, NotGiven] = NOT_GIVEN,
        limit: Union[int, NotGiven] = NOT_GIVEN,
        metadata: Union[Metadata, NotGiven] = NOT_GIVEN,
        model: Union[str, NotGiven] = NOT_GIVEN,
        order: Union[Literal["asc", "desc"], NotGiven] = NOT_GIVEN,
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
        audio: Union[Optional[Any], NotGiven] = NOT_GIVEN,
        response_format: Union[Any, NotGiven] = NOT_GIVEN,
        frequency_penalty: Union[Optional[float], NotGiven] = NOT_GIVEN,
        function_call: Union[Any, NotGiven] = NOT_GIVEN,
        functions: Union[Iterable[Any], NotGiven] = NOT_GIVEN,
        logit_bias: Union[Optional[Dict[str, int]], NotGiven] = NOT_GIVEN,
        logprobs: Union[Optional[bool], NotGiven] = NOT_GIVEN,
        max_completion_tokens: Union[Optional[int], NotGiven] = NOT_GIVEN,
        max_tokens: Union[Optional[int], NotGiven] = NOT_GIVEN,
        metadata: Union[Optional[Metadata], NotGiven] = NOT_GIVEN,
        modalities: Union[Optional[List[Any]], NotGiven] = NOT_GIVEN,
        n: Union[Optional[int], NotGiven] = NOT_GIVEN,
        parallel_tool_calls: Union[bool, NotGiven] = NOT_GIVEN,
        prediction: Union[Any, NotGiven] = NOT_GIVEN,
        presence_penalty: Union[Optional[float], NotGiven] = NOT_GIVEN,
        prompt_cache_key: Union[str, NotGiven] = NOT_GIVEN,
        reasoning_effort: Union[Any, NotGiven] = NOT_GIVEN,
        safety_identifier: Union[str, NotGiven] = NOT_GIVEN,
        seed: Union[Optional[int], NotGiven] = NOT_GIVEN,
        service_tier: Union[
            Literal["auto", "default", "flex", "scale", "priority"], NotGiven
        ] = NOT_GIVEN,
        stop: Union[Optional[str], List[str], None] | NotGiven = NOT_GIVEN,
        store: Union[Optional[bool], NotGiven] = NOT_GIVEN,
        stream_options: Union[Any, NotGiven] = NOT_GIVEN,
        temperature: Union[Optional[float], NotGiven] = NOT_GIVEN,
        tool_choice: Union[Any, NotGiven] = NOT_GIVEN,
        tools: Union[Iterable[Any], NotGiven] = NOT_GIVEN,
        top_logprobs: Union[Optional[int], NotGiven] = NOT_GIVEN,
        top_p: Union[Optional[float], NotGiven] = NOT_GIVEN,
        user: Union[str, NotGiven] = NOT_GIVEN,
        verbosity: Union[Literal["low", "medium", "high"], NotGiven] = NOT_GIVEN,
        web_search_options: Union[Any, NotGiven] = NOT_GIVEN,
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
        audio: Union[Optional[Any], NotGiven] = NOT_GIVEN,
        response_format: Union[Any, NotGiven] = NOT_GIVEN,
        frequency_penalty: Union[Optional[float], NotGiven] = NOT_GIVEN,
        function_call: Union[Any, NotGiven] = NOT_GIVEN,
        functions: Union[Iterable[Any], NotGiven] = NOT_GIVEN,
        logit_bias: Union[Optional[Dict[str, int]], NotGiven] = NOT_GIVEN,
        logprobs: Union[Optional[bool], NotGiven] = NOT_GIVEN,
        max_completion_tokens: Union[Optional[int], NotGiven] = NOT_GIVEN,
        max_tokens: Union[Optional[int], NotGiven] = NOT_GIVEN,
        metadata: Union[Optional[Metadata], NotGiven] = NOT_GIVEN,
        modalities: Union[Optional[List[Any]], NotGiven] = NOT_GIVEN,
        n: Union[Optional[int], NotGiven] = NOT_GIVEN,
        parallel_tool_calls: Union[bool, NotGiven] = NOT_GIVEN,
        prediction: Union[Any, NotGiven] = NOT_GIVEN,
        presence_penalty: Union[Optional[float], NotGiven] = NOT_GIVEN,
        prompt_cache_key: Union[str, NotGiven] = NOT_GIVEN,
        reasoning_effort: Union[Any, NotGiven] = NOT_GIVEN,
        safety_identifier: Union[str, NotGiven] = NOT_GIVEN,
        seed: Union[Optional[int], NotGiven] = NOT_GIVEN,
        service_tier: Union[
            Literal["auto", "default", "flex", "scale", "priority"], NotGiven
        ] = NOT_GIVEN,
        stop: Union[Optional[str], List[str], None] | NotGiven = NOT_GIVEN,
        store: Union[Optional[bool], NotGiven] = NOT_GIVEN,
        stream_options: Union[Any, NotGiven] = NOT_GIVEN,
        temperature: Union[Optional[float], NotGiven] = NOT_GIVEN,
        tool_choice: Union[Any, NotGiven] = NOT_GIVEN,
        tools: Union[Iterable[Any], NotGiven] = NOT_GIVEN,
        top_logprobs: Union[Optional[int], NotGiven] = NOT_GIVEN,
        top_p: Union[Optional[float], NotGiven] = NOT_GIVEN,
        user: Union[str, NotGiven] = NOT_GIVEN,
        verbosity: Union[Literal["low", "medium", "high"], NotGiven] = NOT_GIVEN,
        web_search_options: Union[Any, NotGiven] = NOT_GIVEN,
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
        stream: Union[bool, NotGiven] = NOT_GIVEN,
        temperature: Union[float, NotGiven] = NOT_GIVEN,
        max_tokens: Union[int, NotGiven] = NOT_GIVEN,
        top_p: Union[float, NotGiven] = NOT_GIVEN,
        audio: Optional[Any] = NOT_GIVEN,
        max_completion_tokens: Union[int, NotGiven] = NOT_GIVEN,
        metadata: Union[Dict[str, str], NotGiven] = NOT_GIVEN,
        modalities: Union[List[Any], NotGiven] = NOT_GIVEN,
        prediction: Union[Any, NotGiven] = NOT_GIVEN,
        reasoning_effort: Union[Any, NotGiven] = NOT_GIVEN,
        store: Union[Optional[bool], NotGiven] = NOT_GIVEN,
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
        after: Union[str, NotGiven] = NOT_GIVEN,
        limit: Union[int, NotGiven] = NOT_GIVEN,
        metadata: Union[Metadata, NotGiven] = NOT_GIVEN,
        model: Union[str, NotGiven] = NOT_GIVEN,
        order: Union[Literal["asc", "desc"], NotGiven] = NOT_GIVEN,
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
        audio: Union[Optional[Any], NotGiven] = NOT_GIVEN,
        response_format: Union[Any, NotGiven] = NOT_GIVEN,
        frequency_penalty: Union[Optional[float], NotGiven] = NOT_GIVEN,
        function_call: Union[Any, NotGiven] = NOT_GIVEN,
        functions: Union[Iterable[Any], NotGiven] = NOT_GIVEN,
        logit_bias: Union[Optional[Dict[str, int]], NotGiven] = NOT_GIVEN,
        logprobs: Union[Optional[bool], NotGiven] = NOT_GIVEN,
        max_completion_tokens: Union[Optional[int], NotGiven] = NOT_GIVEN,
        max_tokens: Union[Optional[int], NotGiven] = NOT_GIVEN,
        metadata: Union[Optional[Metadata], NotGiven] = NOT_GIVEN,
        modalities: Union[Optional[List[Any]], NotGiven] = NOT_GIVEN,
        n: Union[Optional[int], NotGiven] = NOT_GIVEN,
        parallel_tool_calls: Union[bool, NotGiven] = NOT_GIVEN,
        prediction: Union[Any, NotGiven] = NOT_GIVEN,
        presence_penalty: Union[Optional[float], NotGiven] = NOT_GIVEN,
        prompt_cache_key: Union[str, NotGiven] = NOT_GIVEN,
        reasoning_effort: Union[Any, NotGiven] = NOT_GIVEN,
        safety_identifier: Union[str, NotGiven] = NOT_GIVEN,
        seed: Union[Optional[int], NotGiven] = NOT_GIVEN,
        service_tier: Union[
            Literal["auto", "default", "flex", "scale", "priority"], NotGiven
        ] = NOT_GIVEN,
        stop: Union[Optional[str], List[str], None] | NotGiven = NOT_GIVEN,
        store: Union[Optional[bool], NotGiven] = NOT_GIVEN,
        stream_options: Union[Any, NotGiven] = NOT_GIVEN,
        temperature: Union[Optional[float], NotGiven] = NOT_GIVEN,
        tool_choice: Union[Any, NotGiven] = NOT_GIVEN,
        tools: Union[Iterable[Any], NotGiven] = NOT_GIVEN,
        top_logprobs: Union[Optional[int], NotGiven] = NOT_GIVEN,
        top_p: Union[Optional[float], NotGiven] = NOT_GIVEN,
        user: Union[str, NotGiven] = NOT_GIVEN,
        verbosity: Union[Literal["low", "medium", "high"], NotGiven] = NOT_GIVEN,
        web_search_options: Union[Any, NotGiven] = NOT_GIVEN,
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
        audio: Union[Optional[Any], NotGiven] = NOT_GIVEN,
        response_format: Union[Any, NotGiven] = NOT_GIVEN,
        frequency_penalty: Union[Optional[float], NotGiven] = NOT_GIVEN,
        function_call: Union[Any, NotGiven] = NOT_GIVEN,
        functions: Union[Iterable[Any], NotGiven] = NOT_GIVEN,
        logit_bias: Union[Optional[Dict[str, int]], NotGiven] = NOT_GIVEN,
        logprobs: Union[Optional[bool], NotGiven] = NOT_GIVEN,
        max_completion_tokens: Union[Optional[int], NotGiven] = NOT_GIVEN,
        max_tokens: Union[Optional[int], NotGiven] = NOT_GIVEN,
        metadata: Union[Optional[Metadata], NotGiven] = NOT_GIVEN,
        modalities: Union[Optional[List[Any]], NotGiven] = NOT_GIVEN,
        n: Union[Optional[int], NotGiven] = NOT_GIVEN,
        parallel_tool_calls: Union[bool, NotGiven] = NOT_GIVEN,
        prediction: Union[Any, NotGiven] = NOT_GIVEN,
        presence_penalty: Union[Optional[float], NotGiven] = NOT_GIVEN,
        prompt_cache_key: Union[str, NotGiven] = NOT_GIVEN,
        reasoning_effort: Union[Any, NotGiven] = NOT_GIVEN,
        safety_identifier: Union[str, NotGiven] = NOT_GIVEN,
        seed: Union[Optional[int], NotGiven] = NOT_GIVEN,
        service_tier: Union[
            Literal["auto", "default", "flex", "scale", "priority"], NotGiven
        ] = NOT_GIVEN,
        stop: Union[Optional[str], List[str], None] | NotGiven = NOT_GIVEN,
        store: Union[Optional[bool], NotGiven] = NOT_GIVEN,
        stream_options: Union[Any, NotGiven] = NOT_GIVEN,
        temperature: Union[Optional[float], NotGiven] = NOT_GIVEN,
        tool_choice: Union[Any, NotGiven] = NOT_GIVEN,
        tools: Union[Iterable[Any], NotGiven] = NOT_GIVEN,
        top_logprobs: Union[Optional[int], NotGiven] = NOT_GIVEN,
        top_p: Union[Optional[float], NotGiven] = NOT_GIVEN,
        user: Union[str, NotGiven] = NOT_GIVEN,
        verbosity: Union[Literal["low", "medium", "high"], NotGiven] = NOT_GIVEN,
        web_search_options: Union[Any, NotGiven] = NOT_GIVEN,
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
        after: Union[str, NotGiven] = NOT_GIVEN,
        limit: Union[int, NotGiven] = NOT_GIVEN,
        order: Union[Literal["asc", "desc"], NotGiven] = NOT_GIVEN,
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
        after: Union[str, NotGiven] = NOT_GIVEN,
        limit: Union[int, NotGiven] = NOT_GIVEN,
        order: Union[Literal["asc", "desc"], NotGiven] = NOT_GIVEN,
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
