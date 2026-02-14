import json
from typing import Iterable, List, Literal, Optional, Union
from portkey_ai._vendor.openai._streaming import AsyncStream, Stream
from portkey_ai._vendor.openai.lib._parsing._responses import TextFormatT
from portkey_ai._vendor.openai.lib.streaming.responses._responses import (
    AsyncResponseStreamManager,
    ResponseStreamManager,
)
from portkey_ai._vendor.openai.types.responses import (
    input_token_count_params,
    response_create_params,
)
from portkey_ai._vendor.openai.types.responses.parsed_response import ParsedResponse
from portkey_ai._vendor.openai.types.responses.response_includable import (
    ResponseIncludable,
)
from portkey_ai._vendor.openai.types.responses.response_input_item_param import (
    ResponseInputItemParam,
)
from portkey_ai._vendor.openai.types.responses.response_input_param import (
    ResponseInputParam,
)
from portkey_ai._vendor.openai.types.responses.response_stream_event import (
    ResponseStreamEvent,
)
from portkey_ai._vendor.openai.types.responses.response_text_config_param import (
    ResponseTextConfigParam,
)
from portkey_ai._vendor.openai.types.responses.tool_param import (
    ParseableToolParam,
    ToolParam,
)
from portkey_ai._vendor.openai.types.responses.response import Response
from portkey_ai._vendor.openai.types.shared.chat_model import ChatModel
from portkey_ai._vendor.openai.types.shared.responses_model import ResponsesModel
from portkey_ai._vendor.openai.types.shared_params.reasoning import Reasoning
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.client import AsyncPortkey, Portkey
from portkey_ai.api_resources.types.response_type import (
    Response as ResponseType,
    CompactedResponse,
)
from portkey_ai.api_resources.types.responses_input_items_type import InputItemList
from portkey_ai.api_resources.types.responses_input_tokens_type import (
    InputTokenCountResponse,
)
from portkey_ai.api_resources.types.shared_types import Metadata
from ..._vendor.openai._types import Omit, omit
from typing_extensions import overload


class Responses(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.input_items = InputItems(client)
        self.input_tokens = InputTokens(client)

    @overload
    def create(
        self,
        *,
        input: Union[str, ResponseInputParam, Omit] = omit,
        model: Union[ResponsesModel, Omit] = omit,
        include: Union[Optional[List[ResponseIncludable]], Omit] = omit,
        instructions: Union[Optional[str], Omit] = omit,
        max_output_tokens: Union[Optional[int], Omit] = omit,
        metadata: Union[Optional[Metadata], Omit] = omit,
        parallel_tool_calls: Union[Optional[bool], Omit] = omit,
        previous_response_id: Union[Optional[str], Omit] = omit,
        prompt_cache_retention: Union[
            Optional[Literal["in-memory", "24h"]], Omit
        ] = omit,
        reasoning: Union[Optional[Reasoning], Omit] = omit,
        store: Union[Optional[bool], Omit] = omit,
        stream: Union[Literal[False], Omit] = omit,
        temperature: Union[Optional[float], Omit] = omit,
        text: Union[ResponseTextConfigParam, Omit] = omit,
        tool_choice: Union[response_create_params.ToolChoice, Omit] = omit,
        tools: Union[Iterable[ToolParam], Omit] = omit,
        top_p: Union[Optional[float], Omit] = omit,
        truncation: Union[Optional[Literal["auto", "disabled"]], Omit] = omit,
        user: Union[str, Omit] = omit,
        **kwargs,
    ) -> Response:
        ...

    @overload
    def create(
        self,
        *,
        input: Union[str, ResponseInputParam, Omit] = omit,
        model: Union[ResponsesModel, Omit] = omit,
        stream: Literal[True],
        include: Union[Optional[List[ResponseIncludable]], Omit] = omit,
        instructions: Union[Optional[str], Omit] = omit,
        max_output_tokens: Union[Optional[int], Omit] = omit,
        metadata: Union[Optional[Metadata], Omit] = omit,
        parallel_tool_calls: Union[Optional[bool], Omit] = omit,
        previous_response_id: Union[Optional[str], Omit] = omit,
        prompt_cache_retention: Union[
            Optional[Literal["in-memory", "24h"]], Omit
        ] = omit,
        reasoning: Union[Optional[Reasoning], Omit] = omit,
        store: Union[Optional[bool], Omit] = omit,
        temperature: Union[Optional[float], Omit] = omit,
        text: Union[ResponseTextConfigParam, Omit] = omit,
        tool_choice: Union[response_create_params.ToolChoice, Omit] = omit,
        tools: Union[Iterable[ToolParam], Omit] = omit,
        top_p: Union[Optional[float], Omit] = omit,
        truncation: Union[Optional[Literal["auto", "disabled"]], Omit] = omit,
        user: Union[str, Omit] = omit,
        **kwargs,
    ) -> Stream[ResponseStreamEvent]:
        ...

    @overload
    def create(
        self,
        *,
        input: Union[str, ResponseInputParam, Omit] = omit,
        model: Union[ResponsesModel, Omit] = omit,
        stream: bool,
        include: Union[Optional[List[ResponseIncludable]], Omit] = omit,
        instructions: Union[Optional[str], Omit] = omit,
        max_output_tokens: Union[Optional[int], Omit] = omit,
        metadata: Union[Optional[Metadata], Omit] = omit,
        parallel_tool_calls: Union[Optional[bool], Omit] = omit,
        previous_response_id: Union[Optional[str], Omit] = omit,
        prompt_cache_retention: Union[
            Optional[Literal["in-memory", "24h"]], Omit
        ] = omit,
        reasoning: Union[Optional[Reasoning], Omit] = omit,
        store: Union[Optional[bool], Omit] = omit,
        temperature: Union[Optional[float], Omit] = omit,
        text: Union[ResponseTextConfigParam, Omit] = omit,
        tool_choice: Union[response_create_params.ToolChoice, Omit] = omit,
        tools: Union[Iterable[ToolParam], Omit] = omit,
        top_p: Union[Optional[float], Omit] = omit,
        truncation: Union[Optional[Literal["auto", "disabled"]], Omit] = omit,
        user: Union[str, Omit] = omit,
        **kwargs,
    ) -> Union[Response, Stream[ResponseStreamEvent]]:
        ...

    def create(
        self,
        *,
        input: Union[str, ResponseInputParam, Omit] = omit,
        model: Union[ResponsesModel, Omit] = omit,
        include: Union[Optional[List[ResponseIncludable]], Omit] = omit,
        instructions: Union[Optional[str], Omit] = omit,
        max_output_tokens: Union[Optional[int], Omit] = omit,
        metadata: Union[Optional[Metadata], Omit] = omit,
        parallel_tool_calls: Union[Optional[bool], Omit] = omit,
        previous_response_id: Union[Optional[str], Omit] = omit,
        prompt_cache_retention: Union[
            Optional[Literal["in-memory", "24h"]], Omit
        ] = omit,
        reasoning: Union[Optional[Reasoning], Omit] = omit,
        store: Union[Optional[bool], Omit] = omit,
        stream: Union[Optional[Literal[False]], Literal[True], Omit] = omit,
        temperature: Union[Optional[float], Omit] = omit,
        text: Union[ResponseTextConfigParam, Omit] = omit,
        tool_choice: Union[response_create_params.ToolChoice, Omit] = omit,
        tools: Union[Iterable[ToolParam], Omit] = omit,
        top_p: Union[Optional[float], Omit] = omit,
        truncation: Union[Optional[Literal["auto", "disabled"]], Omit] = omit,
        user: Union[str, Omit] = omit,
        **kwargs,
    ) -> Union[Response, Stream[ResponseStreamEvent]]:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)

        return self.openai_client.responses.create(  # type: ignore[misc]
            input=input,
            model=model,
            include=include,
            instructions=instructions,
            max_output_tokens=max_output_tokens,
            metadata=metadata,
            parallel_tool_calls=parallel_tool_calls,
            previous_response_id=previous_response_id,
            prompt_cache_retention=prompt_cache_retention,
            reasoning=reasoning,
            store=store,
            stream=stream,  # type: ignore[arg-type]
            temperature=temperature,
            text=text,
            tool_choice=tool_choice,
            tools=tools,
            top_p=top_p,
            truncation=truncation,
            user=user,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body={**(extra_body or {}), **kwargs},
            timeout=timeout,
        )

    def retrieve(
        self,
        response_id: str,
        *,
        include: Union[List[ResponseIncludable], Omit] = omit,
        include_obfuscation: Union[bool, Omit] = omit,
        starting_after: Union[int, Omit] = omit,
        **kwargs,
    ) -> ResponseType:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)

        response = self.openai_client.with_raw_response.responses.retrieve(
            response_id=response_id,
            include=include,
            include_obfuscation=include_obfuscation,
            starting_after=starting_after,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body={**(extra_body or {}), **kwargs},
            timeout=timeout,
        )

        data = ResponseType(**json.loads(response.text))
        data._headers = response.headers

        return data

    def delete(self, response_id: str, **kwargs) -> None:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)

        return self.openai_client.responses.delete(
            response_id=response_id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body={**(extra_body or {}), **kwargs},
            timeout=timeout,
        )

    def stream(
        self,
        *,
        input: Union[str, ResponseInputParam],
        model: Union[str, ChatModel],
        text_format: Union[type[TextFormatT], Omit] = omit,  # type: ignore[type-arg]
        tools: Union[Iterable[ParseableToolParam], Omit] = omit,
        include: Union[List[ResponseIncludable], Omit] = omit,
        instructions: Union[str, Omit] = omit,
        max_output_tokens: Union[int, Omit] = omit,
        metadata: Union[Metadata, Omit] = omit,
        parallel_tool_calls: Union[bool, Omit] = omit,
        previous_response_id: Union[str, Omit] = omit,
        prompt_cache_retention: Union[
            Optional[Literal["in-memory", "24h"]], Omit
        ] = omit,
        reasoning: Union[Reasoning, Omit] = omit,
        store: Union[bool, Omit] = omit,
        stream_options: Union[response_create_params.StreamOptions, Omit] = omit,
        temperature: Union[float, Omit] = omit,
        text: Union[ResponseTextConfigParam, Omit] = omit,
        tool_choice: Union[response_create_params.ToolChoice, Omit] = omit,
        top_p: Union[float, Omit] = omit,
        truncation: Union[Literal["auto", "disabled"], Omit] = omit,
        user: Union[str, Omit] = omit,
        **kwargs,
    ) -> ResponseStreamManager[TextFormatT]:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)
        return self.openai_client.responses.stream(
            input=input,
            model=model,
            text_format=text_format,
            tools=tools,
            include=include,
            instructions=instructions,
            max_output_tokens=max_output_tokens,
            metadata=metadata,
            parallel_tool_calls=parallel_tool_calls,
            previous_response_id=previous_response_id,
            prompt_cache_retention=prompt_cache_retention,
            reasoning=reasoning,
            store=store,
            stream_options=stream_options,
            temperature=temperature,
            text=text,
            tool_choice=tool_choice,
            top_p=top_p,
            truncation=truncation,
            user=user,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body={**(extra_body or {}), **kwargs},
            timeout=timeout,
        )

    def parse(
        self,
        *,
        input: Union[str, ResponseInputParam, Omit] = omit,
        model: Union[str, ChatModel, Omit] = omit,
        text_format: Union[type[TextFormatT], Omit] = omit,  # type: ignore[type-arg]
        tools: Union[Iterable[ParseableToolParam], Omit] = omit,
        include: Union[List[ResponseIncludable], Omit] = omit,
        instructions: Union[str, Omit] = omit,
        max_output_tokens: Union[int, Omit] = omit,
        metadata: Union[Metadata, Omit] = omit,
        parallel_tool_calls: Union[bool, Omit] = omit,
        previous_response_id: Union[str, Omit] = omit,
        prompt_cache_retention: Union[
            Optional[Literal["in-memory", "24h"]], Omit
        ] = omit,
        reasoning: Union[Reasoning, Omit] = omit,
        store: Union[bool, Omit] = omit,
        stream: Union[Literal[False], Literal[True], Omit] = omit,
        temperature: Union[float, Omit] = omit,
        text: Union[ResponseTextConfigParam, Omit] = omit,
        tool_choice: Union[response_create_params.ToolChoice, Omit] = omit,
        top_p: Union[float, Omit] = omit,
        truncation: Union[Literal["auto", "disabled"], Omit] = omit,
        user: Union[str, Omit] = omit,
        **kwargs,
    ) -> ParsedResponse[TextFormatT]:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)

        return self.openai_client.responses.parse(
            input=input,
            model=model,
            text_format=text_format,
            tools=tools,
            include=include,
            instructions=instructions,
            max_output_tokens=max_output_tokens,
            metadata=metadata,
            parallel_tool_calls=parallel_tool_calls,
            previous_response_id=previous_response_id,
            prompt_cache_retention=prompt_cache_retention,
            reasoning=reasoning,
            store=store,
            stream=stream,
            temperature=temperature,
            text=text,
            tool_choice=tool_choice,
            top_p=top_p,
            truncation=truncation,
            user=user,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body={**(extra_body or {}), **kwargs},
            timeout=timeout,
        )

    def cancel(
        self,
        response_id: str,
        **kwargs,
    ) -> Response:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)
        return self.openai_client.responses.cancel(
            response_id=response_id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body={**(extra_body or {}), **kwargs},
            timeout=timeout,
        )

    def compact(
        self,
        *,
        model: Union[str, Omit] = omit,
        input: Union[str, Iterable[ResponseInputItemParam], None, Omit] = omit,
        instructions: Union[Optional[str], Omit] = omit,
        previous_response_id: Union[Optional[str], Omit] = omit,
        **kwargs,
    ) -> CompactedResponse:
        import json

        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)
        response = self.openai_client.with_raw_response.responses.compact(
            model=model,  # type: ignore[arg-type]
            input=input,
            instructions=instructions,
            previous_response_id=previous_response_id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body={**(extra_body or {}), **kwargs},
            timeout=timeout,
        )
        data = CompactedResponse(**json.loads(response.text))
        data._headers = response.headers
        return data


class InputItems(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    def list(
        self,
        response_id: str,
        *,
        after: Union[str, Omit] = omit,
        include: Union[List[ResponseIncludable], Omit] = omit,
        limit: Union[int, Omit] = omit,
        order: Union[Literal["asc", "desc"], Omit] = omit,
        **kwargs,
    ) -> InputItemList:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)
        response = self.openai_client.responses.input_items.list(
            response_id=response_id,
            after=after,
            include=include,
            limit=limit,
            order=order,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body={**(extra_body or {}), **kwargs},
            timeout=timeout,
        )

        return response  # type: ignore[return-value]


class InputTokens(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    def count(
        self,
        *,
        conversation: Union[
            Optional[input_token_count_params.Conversation], Omit
        ] = omit,
        input: Union[str, Iterable[ResponseInputItemParam], None, Omit] = omit,
        instructions: Union[Optional[str], Omit] = omit,
        model: Union[Optional[str], Omit] = omit,
        parallel_tool_calls: Union[Optional[bool], Omit] = omit,
        previous_response_id: Union[Optional[str], Omit] = omit,
        reasoning: Union[Optional[Reasoning], Omit] = omit,
        text: Union[Optional[input_token_count_params.Text], Omit] = omit,
        tool_choice: Union[Optional[input_token_count_params.ToolChoice], Omit] = omit,
        tools: Union[Optional[Iterable[ToolParam]], Omit] = omit,
        truncation: Union[Literal["auto", "disabled"], Omit] = omit,
        **kwargs,
    ) -> InputTokenCountResponse:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)
        response = self.openai_client.with_raw_response.responses.input_tokens.count(
            conversation=conversation,
            input=input,
            instructions=instructions,
            model=model,
            parallel_tool_calls=parallel_tool_calls,
            previous_response_id=previous_response_id,
            reasoning=reasoning,
            text=text,
            tool_choice=tool_choice,
            tools=tools,
            truncation=truncation,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body={**(extra_body or {}), **kwargs},
            timeout=timeout,
        )

        data = InputTokenCountResponse(**json.loads(response.text))
        data._headers = response.headers
        return data


class AsyncResponses(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.input_items = AsyncInputItems(client)
        self.input_tokens = AsyncInputTokens(client)

    @overload
    async def create(
        self,
        *,
        input: Union[str, ResponseInputParam, Omit] = omit,
        model: Union[ResponsesModel, Omit] = omit,
        include: Union[Optional[List[ResponseIncludable]], Omit] = omit,
        instructions: Union[Optional[str], Omit] = omit,
        max_output_tokens: Union[Optional[int], Omit] = omit,
        metadata: Union[Optional[Metadata], Omit] = omit,
        parallel_tool_calls: Union[Optional[bool], Omit] = omit,
        previous_response_id: Union[Optional[str], Omit] = omit,
        prompt_cache_retention: Union[
            Optional[Literal["in-memory", "24h"]], Omit
        ] = omit,
        reasoning: Union[Optional[Reasoning], Omit] = omit,
        store: Union[Optional[bool], Omit] = omit,
        stream: Union[Literal[False], Omit] = omit,
        temperature: Union[Optional[float], Omit] = omit,
        text: Union[ResponseTextConfigParam, Omit] = omit,
        tool_choice: Union[response_create_params.ToolChoice, Omit] = omit,
        tools: Union[Iterable[ToolParam], Omit] = omit,
        top_p: Union[Optional[float], Omit] = omit,
        truncation: Union[Optional[Literal["auto", "disabled"]], Omit] = omit,
        user: Union[str, Omit] = omit,
        **kwargs,
    ) -> Response:
        ...

    @overload
    async def create(
        self,
        *,
        input: Union[str, ResponseInputParam, Omit] = omit,
        model: Union[ResponsesModel, Omit] = omit,
        stream: Literal[True],
        include: Union[Optional[List[ResponseIncludable]], Omit] = omit,
        instructions: Union[Optional[str], Omit] = omit,
        max_output_tokens: Union[Optional[int], Omit] = omit,
        metadata: Union[Optional[Metadata], Omit] = omit,
        parallel_tool_calls: Union[Optional[bool], Omit] = omit,
        previous_response_id: Union[Optional[str], Omit] = omit,
        prompt_cache_retention: Union[
            Optional[Literal["in-memory", "24h"]], Omit
        ] = omit,
        reasoning: Union[Optional[Reasoning], Omit] = omit,
        store: Union[Optional[bool], Omit] = omit,
        temperature: Union[Optional[float], Omit] = omit,
        text: Union[ResponseTextConfigParam, Omit] = omit,
        tool_choice: Union[response_create_params.ToolChoice, Omit] = omit,
        tools: Union[Iterable[ToolParam], Omit] = omit,
        top_p: Union[Optional[float], Omit] = omit,
        truncation: Union[Optional[Literal["auto", "disabled"]], Omit] = omit,
        user: Union[str, Omit] = omit,
        **kwargs,
    ) -> AsyncStream[ResponseStreamEvent]:
        ...

    @overload
    async def create(
        self,
        *,
        input: Union[str, ResponseInputParam, Omit] = omit,
        model: Union[ResponsesModel, Omit] = omit,
        stream: bool,
        include: Union[Optional[List[ResponseIncludable]], Omit] = omit,
        instructions: Union[Optional[str], Omit] = omit,
        max_output_tokens: Union[Optional[int], Omit] = omit,
        metadata: Union[Optional[Metadata], Omit] = omit,
        parallel_tool_calls: Union[Optional[bool], Omit] = omit,
        previous_response_id: Union[Optional[str], Omit] = omit,
        prompt_cache_retention: Union[
            Optional[Literal["in-memory", "24h"]], Omit
        ] = omit,
        reasoning: Union[Optional[Reasoning], Omit] = omit,
        store: Union[Optional[bool], Omit] = omit,
        temperature: Union[Optional[float], Omit] = omit,
        text: Union[ResponseTextConfigParam, Omit] = omit,
        tool_choice: Union[response_create_params.ToolChoice, Omit] = omit,
        tools: Union[Iterable[ToolParam], Omit] = omit,
        top_p: Union[Optional[float], Omit] = omit,
        truncation: Union[Optional[Literal["auto", "disabled"]], Omit] = omit,
        user: Union[str, Omit] = omit,
        **kwargs,
    ) -> Union[Response, AsyncStream[ResponseStreamEvent]]:
        ...

    async def create(
        self,
        *,
        input: Union[str, ResponseInputParam, Omit] = omit,
        model: Union[ResponsesModel, Omit] = omit,
        include: Union[Optional[List[ResponseIncludable]], Omit] = omit,
        instructions: Union[Optional[str], Omit] = omit,
        max_output_tokens: Union[Optional[int], Omit] = omit,
        metadata: Union[Optional[Metadata], Omit] = omit,
        parallel_tool_calls: Union[Optional[bool], Omit] = omit,
        previous_response_id: Union[Optional[str], Omit] = omit,
        prompt_cache_retention: Union[
            Optional[Literal["in-memory", "24h"]], Omit
        ] = omit,
        reasoning: Union[Optional[Reasoning], Omit] = omit,
        store: Union[Optional[bool], Omit] = omit,
        stream: Union[Optional[Literal[False]], Literal[True], Omit] = omit,
        temperature: Union[Optional[float], Omit] = omit,
        text: Union[ResponseTextConfigParam, Omit] = omit,
        tool_choice: Union[response_create_params.ToolChoice, Omit] = omit,
        tools: Union[Iterable[ToolParam], Omit] = omit,
        top_p: Union[Optional[float], Omit] = omit,
        truncation: Union[Optional[Literal["auto", "disabled"]], Omit] = omit,
        user: Union[str, Omit] = omit,
        **kwargs,
    ) -> Union[Response, AsyncStream[ResponseStreamEvent]]:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)

        return await self.openai_client.responses.create(  # type: ignore[misc]
            input=input,
            model=model,
            include=include,
            instructions=instructions,
            max_output_tokens=max_output_tokens,
            metadata=metadata,
            parallel_tool_calls=parallel_tool_calls,
            previous_response_id=previous_response_id,
            prompt_cache_retention=prompt_cache_retention,
            reasoning=reasoning,
            store=store,
            stream=stream,  # type: ignore[arg-type]
            temperature=temperature,
            text=text,
            tool_choice=tool_choice,
            tools=tools,
            top_p=top_p,
            truncation=truncation,
            user=user,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body={**(extra_body or {}), **kwargs},
            timeout=timeout,
        )

    async def retrieve(
        self,
        response_id: str,
        *,
        include: Union[List[ResponseIncludable], Omit] = omit,
        include_obfuscation: Union[bool, Omit] = omit,
        starting_after: Union[int, Omit] = omit,
        **kwargs,
    ) -> ResponseType:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)

        response = await self.openai_client.with_raw_response.responses.retrieve(
            response_id=response_id,
            include=include,
            include_obfuscation=include_obfuscation,
            starting_after=starting_after,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body={**(extra_body or {}), **kwargs},
            timeout=timeout,
        )

        data = ResponseType(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def delete(self, response_id: str, **kwargs) -> None:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)

        return await self.openai_client.responses.delete(
            response_id=response_id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body={**(extra_body or {}), **kwargs},
            timeout=timeout,
        )

    def stream(
        self,
        *,
        input: Union[str, ResponseInputParam],
        model: Union[str, ChatModel],
        text_format: Union[type[TextFormatT], Omit] = omit,  # type: ignore[type-arg]
        tools: Union[Iterable[ParseableToolParam], Omit] = omit,
        include: Union[List[ResponseIncludable], Omit] = omit,
        instructions: Union[str, Omit] = omit,
        max_output_tokens: Union[int, Omit] = omit,
        metadata: Union[Metadata, Omit] = omit,
        parallel_tool_calls: Union[bool, Omit] = omit,
        previous_response_id: Union[str, Omit] = omit,
        prompt_cache_retention: Union[
            Optional[Literal["in-memory", "24h"]], Omit
        ] = omit,
        reasoning: Union[Reasoning, Omit] = omit,
        store: Union[bool, Omit] = omit,
        stream_options: Union[response_create_params.StreamOptions, Omit] = omit,
        temperature: Union[float, Omit] = omit,
        text: Union[ResponseTextConfigParam, Omit] = omit,
        tool_choice: Union[response_create_params.ToolChoice, Omit] = omit,
        top_p: Union[float, Omit] = omit,
        truncation: Union[Literal["auto", "disabled"], Omit] = omit,
        user: Union[str, Omit] = omit,
        **kwargs,
    ) -> AsyncResponseStreamManager[TextFormatT]:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)
        return self.openai_client.responses.stream(
            input=input,
            model=model,
            text_format=text_format,
            tools=tools,
            include=include,
            instructions=instructions,
            max_output_tokens=max_output_tokens,
            metadata=metadata,
            parallel_tool_calls=parallel_tool_calls,
            previous_response_id=previous_response_id,
            prompt_cache_retention=prompt_cache_retention,
            reasoning=reasoning,
            store=store,
            stream_options=stream_options,
            temperature=temperature,
            text=text,
            tool_choice=tool_choice,
            top_p=top_p,
            truncation=truncation,
            user=user,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body={**(extra_body or {}), **kwargs},
            timeout=timeout,
        )

    async def parse(
        self,
        *,
        input: Union[str, ResponseInputParam, Omit] = omit,
        model: Union[str, ChatModel, Omit] = omit,
        text_format: Union[type[TextFormatT], Omit] = omit,  # type: ignore[type-arg]
        tools: Union[Iterable[ParseableToolParam], Omit] = omit,
        include: Union[List[ResponseIncludable], Omit] = omit,
        instructions: Union[str, Omit] = omit,
        max_output_tokens: Union[int, Omit] = omit,
        metadata: Union[Metadata, Omit] = omit,
        parallel_tool_calls: Union[bool, Omit] = omit,
        previous_response_id: Union[str, Omit] = omit,
        prompt_cache_retention: Union[
            Optional[Literal["in-memory", "24h"]], Omit
        ] = omit,
        reasoning: Union[Reasoning, Omit] = omit,
        store: Union[bool, Omit] = omit,
        stream: Union[Literal[False], Literal[True], Omit] = omit,
        temperature: Union[float, Omit] = omit,
        text: Union[ResponseTextConfigParam, Omit] = omit,
        tool_choice: Union[response_create_params.ToolChoice, Omit] = omit,
        top_p: Union[float, Omit] = omit,
        truncation: Union[Literal["auto", "disabled"], Omit] = omit,
        user: Union[str, Omit] = omit,
        **kwargs,
    ) -> ParsedResponse[TextFormatT]:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)

        return await self.openai_client.responses.parse(
            input=input,
            model=model,
            text_format=text_format,
            tools=tools,
            include=include,
            instructions=instructions,
            max_output_tokens=max_output_tokens,
            metadata=metadata,
            parallel_tool_calls=parallel_tool_calls,
            previous_response_id=previous_response_id,
            prompt_cache_retention=prompt_cache_retention,
            reasoning=reasoning,
            store=store,
            stream=stream,
            temperature=temperature,
            text=text,
            tool_choice=tool_choice,
            top_p=top_p,
            truncation=truncation,
            user=user,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body={**(extra_body or {}), **kwargs},
            timeout=timeout,
        )

    async def cancel(
        self,
        response_id: str,
        **kwargs,
    ) -> Response:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)
        return await self.openai_client.responses.cancel(
            response_id=response_id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body={**(extra_body or {}), **kwargs},
            timeout=timeout,
        )

    async def compact(
        self,
        *,
        model: Union[str, Omit] = omit,
        input: Union[str, Iterable[ResponseInputItemParam], None, Omit] = omit,
        instructions: Union[Optional[str], Omit] = omit,
        previous_response_id: Union[Optional[str], Omit] = omit,
        **kwargs,
    ) -> CompactedResponse:
        import json

        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)
        response = await self.openai_client.with_raw_response.responses.compact(
            model=model,  # type: ignore[arg-type]
            input=input,
            instructions=instructions,
            previous_response_id=previous_response_id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body={**(extra_body or {}), **kwargs},
            timeout=timeout,
        )
        data = CompactedResponse(**json.loads(response.text))
        data._headers = response.headers
        return data


class AsyncInputItems(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    async def list(
        self,
        response_id: str,
        *,
        after: Union[str, Omit] = omit,
        include: Union[List[ResponseIncludable], Omit] = omit,
        limit: Union[int, Omit] = omit,
        order: Union[Literal["asc", "desc"], Omit] = omit,
        **kwargs,
    ) -> InputItemList:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)
        response = await self.openai_client.responses.input_items.list(
            response_id=response_id,
            after=after,
            include=include,
            limit=limit,
            order=order,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body={**(extra_body or {}), **kwargs},
            timeout=timeout,
        )

        return response  # type: ignore[return-value]


class AsyncInputTokens(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    async def count(
        self,
        *,
        conversation: Union[
            Optional[input_token_count_params.Conversation], Omit
        ] = omit,
        input: Union[str, Iterable[ResponseInputItemParam], None, Omit] = omit,
        instructions: Union[Optional[str], Omit] = omit,
        model: Union[Optional[str], Omit] = omit,
        parallel_tool_calls: Union[Optional[bool], Omit] = omit,
        previous_response_id: Union[Optional[str], Omit] = omit,
        reasoning: Union[Optional[Reasoning], Omit] = omit,
        text: Union[Optional[input_token_count_params.Text], Omit] = omit,
        tool_choice: Union[Optional[input_token_count_params.ToolChoice], Omit] = omit,
        tools: Union[Optional[Iterable[ToolParam]], Omit] = omit,
        truncation: Union[Literal["auto", "disabled"], Omit] = omit,
        **kwargs,
    ) -> InputTokenCountResponse:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)
        response = (
            await self.openai_client.with_raw_response.responses.input_tokens.count(
                conversation=conversation,
                input=input,
                instructions=instructions,
                model=model,
                parallel_tool_calls=parallel_tool_calls,
                previous_response_id=previous_response_id,
                reasoning=reasoning,
                text=text,
                tool_choice=tool_choice,
                tools=tools,
                truncation=truncation,
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body={**(extra_body or {}), **kwargs},
                timeout=timeout,
            )
        )

        data = InputTokenCountResponse(**json.loads(response.text))
        data._headers = response.headers
        return data
