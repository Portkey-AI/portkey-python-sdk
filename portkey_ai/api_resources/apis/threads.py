import json
from typing import (
    Any,
    AsyncIterator,
    Iterable,
    Iterator,
    List,
    Literal,
    Optional,
    Union,
)
import typing

from portkey_ai._vendor.openai.types.beta.assistant_stream_event import (
    AssistantStreamEvent,
)
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.client import AsyncPortkey, Portkey
from portkey_ai.api_resources.types.thread_message_type import (
    MessageList,
    ThreadMessage,
    ThreadMessageDeleted,
)
from portkey_ai.api_resources.types.thread_run_type import (
    Run,
    RunList,
    RunStep,
    RunStepList,
)
from portkey_ai.api_resources.types.thread_type import Thread, ThreadDeleted
from ..._vendor.openai._types import NotGiven, NOT_GIVEN
from ..._vendor.openai.types.beta import thread_create_and_run_params
from ..._vendor.openai.types.beta.assistant_response_format_option_param import (
    AssistantResponseFormatOptionParam,
)
from ..._vendor.openai.types.beta.assistant_tool_choice_option_param import (
    AssistantToolChoiceOptionParam,
)
from ..._vendor.openai.lib.streaming import (
    AssistantEventHandler,
    AssistantEventHandlerT,
    AssistantStreamManager,
    AsyncAssistantEventHandler,
    AsyncAssistantEventHandlerT,
    AsyncAssistantStreamManager,
)
from ..._vendor.openai.types.beta.threads import (
    run_create_params,
    run_submit_tool_outputs_params,
)
from ..._vendor.openai.types.beta.assistant_tool_param import AssistantToolParam


class Threads(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.messages = Messages(client)
        self.runs = Runs(client)

    def create(
        self,
        *,
        messages: Union[Any, NotGiven] = NOT_GIVEN,
        metadata: Union[Optional[object], NotGiven] = NOT_GIVEN,
        tool_resources: Union[Any, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> Thread:
        response = self.openai_client.with_raw_response.beta.threads.create(
            messages=messages,
            metadata=metadata,
            tool_resources=tool_resources,
            extra_body=kwargs,
        )
        data = Thread(**json.loads(response.text))
        data._headers = response.headers

        return data

    def retrieve(self, thread_id, **kwargs) -> Thread:
        if kwargs:
            response = self.openai_client.with_raw_response.beta.threads.retrieve(
                thread_id=thread_id, extra_body=kwargs
            )
        else:
            response = self.openai_client.with_raw_response.beta.threads.retrieve(
                thread_id=thread_id
            )
        data = Thread(**json.loads(response.text))
        data._headers = response.headers

        return data

    def update(
        self,
        thread_id,
        *,
        metadata: Union[Optional[object], NotGiven] = NOT_GIVEN,
        tool_resources: Union[Any, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> Thread:
        response = self.openai_client.with_raw_response.beta.threads.update(
            thread_id=thread_id,
            metadata=metadata,
            tool_resources=tool_resources,
            extra_body=kwargs,
        )
        data = Thread(**json.loads(response.text))
        data._headers = response.headers

        return data

    def delete(
        self,
        thread_id,
    ) -> ThreadDeleted:
        response = self.openai_client.with_raw_response.beta.threads.delete(
            thread_id=thread_id
        )
        data = ThreadDeleted(**json.loads(response.text))
        data._headers = response.headers

        return data

    def stream_create_and_run(  # type: ignore[return]
        self, assistant_id, **kwargs
    ) -> Union[Run, Iterator[AssistantStreamEvent]]:
        with self.openai_client.with_streaming_response.beta.threads.create_and_run(
            assistant_id=assistant_id, stream=True, extra_body=kwargs
        ) as streaming:
            for line in streaming.iter_lines():
                json_string = line.replace("data: ", "")
                json_string = json_string.strip().rstrip("\n")
                if json_string == "[DONE]":
                    break
                elif json_string == "":
                    continue
                elif json_string != "":
                    yield json_string
                else:
                    return ""

    def normal_create_and_run(self, assistant_id, **kwargs) -> Run:
        response = self.openai_client.with_raw_response.beta.threads.create_and_run(
            assistant_id=assistant_id, extra_body=kwargs
        )
        data = Run(**json.loads(response.text))
        data._headers = response.headers
        return data

    def create_and_run(
        self, assistant_id, stream: Union[bool, NotGiven] = NOT_GIVEN, **kwargs
    ) -> Union[Run, Iterator[AssistantStreamEvent]]:
        if stream is True:
            return self.stream_create_and_run(assistant_id, **kwargs)
        else:
            return self.normal_create_and_run(assistant_id, **kwargs)

    def create_and_run_poll(
        self,
        *,
        assistant_id: str,
        instructions: Union[Optional[str], NotGiven] = NOT_GIVEN,
        max_completion_tokens: Union[Optional[int], NotGiven] = NOT_GIVEN,
        max_prompt_tokens: Union[Optional[int], NotGiven] = NOT_GIVEN,
        metadata: Union[Optional[object], NotGiven] = NOT_GIVEN,
        model: Union[str, None, NotGiven] = NOT_GIVEN,
        response_format: Union[
            Optional[AssistantResponseFormatOptionParam], NotGiven
        ] = NOT_GIVEN,
        temperature: Union[Optional[float], NotGiven] = NOT_GIVEN,
        thread: Union[thread_create_and_run_params.Thread, NotGiven] = NOT_GIVEN,
        tool_choice: Union[
            Optional[AssistantToolChoiceOptionParam], NotGiven
        ] = NOT_GIVEN,
        tool_resources: Union[
            Optional[thread_create_and_run_params.ToolResources], NotGiven
        ] = NOT_GIVEN,
        tools: Union[
            Optional[Iterable[thread_create_and_run_params.Tool]], NotGiven
        ] = NOT_GIVEN,
        top_p: Union[Optional[float], NotGiven] = NOT_GIVEN,
        truncation_strategy: Union[
            Optional[thread_create_and_run_params.TruncationStrategy], NotGiven
        ] = NOT_GIVEN,
        poll_interval_ms: Union[int, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> Run:
        response = self.openai_client.beta.threads.create_and_run_poll(
            assistant_id=assistant_id,
            instructions=instructions,
            max_completion_tokens=max_completion_tokens,
            max_prompt_tokens=max_prompt_tokens,
            metadata=metadata,
            model=model,
            response_format=response_format,
            temperature=temperature,
            thread=thread,
            tool_choice=tool_choice,
            tool_resources=tool_resources,
            tools=tools,
            top_p=top_p,
            truncation_strategy=truncation_strategy,
            poll_interval_ms=poll_interval_ms,
            **kwargs,
        )
        data = response

        return data  # type: ignore[return-value]

    @typing.no_type_check
    def create_and_run_stream(
        self,
        *,
        assistant_id: str,
        instructions: Union[Optional[str], NotGiven] = NOT_GIVEN,
        max_completion_tokens: Union[Optional[int], NotGiven] = NOT_GIVEN,
        max_prompt_tokens: Union[Optional[int], NotGiven] = NOT_GIVEN,
        metadata: Union[Optional[object], NotGiven] = NOT_GIVEN,
        model: Union[str, None, NotGiven] = NOT_GIVEN,
        response_format: Union[
            Optional[AssistantResponseFormatOptionParam], NotGiven
        ] = NOT_GIVEN,
        temperature: Union[Optional[float], NotGiven] = NOT_GIVEN,
        thread: Union[thread_create_and_run_params.Thread, NotGiven] = NOT_GIVEN,
        tool_choice: Union[
            Optional[AssistantToolChoiceOptionParam], NotGiven
        ] = NOT_GIVEN,
        tool_resources: Union[
            Optional[thread_create_and_run_params.ToolResources], NotGiven
        ] = NOT_GIVEN,
        tools: Union[
            Optional[Iterable[thread_create_and_run_params.Tool]], NotGiven
        ] = NOT_GIVEN,
        top_p: Union[Optional[float], NotGiven] = NOT_GIVEN,
        truncation_strategy: Union[
            Optional[thread_create_and_run_params.TruncationStrategy], NotGiven
        ] = NOT_GIVEN,
        event_handler: Union[AssistantEventHandlerT, None] = None,
        **kwargs,
    ) -> Union[
        AssistantStreamManager[AssistantEventHandler],
        AssistantStreamManager[AssistantEventHandlerT],
    ]:
        response = self.openai_client.beta.threads.create_and_run_stream(
            assistant_id=assistant_id,
            instructions=instructions,
            max_completion_tokens=max_completion_tokens,
            max_prompt_tokens=max_prompt_tokens,
            metadata=metadata,
            model=model,
            response_format=response_format,
            temperature=temperature,
            thread=thread,
            tool_choice=tool_choice,
            tool_resources=tool_resources,
            tools=tools,
            top_p=top_p,
            truncation_strategy=truncation_strategy,
            event_handler=event_handler,
            **kwargs,
        )
        data = response
        return data


class Messages(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    def create(
        self,
        thread_id,
        *,
        content: Union[str, Any],
        role: Any,
        attachments: Union[Any, NotGiven] = NOT_GIVEN,
        metadata: Union[Optional[object], NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> ThreadMessage:
        response = self.openai_client.with_raw_response.beta.threads.messages.create(
            thread_id=thread_id,
            content=content,
            role=role,
            attachments=attachments,
            metadata=metadata,
            **kwargs,
        )
        data = ThreadMessage(**json.loads(response.text))
        data._headers = response.headers

        return data

    def retrieve(self, thread_id, message_id, **kwargs) -> ThreadMessage:
        if kwargs:
            response = (
                self.openai_client.with_raw_response.beta.threads.messages.retrieve(
                    thread_id=thread_id, message_id=message_id, extra_body=kwargs
                )
            )
        else:
            response = (
                self.openai_client.with_raw_response.beta.threads.messages.retrieve(
                    thread_id=thread_id, message_id=message_id
                )
            )
        data = ThreadMessage(**json.loads(response.text))
        data._headers = response.headers
        return data

    def update(
        self,
        thread_id,
        message_id,
        *,
        metadata: Union[Optional[object], NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> ThreadMessage:
        response = self.openai_client.with_raw_response.beta.threads.messages.update(
            thread_id=thread_id, message_id=message_id, metadata=metadata, **kwargs
        )
        data = ThreadMessage(**json.loads(response.text))
        data._headers = response.headers
        return data

    def list(
        self,
        thread_id,
        *,
        after: Union[str, NotGiven] = NOT_GIVEN,
        before: Union[str, NotGiven] = NOT_GIVEN,
        limit: Union[int, NotGiven] = NOT_GIVEN,
        order: Union[NotGiven, Literal["asc", "desc"]] = NOT_GIVEN,
        run_id: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> MessageList:
        response = self.openai_client.with_raw_response.beta.threads.messages.list(
            thread_id=thread_id,
            after=after,
            before=before,
            limit=limit,
            order=order,
            run_id=run_id,
            **kwargs,
        )
        data = MessageList(**json.loads(response.text))
        data._headers = response.headers
        return data

    def delete(
        self, message_id: str, *, thread_id: str, **kwargs
    ) -> ThreadMessageDeleted:
        response = self.openai_client.with_raw_response.beta.threads.messages.delete(
            message_id=message_id, thread_id=thread_id, **kwargs
        )
        data = ThreadMessageDeleted(**json.loads(response.text))
        data._headers = response.headers

        return data


class Runs(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.steps = Steps(client)

    def stream_create(  # type: ignore[return]
        self,
        thread_id,
        assistant_id,
        **kwargs,
    ) -> Union[Run, Iterator[AssistantStreamEvent]]:
        with self.openai_client.with_streaming_response.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id,
            stream=True,
            extra_body=kwargs,
        ) as streaming:
            for line in streaming.iter_lines():
                json_string = line.replace("data: ", "")
                json_string = json_string.strip().rstrip("\n")
                if json_string == "[DONE]":
                    break
                elif json_string == "":
                    continue
                elif json_string != "":
                    yield json_string
                else:
                    return ""

    def normal_create(
        self,
        thread_id,
        assistant_id,
        **kwargs,
    ) -> Run:
        response = self.openai_client.with_raw_response.beta.threads.runs.create(
            thread_id=thread_id, assistant_id=assistant_id, extra_body=kwargs
        )
        data = Run(**json.loads(response.text))
        data._headers = response.headers
        return data

    def create(
        self,
        thread_id: str,
        *,
        assistant_id: str,
        stream: Union[bool, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> Union[Run, Iterator[AssistantStreamEvent]]:
        if stream is True:
            return self.stream_create(
                thread_id=thread_id, assistant_id=assistant_id, **kwargs
            )
        else:
            return self.normal_create(
                thread_id=thread_id, assistant_id=assistant_id, **kwargs
            )

    def retrieve(self, thread_id, run_id, **kwargs) -> Run:
        if kwargs:
            response = self.openai_client.with_raw_response.beta.threads.runs.retrieve(
                thread_id=thread_id, run_id=run_id, extra_body=kwargs
            )
        else:
            response = self.openai_client.with_raw_response.beta.threads.runs.retrieve(
                thread_id=thread_id, run_id=run_id
            )
        data = Run(**json.loads(response.text))
        data._headers = response.headers

        return data

    def update(
        self,
        thread_id,
        run_id,
        metadata: Union[Optional[object], NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> Run:
        response = self.openai_client.with_raw_response.beta.threads.runs.update(
            thread_id=thread_id, run_id=run_id, metadata=metadata, extra_body=kwargs
        )
        data = Run(**json.loads(response.text))
        data._headers = response.headers

        return data

    def list(
        self,
        thread_id,
        *,
        after: Union[str, NotGiven] = NOT_GIVEN,
        before: Union[str, NotGiven] = NOT_GIVEN,
        limit: Union[int, NotGiven] = NOT_GIVEN,
        order: Union[NotGiven, Literal["asc", "desc"]] = NOT_GIVEN,
        **kwargs,
    ) -> RunList:
        response = self.openai_client.with_raw_response.beta.threads.runs.list(
            thread_id=thread_id,
            after=after,
            before=before,
            limit=limit,
            order=order,
            **kwargs,
        )
        data = RunList(**json.loads(response.text))
        data._headers = response.headers

        return data

    def cancel(self, thread_id, run_id, **kwargs) -> Run:
        response = self.openai_client.with_raw_response.beta.threads.runs.cancel(
            thread_id=thread_id, run_id=run_id, **kwargs
        )
        data = Run(**json.loads(response.text))
        data._headers = response.headers

        return data

    def create_and_poll(
        self,
        *,
        assistant_id: str,
        include: Union[List[Any], NotGiven] = NOT_GIVEN,
        additional_instructions: Union[Optional[str], NotGiven] = NOT_GIVEN,
        additional_messages: Union[
            Optional[Iterable[run_create_params.AdditionalMessage]], NotGiven
        ] = NOT_GIVEN,
        instructions: Union[Optional[str], NotGiven] = NOT_GIVEN,
        max_completion_tokens: Union[Optional[int], NotGiven] = NOT_GIVEN,
        max_prompt_tokens: Union[Optional[int], NotGiven] = NOT_GIVEN,
        metadata: Union[Optional[object], NotGiven] = NOT_GIVEN,
        model: Union[str, None, NotGiven] = NOT_GIVEN,
        parallel_tool_calls: Union[bool, NotGiven] = NOT_GIVEN,
        response_format: Union[
            Optional[AssistantResponseFormatOptionParam], NotGiven
        ] = NOT_GIVEN,
        temperature: Union[Optional[float], NotGiven] = NOT_GIVEN,
        tool_choice: Union[
            Optional[AssistantToolChoiceOptionParam], NotGiven
        ] = NOT_GIVEN,
        tools: Union[Optional[Iterable[AssistantToolParam]], NotGiven] = NOT_GIVEN,
        top_p: Union[Optional[float], NotGiven] = NOT_GIVEN,
        truncation_strategy: Union[
            Optional[run_create_params.TruncationStrategy], NotGiven
        ] = NOT_GIVEN,
        poll_interval_ms: Union[int, NotGiven] = NOT_GIVEN,
        thread_id: str,
        **kwargs,
    ) -> Run:
        response = self.openai_client.beta.threads.runs.create_and_poll(
            assistant_id=assistant_id,
            include=include,
            additional_instructions=additional_instructions,
            additional_messages=additional_messages,
            instructions=instructions,
            max_completion_tokens=max_completion_tokens,
            max_prompt_tokens=max_prompt_tokens,
            metadata=metadata,
            model=model,
            parallel_tool_calls=parallel_tool_calls,
            response_format=response_format,
            temperature=temperature,
            tool_choice=tool_choice,
            tools=tools,
            top_p=top_p,
            truncation_strategy=truncation_strategy,
            poll_interval_ms=poll_interval_ms,
            thread_id=thread_id,
            extra_body=kwargs,
        )
        data = response

        return data  # type: ignore[return-value]

    @typing.no_type_check
    def create_and_stream(
        self,
        *,
        assistant_id: str,
        additional_instructions: Union[Optional[str], NotGiven] = NOT_GIVEN,
        additional_messages: Union[
            Optional[Iterable[run_create_params.AdditionalMessage]], NotGiven
        ] = NOT_GIVEN,
        instructions: Union[Optional[str], NotGiven] = NOT_GIVEN,
        max_completion_tokens: Union[Optional[int], NotGiven] = NOT_GIVEN,
        max_prompt_tokens: Union[Optional[int], NotGiven] = NOT_GIVEN,
        metadata: Union[Optional[object], NotGiven] = NOT_GIVEN,
        model: Union[str, None, NotGiven] = NOT_GIVEN,
        parallel_tool_calls: Union[bool, NotGiven] = NOT_GIVEN,
        response_format: Union[
            Optional[AssistantResponseFormatOptionParam], NotGiven
        ] = NOT_GIVEN,
        temperature: Union[Optional[float], NotGiven] = NOT_GIVEN,
        tool_choice: Union[
            Optional[AssistantToolChoiceOptionParam], NotGiven
        ] = NOT_GIVEN,
        tools: Union[Optional[Iterable[AssistantToolParam]], NotGiven] = NOT_GIVEN,
        top_p: Union[Optional[float], NotGiven] = NOT_GIVEN,
        truncation_strategy: Union[
            Optional[run_create_params.TruncationStrategy], NotGiven
        ] = NOT_GIVEN,
        thread_id: str,
        event_handler: Union[AssistantEventHandlerT, None] = None,
        **kwargs,
    ) -> Union[
        AssistantStreamManager[AssistantEventHandler],
        AssistantStreamManager[AssistantEventHandlerT],
    ]:
        response = self.openai_client.beta.threads.runs.create_and_stream(
            assistant_id=assistant_id,
            additional_instructions=additional_instructions,
            additional_messages=additional_messages,
            instructions=instructions,
            max_completion_tokens=max_completion_tokens,
            max_prompt_tokens=max_prompt_tokens,
            metadata=metadata,
            model=model,
            parallel_tool_calls=parallel_tool_calls,
            response_format=response_format,
            temperature=temperature,
            tool_choice=tool_choice,
            tools=tools,
            top_p=top_p,
            truncation_strategy=truncation_strategy,
            thread_id=thread_id,
            event_handler=event_handler,
            extra_body=kwargs,
        )
        data = response
        return data

    def poll(
        self,
        *,
        run_id: str,
        thread_id: str,
        **kwargs,
    ) -> Run:
        response = self.openai_client.beta.threads.runs.poll(
            run_id=run_id, thread_id=thread_id, **kwargs
        )
        data = response

        return data  # type: ignore[return-value]

    @typing.no_type_check
    def stream(
        self,
        *,
        assistant_id: str,
        include: Union[List[Any], NotGiven] = NOT_GIVEN,
        additional_instructions: Union[Optional[str], NotGiven] = NOT_GIVEN,
        additional_messages: Union[
            Optional[Iterable[run_create_params.AdditionalMessage]], NotGiven
        ] = NOT_GIVEN,
        instructions: Union[Optional[str], NotGiven] = NOT_GIVEN,
        max_completion_tokens: Union[Optional[int], NotGiven] = NOT_GIVEN,
        max_prompt_tokens: Union[Optional[int], NotGiven] = NOT_GIVEN,
        metadata: Union[Optional[object], NotGiven] = NOT_GIVEN,
        model: Union[str, None, NotGiven] = NOT_GIVEN,
        parallel_tool_calls: Union[bool, NotGiven] = NOT_GIVEN,
        response_format: Union[
            Optional[AssistantResponseFormatOptionParam], NotGiven
        ] = NOT_GIVEN,
        temperature: Union[Optional[float], NotGiven] = NOT_GIVEN,
        tool_choice: Union[
            Optional[AssistantToolChoiceOptionParam], NotGiven
        ] = NOT_GIVEN,
        tools: Union[Optional[Iterable[AssistantToolParam]], NotGiven] = NOT_GIVEN,
        top_p: Union[Optional[float], NotGiven] = NOT_GIVEN,
        truncation_strategy: Union[
            Optional[run_create_params.TruncationStrategy], NotGiven
        ] = NOT_GIVEN,
        thread_id: str,
        event_handler: Union[AssistantEventHandlerT, None] = None,
        **kwargs,
    ) -> Union[
        AssistantStreamManager[AssistantEventHandler],
        AssistantStreamManager[AssistantEventHandlerT],
    ]:
        response = self.openai_client.beta.threads.runs.stream(
            assistant_id=assistant_id,
            include=include,
            additional_instructions=additional_instructions,
            additional_messages=additional_messages,
            instructions=instructions,
            max_completion_tokens=max_completion_tokens,
            max_prompt_tokens=max_prompt_tokens,
            metadata=metadata,
            model=model,
            parallel_tool_calls=parallel_tool_calls,
            response_format=response_format,
            temperature=temperature,
            tool_choice=tool_choice,
            tools=tools,
            top_p=top_p,
            truncation_strategy=truncation_strategy,
            thread_id=thread_id,
            event_handler=event_handler,
            extra_body=kwargs,
        )
        data = response
        return data

    def submit_tool_outputs(
        self,
        run_id,
        *,
        thread_id,
        tool_outputs,
        stream: Union[bool, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> Run:
        response = (
            self.openai_client.with_raw_response.beta.threads.runs.submit_tool_outputs(
                thread_id=thread_id,
                run_id=run_id,
                tool_outputs=tool_outputs,
                stream=stream,
                **kwargs,
            )
        )
        data = Run(**json.loads(response.text))
        data._headers = response.headers

        return data

    def submit_tool_outputs_and_poll(
        self,
        *,
        tool_outputs: Union[Iterable[run_submit_tool_outputs_params.ToolOutput]],
        run_id: str,
        thread_id: str,
        poll_interval_ms: Union[int, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> Run:
        response = self.openai_client.beta.threads.runs.submit_tool_outputs_and_poll(
            tool_outputs=tool_outputs,
            run_id=run_id,
            thread_id=thread_id,
            poll_interval_ms=poll_interval_ms,
            extra_body=kwargs,
        )
        data = response

        return data  # type: ignore[return-value]

    def submit_tool_outputs_stream(
        self,
        *,
        tool_outputs: Union[Iterable[run_submit_tool_outputs_params.ToolOutput]],
        run_id: str,
        thread_id: str,
        event_handler: Union[AssistantEventHandlerT, None] = None,
        **kwargs,
    ) -> Union[
        AssistantStreamManager[AssistantEventHandler],
        AssistantStreamManager[AssistantEventHandlerT],
    ]:
        response = self.openai_client.beta.threads.runs.submit_tool_outputs_stream(  # type: ignore[type-var]
            tool_outputs=tool_outputs,
            run_id=run_id,
            thread_id=thread_id,
            event_handler=event_handler,
            extra_body=kwargs,
        )
        data = response

        return data  # type: ignore[return-value]


class Steps(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    def retrieve(
        self,
        thread_id,
        run_id,
        step_id,
        include: Union[List[Any], NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> RunStep:
        if kwargs:
            response = (
                self.openai_client.with_raw_response.beta.threads.runs.steps.retrieve(
                    thread_id=thread_id,
                    run_id=run_id,
                    step_id=step_id,
                    include=include,
                    extra_body=kwargs,
                )
            )
        else:
            response = (
                self.openai_client.with_raw_response.beta.threads.runs.steps.retrieve(
                    thread_id=thread_id,
                    run_id=run_id,
                    step_id=step_id,
                    include=include,
                )
            )
        data = RunStep(**json.loads(response.text))
        data._headers = response.headers

        return data

    def list(
        self,
        run_id,
        *,
        thread_id,
        after: Union[str, NotGiven] = NOT_GIVEN,
        before: Union[str, NotGiven] = NOT_GIVEN,
        include: Union[List[Any], NotGiven] = NOT_GIVEN,
        limit: Union[int, NotGiven] = NOT_GIVEN,
        order: Union[Any, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> RunStepList:
        response = self.openai_client.with_raw_response.beta.threads.runs.steps.list(
            thread_id=thread_id,
            run_id=run_id,
            after=after,
            before=before,
            include=include,
            limit=limit,
            order=order,
            **kwargs,
        )
        data = RunStepList(**json.loads(response.text))
        data._headers = response.headers

        return data


class AsyncThreads(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.messages = AsyncMessages(client)
        self.runs = AsyncRuns(client)

    async def create(
        self,
        *,
        messages: Union[Any, NotGiven] = NOT_GIVEN,
        metadata: Union[Optional[object], NotGiven] = NOT_GIVEN,
        tool_resources: Union[Any, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> Thread:
        response = await self.openai_client.with_raw_response.beta.threads.create(
            messages=messages,
            metadata=metadata,
            tool_resources=tool_resources,
            extra_body=kwargs,
        )
        data = Thread(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def retrieve(self, thread_id, **kwargs) -> Thread:
        if kwargs:
            response = await self.openai_client.with_raw_response.beta.threads.retrieve(
                thread_id=thread_id, extra_body=kwargs
            )
        else:
            response = await self.openai_client.with_raw_response.beta.threads.retrieve(
                thread_id=thread_id
            )
        data = Thread(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def update(
        self,
        thread_id,
        *,
        metadata: Union[Optional[object], NotGiven] = NOT_GIVEN,
        tool_resources: Union[Any, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> Thread:
        response = await self.openai_client.with_raw_response.beta.threads.update(
            thread_id=thread_id,
            metadata=metadata,
            tool_resources=tool_resources,
            extra_body=kwargs,
        )
        data = Thread(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def delete(
        self,
        thread_id,
    ) -> ThreadDeleted:
        response = await self.openai_client.with_raw_response.beta.threads.delete(
            thread_id=thread_id
        )
        data = ThreadDeleted(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def stream_create_and_run(
        self, assistant_id, **kwargs
    ) -> Union[Run, AsyncIterator[AssistantStreamEvent]]:
        async with self.openai_client.with_streaming_response.beta.threads.create_and_run(  # noqa: E501
            assistant_id=assistant_id, stream=True, extra_body=kwargs
        ) as streaming:
            async for line in streaming.iter_lines():
                json_string = line.replace("data: ", "")
                json_string = json_string.strip().rstrip("\n")
                if json_string == "[DONE]":
                    break
                elif json_string == "":
                    continue
                elif json_string != "":
                    yield json_string
                else:
                    pass

    async def normal_create_and_run(self, assistant_id, **kwargs) -> Run:
        response = (
            await self.openai_client.with_raw_response.beta.threads.create_and_run(
                assistant_id=assistant_id, extra_body=kwargs
            )
        )
        data = Run(**json.loads(response.text))
        data._headers = response.headers
        return data

    async def create_and_run(
        self, assistant_id, stream: Union[bool, NotGiven] = NOT_GIVEN, **kwargs
    ) -> Union[Run, AsyncIterator[AssistantStreamEvent]]:
        if stream is True:
            return self.stream_create_and_run(assistant_id=assistant_id, **kwargs)
        else:
            return await self.normal_create_and_run(assistant_id=assistant_id, **kwargs)

    async def create_and_run_poll(
        self,
        *,
        assistant_id: str,
        instructions: Union[Optional[str], NotGiven] = NOT_GIVEN,
        max_completion_tokens: Union[Optional[int], NotGiven] = NOT_GIVEN,
        max_prompt_tokens: Union[Optional[int], NotGiven] = NOT_GIVEN,
        metadata: Union[Optional[object], NotGiven] = NOT_GIVEN,
        model: Union[str, None, NotGiven] = NOT_GIVEN,
        response_format: Union[
            Optional[AssistantResponseFormatOptionParam], NotGiven
        ] = NOT_GIVEN,
        temperature: Union[Optional[float], NotGiven] = NOT_GIVEN,
        thread: Union[thread_create_and_run_params.Thread, NotGiven] = NOT_GIVEN,
        tool_choice: Union[
            Optional[AssistantToolChoiceOptionParam], NotGiven
        ] = NOT_GIVEN,
        tool_resources: Union[
            Optional[thread_create_and_run_params.ToolResources], NotGiven
        ] = NOT_GIVEN,
        tools: Union[
            Optional[Iterable[thread_create_and_run_params.Tool]], NotGiven
        ] = NOT_GIVEN,
        top_p: Union[Optional[float], NotGiven] = NOT_GIVEN,
        truncation_strategy: Union[
            Optional[thread_create_and_run_params.TruncationStrategy], NotGiven
        ] = NOT_GIVEN,
        poll_interval_ms: Union[int, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> Run:
        response = await self.openai_client.beta.threads.create_and_run_poll(
            assistant_id=assistant_id,
            instructions=instructions,
            max_completion_tokens=max_completion_tokens,
            max_prompt_tokens=max_prompt_tokens,
            metadata=metadata,
            model=model,
            response_format=response_format,
            temperature=temperature,
            thread=thread,
            tool_choice=tool_choice,
            tool_resources=tool_resources,
            tools=tools,
            top_p=top_p,
            truncation_strategy=truncation_strategy,
            poll_interval_ms=poll_interval_ms,
            **kwargs,
        )
        data = response

        return data  # type: ignore[return-value]

    @typing.no_type_check
    async def create_and_run_stream(
        self,
        *,
        assistant_id: str,
        instructions: Union[Optional[str], NotGiven] = NOT_GIVEN,
        max_completion_tokens: Union[Optional[int], NotGiven] = NOT_GIVEN,
        max_prompt_tokens: Union[Optional[int], NotGiven] = NOT_GIVEN,
        metadata: Union[Optional[object], NotGiven] = NOT_GIVEN,
        model: Union[str, None, NotGiven] = NOT_GIVEN,
        response_format: Union[
            Optional[AssistantResponseFormatOptionParam], NotGiven
        ] = NOT_GIVEN,
        temperature: Union[Optional[float], NotGiven] = NOT_GIVEN,
        thread: Union[thread_create_and_run_params.Thread, NotGiven] = NOT_GIVEN,
        tool_choice: Union[
            Optional[AssistantToolChoiceOptionParam], NotGiven
        ] = NOT_GIVEN,
        tool_resources: Union[
            Optional[thread_create_and_run_params.ToolResources], NotGiven
        ] = NOT_GIVEN,
        tools: Union[
            Optional[Iterable[thread_create_and_run_params.Tool]], NotGiven
        ] = NOT_GIVEN,
        top_p: Union[Optional[float], NotGiven] = NOT_GIVEN,
        truncation_strategy: Union[
            Optional[thread_create_and_run_params.TruncationStrategy], NotGiven
        ] = NOT_GIVEN,
        event_handler: Union[AsyncAssistantEventHandlerT, None] = None,
        **kwargs,
    ) -> (
        Union[
            AsyncAssistantStreamManager[AsyncAssistantEventHandler],
            AsyncAssistantStreamManager[AsyncAssistantEventHandlerT],
        ]
    ):
        response = await self.openai_client.beta.threads.create_and_run_stream(
            assistant_id=assistant_id,
            instructions=instructions,
            max_completion_tokens=max_completion_tokens,
            max_prompt_tokens=max_prompt_tokens,
            metadata=metadata,
            model=model,
            response_format=response_format,
            temperature=temperature,
            thread=thread,
            tool_choice=tool_choice,
            tool_resources=tool_resources,
            tools=tools,
            top_p=top_p,
            truncation_strategy=truncation_strategy,
            event_handler=event_handler,
            **kwargs,
        )
        data = response
        return data


class AsyncMessages(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    async def create(
        self,
        thread_id,
        *,
        content: Union[str, Any],
        role: Any,
        attachments: Union[Any, NotGiven] = NOT_GIVEN,
        metadata: Union[Optional[object], NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> ThreadMessage:
        response = (
            await self.openai_client.with_raw_response.beta.threads.messages.create(
                thread_id=thread_id,
                content=content,
                role=role,
                attachments=attachments,
                metadata=metadata,
                **kwargs,
            )
        )
        data = ThreadMessage(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def retrieve(self, thread_id, message_id, **kwargs) -> ThreadMessage:
        if kwargs:
            response = await self.openai_client.with_raw_response.beta.threads.messages.retrieve(  # noqa: E501
                thread_id=thread_id, message_id=message_id, extra_body=kwargs
            )
        else:
            response = await self.openai_client.with_raw_response.beta.threads.messages.retrieve(  # noqa: E501
                thread_id=thread_id, message_id=message_id
            )
        data = ThreadMessage(**json.loads(response.text))
        data._headers = response.headers
        return data

    async def update(
        self,
        thread_id,
        message_id,
        *,
        metadata: Union[Optional[object], NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> ThreadMessage:
        response = (
            await self.openai_client.with_raw_response.beta.threads.messages.update(
                thread_id=thread_id, message_id=message_id, metadata=metadata, **kwargs
            )
        )
        data = ThreadMessage(**json.loads(response.text))
        data._headers = response.headers
        return data

    async def list(
        self,
        thread_id,
        *,
        after: Union[str, NotGiven] = NOT_GIVEN,
        before: Union[str, NotGiven] = NOT_GIVEN,
        limit: Union[int, NotGiven] = NOT_GIVEN,
        order: Union[NotGiven, Literal["asc", "desc"]] = NOT_GIVEN,
        run_id: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> MessageList:
        response = (
            await self.openai_client.with_raw_response.beta.threads.messages.list(
                thread_id=thread_id,
                after=after,
                before=before,
                limit=limit,
                order=order,
                run_id=run_id,
                **kwargs,
            )
        )
        data = MessageList(**json.loads(response.text))
        data._headers = response.headers
        return data

    async def delete(
        self, message_id: str, *, thread_id: str, **kwargs
    ) -> ThreadMessageDeleted:
        response = (
            await self.openai_client.with_raw_response.beta.threads.messages.delete(
                message_id=message_id, thread_id=thread_id, **kwargs
            )
        )
        data = ThreadMessageDeleted(**json.loads(response.text))
        data._headers = response.headers

        return data


class AsyncRuns(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.steps = AsyncSteps(client)

    async def stream_create(
        self,
        thread_id,
        assistant_id,
        **kwargs,
    ) -> Union[Run, AsyncIterator[AssistantStreamEvent]]:
        async with self.openai_client.with_streaming_response.beta.threads.runs.create(  # noqa: E501
            thread_id=thread_id,
            assistant_id=assistant_id,
            stream=True,
            extra_body=kwargs,
        ) as response:
            async for line in response.iter_lines():
                json_string = line.replace("data: ", "")
                json_string = json_string.strip().rstrip("\n")
                if json_string == "[DONE]":
                    break
                elif json_string == "":
                    continue
                elif json_string != "":
                    yield json_string
                else:
                    pass

    async def normal_create(
        self,
        thread_id,
        assistant_id,
        **kwargs,
    ) -> Run:
        response = await self.openai_client.with_raw_response.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id,
            extra_body=kwargs,
        )
        data = Run(**json.loads(response.text))
        data._headers = response.headers
        return data

    async def create(
        self,
        thread_id: str,
        *,
        assistant_id: str,
        stream: Union[bool, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> Union[Run, AsyncIterator[AssistantStreamEvent]]:
        if stream is True:
            return self.stream_create(thread_id, assistant_id, **kwargs)
        else:
            return await self.normal_create(thread_id, assistant_id, **kwargs)

    async def retrieve(self, thread_id, run_id, **kwargs) -> Run:
        if kwargs:
            response = (
                await self.openai_client.with_raw_response.beta.threads.runs.retrieve(
                    thread_id=thread_id, run_id=run_id, extra_body=kwargs
                )
            )
        else:
            response = (
                await self.openai_client.with_raw_response.beta.threads.runs.retrieve(
                    thread_id=thread_id, run_id=run_id
                )
            )
        data = Run(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def update(
        self,
        thread_id,
        run_id,
        metadata: Union[Optional[object], NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> Run:
        response = await self.openai_client.with_raw_response.beta.threads.runs.update(
            thread_id=thread_id, run_id=run_id, metadata=metadata, extra_body=kwargs
        )
        data = Run(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def list(
        self,
        thread_id,
        *,
        after: Union[str, NotGiven] = NOT_GIVEN,
        before: Union[str, NotGiven] = NOT_GIVEN,
        limit: Union[int, NotGiven] = NOT_GIVEN,
        order: Union[NotGiven, Literal["asc", "desc"]] = NOT_GIVEN,
        **kwargs,
    ) -> RunList:
        response = await self.openai_client.with_raw_response.beta.threads.runs.list(
            thread_id=thread_id,
            after=after,
            before=before,
            limit=limit,
            order=order,
            **kwargs,
        )
        data = RunList(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def cancel(self, thread_id, run_id, **kwargs) -> Run:
        response = await self.openai_client.with_raw_response.beta.threads.runs.cancel(
            thread_id=thread_id, run_id=run_id, extra_body=kwargs
        )
        data = Run(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def create_and_poll(
        self,
        *,
        assistant_id: str,
        include: Union[List[Any], NotGiven] = NOT_GIVEN,
        additional_instructions: Union[Optional[str], NotGiven] = NOT_GIVEN,
        additional_messages: Union[
            Optional[Iterable[run_create_params.AdditionalMessage]], NotGiven
        ] = NOT_GIVEN,
        instructions: Union[Optional[str], NotGiven] = NOT_GIVEN,
        max_completion_tokens: Union[Optional[int], NotGiven] = NOT_GIVEN,
        max_prompt_tokens: Union[Optional[int], NotGiven] = NOT_GIVEN,
        metadata: Union[Optional[object], NotGiven] = NOT_GIVEN,
        model: Union[str, None, NotGiven] = NOT_GIVEN,
        parallel_tool_calls: Union[bool, NotGiven] = NOT_GIVEN,
        response_format: Union[
            Optional[AssistantResponseFormatOptionParam], NotGiven
        ] = NOT_GIVEN,
        temperature: Union[Optional[float], NotGiven] = NOT_GIVEN,
        tool_choice: Union[
            Optional[AssistantToolChoiceOptionParam], NotGiven
        ] = NOT_GIVEN,
        tools: Union[Optional[Iterable[AssistantToolParam]], NotGiven] = NOT_GIVEN,
        top_p: Union[Optional[float], NotGiven] = NOT_GIVEN,
        truncation_strategy: Union[
            Optional[run_create_params.TruncationStrategy], NotGiven
        ] = NOT_GIVEN,
        poll_interval_ms: Union[int, NotGiven] = NOT_GIVEN,
        thread_id: str,
        **kwargs,
    ) -> Run:
        response = await self.openai_client.beta.threads.runs.create_and_poll(
            assistant_id=assistant_id,
            include=include,
            additional_instructions=additional_instructions,
            additional_messages=additional_messages,
            instructions=instructions,
            max_completion_tokens=max_completion_tokens,
            max_prompt_tokens=max_prompt_tokens,
            metadata=metadata,
            model=model,
            parallel_tool_calls=parallel_tool_calls,
            response_format=response_format,
            temperature=temperature,
            tool_choice=tool_choice,
            tools=tools,
            top_p=top_p,
            truncation_strategy=truncation_strategy,
            poll_interval_ms=poll_interval_ms,
            thread_id=thread_id,
            extra_body=kwargs,
        )
        data = response

        return data  # type: ignore[return-value]

    @typing.no_type_check
    async def create_and_stream(
        self,
        *,
        assistant_id: str,
        additional_instructions: Union[Optional[str], NotGiven] = NOT_GIVEN,
        additional_messages: Union[
            Optional[Iterable[run_create_params.AdditionalMessage]], NotGiven
        ] = NOT_GIVEN,
        instructions: Union[Optional[str], NotGiven] = NOT_GIVEN,
        max_completion_tokens: Union[Optional[int], NotGiven] = NOT_GIVEN,
        max_prompt_tokens: Union[Optional[int], NotGiven] = NOT_GIVEN,
        metadata: Union[Optional[object], NotGiven] = NOT_GIVEN,
        model: Union[str, None, NotGiven] = NOT_GIVEN,
        parallel_tool_calls: Union[bool, NotGiven] = NOT_GIVEN,
        response_format: Union[
            Optional[AssistantResponseFormatOptionParam], NotGiven
        ] = NOT_GIVEN,
        temperature: Union[Optional[float], NotGiven] = NOT_GIVEN,
        tool_choice: Union[
            Optional[AssistantToolChoiceOptionParam], NotGiven
        ] = NOT_GIVEN,
        tools: Union[Optional[Iterable[AssistantToolParam]], NotGiven] = NOT_GIVEN,
        top_p: Union[Optional[float], NotGiven] = NOT_GIVEN,
        truncation_strategy: Union[
            Optional[run_create_params.TruncationStrategy], NotGiven
        ] = NOT_GIVEN,
        thread_id: str,
        event_handler: Union[AsyncAssistantEventHandlerT, None] = None,
        **kwargs,
    ) -> (
        Union[
            AsyncAssistantStreamManager[AsyncAssistantEventHandler],
            AsyncAssistantStreamManager[AsyncAssistantEventHandlerT],
        ]
    ):
        response = await self.openai_client.beta.threads.runs.create_and_stream(
            assistant_id=assistant_id,
            additional_instructions=additional_instructions,
            additional_messages=additional_messages,
            instructions=instructions,
            max_completion_tokens=max_completion_tokens,
            max_prompt_tokens=max_prompt_tokens,
            metadata=metadata,
            model=model,
            parallel_tool_calls=parallel_tool_calls,
            response_format=response_format,
            temperature=temperature,
            tool_choice=tool_choice,
            tools=tools,
            top_p=top_p,
            truncation_strategy=truncation_strategy,
            thread_id=thread_id,
            event_handler=event_handler,
            extra_body=kwargs,
        )
        data = response
        return data

    async def poll(
        self,
        *,
        run_id: str,
        thread_id: str,
        **kwargs,
    ) -> Run:
        response = await self.openai_client.beta.threads.runs.poll(
            run_id=run_id, thread_id=thread_id, extra_body=kwargs
        )
        data = response

        return data  # type: ignore[return-value]

    @typing.no_type_check
    async def stream(
        self,
        *,
        assistant_id: str,
        include: Union[List[Any], NotGiven] = NOT_GIVEN,
        additional_instructions: Union[Optional[str], NotGiven] = NOT_GIVEN,
        additional_messages: Union[
            Optional[Iterable[run_create_params.AdditionalMessage]], NotGiven
        ] = NOT_GIVEN,
        instructions: Union[Optional[str], NotGiven] = NOT_GIVEN,
        max_completion_tokens: Union[Optional[int], NotGiven] = NOT_GIVEN,
        max_prompt_tokens: Union[Optional[int], NotGiven] = NOT_GIVEN,
        metadata: Union[Optional[object], NotGiven] = NOT_GIVEN,
        model: Union[str, None, NotGiven] = NOT_GIVEN,
        parallel_tool_calls: Union[bool, NotGiven] = NOT_GIVEN,
        response_format: Union[
            Optional[AssistantResponseFormatOptionParam], NotGiven
        ] = NOT_GIVEN,
        temperature: Union[Optional[float], NotGiven] = NOT_GIVEN,
        tool_choice: Union[
            Optional[AssistantToolChoiceOptionParam], NotGiven
        ] = NOT_GIVEN,
        tools: Union[Optional[Iterable[AssistantToolParam]], NotGiven] = NOT_GIVEN,
        top_p: Union[Optional[float], NotGiven] = NOT_GIVEN,
        truncation_strategy: Union[
            Optional[run_create_params.TruncationStrategy], NotGiven
        ] = NOT_GIVEN,
        thread_id: str,
        event_handler: Union[AsyncAssistantEventHandlerT, None] = None,
        **kwargs,
    ) -> (
        Union[
            AsyncAssistantStreamManager[AsyncAssistantEventHandler],
            AsyncAssistantStreamManager[AsyncAssistantEventHandlerT],
        ]
    ):
        response = await self.openai_client.beta.threads.runs.stream(
            assistant_id=assistant_id,
            include=include,
            additional_instructions=additional_instructions,
            additional_messages=additional_messages,
            instructions=instructions,
            max_completion_tokens=max_completion_tokens,
            max_prompt_tokens=max_prompt_tokens,
            metadata=metadata,
            model=model,
            parallel_tool_calls=parallel_tool_calls,
            response_format=response_format,
            temperature=temperature,
            tool_choice=tool_choice,
            tools=tools,
            top_p=top_p,
            truncation_strategy=truncation_strategy,
            thread_id=thread_id,
            event_handler=event_handler,
            extra_body=kwargs,
        )
        data = response
        return data

    async def submit_tool_outputs(
        self,
        run_id,
        *,
        thread_id,
        tool_outputs,
        stream: Union[bool, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> Run:
        # fmt: off
        response = await self.openai_client\
            .with_raw_response\
            .beta\
            .threads\
            .runs\
            .submit_tool_outputs(
                thread_id=thread_id,
                run_id=run_id,
                tool_outputs=tool_outputs,
                stream=stream,
                **kwargs
        )
        # fmt: on
        data = Run(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def submit_tool_outputs_and_poll(
        self,
        *,
        tool_outputs: Union[Iterable[run_submit_tool_outputs_params.ToolOutput]],
        run_id: str,
        thread_id: str,
        poll_interval_ms: Union[int, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> Run:
        response = (
            await self.openai_client.beta.threads.runs.submit_tool_outputs_and_poll(
                tool_outputs=tool_outputs,
                run_id=run_id,
                thread_id=thread_id,
                poll_interval_ms=poll_interval_ms,
                extra_body=kwargs,
            )
        )
        data = response

        return data  # type: ignore[return-value]

    def submit_tool_outputs_stream(
        self,
        *,
        tool_outputs: Union[Iterable[run_submit_tool_outputs_params.ToolOutput]],
        run_id: str,
        thread_id: str,
        event_handler: Union[AsyncAssistantEventHandlerT, None] = None,
        **kwargs,
    ) -> Union[
        AsyncAssistantStreamManager[AsyncAssistantEventHandler],
        AsyncAssistantStreamManager[AsyncAssistantEventHandlerT],
    ]:
        response = self.openai_client.beta.threads.runs.submit_tool_outputs_stream(  # type: ignore[type-var]
            tool_outputs=tool_outputs,
            run_id=run_id,
            thread_id=thread_id,
            event_handler=event_handler,
            extra_body=kwargs,
        )
        data = response

        return data  # type: ignore[return-value]


class AsyncSteps(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    async def retrieve(
        self,
        thread_id,
        run_id,
        step_id,
        include: Union[List[Any], NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> RunStep:
        if kwargs:
            response = await self.openai_client.with_raw_response.beta.threads.runs.steps.retrieve(  # noqa: E501
                thread_id=thread_id,
                run_id=run_id,
                step_id=step_id,
                include=include,
                extra_body=kwargs,
            )
        else:
            response = await self.openai_client.with_raw_response.beta.threads.runs.steps.retrieve(  # noqa: E501
                thread_id=thread_id, run_id=run_id, step_id=step_id, include=include
            )
        data = RunStep(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def list(
        self,
        run_id,
        *,
        thread_id,
        after: Union[str, NotGiven] = NOT_GIVEN,
        before: Union[str, NotGiven] = NOT_GIVEN,
        include: Union[List[Any], NotGiven] = NOT_GIVEN,
        limit: Union[int, NotGiven] = NOT_GIVEN,
        order: Union[Any, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> RunStepList:
        response = (
            await self.openai_client.with_raw_response.beta.threads.runs.steps.list(
                thread_id=thread_id,
                run_id=run_id,
                after=after,
                before=before,
                include=include,
                limit=limit,
                order=order,
                **kwargs,
            )
        )
        data = RunStepList(**json.loads(response.text))
        data._headers = response.headers

        return data
