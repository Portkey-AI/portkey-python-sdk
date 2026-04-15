import json
from typing import Iterable, List, Literal, Optional, Type, Union
from portkey_ai._vendor.openai._streaming import AsyncStream, Stream
from portkey_ai._vendor.openai.lib._parsing._responses import TextFormatT
from portkey_ai._vendor.openai.lib.streaming.responses._responses import (
    AsyncResponseStreamManager,
    ResponseStreamManager,
)
from portkey_ai._vendor.openai.resources.responses.responses import (
    AsyncResponsesConnectionManager,
    ResponsesConnectionManager,
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
from portkey_ai._vendor.openai.types.responses.response_prompt_param import (
    ResponsePromptParam,
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
from portkey_ai._vendor.openai.types.websocket_connection_options import (
    WebSocketConnectionOptions,
)
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
        background: Union[Optional[bool], Omit] = omit,
        context_management: Union[
            Optional[Iterable[response_create_params.ContextManagement]], Omit
        ] = omit,
        conversation: Union[Optional[response_create_params.Conversation], Omit] = omit,
        include: Union[Optional[List[ResponseIncludable]], Omit] = omit,
        input: Union[str, ResponseInputParam, Omit] = omit,
        instructions: Union[Optional[str], Omit] = omit,
        max_output_tokens: Union[Optional[int], Omit] = omit,
        max_tool_calls: Union[Optional[int], Omit] = omit,
        metadata: Union[Optional[Metadata], Omit] = omit,
        model: Union[ResponsesModel, Omit] = omit,
        parallel_tool_calls: Union[Optional[bool], Omit] = omit,
        previous_response_id: Union[Optional[str], Omit] = omit,
        prompt: Union[Optional[ResponsePromptParam], Omit] = omit,
        prompt_cache_key: Union[str, Omit] = omit,
        prompt_cache_retention: Union[
            Optional[Literal["in-memory", "24h"]], Omit
        ] = omit,
        reasoning: Union[Optional[Reasoning], Omit] = omit,
        safety_identifier: Union[str, Omit] = omit,
        service_tier: Union[
            Optional[Literal["auto", "default", "flex", "scale", "priority"]], Omit
        ] = omit,
        store: Union[Optional[bool], Omit] = omit,
        stream: Union[Optional[Literal[False]], Omit] = omit,
        stream_options: Union[
            Optional[response_create_params.StreamOptions], Omit
        ] = omit,
        temperature: Union[Optional[float], Omit] = omit,
        text: Union[ResponseTextConfigParam, Omit] = omit,
        tool_choice: Union[response_create_params.ToolChoice, Omit] = omit,
        tools: Union[Iterable[ToolParam], Omit] = omit,
        top_logprobs: Union[Optional[int], Omit] = omit,
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
        stream: Literal[True],
        background: Union[Optional[bool], Omit] = omit,
        context_management: Union[
            Optional[Iterable[response_create_params.ContextManagement]], Omit
        ] = omit,
        conversation: Union[Optional[response_create_params.Conversation], Omit] = omit,
        include: Union[Optional[List[ResponseIncludable]], Omit] = omit,
        input: Union[str, ResponseInputParam, Omit] = omit,
        instructions: Union[Optional[str], Omit] = omit,
        max_output_tokens: Union[Optional[int], Omit] = omit,
        max_tool_calls: Union[Optional[int], Omit] = omit,
        metadata: Union[Optional[Metadata], Omit] = omit,
        model: Union[ResponsesModel, Omit] = omit,
        parallel_tool_calls: Union[Optional[bool], Omit] = omit,
        previous_response_id: Union[Optional[str], Omit] = omit,
        prompt: Union[Optional[ResponsePromptParam], Omit] = omit,
        prompt_cache_key: Union[str, Omit] = omit,
        prompt_cache_retention: Union[
            Optional[Literal["in-memory", "24h"]], Omit
        ] = omit,
        reasoning: Union[Optional[Reasoning], Omit] = omit,
        safety_identifier: Union[str, Omit] = omit,
        service_tier: Union[
            Optional[Literal["auto", "default", "flex", "scale", "priority"]], Omit
        ] = omit,
        store: Union[Optional[bool], Omit] = omit,
        stream_options: Union[
            Optional[response_create_params.StreamOptions], Omit
        ] = omit,
        temperature: Union[Optional[float], Omit] = omit,
        text: Union[ResponseTextConfigParam, Omit] = omit,
        tool_choice: Union[response_create_params.ToolChoice, Omit] = omit,
        tools: Union[Iterable[ToolParam], Omit] = omit,
        top_logprobs: Union[Optional[int], Omit] = omit,
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
        stream: bool,
        background: Union[Optional[bool], Omit] = omit,
        context_management: Union[
            Optional[Iterable[response_create_params.ContextManagement]], Omit
        ] = omit,
        conversation: Union[Optional[response_create_params.Conversation], Omit] = omit,
        include: Union[Optional[List[ResponseIncludable]], Omit] = omit,
        input: Union[str, ResponseInputParam, Omit] = omit,
        instructions: Union[Optional[str], Omit] = omit,
        max_output_tokens: Union[Optional[int], Omit] = omit,
        max_tool_calls: Union[Optional[int], Omit] = omit,
        metadata: Union[Optional[Metadata], Omit] = omit,
        model: Union[ResponsesModel, Omit] = omit,
        parallel_tool_calls: Union[Optional[bool], Omit] = omit,
        previous_response_id: Union[Optional[str], Omit] = omit,
        prompt: Union[Optional[ResponsePromptParam], Omit] = omit,
        prompt_cache_key: Union[str, Omit] = omit,
        prompt_cache_retention: Union[
            Optional[Literal["in-memory", "24h"]], Omit
        ] = omit,
        reasoning: Union[Optional[Reasoning], Omit] = omit,
        safety_identifier: Union[str, Omit] = omit,
        service_tier: Union[
            Optional[Literal["auto", "default", "flex", "scale", "priority"]], Omit
        ] = omit,
        store: Union[Optional[bool], Omit] = omit,
        stream_options: Union[
            Optional[response_create_params.StreamOptions], Omit
        ] = omit,
        temperature: Union[Optional[float], Omit] = omit,
        text: Union[ResponseTextConfigParam, Omit] = omit,
        tool_choice: Union[response_create_params.ToolChoice, Omit] = omit,
        tools: Union[Iterable[ToolParam], Omit] = omit,
        top_logprobs: Union[Optional[int], Omit] = omit,
        top_p: Union[Optional[float], Omit] = omit,
        truncation: Union[Optional[Literal["auto", "disabled"]], Omit] = omit,
        user: Union[str, Omit] = omit,
        **kwargs,
    ) -> Union[Response, Stream[ResponseStreamEvent]]:
        ...

    def create(
        self,
        *,
        background: Union[Optional[bool], Omit] = omit,
        context_management: Union[
            Optional[Iterable[response_create_params.ContextManagement]], Omit
        ] = omit,
        conversation: Union[Optional[response_create_params.Conversation], Omit] = omit,
        include: Union[Optional[List[ResponseIncludable]], Omit] = omit,
        input: Union[str, ResponseInputParam, Omit] = omit,
        instructions: Union[Optional[str], Omit] = omit,
        max_output_tokens: Union[Optional[int], Omit] = omit,
        max_tool_calls: Union[Optional[int], Omit] = omit,
        metadata: Union[Optional[Metadata], Omit] = omit,
        model: Union[ResponsesModel, Omit] = omit,
        parallel_tool_calls: Union[Optional[bool], Omit] = omit,
        previous_response_id: Union[Optional[str], Omit] = omit,
        prompt: Union[Optional[ResponsePromptParam], Omit] = omit,
        prompt_cache_key: Union[str, Omit] = omit,
        prompt_cache_retention: Union[
            Optional[Literal["in-memory", "24h"]], Omit
        ] = omit,
        reasoning: Union[Optional[Reasoning], Omit] = omit,
        safety_identifier: Union[str, Omit] = omit,
        service_tier: Union[
            Optional[Literal["auto", "default", "flex", "scale", "priority"]], Omit
        ] = omit,
        store: Union[Optional[bool], Omit] = omit,
        stream: Union[Optional[Literal[False]], Literal[True], Omit] = omit,
        stream_options: Union[
            Optional[response_create_params.StreamOptions], Omit
        ] = omit,
        temperature: Union[Optional[float], Omit] = omit,
        text: Union[ResponseTextConfigParam, Omit] = omit,
        tool_choice: Union[response_create_params.ToolChoice, Omit] = omit,
        tools: Union[Iterable[ToolParam], Omit] = omit,
        top_logprobs: Union[Optional[int], Omit] = omit,
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
            background=background,
            context_management=context_management,
            conversation=conversation,
            include=include,
            input=input,
            instructions=instructions,
            max_output_tokens=max_output_tokens,
            max_tool_calls=max_tool_calls,
            metadata=metadata,
            model=model,
            parallel_tool_calls=parallel_tool_calls,
            previous_response_id=previous_response_id,
            prompt=prompt,
            prompt_cache_key=prompt_cache_key,
            prompt_cache_retention=prompt_cache_retention,
            reasoning=reasoning,
            safety_identifier=safety_identifier,
            service_tier=service_tier,
            store=store,
            stream=stream,  # type: ignore[arg-type]
            stream_options=stream_options,
            temperature=temperature,
            text=text,
            tool_choice=tool_choice,
            tools=tools,
            top_logprobs=top_logprobs,
            top_p=top_p,
            truncation=truncation,
            user=user,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body={**(extra_body or {}), **kwargs},
            timeout=timeout,
        )

    @overload
    def retrieve(
        self,
        response_id: str,
        *,
        include: Union[List[ResponseIncludable], Omit] = omit,
        include_obfuscation: Union[bool, Omit] = omit,
        starting_after: Union[int, Omit] = omit,
        stream: Union[Literal[False], Omit] = omit,
        **kwargs,
    ) -> ResponseType:
        ...

    @overload
    def retrieve(
        self,
        response_id: str,
        *,
        stream: Literal[True],
        include: Union[List[ResponseIncludable], Omit] = omit,
        include_obfuscation: Union[bool, Omit] = omit,
        starting_after: Union[int, Omit] = omit,
        **kwargs,
    ) -> Stream[ResponseStreamEvent]:
        ...

    @overload
    def retrieve(
        self,
        response_id: str,
        *,
        stream: bool,
        include: Union[List[ResponseIncludable], Omit] = omit,
        include_obfuscation: Union[bool, Omit] = omit,
        starting_after: Union[int, Omit] = omit,
        **kwargs,
    ) -> Union[ResponseType, Stream[ResponseStreamEvent]]:
        ...

    def retrieve(
        self,
        response_id: str,
        *,
        include: Union[List[ResponseIncludable], Omit] = omit,
        include_obfuscation: Union[bool, Omit] = omit,
        starting_after: Union[int, Omit] = omit,
        stream: Union[Literal[False], Literal[True], Omit] = omit,
        **kwargs,
    ) -> Union[ResponseType, Stream[ResponseStreamEvent]]:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)

        if stream is True:
            return self.openai_client.responses.retrieve(
                response_id=response_id,
                stream=stream,
                include=include,
                include_obfuscation=include_obfuscation,
                starting_after=starting_after,
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body={**(extra_body or {}), **kwargs},
                timeout=timeout,
            )

        response = self.openai_client.with_raw_response.responses.retrieve(
            response_id=response_id,
            include=include,
            include_obfuscation=include_obfuscation,
            starting_after=starting_after,
            stream=stream,
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

    @overload
    def stream(
        self,
        *,
        response_id: str,
        text_format: Union[Type[TextFormatT], Omit] = omit,
        starting_after: Union[int, Omit] = omit,
        tools: Union[Iterable[ParseableToolParam], Omit] = omit,
        **kwargs,
    ) -> ResponseStreamManager[TextFormatT]:
        ...

    @overload
    def stream(
        self,
        *,
        input: Union[str, ResponseInputParam],
        model: ResponsesModel,
        background: Union[Optional[bool], Omit] = omit,
        context_management: Union[
            Optional[Iterable[response_create_params.ContextManagement]], Omit
        ] = omit,
        text_format: Union[Type[TextFormatT], Omit] = omit,
        tools: Union[Iterable[ParseableToolParam], Omit] = omit,
        conversation: Union[Optional[response_create_params.Conversation], Omit] = omit,
        include: Union[Optional[List[ResponseIncludable]], Omit] = omit,
        instructions: Union[Optional[str], Omit] = omit,
        max_output_tokens: Union[Optional[int], Omit] = omit,
        max_tool_calls: Union[Optional[int], Omit] = omit,
        metadata: Union[Optional[Metadata], Omit] = omit,
        parallel_tool_calls: Union[Optional[bool], Omit] = omit,
        previous_response_id: Union[Optional[str], Omit] = omit,
        prompt: Union[Optional[ResponsePromptParam], Omit] = omit,
        prompt_cache_key: Union[str, Omit] = omit,
        prompt_cache_retention: Union[
            Optional[Literal["in-memory", "24h"]], Omit
        ] = omit,
        reasoning: Union[Optional[Reasoning], Omit] = omit,
        safety_identifier: Union[str, Omit] = omit,
        service_tier: Union[
            Optional[Literal["auto", "default", "flex", "scale", "priority"]], Omit
        ] = omit,
        store: Union[Optional[bool], Omit] = omit,
        stream_options: Union[
            Optional[response_create_params.StreamOptions], Omit
        ] = omit,
        temperature: Union[Optional[float], Omit] = omit,
        text: Union[ResponseTextConfigParam, Omit] = omit,
        tool_choice: Union[response_create_params.ToolChoice, Omit] = omit,
        top_logprobs: Union[Optional[int], Omit] = omit,
        top_p: Union[Optional[float], Omit] = omit,
        truncation: Union[Optional[Literal["auto", "disabled"]], Omit] = omit,
        user: Union[str, Omit] = omit,
        **kwargs,
    ) -> ResponseStreamManager[TextFormatT]:
        ...

    def stream(
        self,
        *,
        response_id: Union[str, Omit] = omit,
        input: Union[str, ResponseInputParam, Omit] = omit,
        model: Union[ResponsesModel, Omit] = omit,
        background: Union[Optional[bool], Omit] = omit,
        context_management: Union[
            Optional[Iterable[response_create_params.ContextManagement]], Omit
        ] = omit,
        text_format: Union[Type[TextFormatT], Omit] = omit,
        tools: Union[Iterable[ParseableToolParam], Omit] = omit,
        conversation: Union[Optional[response_create_params.Conversation], Omit] = omit,
        include: Union[Optional[List[ResponseIncludable]], Omit] = omit,
        instructions: Union[Optional[str], Omit] = omit,
        max_output_tokens: Union[Optional[int], Omit] = omit,
        max_tool_calls: Union[Optional[int], Omit] = omit,
        metadata: Union[Optional[Metadata], Omit] = omit,
        parallel_tool_calls: Union[Optional[bool], Omit] = omit,
        previous_response_id: Union[Optional[str], Omit] = omit,
        prompt: Union[Optional[ResponsePromptParam], Omit] = omit,
        prompt_cache_key: Union[str, Omit] = omit,
        prompt_cache_retention: Union[
            Optional[Literal["in-memory", "24h"]], Omit
        ] = omit,
        reasoning: Union[Optional[Reasoning], Omit] = omit,
        safety_identifier: Union[str, Omit] = omit,
        service_tier: Union[
            Optional[Literal["auto", "default", "flex", "scale", "priority"]], Omit
        ] = omit,
        store: Union[Optional[bool], Omit] = omit,
        stream_options: Union[
            Optional[response_create_params.StreamOptions], Omit
        ] = omit,
        temperature: Union[Optional[float], Omit] = omit,
        text: Union[ResponseTextConfigParam, Omit] = omit,
        tool_choice: Union[response_create_params.ToolChoice, Omit] = omit,
        top_logprobs: Union[Optional[int], Omit] = omit,
        top_p: Union[Optional[float], Omit] = omit,
        truncation: Union[Optional[Literal["auto", "disabled"]], Omit] = omit,
        user: Union[str, Omit] = omit,
        starting_after: Union[int, Omit] = omit,
        **kwargs,
    ) -> ResponseStreamManager[TextFormatT]:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)
        return self.openai_client.responses.stream(  # type: ignore[call-overload, misc]
            response_id=response_id,
            input=input,
            model=model,
            background=background,
            context_management=context_management,
            text_format=text_format,
            tools=tools,
            conversation=conversation,
            include=include,
            instructions=instructions,
            max_output_tokens=max_output_tokens,
            max_tool_calls=max_tool_calls,
            metadata=metadata,
            parallel_tool_calls=parallel_tool_calls,
            previous_response_id=previous_response_id,
            prompt=prompt,
            prompt_cache_key=prompt_cache_key,
            prompt_cache_retention=prompt_cache_retention,
            reasoning=reasoning,
            safety_identifier=safety_identifier,
            service_tier=service_tier,
            store=store,
            stream_options=stream_options,
            temperature=temperature,
            text=text,
            tool_choice=tool_choice,
            top_logprobs=top_logprobs,
            top_p=top_p,
            truncation=truncation,
            user=user,
            starting_after=starting_after,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body={**(extra_body or {}), **kwargs},
            timeout=timeout,
        )

    def parse(
        self,
        *,
        text_format: Union[Type[TextFormatT], Omit] = omit,
        background: Union[Optional[bool], Omit] = omit,
        context_management: Union[
            Optional[Iterable[response_create_params.ContextManagement]], Omit
        ] = omit,
        conversation: Union[Optional[response_create_params.Conversation], Omit] = omit,
        include: Union[Optional[List[ResponseIncludable]], Omit] = omit,
        input: Union[str, ResponseInputParam, Omit] = omit,
        instructions: Union[Optional[str], Omit] = omit,
        max_output_tokens: Union[Optional[int], Omit] = omit,
        max_tool_calls: Union[Optional[int], Omit] = omit,
        metadata: Union[Optional[Metadata], Omit] = omit,
        model: Union[ResponsesModel, Omit] = omit,
        parallel_tool_calls: Union[Optional[bool], Omit] = omit,
        previous_response_id: Union[Optional[str], Omit] = omit,
        prompt: Union[Optional[ResponsePromptParam], Omit] = omit,
        prompt_cache_key: Union[str, Omit] = omit,
        prompt_cache_retention: Union[
            Optional[Literal["in-memory", "24h"]], Omit
        ] = omit,
        reasoning: Union[Optional[Reasoning], Omit] = omit,
        safety_identifier: Union[str, Omit] = omit,
        service_tier: Union[
            Optional[Literal["auto", "default", "flex", "scale", "priority"]], Omit
        ] = omit,
        store: Union[Optional[bool], Omit] = omit,
        stream: Union[Optional[Literal[False]], Literal[True], Omit] = omit,
        stream_options: Union[
            Optional[response_create_params.StreamOptions], Omit
        ] = omit,
        temperature: Union[Optional[float], Omit] = omit,
        text: Union[ResponseTextConfigParam, Omit] = omit,
        tool_choice: Union[response_create_params.ToolChoice, Omit] = omit,
        tools: Union[Iterable[ParseableToolParam], Omit] = omit,
        top_logprobs: Union[Optional[int], Omit] = omit,
        top_p: Union[Optional[float], Omit] = omit,
        truncation: Union[Optional[Literal["auto", "disabled"]], Omit] = omit,
        user: Union[str, Omit] = omit,
        verbosity: Union[Optional[Literal["low", "medium", "high"]], Omit] = omit,
        **kwargs,
    ) -> ParsedResponse[TextFormatT]:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)

        return self.openai_client.responses.parse(
            text_format=text_format,
            background=background,
            context_management=context_management,
            conversation=conversation,
            input=input,
            model=model,
            tools=tools,
            include=include,
            instructions=instructions,
            max_output_tokens=max_output_tokens,
            max_tool_calls=max_tool_calls,
            metadata=metadata,
            parallel_tool_calls=parallel_tool_calls,
            previous_response_id=previous_response_id,
            prompt=prompt,
            prompt_cache_key=prompt_cache_key,
            prompt_cache_retention=prompt_cache_retention,
            reasoning=reasoning,
            safety_identifier=safety_identifier,
            service_tier=service_tier,
            store=store,
            stream=stream,
            stream_options=stream_options,
            temperature=temperature,
            text=text,
            tool_choice=tool_choice,
            top_logprobs=top_logprobs,
            top_p=top_p,
            truncation=truncation,
            user=user,
            verbosity=verbosity,
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
        model: Union[
            Literal[
                "gpt-5.4",
                "gpt-5.4-mini",
                "gpt-5.4-nano",
                "gpt-5.4-mini-2026-03-17",
                "gpt-5.4-nano-2026-03-17",
                "gpt-5.3-chat-latest",
                "gpt-5.2",
                "gpt-5.2-2025-12-11",
                "gpt-5.2-chat-latest",
                "gpt-5.2-pro",
                "gpt-5.2-pro-2025-12-11",
                "gpt-5.1",
                "gpt-5.1-2025-11-13",
                "gpt-5.1-codex",
                "gpt-5.1-mini",
                "gpt-5.1-chat-latest",
                "gpt-5",
                "gpt-5-mini",
                "gpt-5-nano",
                "gpt-5-2025-08-07",
                "gpt-5-mini-2025-08-07",
                "gpt-5-nano-2025-08-07",
                "gpt-5-chat-latest",
                "gpt-4.1",
                "gpt-4.1-mini",
                "gpt-4.1-nano",
                "gpt-4.1-2025-04-14",
                "gpt-4.1-mini-2025-04-14",
                "gpt-4.1-nano-2025-04-14",
                "o4-mini",
                "o4-mini-2025-04-16",
                "o3",
                "o3-2025-04-16",
                "o3-mini",
                "o3-mini-2025-01-31",
                "o1",
                "o1-2024-12-17",
                "o1-preview",
                "o1-preview-2024-09-12",
                "o1-mini",
                "o1-mini-2024-09-12",
                "gpt-4o",
                "gpt-4o-2024-11-20",
                "gpt-4o-2024-08-06",
                "gpt-4o-2024-05-13",
                "gpt-4o-audio-preview",
                "gpt-4o-audio-preview-2024-10-01",
                "gpt-4o-audio-preview-2024-12-17",
                "gpt-4o-audio-preview-2025-06-03",
                "gpt-4o-mini-audio-preview",
                "gpt-4o-mini-audio-preview-2024-12-17",
                "gpt-4o-search-preview",
                "gpt-4o-mini-search-preview",
                "gpt-4o-search-preview-2025-03-11",
                "gpt-4o-mini-search-preview-2025-03-11",
                "chatgpt-4o-latest",
                "codex-mini-latest",
                "gpt-4o-mini",
                "gpt-4o-mini-2024-07-18",
                "gpt-4-turbo",
                "gpt-4-turbo-2024-04-09",
                "gpt-4-0125-preview",
                "gpt-4-turbo-preview",
                "gpt-4-1106-preview",
                "gpt-4-vision-preview",
                "gpt-4",
                "gpt-4-0314",
                "gpt-4-0613",
                "gpt-4-32k",
                "gpt-4-32k-0314",
                "gpt-4-32k-0613",
                "gpt-3.5-turbo",
                "gpt-3.5-turbo-16k",
                "gpt-3.5-turbo-0301",
                "gpt-3.5-turbo-0613",
                "gpt-3.5-turbo-1106",
                "gpt-3.5-turbo-0125",
                "gpt-3.5-turbo-16k-0613",
                "o1-pro",
                "o1-pro-2025-03-19",
                "o3-pro",
                "o3-pro-2025-06-10",
                "o3-deep-research",
                "o3-deep-research-2025-06-26",
                "o4-mini-deep-research",
                "o4-mini-deep-research-2025-06-26",
                "computer-use-preview",
                "computer-use-preview-2025-03-11",
                "gpt-5-codex",
                "gpt-5-pro",
                "gpt-5-pro-2025-10-06",
                "gpt-5.1-codex-max",
            ],
            str,
            None,
        ],
        input: Union[str, Iterable[ResponseInputItemParam], None, Omit] = omit,
        instructions: Union[Optional[str], Omit] = omit,
        previous_response_id: Union[Optional[str], Omit] = omit,
        prompt_cache_key: Union[Optional[str], Omit] = omit,
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
            prompt_cache_key=prompt_cache_key,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body={**(extra_body or {}), **kwargs},
            timeout=timeout,
        )
        data = CompactedResponse(**json.loads(response.text))
        data._headers = response.headers
        return data

    def connect(
        self,
        *,
        websocket_connection_options: WebSocketConnectionOptions = {},
        **kwargs,
    ) -> ResponsesConnectionManager:
        return self.openai_client.responses.connect(
            websocket_connection_options=websocket_connection_options,
            extra_headers=self.openai_client.default_headers,
            **kwargs,
        )


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
        background: Union[Optional[bool], Omit] = omit,
        context_management: Union[
            Optional[Iterable[response_create_params.ContextManagement]], Omit
        ] = omit,
        conversation: Union[Optional[response_create_params.Conversation], Omit] = omit,
        include: Union[Optional[List[ResponseIncludable]], Omit] = omit,
        input: Union[str, ResponseInputParam, Omit] = omit,
        instructions: Union[Optional[str], Omit] = omit,
        max_output_tokens: Union[Optional[int], Omit] = omit,
        max_tool_calls: Union[Optional[int], Omit] = omit,
        metadata: Union[Optional[Metadata], Omit] = omit,
        model: Union[ResponsesModel, Omit] = omit,
        parallel_tool_calls: Union[Optional[bool], Omit] = omit,
        previous_response_id: Union[Optional[str], Omit] = omit,
        prompt: Union[Optional[ResponsePromptParam], Omit] = omit,
        prompt_cache_key: Union[str, Omit] = omit,
        prompt_cache_retention: Union[
            Optional[Literal["in-memory", "24h"]], Omit
        ] = omit,
        reasoning: Union[Optional[Reasoning], Omit] = omit,
        safety_identifier: Union[str, Omit] = omit,
        service_tier: Union[
            Optional[Literal["auto", "default", "flex", "scale", "priority"]], Omit
        ] = omit,
        store: Union[Optional[bool], Omit] = omit,
        stream: Union[Literal[False], Omit] = omit,
        stream_options: Union[
            Optional[response_create_params.StreamOptions], Omit
        ] = omit,
        temperature: Union[Optional[float], Omit] = omit,
        text: Union[ResponseTextConfigParam, Omit] = omit,
        tool_choice: Union[response_create_params.ToolChoice, Omit] = omit,
        tools: Union[Iterable[ToolParam], Omit] = omit,
        top_logprobs: Union[Optional[int], Omit] = omit,
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
        stream: Literal[True],
        background: Union[Optional[bool], Omit] = omit,
        context_management: Union[
            Optional[Iterable[response_create_params.ContextManagement]], Omit
        ] = omit,
        conversation: Union[Optional[response_create_params.Conversation], Omit] = omit,
        include: Union[Optional[List[ResponseIncludable]], Omit] = omit,
        input: Union[str, ResponseInputParam, Omit] = omit,
        instructions: Union[Optional[str], Omit] = omit,
        max_output_tokens: Union[Optional[int], Omit] = omit,
        max_tool_calls: Union[Optional[int], Omit] = omit,
        metadata: Union[Optional[Metadata], Omit] = omit,
        model: Union[ResponsesModel, Omit] = omit,
        parallel_tool_calls: Union[Optional[bool], Omit] = omit,
        previous_response_id: Union[Optional[str], Omit] = omit,
        prompt: Union[Optional[ResponsePromptParam], Omit] = omit,
        prompt_cache_key: Union[str, Omit] = omit,
        prompt_cache_retention: Union[
            Optional[Literal["in-memory", "24h"]], Omit
        ] = omit,
        reasoning: Union[Optional[Reasoning], Omit] = omit,
        safety_identifier: Union[str, Omit] = omit,
        service_tier: Union[
            Optional[Literal["auto", "default", "flex", "scale", "priority"]], Omit
        ] = omit,
        store: Union[Optional[bool], Omit] = omit,
        stream_options: Union[
            Optional[response_create_params.StreamOptions], Omit
        ] = omit,
        temperature: Union[Optional[float], Omit] = omit,
        text: Union[ResponseTextConfigParam, Omit] = omit,
        tool_choice: Union[response_create_params.ToolChoice, Omit] = omit,
        tools: Union[Iterable[ToolParam], Omit] = omit,
        top_logprobs: Union[Optional[int], Omit] = omit,
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
        stream: bool,
        background: Union[Optional[bool], Omit] = omit,
        context_management: Union[
            Optional[Iterable[response_create_params.ContextManagement]], Omit
        ] = omit,
        conversation: Union[Optional[response_create_params.Conversation], Omit] = omit,
        include: Union[Optional[List[ResponseIncludable]], Omit] = omit,
        input: Union[str, ResponseInputParam, Omit] = omit,
        instructions: Union[Optional[str], Omit] = omit,
        max_output_tokens: Union[Optional[int], Omit] = omit,
        max_tool_calls: Union[Optional[int], Omit] = omit,
        metadata: Union[Optional[Metadata], Omit] = omit,
        model: Union[ResponsesModel, Omit] = omit,
        parallel_tool_calls: Union[Optional[bool], Omit] = omit,
        previous_response_id: Union[Optional[str], Omit] = omit,
        prompt: Union[Optional[ResponsePromptParam], Omit] = omit,
        prompt_cache_key: Union[str, Omit] = omit,
        prompt_cache_retention: Union[
            Optional[Literal["in-memory", "24h"]], Omit
        ] = omit,
        reasoning: Union[Optional[Reasoning], Omit] = omit,
        safety_identifier: Union[str, Omit] = omit,
        service_tier: Union[
            Optional[Literal["auto", "default", "flex", "scale", "priority"]], Omit
        ] = omit,
        store: Union[Optional[bool], Omit] = omit,
        stream_options: Union[
            Optional[response_create_params.StreamOptions], Omit
        ] = omit,
        temperature: Union[Optional[float], Omit] = omit,
        text: Union[ResponseTextConfigParam, Omit] = omit,
        tool_choice: Union[response_create_params.ToolChoice, Omit] = omit,
        tools: Union[Iterable[ToolParam], Omit] = omit,
        top_logprobs: Union[Optional[int], Omit] = omit,
        top_p: Union[Optional[float], Omit] = omit,
        truncation: Union[Optional[Literal["auto", "disabled"]], Omit] = omit,
        user: Union[str, Omit] = omit,
        **kwargs,
    ) -> Union[Response, AsyncStream[ResponseStreamEvent]]:
        ...

    async def create(
        self,
        *,
        background: Union[Optional[bool], Omit] = omit,
        context_management: Union[
            Optional[Iterable[response_create_params.ContextManagement]], Omit
        ] = omit,
        conversation: Union[Optional[response_create_params.Conversation], Omit] = omit,
        include: Union[Optional[List[ResponseIncludable]], Omit] = omit,
        input: Union[str, ResponseInputParam, Omit] = omit,
        instructions: Union[Optional[str], Omit] = omit,
        max_output_tokens: Union[Optional[int], Omit] = omit,
        max_tool_calls: Union[Optional[int], Omit] = omit,
        metadata: Union[Optional[Metadata], Omit] = omit,
        model: Union[ResponsesModel, Omit] = omit,
        parallel_tool_calls: Union[Optional[bool], Omit] = omit,
        previous_response_id: Union[Optional[str], Omit] = omit,
        prompt: Union[Optional[ResponsePromptParam], Omit] = omit,
        prompt_cache_key: Union[str, Omit] = omit,
        prompt_cache_retention: Union[
            Optional[Literal["in-memory", "24h"]], Omit
        ] = omit,
        reasoning: Union[Optional[Reasoning], Omit] = omit,
        safety_identifier: Union[str, Omit] = omit,
        service_tier: Union[
            Optional[Literal["auto", "default", "flex", "scale", "priority"]], Omit
        ] = omit,
        store: Union[Optional[bool], Omit] = omit,
        stream: Union[Optional[Literal[False]], Literal[True], Omit] = omit,
        stream_options: Union[
            Optional[response_create_params.StreamOptions], Omit
        ] = omit,
        temperature: Union[Optional[float], Omit] = omit,
        text: Union[ResponseTextConfigParam, Omit] = omit,
        tool_choice: Union[response_create_params.ToolChoice, Omit] = omit,
        tools: Union[Iterable[ToolParam], Omit] = omit,
        top_logprobs: Union[Optional[int], Omit] = omit,
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
            background=background,
            context_management=context_management,
            conversation=conversation,
            include=include,
            input=input,
            instructions=instructions,
            max_output_tokens=max_output_tokens,
            max_tool_calls=max_tool_calls,
            metadata=metadata,
            model=model,
            parallel_tool_calls=parallel_tool_calls,
            previous_response_id=previous_response_id,
            prompt=prompt,
            prompt_cache_key=prompt_cache_key,
            prompt_cache_retention=prompt_cache_retention,
            reasoning=reasoning,
            safety_identifier=safety_identifier,
            service_tier=service_tier,
            store=store,
            stream=stream,  # type: ignore[arg-type]
            stream_options=stream_options,
            temperature=temperature,
            text=text,
            tool_choice=tool_choice,
            tools=tools,
            top_logprobs=top_logprobs,
            top_p=top_p,
            truncation=truncation,
            user=user,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body={**(extra_body or {}), **kwargs},
            timeout=timeout,
        )

    @overload
    async def retrieve(
        self,
        response_id: str,
        *,
        include: Union[List[ResponseIncludable], Omit] = omit,
        include_obfuscation: Union[bool, Omit] = omit,
        starting_after: Union[int, Omit] = omit,
        stream: Union[Literal[False], Omit] = omit,
        **kwargs,
    ) -> ResponseType:
        ...

    @overload
    async def retrieve(
        self,
        response_id: str,
        *,
        stream: Literal[True],
        include: Union[List[ResponseIncludable], Omit] = omit,
        include_obfuscation: Union[bool, Omit] = omit,
        starting_after: Union[int, Omit] = omit,
        **kwargs,
    ) -> AsyncStream[ResponseStreamEvent]:
        ...

    @overload
    async def retrieve(
        self,
        response_id: str,
        *,
        stream: bool,
        include: Union[List[ResponseIncludable], Omit] = omit,
        include_obfuscation: Union[bool, Omit] = omit,
        starting_after: Union[int, Omit] = omit,
        **kwargs,
    ) -> Union[ResponseType, AsyncStream[ResponseStreamEvent]]:
        ...

    async def retrieve(
        self,
        response_id: str,
        *,
        include: Union[List[ResponseIncludable], Omit] = omit,
        include_obfuscation: Union[bool, Omit] = omit,
        starting_after: Union[int, Omit] = omit,
        stream: Union[Literal[False], Literal[True], Omit] = omit,
        **kwargs,
    ) -> Union[ResponseType, AsyncStream[ResponseStreamEvent]]:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)

        if stream is True:
            return await self.openai_client.responses.retrieve(
                response_id=response_id,
                stream=stream,
                include=include,
                include_obfuscation=include_obfuscation,
                starting_after=starting_after,
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body={**(extra_body or {}), **kwargs},
                timeout=timeout,
            )

        response = await self.openai_client.with_raw_response.responses.retrieve(
            response_id=response_id,
            include=include,
            include_obfuscation=include_obfuscation,
            starting_after=starting_after,
            stream=stream,
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

    @overload
    def stream(
        self,
        *,
        response_id: str,
        text_format: Union[Type[TextFormatT], Omit] = omit,
        starting_after: Union[int, Omit] = omit,
        tools: Union[Iterable[ParseableToolParam], Omit] = omit,
        **kwargs,
    ) -> AsyncResponseStreamManager[TextFormatT]:
        ...

    @overload
    def stream(
        self,
        *,
        input: Union[str, ResponseInputParam],
        model: Union[str, ChatModel],
        background: Union[Optional[bool], Omit] = omit,
        context_management: Union[
            Optional[Iterable[response_create_params.ContextManagement]], Omit
        ] = omit,
        text_format: Union[Type[TextFormatT], Omit] = omit,
        tools: Union[Iterable[ParseableToolParam], Omit] = omit,
        conversation: Union[Optional[response_create_params.Conversation], Omit] = omit,
        include: Union[Optional[List[ResponseIncludable]], Omit] = omit,
        instructions: Union[Optional[str], Omit] = omit,
        max_output_tokens: Union[Optional[int], Omit] = omit,
        max_tool_calls: Union[Optional[int], Omit] = omit,
        metadata: Union[Optional[Metadata], Omit] = omit,
        parallel_tool_calls: Union[Optional[bool], Omit] = omit,
        previous_response_id: Union[Optional[str], Omit] = omit,
        prompt: Union[Optional[ResponsePromptParam], Omit] = omit,
        prompt_cache_key: Union[str, Omit] = omit,
        prompt_cache_retention: Union[
            Optional[Literal["in-memory", "24h"]], Omit
        ] = omit,
        reasoning: Union[Optional[Reasoning], Omit] = omit,
        safety_identifier: Union[str, Omit] = omit,
        service_tier: Union[
            Optional[Literal["auto", "default", "flex", "scale", "priority"]], Omit
        ] = omit,
        store: Union[Optional[bool], Omit] = omit,
        stream_options: Union[
            Optional[response_create_params.StreamOptions], Omit
        ] = omit,
        temperature: Union[Optional[float], Omit] = omit,
        text: Union[ResponseTextConfigParam, Omit] = omit,
        tool_choice: Union[response_create_params.ToolChoice, Omit] = omit,
        top_logprobs: Union[Optional[int], Omit] = omit,
        top_p: Union[Optional[float], Omit] = omit,
        truncation: Union[Optional[Literal["auto", "disabled"]], Omit] = omit,
        user: Union[str, Omit] = omit,
        **kwargs,
    ) -> AsyncResponseStreamManager[TextFormatT]:
        ...

    def stream(
        self,
        *,
        response_id: Union[str, Omit] = omit,
        input: Union[str, ResponseInputParam, Omit] = omit,
        model: Union[str, ChatModel, Omit] = omit,
        background: Union[Optional[bool], Omit] = omit,
        context_management: Union[
            Optional[Iterable[response_create_params.ContextManagement]], Omit
        ] = omit,
        text_format: Union[Type[TextFormatT], Omit] = omit,
        tools: Union[Iterable[ParseableToolParam], Omit] = omit,
        conversation: Union[Optional[response_create_params.Conversation], Omit] = omit,
        include: Union[Optional[List[ResponseIncludable]], Omit] = omit,
        instructions: Union[Optional[str], Omit] = omit,
        max_output_tokens: Union[Optional[int], Omit] = omit,
        max_tool_calls: Union[Optional[int], Omit] = omit,
        metadata: Union[Optional[Metadata], Omit] = omit,
        parallel_tool_calls: Union[Optional[bool], Omit] = omit,
        previous_response_id: Union[Optional[str], Omit] = omit,
        prompt: Union[Optional[ResponsePromptParam], Omit] = omit,
        prompt_cache_key: Union[str, Omit] = omit,
        prompt_cache_retention: Union[
            Optional[Literal["in-memory", "24h"]], Omit
        ] = omit,
        reasoning: Union[Optional[Reasoning], Omit] = omit,
        safety_identifier: Union[str, Omit] = omit,
        service_tier: Union[
            Optional[Literal["auto", "default", "flex", "scale", "priority"]], Omit
        ] = omit,
        store: Union[Optional[bool], Omit] = omit,
        stream_options: Union[
            Optional[response_create_params.StreamOptions], Omit
        ] = omit,
        temperature: Union[Optional[float], Omit] = omit,
        text: Union[ResponseTextConfigParam, Omit] = omit,
        tool_choice: Union[response_create_params.ToolChoice, Omit] = omit,
        top_logprobs: Union[Optional[int], Omit] = omit,
        top_p: Union[Optional[float], Omit] = omit,
        truncation: Union[Optional[Literal["auto", "disabled"]], Omit] = omit,
        user: Union[str, Omit] = omit,
        starting_after: Union[int, Omit] = omit,
        **kwargs,
    ) -> AsyncResponseStreamManager[TextFormatT]:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)
        return self.openai_client.responses.stream(  # type: ignore[call-overload, misc]
            response_id=response_id,
            input=input,
            model=model,
            background=background,
            context_management=context_management,
            text_format=text_format,
            tools=tools,
            conversation=conversation,
            include=include,
            instructions=instructions,
            max_output_tokens=max_output_tokens,
            max_tool_calls=max_tool_calls,
            metadata=metadata,
            parallel_tool_calls=parallel_tool_calls,
            previous_response_id=previous_response_id,
            prompt=prompt,
            prompt_cache_key=prompt_cache_key,
            prompt_cache_retention=prompt_cache_retention,
            reasoning=reasoning,
            safety_identifier=safety_identifier,
            service_tier=service_tier,
            store=store,
            stream_options=stream_options,
            temperature=temperature,
            text=text,
            tool_choice=tool_choice,
            top_logprobs=top_logprobs,
            top_p=top_p,
            truncation=truncation,
            user=user,
            starting_after=starting_after,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body={**(extra_body or {}), **kwargs},
            timeout=timeout,
        )

    async def parse(
        self,
        *,
        background: Union[Optional[bool], Omit] = omit,
        context_management: Union[
            Optional[Iterable[response_create_params.ContextManagement]], Omit
        ] = omit,
        conversation: Union[Optional[response_create_params.Conversation], Omit] = omit,
        input: Union[str, ResponseInputParam, Omit] = omit,
        model: Union[ResponsesModel, Omit] = omit,
        text_format: Union[Type[TextFormatT], Omit] = omit,
        tools: Union[Iterable[ParseableToolParam], Omit] = omit,
        include: Union[Optional[List[ResponseIncludable]], Omit] = omit,
        instructions: Union[Optional[str], Omit] = omit,
        max_output_tokens: Union[Optional[int], Omit] = omit,
        max_tool_calls: Union[Optional[int], Omit] = omit,
        metadata: Union[Optional[Metadata], Omit] = omit,
        parallel_tool_calls: Union[Optional[bool], Omit] = omit,
        previous_response_id: Union[Optional[str], Omit] = omit,
        prompt: Union[Optional[ResponsePromptParam], Omit] = omit,
        prompt_cache_key: Union[str, Omit] = omit,
        prompt_cache_retention: Union[
            Optional[Literal["in-memory", "24h"]], Omit
        ] = omit,
        reasoning: Union[Optional[Reasoning], Omit] = omit,
        safety_identifier: Union[str, Omit] = omit,
        service_tier: Union[
            Optional[Literal["auto", "default", "flex", "scale", "priority"]], Omit
        ] = omit,
        store: Union[Optional[bool], Omit] = omit,
        stream: Union[Optional[Literal[False]], Literal[True], Omit] = omit,
        stream_options: Union[
            Optional[response_create_params.StreamOptions], Omit
        ] = omit,
        temperature: Union[Optional[float], Omit] = omit,
        text: Union[ResponseTextConfigParam, Omit] = omit,
        tool_choice: Union[response_create_params.ToolChoice, Omit] = omit,
        top_logprobs: Union[Optional[int], Omit] = omit,
        top_p: Union[Optional[float], Omit] = omit,
        truncation: Union[Optional[Literal["auto", "disabled"]], Omit] = omit,
        user: Union[str, Omit] = omit,
        verbosity: Union[Optional[Literal["low", "medium", "high"]], Omit] = omit,
        **kwargs,
    ) -> ParsedResponse[TextFormatT]:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)

        return await self.openai_client.responses.parse(
            background=background,
            context_management=context_management,
            conversation=conversation,
            input=input,
            model=model,
            text_format=text_format,
            tools=tools,
            include=include,
            instructions=instructions,
            max_output_tokens=max_output_tokens,
            max_tool_calls=max_tool_calls,
            metadata=metadata,
            parallel_tool_calls=parallel_tool_calls,
            previous_response_id=previous_response_id,
            prompt=prompt,
            prompt_cache_key=prompt_cache_key,
            prompt_cache_retention=prompt_cache_retention,
            reasoning=reasoning,
            safety_identifier=safety_identifier,
            service_tier=service_tier,
            store=store,
            stream=stream,
            stream_options=stream_options,
            temperature=temperature,
            text=text,
            tool_choice=tool_choice,
            top_logprobs=top_logprobs,
            top_p=top_p,
            truncation=truncation,
            user=user,
            verbosity=verbosity,
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
        model: Union[
            Literal[
                "gpt-5.4",
                "gpt-5.4-mini",
                "gpt-5.4-nano",
                "gpt-5.4-mini-2026-03-17",
                "gpt-5.4-nano-2026-03-17",
                "gpt-5.3-chat-latest",
                "gpt-5.2",
                "gpt-5.2-2025-12-11",
                "gpt-5.2-chat-latest",
                "gpt-5.2-pro",
                "gpt-5.2-pro-2025-12-11",
                "gpt-5.1",
                "gpt-5.1-2025-11-13",
                "gpt-5.1-codex",
                "gpt-5.1-mini",
                "gpt-5.1-chat-latest",
                "gpt-5",
                "gpt-5-mini",
                "gpt-5-nano",
                "gpt-5-2025-08-07",
                "gpt-5-mini-2025-08-07",
                "gpt-5-nano-2025-08-07",
                "gpt-5-chat-latest",
                "gpt-4.1",
                "gpt-4.1-mini",
                "gpt-4.1-nano",
                "gpt-4.1-2025-04-14",
                "gpt-4.1-mini-2025-04-14",
                "gpt-4.1-nano-2025-04-14",
                "o4-mini",
                "o4-mini-2025-04-16",
                "o3",
                "o3-2025-04-16",
                "o3-mini",
                "o3-mini-2025-01-31",
                "o1",
                "o1-2024-12-17",
                "o1-preview",
                "o1-preview-2024-09-12",
                "o1-mini",
                "o1-mini-2024-09-12",
                "gpt-4o",
                "gpt-4o-2024-11-20",
                "gpt-4o-2024-08-06",
                "gpt-4o-2024-05-13",
                "gpt-4o-audio-preview",
                "gpt-4o-audio-preview-2024-10-01",
                "gpt-4o-audio-preview-2024-12-17",
                "gpt-4o-audio-preview-2025-06-03",
                "gpt-4o-mini-audio-preview",
                "gpt-4o-mini-audio-preview-2024-12-17",
                "gpt-4o-search-preview",
                "gpt-4o-mini-search-preview",
                "gpt-4o-search-preview-2025-03-11",
                "gpt-4o-mini-search-preview-2025-03-11",
                "chatgpt-4o-latest",
                "codex-mini-latest",
                "gpt-4o-mini",
                "gpt-4o-mini-2024-07-18",
                "gpt-4-turbo",
                "gpt-4-turbo-2024-04-09",
                "gpt-4-0125-preview",
                "gpt-4-turbo-preview",
                "gpt-4-1106-preview",
                "gpt-4-vision-preview",
                "gpt-4",
                "gpt-4-0314",
                "gpt-4-0613",
                "gpt-4-32k",
                "gpt-4-32k-0314",
                "gpt-4-32k-0613",
                "gpt-3.5-turbo",
                "gpt-3.5-turbo-16k",
                "gpt-3.5-turbo-0301",
                "gpt-3.5-turbo-0613",
                "gpt-3.5-turbo-1106",
                "gpt-3.5-turbo-0125",
                "gpt-3.5-turbo-16k-0613",
                "o1-pro",
                "o1-pro-2025-03-19",
                "o3-pro",
                "o3-pro-2025-06-10",
                "o3-deep-research",
                "o3-deep-research-2025-06-26",
                "o4-mini-deep-research",
                "o4-mini-deep-research-2025-06-26",
                "computer-use-preview",
                "computer-use-preview-2025-03-11",
                "gpt-5-codex",
                "gpt-5-pro",
                "gpt-5-pro-2025-10-06",
                "gpt-5.1-codex-max",
            ],
            str,
            None,
        ],
        input: Union[str, Iterable[ResponseInputItemParam], None, Omit] = omit,
        instructions: Union[Optional[str], Omit] = omit,
        previous_response_id: Union[Optional[str], Omit] = omit,
        prompt_cache_key: Union[Optional[str], Omit] = omit,
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
            prompt_cache_key=prompt_cache_key,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body={**(extra_body or {}), **kwargs},
            timeout=timeout,
        )
        data = CompactedResponse(**json.loads(response.text))
        data._headers = response.headers
        return data

    def connect(
        self,
        *,
        websocket_connection_options: WebSocketConnectionOptions = {},
        **kwargs,
    ) -> AsyncResponsesConnectionManager:
        return self.openai_client.responses.connect(
            websocket_connection_options=websocket_connection_options,
            extra_headers=self.openai_client.default_headers,
            **kwargs,
        )


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
