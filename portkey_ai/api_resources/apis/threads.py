import json
from typing import Iterable, Optional, Union

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
from openai._types import NotGiven, NOT_GIVEN
from openai.types.beta import thread_create_and_run_params
from openai.types.beta.assistant_response_format_option_param import AssistantResponseFormatOptionParam
from openai.types.beta.assistant_tool_choice_option_param import AssistantToolChoiceOptionParam
from openai.lib.streaming import (
    AssistantEventHandler,
    AssistantEventHandlerT,
    AssistantStreamManager,
    AsyncAssistantEventHandler,
    AsyncAssistantEventHandlerT,
    AsyncAssistantStreamManager,
)
from openai.types.beta.threads import (
    run_create_params,
    run_submit_tool_outputs_params,
)
from openai.types.beta.assistant_tool_param import AssistantToolParam

class Threads(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.messages = Messages(client)
        self.runs = Runs(client)

    def create(
        self,
    ) -> Thread:
        response = self.openai_client.with_raw_response.beta.threads.create()
        data = Thread(**json.loads(response.text))
        data._headers = response.headers

        return data

    def retrieve(self, thread_id, **kwargs) -> Thread:
        response = self.openai_client.with_raw_response.beta.threads.retrieve(
            thread_id=thread_id, **kwargs
        )
        data = Thread(**json.loads(response.text))
        data._headers = response.headers

        return data

    def update(self, thread_id, **kwargs) -> Thread:
        response = self.openai_client.with_raw_response.beta.threads.update(
            thread_id=thread_id, **kwargs
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

    def create_and_run(self, assistant_id, **kwargs) -> Run:
        response = self.openai_client.with_raw_response.beta.threads.create_and_run(
            assistant_id=assistant_id, **kwargs
        )
        data = Run(**json.loads(response.text))
        data._headers = response.headers
        return data

    def create_and_run_poll(
        self,
        *,
        assistant_id: str,
        instructions: Optional[str] | NotGiven = NOT_GIVEN,
        max_completion_tokens: Optional[int] | NotGiven = NOT_GIVEN,
        max_prompt_tokens: Optional[int] | NotGiven = NOT_GIVEN,
        metadata: Optional[object] | NotGiven = NOT_GIVEN,
        model: Union[str, None, NotGiven] = NOT_GIVEN,
        response_format: Union[Optional[AssistantResponseFormatOptionParam] , NotGiven] = NOT_GIVEN,
        temperature: Union[Optional[float], NotGiven] = NOT_GIVEN,
        thread: Union[thread_create_and_run_params.Thread, NotGiven] = NOT_GIVEN,
        tool_choice: Union[Optional[AssistantToolChoiceOptionParam], NotGiven] = NOT_GIVEN,
        tool_resources: Union[Optional[thread_create_and_run_params.ToolResources], NotGiven] = NOT_GIVEN,
        tools: Union[Optional[Iterable[thread_create_and_run_params.Tool]], NotGiven] = NOT_GIVEN,
        top_p: Union[Optional[float], NotGiven] = NOT_GIVEN,
        truncation_strategy: Union[Optional[thread_create_and_run_params.TruncationStrategy], NotGiven] = NOT_GIVEN,
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
            **kwargs
        )
        data = Run(**json.loads(response.text))
        data._headers = response.headers

        return data

    def create_and_run_stream(
        self,
        *,
        assistant_id: str,
        instructions: Union[Optional[str], NotGiven] = NOT_GIVEN,
        max_completion_tokens: Union[Optional[int], NotGiven] = NOT_GIVEN,
        max_prompt_tokens: Union[Optional[int], NotGiven] = NOT_GIVEN,
        metadata: Union[Optional[object], NotGiven] = NOT_GIVEN,
        model: Union[str, None, NotGiven] = NOT_GIVEN,
        response_format: Union[Optional[AssistantResponseFormatOptionParam], NotGiven] = NOT_GIVEN,
        temperature: Union[Optional[float], NotGiven] = NOT_GIVEN,
        thread: Union[thread_create_and_run_params.Thread, NotGiven] = NOT_GIVEN,
        tool_choice: Union[Optional[AssistantToolChoiceOptionParam], NotGiven] = NOT_GIVEN,
        tool_resources: Union[Optional[thread_create_and_run_params.ToolResources], NotGiven] = NOT_GIVEN,
        tools: Union[Optional[Iterable[thread_create_and_run_params.Tool]], NotGiven] = NOT_GIVEN,
        top_p: Union[Optional[float], NotGiven] = NOT_GIVEN,
        truncation_strategy: Union[Optional[thread_create_and_run_params.TruncationStrategy], NotGiven] = NOT_GIVEN,
        event_handler: Union[AssistantEventHandlerT, None] = None,
        **kwargs,
        ) -> AssistantStreamManager[AssistantEventHandler] | AssistantStreamManager[AssistantEventHandlerT]:

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
            **kwargs
        )
        data = response
        return data


class Messages(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    def create(self, thread_id, **kwargs) -> ThreadMessage:
        response = self.openai_client.with_raw_response.beta.threads.messages.create(
            thread_id=thread_id, **kwargs
        )
        data = ThreadMessage(**json.loads(response.text))
        data._headers = response.headers

        return data

    def list(self, thread_id, **kwargs) -> MessageList:
        response = self.openai_client.with_raw_response.beta.threads.messages.list(
            thread_id=thread_id, **kwargs
        )
        data = MessageList(**json.loads(response.text))
        data._headers = response.headers
        return data

    def retrieve(self, thread_id, message_id, **kwargs) -> ThreadMessage:
        response = self.openai_client.with_raw_response.beta.threads.messages.retrieve(
            thread_id=thread_id, message_id=message_id, **kwargs
        )
        data = ThreadMessage(**json.loads(response.text))
        data._headers = response.headers
        return data

    def update(self, thread_id, message_id, **kwargs) -> ThreadMessage:
        response = self.openai_client.with_raw_response.beta.threads.messages.update(
            thread_id=thread_id, message_id=message_id, **kwargs
        )
        data = ThreadMessage(**json.loads(response.text))
        data._headers = response.headers
        return data

    def delete(
            self,
            message_id: str,
            *,
            thread_id: str,
            **kwargs
    ) -> ThreadMessageDeleted:
        response = self.openai_client.with_raw_response.beta.threads.messages.delete(
            message_id=message_id,
            thread_id=thread_id,
            **kwargs
        )
        data = ThreadMessageDeleted(**json.loads(response.text))
        data._headers = response.headers

        return data
        

# class ThreadFiles(APIResource):
#     def __init__(self, client: Portkey) -> None:
#         super().__init__(client)
#         self.openai_client = client.openai_client

#     def list(self, thread_id, message_id, **kwargs) -> MessageList:
#         response = (
#             self.openai_client.with_raw_response.beta.threads.messages.files.list(
#                 thread_id=thread_id, message_id=message_id, **kwargs
#             )
#         )
#         data = MessageList(**json.loads(response.text))
#         data._headers = response.headers

#         return data

#     def retrieve(self, thread_id, message_id, file_id, **kwargs) -> MessageFile:
#         response = (
#             self.openai_client.with_raw_response.beta.threads.messages.files.retrieve(
#                 thread_id=thread_id, message_id=message_id, file_id=file_id, **kwargs
#             )
#         )
#         data = MessageFile(**json.loads(response.text))
#         data._headers = response.headers

#         return data


class Runs(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.steps = Steps(client)

    def create(self, **kwargs) -> Run:
        response = self.openai_client.with_raw_response.beta.threads.runs.create(
            **kwargs
        )
        data = Run(**json.loads(response.text))
        data._headers = response.headers

        return data

    def retrieve(self, thread_id, run_id, **kwargs) -> Run:
        response = self.openai_client.with_raw_response.beta.threads.runs.retrieve(
            thread_id=thread_id, run_id=run_id, **kwargs
        )
        data = Run(**json.loads(response.text))
        data._headers = response.headers

        return data

    def list(self, thread_id, **kwargs) -> RunList:
        response = self.openai_client.with_raw_response.beta.threads.runs.list(
            thread_id=thread_id, **kwargs
        )
        data = RunList(**json.loads(response.text))
        data._headers = response.headers

        return data

    def update(self, thread_id, run_id, **kwargs) -> Run:
        response = self.openai_client.with_raw_response.beta.threads.runs.update(
            thread_id=thread_id, run_id=run_id, **kwargs
        )
        data = Run(**json.loads(response.text))
        data._headers = response.headers

        return data

    def submit_tool_outputs(self, thread_id, tool_outputs, run_id, **kwargs) -> Run:
        response = (
            self.openai_client.with_raw_response.beta.threads.runs.submit_tool_outputs(
                thread_id=thread_id, run_id=run_id, tool_outputs=tool_outputs, **kwargs
            )
        )
        data = Run(**json.loads(response.text))
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
        additional_instructions: Union[Optional[str], NotGiven] = NOT_GIVEN,
        additional_messages: Union[Optional[Iterable[run_create_params.AdditionalMessage]], NotGiven] = NOT_GIVEN,
        instructions: Union[Optional[str], NotGiven] = NOT_GIVEN,
        max_completion_tokens: Union[Optional[int], NotGiven] = NOT_GIVEN,
        max_prompt_tokens: Union[Optional[int], NotGiven] = NOT_GIVEN,
        metadata: Union[Optional[object], NotGiven] = NOT_GIVEN,
        model: Union[str, None, NotGiven] = NOT_GIVEN,
        response_format: Union[Optional[AssistantResponseFormatOptionParam], NotGiven] = NOT_GIVEN,
        temperature: Union[Optional[float], NotGiven] = NOT_GIVEN,
        tool_choice: Union[Optional[AssistantToolChoiceOptionParam], NotGiven] = NOT_GIVEN,
        tools: Union[Optional[Iterable[AssistantToolParam]], NotGiven] = NOT_GIVEN,
        top_p: Union[Optional[float], NotGiven] = NOT_GIVEN,
        truncation_strategy: Union[Optional[run_create_params.TruncationStrategy], NotGiven] = NOT_GIVEN,
        poll_interval_ms: Union[int, NotGiven] = NOT_GIVEN,
        thread_id: str,
        **kwargs,
    )-> Run:
        response = self.openai_client.beta.threads.runs.create_and_poll(
            assistant_id=assistant_id,
            additional_instructions=additional_instructions,
            additional_messages=additional_messages,
            instructions=instructions,
            max_completion_tokens=max_completion_tokens,
            max_prompt_tokens=max_prompt_tokens,
            metadata=metadata,
            model=model,
            response_format=response_format,
            temperature=temperature,
            tool_choice=tool_choice,
            tools=tools,
            top_p=top_p,
            truncation_strategy=truncation_strategy,
            poll_interval_ms=poll_interval_ms,
            thread_id=thread_id,
            **kwargs
        )
        data = Run(**json.loads(response.text))
        data._headers = response.headers

        return data

    def create_and_stream(
            self,
        *,
        assistant_id: str,
        additional_instructions: Union[Optional[str], NotGiven] = NOT_GIVEN,
        additional_messages: Union[Optional[Iterable[run_create_params.AdditionalMessage]], NotGiven] = NOT_GIVEN,
        instructions: Union[Optional[str], NotGiven] = NOT_GIVEN,
        max_completion_tokens: Union[Optional[int], NotGiven] = NOT_GIVEN,
        max_prompt_tokens: Union[Optional[int], NotGiven] = NOT_GIVEN,
        metadata: Union[Optional[object], NotGiven] = NOT_GIVEN,
        model: Union[str, None, NotGiven] = NOT_GIVEN,
        response_format: Union[Optional[AssistantResponseFormatOptionParam], NotGiven] = NOT_GIVEN,
        temperature: Union[Optional[float], NotGiven] = NOT_GIVEN,
        tool_choice: Union[Optional[AssistantToolChoiceOptionParam], NotGiven] = NOT_GIVEN,
        tools: Union[Optional[Iterable[AssistantToolParam]], NotGiven] = NOT_GIVEN,
        top_p: Union[Optional[float], NotGiven] = NOT_GIVEN,
        truncation_strategy: Union[Optional[run_create_params.TruncationStrategy], NotGiven] = NOT_GIVEN,
        thread_id: str,
        event_handler: Union[AssistantEventHandlerT, None] = None,
        **kwargs,
    )-> AssistantStreamManager[AssistantEventHandler] | AssistantStreamManager[AssistantEventHandlerT]:
        response = self.openai_client.beta.threads.runs.create_and_stream(
            assistant_id=assistant_id,
            additional_instructions=additional_instructions,
            additional_messages=additional_messages,
            instructions=instructions,
            max_completion_tokens=max_completion_tokens,
            max_prompt_tokens=max_prompt_tokens,
            metadata=metadata,
            model=model,
            response_format=response_format,
            temperature=temperature,
            tool_choice=tool_choice,
            tools=tools,
            top_p=top_p,
            truncation_strategy=truncation_strategy,
            thread_id=thread_id,
            event_handler=event_handler,
            **kwargs
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
            run_id=run_id,
            thread_id=thread_id,
            **kwargs
        )
        data = response

        return data

    def stream(
        self,
        *,
        assistant_id: str,
        additional_instructions: Union[Optional[str], NotGiven] = NOT_GIVEN,
        additional_messages: Union[Optional[Iterable[run_create_params.AdditionalMessage]], NotGiven] = NOT_GIVEN,
        instructions: Union[Optional[str], NotGiven] = NOT_GIVEN,
        max_completion_tokens: Union[Optional[int], NotGiven] = NOT_GIVEN,
        max_prompt_tokens: Union[Optional[int], NotGiven] = NOT_GIVEN,
        metadata: Union[Optional[object], NotGiven] = NOT_GIVEN,
        model: Union[str, None, NotGiven] = NOT_GIVEN,
        response_format: Union[Optional[AssistantResponseFormatOptionParam], NotGiven] = NOT_GIVEN,
        temperature: Union[Optional[float], NotGiven] = NOT_GIVEN,
        tool_choice: Union[Optional[AssistantToolChoiceOptionParam], NotGiven] = NOT_GIVEN,
        tools: Union[Optional[Iterable[AssistantToolParam]], NotGiven] = NOT_GIVEN,
        top_p: Union[Optional[float], NotGiven] = NOT_GIVEN,
        truncation_strategy: Union[Optional[run_create_params.TruncationStrategy], NotGiven] = NOT_GIVEN,
        thread_id: str,
        event_handler: Union[AssistantEventHandlerT, None] = None,
        **kwargs,
    )-> AssistantStreamManager[AssistantEventHandler] | AssistantStreamManager[AssistantEventHandlerT]:
        
        response = self.openai_client.beta.threads.runs.stream(
            assistant_id=assistant_id,
            additional_instructions=additional_instructions,
            additional_messages=additional_messages,
            instructions=instructions,
            max_completion_tokens=max_completion_tokens,
            max_prompt_tokens=max_prompt_tokens,
            metadata=metadata,
            model=model,
            response_format=response_format,
            temperature=temperature,
            tool_choice=tool_choice,
            tools=tools,
            top_p=top_p,
            truncation_strategy=truncation_strategy,
            thread_id=thread_id,
            event_handler=event_handler,
            **kwargs
        )
        data = response
        return data

    def submit_tool_outputs_and_poll(
        self,
        *,
        tool_outputs: Union[Iterable[run_submit_tool_outputs_params.ToolOutput]],
        run_id: str,
        thread_id: str,
        poll_interval_ms: Union[int,  NotGiven] = NOT_GIVEN,  
    )-> Run:
        response = self.openai_client.beta.threads.runs.submit_tool_outputs_and_poll(
            tool_outputs=tool_outputs,
            run_id=run_id,
            thread_id=thread_id,
            poll_interval_ms=poll_interval_ms
        )
        data = response

        return data

    def submit_tool_outputs_stream(
        self,
        *,
        tool_outputs: Union[Iterable[run_submit_tool_outputs_params.ToolOutput]],
        run_id: str,
        thread_id: str,
        event_handler: Union[AssistantEventHandlerT, None] = None,  
    ) -> AssistantStreamManager[AssistantEventHandler] | AssistantStreamManager[AssistantEventHandlerT]:
        response = self.openai_client.beta.threads.runs.submit_tool_outputs_stream(
            tool_outputs=tool_outputs,
            run_id=run_id,
            thread_id=thread_id,
            event_handler=event_handler
        )
        data = response

        return data

class Steps(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    def list(self, thread_id, run_id, **kwargs) -> RunStepList:
        response = self.openai_client.with_raw_response.beta.threads.runs.steps.list(
            thread_id=thread_id, run_id=run_id, **kwargs
        )
        data = RunStepList(**json.loads(response.text))
        data._headers = response.headers

        return data

    def retrieve(self, thread_id, run_id, step_id, **kwargs) -> RunStep:
        response = (
            self.openai_client.with_raw_response.beta.threads.runs.steps.retrieve(
                thread_id=thread_id, run_id=run_id, step_id=step_id, **kwargs
            )
        )
        data = RunStep(**json.loads(response.text))
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
    ) -> Thread:
        response = await self.openai_client.with_raw_response.beta.threads.create()
        data = Thread(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def retrieve(self, thread_id, **kwargs) -> Thread:
        response = await self.openai_client.with_raw_response.beta.threads.retrieve(
            thread_id=thread_id, **kwargs
        )
        data = Thread(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def update(self, thread_id, **kwargs) -> Thread:
        response = await self.openai_client.with_raw_response.beta.threads.update(
            thread_id=thread_id, **kwargs
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

    async def create_and_run(self, assistant_id, **kwargs) -> Run:
        response = (
            await self.openai_client.with_raw_response.beta.threads.create_and_run(
                assistant_id=assistant_id, **kwargs
            )
        )
        data = Run(**json.loads(response.text))
        data._headers = response.headers
        return data

    async def create_and_run_poll(
        self,
        *,
        assistant_id: str,
        instructions: Optional[str] | NotGiven = NOT_GIVEN,
        max_completion_tokens: Optional[int] | NotGiven = NOT_GIVEN,
        max_prompt_tokens: Optional[int] | NotGiven = NOT_GIVEN,
        metadata: Optional[object] | NotGiven = NOT_GIVEN,
        model: Union[str, None, NotGiven] = NOT_GIVEN,
        response_format: Union[Optional[AssistantResponseFormatOptionParam] , NotGiven] = NOT_GIVEN,
        temperature: Union[Optional[float], NotGiven] = NOT_GIVEN,
        thread: Union[thread_create_and_run_params.Thread, NotGiven] = NOT_GIVEN,
        tool_choice: Union[Optional[AssistantToolChoiceOptionParam], NotGiven] = NOT_GIVEN,
        tool_resources: Union[Optional[thread_create_and_run_params.ToolResources], NotGiven] = NOT_GIVEN,
        tools: Union[Optional[Iterable[thread_create_and_run_params.Tool]], NotGiven] = NOT_GIVEN,
        top_p: Union[Optional[float], NotGiven] = NOT_GIVEN,
        truncation_strategy: Union[Optional[thread_create_and_run_params.TruncationStrategy], NotGiven] = NOT_GIVEN,
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
            **kwargs
        )
        data = Run(**json.loads(response.text))
        data._headers = response.headers

        return data
    
    async def create_and_run_stream(
        self,
        *,
        assistant_id: str,
        instructions: Union[Optional[str], NotGiven] = NOT_GIVEN,
        max_completion_tokens: Union[Optional[int], NotGiven] = NOT_GIVEN,
        max_prompt_tokens: Union[Optional[int], NotGiven] = NOT_GIVEN,
        metadata: Union[Optional[object], NotGiven] = NOT_GIVEN,
        model: Union[str, None, NotGiven] = NOT_GIVEN,
        response_format: Union[Optional[AssistantResponseFormatOptionParam], NotGiven] = NOT_GIVEN,
        temperature: Union[Optional[float], NotGiven] = NOT_GIVEN,
        thread: Union[thread_create_and_run_params.Thread, NotGiven] = NOT_GIVEN,
        tool_choice: Union[Optional[AssistantToolChoiceOptionParam], NotGiven] = NOT_GIVEN,
        tool_resources: Union[Optional[thread_create_and_run_params.ToolResources], NotGiven] = NOT_GIVEN,
        tools: Union[Optional[Iterable[thread_create_and_run_params.Tool]], NotGiven] = NOT_GIVEN,
        top_p: Union[Optional[float], NotGiven] = NOT_GIVEN,
        truncation_strategy: Union[Optional[thread_create_and_run_params.TruncationStrategy], NotGiven] = NOT_GIVEN,
        event_handler: Union[AsyncAssistantEventHandlerT, None] = None,
        **kwargs,
    ) -> (
        AsyncAssistantStreamManager[AsyncAssistantEventHandler]
        | AsyncAssistantStreamManager[AsyncAssistantEventHandlerT]
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
            **kwargs
        )
        data = response
        return data


class AsyncMessages(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    async def create(self, thread_id, **kwargs) -> ThreadMessage:
        response = (
            await self.openai_client.with_raw_response.beta.threads.messages.create(
                thread_id=thread_id, **kwargs
            )
        )
        data = ThreadMessage(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def list(self, thread_id, **kwargs) -> MessageList:
        response = (
            await self.openai_client.with_raw_response.beta.threads.messages.list(
                thread_id=thread_id, **kwargs
            )
        )
        data = MessageList(**json.loads(response.text))
        data._headers = response.headers
        return data

    async def retrieve(self, thread_id, message_id, **kwargs) -> ThreadMessage:
        response = (
            await self.openai_client.with_raw_response.beta.threads.messages.retrieve(
                thread_id=thread_id, message_id=message_id, **kwargs
            )
        )
        data = ThreadMessage(**json.loads(response.text))
        data._headers = response.headers
        return data

    async def update(self, thread_id, message_id, **kwargs) -> ThreadMessage:
        response = (
            await self.openai_client.with_raw_response.beta.threads.messages.update(
                thread_id=thread_id, message_id=message_id, **kwargs
            )
        )
        data = ThreadMessage(**json.loads(response.text))
        data._headers = response.headers
        return data

    async def delete(
        self,
        message_id: str,
        *,
        thread_id: str,
        **kwargs
    ) -> ThreadMessageDeleted:
        response = (
            await self.openai_client.with_raw_response.beta.threads.messages.delete(
                message_id=message_id,
                thread_id=thread_id,
                **kwargs
            )
        )
        data = ThreadMessageDeleted(**json.loads(response.text))
        data._headers = response.headers

        return data


# class AsyncThreadFiles(AsyncAPIResource):
#     def __init__(self, client: AsyncPortkey) -> None:
#         super().__init__(client)
#         self.openai_client = client.openai_client

#     async def list(self, thread_id, message_id, **kwargs) -> MessageList:
#         response = (
#             await self.openai_client.with_raw_response.beta.threads.messages.files.list(
#                 thread_id=thread_id, message_id=message_id, **kwargs
#             )
#         )
#         data = MessageList(**json.loads(response.text))
#         data._headers = response.headers

#         return data

#     async def retrieve(self, thread_id, message_id, file_id, **kwargs) -> MessageFile:
#         # fmt: off
#         response = await self.openai_client\
#             .with_raw_response\
#             .beta\
#             .threads\
#             .messages\
#             .files\
#             .retrieve(
#                 thread_id=thread_id, 
#                 message_id=message_id, 
#                 file_id=file_id, 
#                 **kwargs
#             )
#         # fmt: off
#         data = MessageFile(**json.loads( response.text))
#         data._headers = response.headers

#         return data


class AsyncRuns(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.steps = AsyncSteps(client)

    async def create(self, **kwargs) -> Run:
        response = await self.openai_client.with_raw_response.beta.threads.runs.create(
            **kwargs
        )
        data = Run(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def retrieve(self, thread_id, run_id, **kwargs) -> Run:
        response = (
            await self.openai_client.with_raw_response.beta.threads.runs.retrieve(
                thread_id=thread_id, run_id=run_id, **kwargs
            )
        )
        data = Run(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def list(self, thread_id, **kwargs) -> RunList:
        response = await self.openai_client.with_raw_response.beta.threads.runs.list(
            thread_id=thread_id, **kwargs
        )
        data = RunList(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def update(self, thread_id, run_id, **kwargs) -> Run:
        response = await self.openai_client.with_raw_response.beta.threads.runs.update(
            thread_id=thread_id, run_id=run_id, **kwargs
        )
        data = Run(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def submit_tool_outputs(
        self, thread_id, tool_outputs, run_id, **kwargs
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
                **kwargs
        )
        # fmt: on
        data = Run(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def cancel(self, thread_id, run_id, **kwargs) -> Run:
        response = await self.openai_client.with_raw_response.beta.threads.runs.cancel(
            thread_id=thread_id, run_id=run_id, **kwargs
        )
        data = Run(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def create_and_poll(
        self,
        *,
        assistant_id: str,
        additional_instructions: Union[Optional[str], NotGiven] = NOT_GIVEN,
        additional_messages: Union[Optional[Iterable[run_create_params.AdditionalMessage]], NotGiven] = NOT_GIVEN,
        instructions: Union[Optional[str], NotGiven] = NOT_GIVEN,
        max_completion_tokens: Union[Optional[int], NotGiven] = NOT_GIVEN,
        max_prompt_tokens: Union[Optional[int], NotGiven] = NOT_GIVEN,
        metadata: Union[Optional[object], NotGiven] = NOT_GIVEN,
        model: Union[str, None, NotGiven] = NOT_GIVEN,
        response_format: Union[Optional[AssistantResponseFormatOptionParam], NotGiven] = NOT_GIVEN,
        temperature: Union[Optional[float], NotGiven] = NOT_GIVEN,
        tool_choice: Union[Optional[AssistantToolChoiceOptionParam], NotGiven] = NOT_GIVEN,
        tools: Union[Optional[Iterable[AssistantToolParam]], NotGiven] = NOT_GIVEN,
        top_p: Union[Optional[float], NotGiven] = NOT_GIVEN,
        truncation_strategy: Union[Optional[run_create_params.TruncationStrategy], NotGiven] = NOT_GIVEN,
        poll_interval_ms: Union[int, NotGiven] = NOT_GIVEN,
        thread_id: str,
        **kwargs,
    )-> Run:
        response = await self.openai_client.beta.threads.runs.create_and_poll(
            assistant_id=assistant_id,
            additional_instructions=additional_instructions,
            additional_messages=additional_messages,
            instructions=instructions,
            max_completion_tokens=max_completion_tokens,
            max_prompt_tokens=max_prompt_tokens,
            metadata=metadata,
            model=model,
            response_format=response_format,
            temperature=temperature,
            tool_choice=tool_choice,
            tools=tools,
            top_p=top_p,
            truncation_strategy=truncation_strategy,
            poll_interval_ms=poll_interval_ms,
            thread_id=thread_id,
            **kwargs
        )
        data = Run(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def create_and_stream(
        self,
        *,
        assistant_id: str,
        additional_instructions: Union[Optional[str], NotGiven] = NOT_GIVEN,
        additional_messages: Union[Optional[Iterable[run_create_params.AdditionalMessage]], NotGiven] = NOT_GIVEN,
        instructions: Union[Optional[str], NotGiven] = NOT_GIVEN,
        max_completion_tokens: Union[Optional[int], NotGiven] = NOT_GIVEN,
        max_prompt_tokens: Union[Optional[int], NotGiven] = NOT_GIVEN,
        metadata: Union[Optional[object], NotGiven] = NOT_GIVEN,
        model: Union[str, None, NotGiven] = NOT_GIVEN,
        response_format: Union[Optional[AssistantResponseFormatOptionParam], NotGiven] = NOT_GIVEN,
        temperature: Union[Optional[float], NotGiven] = NOT_GIVEN,
        tool_choice: Union[Optional[AssistantToolChoiceOptionParam], NotGiven] = NOT_GIVEN,
        tools: Union[Optional[Iterable[AssistantToolParam]], NotGiven] = NOT_GIVEN,
        top_p: Union[Optional[float], NotGiven] = NOT_GIVEN,
        truncation_strategy: Union[Optional[run_create_params.TruncationStrategy], NotGiven] = NOT_GIVEN,
        thread_id: str,
        event_handler: Union[AsyncAssistantEventHandlerT, None] = None,
        **kwargs,
    )-> (
        AsyncAssistantStreamManager[AsyncAssistantEventHandler] 
        | AsyncAssistantStreamManager[AsyncAssistantEventHandlerT]
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
            response_format=response_format,
            temperature=temperature,
            tool_choice=tool_choice,
            tools=tools,
            top_p=top_p,
            truncation_strategy=truncation_strategy,
            thread_id=thread_id,
            event_handler=event_handler,
            **kwargs
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
            run_id=run_id,
            thread_id=thread_id,
            **kwargs
        )
        data = response

        return data
    
    async def stream(
        self,
        *,
        assistant_id: str,
        additional_instructions: Union[Optional[str], NotGiven] = NOT_GIVEN,
        additional_messages: Union[Optional[Iterable[run_create_params.AdditionalMessage]], NotGiven] = NOT_GIVEN,
        instructions: Union[Optional[str], NotGiven] = NOT_GIVEN,
        max_completion_tokens: Union[Optional[int], NotGiven] = NOT_GIVEN,
        max_prompt_tokens: Union[Optional[int], NotGiven] = NOT_GIVEN,
        metadata: Union[Optional[object], NotGiven] = NOT_GIVEN,
        model: Union[str, None, NotGiven] = NOT_GIVEN,
        response_format: Union[Optional[AssistantResponseFormatOptionParam], NotGiven] = NOT_GIVEN,
        temperature: Union[Optional[float], NotGiven] = NOT_GIVEN,
        tool_choice: Union[Optional[AssistantToolChoiceOptionParam], NotGiven] = NOT_GIVEN,
        tools: Union[Optional[Iterable[AssistantToolParam]], NotGiven] = NOT_GIVEN,
        top_p: Union[Optional[float], NotGiven] = NOT_GIVEN,
        truncation_strategy: Union[Optional[run_create_params.TruncationStrategy], NotGiven] = NOT_GIVEN,
        thread_id: str,
        event_handler: Union[AsyncAssistantEventHandlerT, None] = None,
        **kwargs,
    ) -> (
        AsyncAssistantStreamManager[AsyncAssistantEventHandler] 
        | AsyncAssistantStreamManager[AsyncAssistantEventHandlerT]
    ):
        response = await self.openai_client.beta.threads.runs.stream(
            assistant_id=assistant_id,
            additional_instructions=additional_instructions,
            additional_messages=additional_messages,
            instructions=instructions,
            max_completion_tokens=max_completion_tokens,
            max_prompt_tokens=max_prompt_tokens,
            metadata=metadata,
            model=model,
            response_format=response_format,
            temperature=temperature,
            tool_choice=tool_choice,
            tools=tools,
            top_p=top_p,
            truncation_strategy=truncation_strategy,
            thread_id=thread_id,
            event_handler=event_handler,
            **kwargs
        )
        data = response
        return data
    
    async def submit_tool_outputs_and_poll(
        self,
        *,
        tool_outputs: Union[Iterable[run_submit_tool_outputs_params.ToolOutput]],
        run_id: str,
        thread_id: str,
        poll_interval_ms: Union[int,  NotGiven] = NOT_GIVEN,  
    ) -> Run:
        response = await self.openai_client.beta.threads.runs.submit_tool_outputs_and_poll(
            tool_outputs=tool_outputs,
            run_id=run_id,
            thread_id=thread_id,
            poll_interval_ms=poll_interval_ms
        )
        data = response

        return data
    
    async def submit_tool_outputs_stream(
        self,
        *,
        tool_outputs: Union[Iterable[run_submit_tool_outputs_params.ToolOutput]],
        run_id: str,
        thread_id: str,
        event_handler: Union[AsyncAssistantEventHandlerT, None] = None,  
    ) -> (
        AsyncAssistantStreamManager[AsyncAssistantEventHandler] 
        | AsyncAssistantStreamManager[AsyncAssistantEventHandlerT]
    ):
        response = await self.openai_client.beta.threads.runs.submit_tool_outputs_stream(
            tool_outputs=tool_outputs,
            run_id=run_id,
            thread_id=thread_id,
            event_handler=event_handler
        )
        data = response

        return data


class AsyncSteps(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    async def list(self, thread_id, run_id, **kwargs) -> RunStepList:
        response = (
            await self.openai_client.with_raw_response.beta.threads.runs.steps.list(
                thread_id=thread_id, run_id=run_id, **kwargs
            )
        )
        data = RunStepList(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def retrieve(self, thread_id, run_id, step_id, **kwargs) -> RunStep:
        response = (
            await self.openai_client.with_raw_response.beta.threads.runs.steps.retrieve(
                thread_id=thread_id, run_id=run_id, step_id=step_id, **kwargs
            )
        )
        data = RunStep(**json.loads(response.text))
        data._headers = response.headers

        return data
