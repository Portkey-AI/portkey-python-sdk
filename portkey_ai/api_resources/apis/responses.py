import json
from typing import Iterable, List, Literal, Optional, Union
from portkey_ai._vendor.openai._streaming import AsyncStream, Stream
from portkey_ai._vendor.openai.lib._parsing._responses import TextFormatT
from portkey_ai._vendor.openai.lib.streaming.responses._responses import (
    AsyncResponseStreamManager,
    ResponseStreamManager,
)
from portkey_ai._vendor.openai.types.responses import response_create_params
from portkey_ai._vendor.openai.types.responses.parsed_response import ParsedResponse
from portkey_ai._vendor.openai.types.responses.response_includable import (
    ResponseIncludable,
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
from portkey_ai.api_resources.types.response_type import Response as ResponseType
from portkey_ai.api_resources.types.responses_input_items_type import InputItemList
from portkey_ai.api_resources.types.shared_types import Metadata
from ..._vendor.openai._types import NotGiven, NOT_GIVEN
from typing_extensions import overload


class Responses(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.input_items = InputItems(client)

    @overload
    def create(
        self,
        *,
        input: Union[str, ResponseInputParam, NotGiven] = NOT_GIVEN,
        model: Union[ResponsesModel, NotGiven] = NOT_GIVEN,
        include: Union[Optional[List[ResponseIncludable]], NotGiven] = NOT_GIVEN,
        instructions: Union[Optional[str], NotGiven] = NOT_GIVEN,
        max_output_tokens: Union[Optional[int], NotGiven] = NOT_GIVEN,
        metadata: Union[Optional[Metadata], NotGiven] = NOT_GIVEN,
        parallel_tool_calls: Union[Optional[bool], NotGiven] = NOT_GIVEN,
        previous_response_id: Union[Optional[str], NotGiven] = NOT_GIVEN,
        reasoning: Union[Optional[Reasoning], NotGiven] = NOT_GIVEN,
        store: Union[Optional[bool], NotGiven] = NOT_GIVEN,
        stream: Union[Literal[False], NotGiven] = NOT_GIVEN,
        temperature: Union[Optional[float], NotGiven] = NOT_GIVEN,
        text: Union[ResponseTextConfigParam, NotGiven] = NOT_GIVEN,
        tool_choice: Union[response_create_params.ToolChoice, NotGiven] = NOT_GIVEN,
        tools: Union[Iterable[ToolParam], NotGiven] = NOT_GIVEN,
        top_p: Union[Optional[float], NotGiven] = NOT_GIVEN,
        truncation: Union[Optional[Literal["auto", "disabled"]], NotGiven] = NOT_GIVEN,
        user: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> Response:
        ...

    @overload
    def create(
        self,
        *,
        input: Union[str, ResponseInputParam, NotGiven] = NOT_GIVEN,
        model: Union[ResponsesModel, NotGiven] = NOT_GIVEN,
        stream: Literal[True],
        include: Union[Optional[List[ResponseIncludable]], NotGiven] = NOT_GIVEN,
        instructions: Union[Optional[str], NotGiven] = NOT_GIVEN,
        max_output_tokens: Union[Optional[int], NotGiven] = NOT_GIVEN,
        metadata: Union[Optional[Metadata], NotGiven] = NOT_GIVEN,
        parallel_tool_calls: Union[Optional[bool], NotGiven] = NOT_GIVEN,
        previous_response_id: Union[Optional[str], NotGiven] = NOT_GIVEN,
        reasoning: Union[Optional[Reasoning], NotGiven] = NOT_GIVEN,
        store: Union[Optional[bool], NotGiven] = NOT_GIVEN,
        temperature: Union[Optional[float], NotGiven] = NOT_GIVEN,
        text: Union[ResponseTextConfigParam, NotGiven] = NOT_GIVEN,
        tool_choice: Union[response_create_params.ToolChoice, NotGiven] = NOT_GIVEN,
        tools: Union[Iterable[ToolParam], NotGiven] = NOT_GIVEN,
        top_p: Union[Optional[float], NotGiven] = NOT_GIVEN,
        truncation: Union[Optional[Literal["auto", "disabled"]], NotGiven] = NOT_GIVEN,
        user: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> Stream[ResponseStreamEvent]:
        ...

    @overload
    def create(
        self,
        *,
        input: Union[str, ResponseInputParam, NotGiven] = NOT_GIVEN,
        model: Union[ResponsesModel, NotGiven] = NOT_GIVEN,
        stream: bool,
        include: Union[Optional[List[ResponseIncludable]], NotGiven] = NOT_GIVEN,
        instructions: Union[Optional[str], NotGiven] = NOT_GIVEN,
        max_output_tokens: Union[Optional[int], NotGiven] = NOT_GIVEN,
        metadata: Union[Optional[Metadata], NotGiven] = NOT_GIVEN,
        parallel_tool_calls: Union[Optional[bool], NotGiven] = NOT_GIVEN,
        previous_response_id: Union[Optional[str], NotGiven] = NOT_GIVEN,
        reasoning: Union[Optional[Reasoning], NotGiven] = NOT_GIVEN,
        store: Union[Optional[bool], NotGiven] = NOT_GIVEN,
        temperature: Union[Optional[float], NotGiven] = NOT_GIVEN,
        text: Union[ResponseTextConfigParam, NotGiven] = NOT_GIVEN,
        tool_choice: Union[response_create_params.ToolChoice, NotGiven] = NOT_GIVEN,
        tools: Union[Iterable[ToolParam], NotGiven] = NOT_GIVEN,
        top_p: Union[Optional[float], NotGiven] = NOT_GIVEN,
        truncation: Union[Optional[Literal["auto", "disabled"]], NotGiven] = NOT_GIVEN,
        user: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> Union[Response, Stream[ResponseStreamEvent]]:
        ...

    def create(
        self,
        *,
        input: Union[str, ResponseInputParam, NotGiven] = NOT_GIVEN,
        model: Union[ResponsesModel, NotGiven] = NOT_GIVEN,
        include: Union[Optional[List[ResponseIncludable]], NotGiven] = NOT_GIVEN,
        instructions: Union[Optional[str], NotGiven] = NOT_GIVEN,
        max_output_tokens: Union[Optional[int], NotGiven] = NOT_GIVEN,
        metadata: Union[Optional[Metadata], NotGiven] = NOT_GIVEN,
        parallel_tool_calls: Union[Optional[bool], NotGiven] = NOT_GIVEN,
        previous_response_id: Union[Optional[str], NotGiven] = NOT_GIVEN,
        reasoning: Union[Optional[Reasoning], NotGiven] = NOT_GIVEN,
        store: Union[Optional[bool], NotGiven] = NOT_GIVEN,
        stream: Union[Optional[Literal[False]], Literal[True], NotGiven] = NOT_GIVEN,
        temperature: Union[Optional[float], NotGiven] = NOT_GIVEN,
        text: Union[ResponseTextConfigParam, NotGiven] = NOT_GIVEN,
        tool_choice: Union[response_create_params.ToolChoice, NotGiven] = NOT_GIVEN,
        tools: Union[Iterable[ToolParam], NotGiven] = NOT_GIVEN,
        top_p: Union[Optional[float], NotGiven] = NOT_GIVEN,
        truncation: Union[Optional[Literal["auto", "disabled"]], NotGiven] = NOT_GIVEN,
        user: Union[str, NotGiven] = NOT_GIVEN,
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
        include: Union[List[ResponseIncludable], NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> ResponseType:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)

        response = self.openai_client.with_raw_response.responses.retrieve(
            response_id=response_id,
            include=include,
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
        text_format: Union[type[TextFormatT], NotGiven] = NOT_GIVEN,  # type: ignore[type-arg]
        tools: Union[Iterable[ParseableToolParam], NotGiven] = NOT_GIVEN,
        include: Union[List[ResponseIncludable], NotGiven] = NOT_GIVEN,
        instructions: Union[str, NotGiven] = NOT_GIVEN,
        max_output_tokens: Union[int, NotGiven] = NOT_GIVEN,
        metadata: Union[Metadata, NotGiven] = NOT_GIVEN,
        parallel_tool_calls: Union[bool, NotGiven] = NOT_GIVEN,
        previous_response_id: Union[str, NotGiven] = NOT_GIVEN,
        reasoning: Union[Reasoning, NotGiven] = NOT_GIVEN,
        store: Union[bool, NotGiven] = NOT_GIVEN,
        temperature: Union[float, NotGiven] = NOT_GIVEN,
        text: Union[ResponseTextConfigParam, NotGiven] = NOT_GIVEN,
        tool_choice: Union[response_create_params.ToolChoice, NotGiven] = NOT_GIVEN,
        top_p: Union[float, NotGiven] = NOT_GIVEN,
        truncation: Union[Literal["auto", "disabled"], NotGiven] = NOT_GIVEN,
        user: Union[str, NotGiven] = NOT_GIVEN,
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
            reasoning=reasoning,
            store=store,
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
        input: Union[str, ResponseInputParam, NotGiven] = NOT_GIVEN,
        model: Union[str, ChatModel, NotGiven] = NOT_GIVEN,
        text_format: Union[type[TextFormatT], NotGiven] = NOT_GIVEN,  # type: ignore[type-arg]
        tools: Union[Iterable[ParseableToolParam], NotGiven] = NOT_GIVEN,
        include: Union[List[ResponseIncludable], NotGiven] = NOT_GIVEN,
        instructions: Union[str, NotGiven] = NOT_GIVEN,
        max_output_tokens: Union[int, NotGiven] = NOT_GIVEN,
        metadata: Union[Metadata, NotGiven] = NOT_GIVEN,
        parallel_tool_calls: Union[bool, NotGiven] = NOT_GIVEN,
        previous_response_id: Union[str, NotGiven] = NOT_GIVEN,
        reasoning: Union[Reasoning, NotGiven] = NOT_GIVEN,
        store: Union[bool, NotGiven] = NOT_GIVEN,
        stream: Union[Literal[False], Literal[True], NotGiven] = NOT_GIVEN,
        temperature: Union[float, NotGiven] = NOT_GIVEN,
        text: Union[ResponseTextConfigParam, NotGiven] = NOT_GIVEN,
        tool_choice: Union[response_create_params.ToolChoice, NotGiven] = NOT_GIVEN,
        top_p: Union[float, NotGiven] = NOT_GIVEN,
        truncation: Union[Literal["auto", "disabled"], NotGiven] = NOT_GIVEN,
        user: Union[str, NotGiven] = NOT_GIVEN,
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


class InputItems(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    def list(
        self,
        response_id: str,
        *,
        after: Union[str, NotGiven] = NOT_GIVEN,
        before: Union[str, NotGiven] = NOT_GIVEN,
        include: Union[List[ResponseIncludable], NotGiven] = NOT_GIVEN,
        limit: Union[int, NotGiven] = NOT_GIVEN,
        order: Union[Literal["asc", "desc"], NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> InputItemList:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)
        response = self.openai_client.responses.input_items.list(
            response_id=response_id,
            after=after,
            before=before,
            include=include,
            limit=limit,
            order=order,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body={**(extra_body or {}), **kwargs},
            timeout=timeout,
        )

        return response  # type: ignore[return-value]


class AsyncResponses(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.input_items = AsyncInputItems(client)

    @overload
    async def create(
        self,
        *,
        input: Union[str, ResponseInputParam, NotGiven] = NOT_GIVEN,
        model: Union[ResponsesModel, NotGiven] = NOT_GIVEN,
        include: Union[Optional[List[ResponseIncludable]], NotGiven] = NOT_GIVEN,
        instructions: Union[Optional[str], NotGiven] = NOT_GIVEN,
        max_output_tokens: Union[Optional[int], NotGiven] = NOT_GIVEN,
        metadata: Union[Optional[Metadata], NotGiven] = NOT_GIVEN,
        parallel_tool_calls: Union[Optional[bool], NotGiven] = NOT_GIVEN,
        previous_response_id: Union[Optional[str], NotGiven] = NOT_GIVEN,
        reasoning: Union[Optional[Reasoning], NotGiven] = NOT_GIVEN,
        store: Union[Optional[bool], NotGiven] = NOT_GIVEN,
        stream: Union[Literal[False], NotGiven] = NOT_GIVEN,
        temperature: Union[Optional[float], NotGiven] = NOT_GIVEN,
        text: Union[ResponseTextConfigParam, NotGiven] = NOT_GIVEN,
        tool_choice: Union[response_create_params.ToolChoice, NotGiven] = NOT_GIVEN,
        tools: Union[Iterable[ToolParam], NotGiven] = NOT_GIVEN,
        top_p: Union[Optional[float], NotGiven] = NOT_GIVEN,
        truncation: Union[Optional[Literal["auto", "disabled"]], NotGiven] = NOT_GIVEN,
        user: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> Response:
        ...

    @overload
    async def create(
        self,
        *,
        input: Union[str, ResponseInputParam, NotGiven] = NOT_GIVEN,
        model: Union[ResponsesModel, NotGiven] = NOT_GIVEN,
        stream: Literal[True],
        include: Union[Optional[List[ResponseIncludable]], NotGiven] = NOT_GIVEN,
        instructions: Union[Optional[str], NotGiven] = NOT_GIVEN,
        max_output_tokens: Union[Optional[int], NotGiven] = NOT_GIVEN,
        metadata: Union[Optional[Metadata], NotGiven] = NOT_GIVEN,
        parallel_tool_calls: Union[Optional[bool], NotGiven] = NOT_GIVEN,
        previous_response_id: Union[Optional[str], NotGiven] = NOT_GIVEN,
        reasoning: Union[Optional[Reasoning], NotGiven] = NOT_GIVEN,
        store: Union[Optional[bool], NotGiven] = NOT_GIVEN,
        temperature: Union[Optional[float], NotGiven] = NOT_GIVEN,
        text: Union[ResponseTextConfigParam, NotGiven] = NOT_GIVEN,
        tool_choice: Union[response_create_params.ToolChoice, NotGiven] = NOT_GIVEN,
        tools: Union[Iterable[ToolParam], NotGiven] = NOT_GIVEN,
        top_p: Union[Optional[float], NotGiven] = NOT_GIVEN,
        truncation: Union[Optional[Literal["auto", "disabled"]], NotGiven] = NOT_GIVEN,
        user: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> AsyncStream[ResponseStreamEvent]:
        ...

    @overload
    async def create(
        self,
        *,
        input: Union[str, ResponseInputParam, NotGiven] = NOT_GIVEN,
        model: Union[ResponsesModel, NotGiven] = NOT_GIVEN,
        stream: bool,
        include: Union[Optional[List[ResponseIncludable]], NotGiven] = NOT_GIVEN,
        instructions: Union[Optional[str], NotGiven] = NOT_GIVEN,
        max_output_tokens: Union[Optional[int], NotGiven] = NOT_GIVEN,
        metadata: Union[Optional[Metadata], NotGiven] = NOT_GIVEN,
        parallel_tool_calls: Union[Optional[bool], NotGiven] = NOT_GIVEN,
        previous_response_id: Union[Optional[str], NotGiven] = NOT_GIVEN,
        reasoning: Union[Optional[Reasoning], NotGiven] = NOT_GIVEN,
        store: Union[Optional[bool], NotGiven] = NOT_GIVEN,
        temperature: Union[Optional[float], NotGiven] = NOT_GIVEN,
        text: Union[ResponseTextConfigParam, NotGiven] = NOT_GIVEN,
        tool_choice: Union[response_create_params.ToolChoice, NotGiven] = NOT_GIVEN,
        tools: Union[Iterable[ToolParam], NotGiven] = NOT_GIVEN,
        top_p: Union[Optional[float], NotGiven] = NOT_GIVEN,
        truncation: Union[Optional[Literal["auto", "disabled"]], NotGiven] = NOT_GIVEN,
        user: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> Union[Response, AsyncStream[ResponseStreamEvent]]:
        ...

    async def create(
        self,
        *,
        input: Union[str, ResponseInputParam, NotGiven] = NOT_GIVEN,
        model: Union[ResponsesModel, NotGiven] = NOT_GIVEN,
        include: Union[Optional[List[ResponseIncludable]], NotGiven] = NOT_GIVEN,
        instructions: Union[Optional[str], NotGiven] = NOT_GIVEN,
        max_output_tokens: Union[Optional[int], NotGiven] = NOT_GIVEN,
        metadata: Union[Optional[Metadata], NotGiven] = NOT_GIVEN,
        parallel_tool_calls: Union[Optional[bool], NotGiven] = NOT_GIVEN,
        previous_response_id: Union[Optional[str], NotGiven] = NOT_GIVEN,
        reasoning: Union[Optional[Reasoning], NotGiven] = NOT_GIVEN,
        store: Union[Optional[bool], NotGiven] = NOT_GIVEN,
        stream: Union[Optional[Literal[False]], Literal[True], NotGiven] = NOT_GIVEN,
        temperature: Union[Optional[float], NotGiven] = NOT_GIVEN,
        text: Union[ResponseTextConfigParam, NotGiven] = NOT_GIVEN,
        tool_choice: Union[response_create_params.ToolChoice, NotGiven] = NOT_GIVEN,
        tools: Union[Iterable[ToolParam], NotGiven] = NOT_GIVEN,
        top_p: Union[Optional[float], NotGiven] = NOT_GIVEN,
        truncation: Union[Optional[Literal["auto", "disabled"]], NotGiven] = NOT_GIVEN,
        user: Union[str, NotGiven] = NOT_GIVEN,
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
        include: Union[List[ResponseIncludable], NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> ResponseType:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)

        response = await self.openai_client.with_raw_response.responses.retrieve(
            response_id=response_id,
            include=include,
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
        text_format: Union[type[TextFormatT], NotGiven] = NOT_GIVEN,  # type: ignore[type-arg]
        tools: Union[Iterable[ParseableToolParam], NotGiven] = NOT_GIVEN,
        include: Union[List[ResponseIncludable], NotGiven] = NOT_GIVEN,
        instructions: Union[str, NotGiven] = NOT_GIVEN,
        max_output_tokens: Union[int, NotGiven] = NOT_GIVEN,
        metadata: Union[Metadata, NotGiven] = NOT_GIVEN,
        parallel_tool_calls: Union[bool, NotGiven] = NOT_GIVEN,
        previous_response_id: Union[str, NotGiven] = NOT_GIVEN,
        reasoning: Union[Reasoning, NotGiven] = NOT_GIVEN,
        store: Union[bool, NotGiven] = NOT_GIVEN,
        temperature: Union[float, NotGiven] = NOT_GIVEN,
        text: Union[ResponseTextConfigParam, NotGiven] = NOT_GIVEN,
        tool_choice: Union[response_create_params.ToolChoice, NotGiven] = NOT_GIVEN,
        top_p: Union[float, NotGiven] = NOT_GIVEN,
        truncation: Union[Literal["auto", "disabled"], NotGiven] = NOT_GIVEN,
        user: Union[str, NotGiven] = NOT_GIVEN,
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
            reasoning=reasoning,
            store=store,
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
        input: Union[str, ResponseInputParam, NotGiven] = NOT_GIVEN,
        model: Union[str, ChatModel, NotGiven] = NOT_GIVEN,
        text_format: Union[type[TextFormatT], NotGiven] = NOT_GIVEN,  # type: ignore[type-arg]
        tools: Union[Iterable[ParseableToolParam], NotGiven] = NOT_GIVEN,
        include: Union[List[ResponseIncludable], NotGiven] = NOT_GIVEN,
        instructions: Union[str, NotGiven] = NOT_GIVEN,
        max_output_tokens: Union[int, NotGiven] = NOT_GIVEN,
        metadata: Union[Metadata, NotGiven] = NOT_GIVEN,
        parallel_tool_calls: Union[bool, NotGiven] = NOT_GIVEN,
        previous_response_id: Union[str, NotGiven] = NOT_GIVEN,
        reasoning: Union[Reasoning, NotGiven] = NOT_GIVEN,
        store: Union[bool, NotGiven] = NOT_GIVEN,
        stream: Union[Literal[False], Literal[True], NotGiven] = NOT_GIVEN,
        temperature: Union[float, NotGiven] = NOT_GIVEN,
        text: Union[ResponseTextConfigParam, NotGiven] = NOT_GIVEN,
        tool_choice: Union[response_create_params.ToolChoice, NotGiven] = NOT_GIVEN,
        top_p: Union[float, NotGiven] = NOT_GIVEN,
        truncation: Union[Literal["auto", "disabled"], NotGiven] = NOT_GIVEN,
        user: Union[str, NotGiven] = NOT_GIVEN,
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


class AsyncInputItems(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    async def list(
        self,
        response_id: str,
        *,
        after: Union[str, NotGiven] = NOT_GIVEN,
        before: Union[str, NotGiven] = NOT_GIVEN,
        include: Union[List[ResponseIncludable], NotGiven] = NOT_GIVEN,
        limit: Union[int, NotGiven] = NOT_GIVEN,
        order: Union[Literal["asc", "desc"], NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> InputItemList:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)
        response = await self.openai_client.responses.input_items.list(
            response_id=response_id,
            after=after,
            before=before,
            include=include,
            limit=limit,
            order=order,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body={**(extra_body or {}), **kwargs},
            timeout=timeout,
        )

        return response  # type: ignore[return-value]
