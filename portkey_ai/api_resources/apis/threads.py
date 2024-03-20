import json

from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.client import AsyncPortkey, Portkey
from portkey_ai.api_resources.types.thread_message_type import (
    MessageFile,
    MessageList,
    ThreadMessage,
)
from portkey_ai.api_resources.types.thread_run_type import (
    Run,
    RunList,
    RunStep,
    RunStepList,
)
from portkey_ai.api_resources.types.thread_type import Thread, ThreadDeleted


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


class Messages(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.files = ThreadFiles(client)

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


class ThreadFiles(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    def list(self, thread_id, message_id, **kwargs) -> MessageList:
        response = (
            self.openai_client.with_raw_response.beta.threads.messages.files.list(
                thread_id=thread_id, message_id=message_id, **kwargs
            )
        )
        data = MessageList(**json.loads(response.text))
        data._headers = response.headers

        return data

    def retrieve(self, thread_id, message_id, file_id, **kwargs) -> MessageFile:
        response = (
            self.openai_client.with_raw_response.beta.threads.messages.files.retrieve(
                thread_id=thread_id, message_id=message_id, file_id=file_id, **kwargs
            )
        )
        data = MessageFile(**json.loads(response.text))
        data._headers = response.headers

        return data


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


class AsyncMessages(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.files = AsyncThreadFiles(client)

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


class AsyncThreadFiles(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    async def list(self, thread_id, message_id, **kwargs) -> MessageList:
        response = (
            await self.openai_client.with_raw_response.beta.threads.messages.files.list(
                thread_id=thread_id, message_id=message_id, **kwargs
            )
        )
        data = MessageList(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def retrieve(self, thread_id, message_id, file_id, **kwargs) -> MessageFile:
        # fmt: off
        response = await self.openai_client\
            .with_raw_response\
            .beta\
            .threads\
            .messages\
            .files\
            .retrieve(
                thread_id=thread_id, 
                message_id=message_id, 
                file_id=file_id, 
                **kwargs
            )
        # fmt: off
        data = MessageFile(**json.loads( response.text))
        data._headers = response.headers

        return data


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
