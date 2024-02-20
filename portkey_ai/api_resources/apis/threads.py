from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.base_client import APIClient, AsyncAPIClient
from portkey_ai.api_resources.client import AsyncPortkey, Portkey
from portkey_ai.api_resources.utils import PortkeyApiPaths, GenericResponse


class Threads(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.messages = Messages(client)
        self.runs = Runs(client)

    def create(
        self,
    ) -> GenericResponse:

        response = self.openai_client.beta.threads.create()
        return response

    def retrieve(
        self,
        thread_id,
        **kwargs
    ) -> GenericResponse:

        response = self.openai_client.beta.threads.retrieve(
            thread_id=thread_id, **kwargs)
        return response

    def update(
        self,
        thread_id,
        **kwargs
    ) -> GenericResponse:

        response = self.openai_client.beta.threads.update(
            thread_id=thread_id, **kwargs)
        return response

    def delete(
        self,
        thread_id,
    ) -> GenericResponse:

        response = self.openai_client.beta.threads.delete(thread_id=thread_id)
        return response

    def create_and_run(
        self,
        assistant_id,
        **kwargs
    ) -> GenericResponse:

        response = self.openai_client.beta.threads.create_and_run(
            assistant_id == assistant_id, **kwargs)
        return response



class Messages(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.files = Files(client)

    def create(self, thread_id, **kwargs) -> GenericResponse:
        response = self.openai_client.beta.threads.messages.create(
            thread_id=thread_id, **kwargs)
        return response

    def list(self, thread_id, **kwargs) -> GenericResponse:
        response = self.openai_client.beta.threads.messages.list(
            thread_id=thread_id, **kwargs)
        return response

    def retrieve(self, thread_id, message_id, **kwargs) -> GenericResponse:
        response = self.openai_client.beta.threads.messages.retrieve(
            thread_id=thread_id, message_id=message_id, **kwargs)
        return response

    def update(self, thread_id, message_id, **kwargs) -> GenericResponse:
        response = self.openai_client.beta.threads.messages.update(
            thread_id=thread_id, message_id=message_id, **kwargs)
        return response



class Files(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    def list(self, thread_id, message_id, **kwargs) -> GenericResponse:
        response = self.openai_client.beta.threads.messages.files.list(
            thread_id=thread_id, message_id=message_id, **kwargs)
        return response

    def retrieve(self, thread_id, message_id, file_id, **kwargs) -> GenericResponse:
        response = self.openai_client.beta.threads.messages.files.retrieve(
            thread_id=thread_id, message_id=message_id, file_id=file_id ** kwargs)
        return response



class Runs(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.steps = Steps(client)

    def create(self, **kwargs) -> GenericResponse:
        response = self.openai_client.beta.threads.runs.create(**kwargs)
        return response

    def retrieve(self, thread_id, run_id, **kwargs) -> GenericResponse:
        response = self.openai_client.beta.threads.runs.retrieve(
            thread_id=thread_id, run_id=run_id, **kwargs)
        return response

    def list(self, thread_id, **kwargs) -> GenericResponse:
        response = self.openai_client.beta.threads.runs.list(
            thread_id=thread_id, **kwargs)
        return response

    def update(self, thread_id, run_id, **kwargs) -> GenericResponse:
        response = self.openai_client.beta.threads.runs.update(
            thread_id=thread_id, run_id=run_id, **kwargs)
        return response

    def submit_tool_outputs(self, thread_id, tool_outputs, run_id, **kwargs) -> GenericResponse:
        response = self.openai_client.beta.threads.runs.submit_tool_outputs(
            thread_id=thread_id, run_id=run_id, tool_outputs=tool_outputs, **kwargs)
        return response

    def cancel(self, thread_id, run_id, **kwargs) -> GenericResponse:
        response = self.openai_client.beta.threads.runs.cancel(
            thread_id=thread_id, run_id=run_id, **kwargs)
        return response

class Steps(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    def list(self, thread_id, run_id, **kwargs) -> GenericResponse:
        reponse = self.openai_client.beta.threads.runs.steps.list(
            thread_id=thread_id, run_id=run_id, **kwargs)
        return reponse

    def retrieve(self, thread_id, run_id, step_id, **kwargs) -> GenericResponse:
        response = self.openai_client.beta.threads.runs.steps.retrieve(
            thread_id=thread_id, run_id=run_id, step_id=step_id, **kwargs)
        return response

class AsyncThreads(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.messages = AsyncMessages(client)
        self.runs = AsyncRuns(client)

    async def create(
        self,
    ) -> GenericResponse:

        response = await self.openai_client.beta.threads.create()
        return response

    async def retrieve(
        self,
        thread_id,
        **kwargs
    ) -> GenericResponse:

        response = await self.openai_client.beta.threads.retrieve(
            thread_id=thread_id, **kwargs)
        return response

    async def update(
        self,
        thread_id,
        **kwargs
    ) -> GenericResponse:

        response = await self.openai_client.beta.threads.update(
            thread_id=thread_id, **kwargs)
        return response

    async def delete(
        self,
        thread_id,
    ) -> GenericResponse:

        response = await self.openai_client.beta.threads.delete(thread_id=thread_id)
        return response

    async def create_and_run(
        self,
        assistant_id,
        **kwargs
    ) -> GenericResponse:

        response = await self.openai_client.beta.threads.create_and_run(
            assistant_id == assistant_id, **kwargs)
        return response

class AsyncMessages(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.files = AsyncFiles(client)

    async def create(self, thread_id, **kwargs) -> GenericResponse:
        response = await self.openai_client.beta.threads.messages.create(
            thread_id=thread_id, **kwargs)
        return response

    async def list(self, thread_id, **kwargs) -> GenericResponse:
        response = await self.openai_client.beta.threads.messages.list(
            thread_id=thread_id, **kwargs)
        return response

    async def retrieve(self, thread_id, message_id, **kwargs) -> GenericResponse:
        response = await self.openai_client.beta.threads.messages.retrieve(
            thread_id=thread_id, message_id=message_id, **kwargs)
        return response

    async def update(self, thread_id, message_id, **kwargs) -> GenericResponse:
        response = await self.openai_client.beta.threads.messages.update(
            thread_id=thread_id, message_id=message_id, **kwargs)
        return response

class AsyncFiles(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    async def list(self, thread_id, message_id, **kwargs) -> GenericResponse:
        response = await self.openai_client.beta.threads.messages.files.list(
            thread_id=thread_id, message_id=message_id, **kwargs)
        return response

    async def retrieve(self, thread_id, message_id, file_id, **kwargs) -> GenericResponse:
        response = await self.openai_client.beta.threads.messages.files.retrieve(
            thread_id=thread_id, message_id=message_id, file_id=file_id ** kwargs)
        return response

class AsyncRuns(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.steps = AsyncSteps(client)

    async def create(self, **kwargs) -> GenericResponse:
        response = await self.openai_client.beta.threads.runs.create(**kwargs)
        return response

    async def retrieve(self, thread_id, run_id, **kwargs) -> GenericResponse:
        response = await self.openai_client.beta.threads.runs.retrieve(
            thread_id=thread_id, run_id=run_id, **kwargs)
        return response

    async def list(self, thread_id, **kwargs) -> GenericResponse:
        response = await self.openai_client.beta.threads.runs.list(
            thread_id=thread_id, **kwargs)
        return response

    async def update(self, thread_id, run_id, **kwargs) -> GenericResponse:
        response = await self.openai_client.beta.threads.runs.update(
            thread_id=thread_id, run_id=run_id, **kwargs)
        return response

    async def submit_tool_outputs(self, thread_id, tool_outputs, run_id, **kwargs) -> GenericResponse:
        response = await self.openai_client.beta.threads.runs.submit_tool_outputs(
            thread_id=thread_id, run_id=run_id, tool_outputs=tool_outputs, **kwargs)
        return response

    async def cancel(self, thread_id, run_id, **kwargs) -> GenericResponse:
        response = await self.openai_client.beta.threads.runs.cancel(
            thread_id=thread_id, run_id=run_id, **kwargs)
        return response

class AsyncSteps(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    async def list(self, thread_id, run_id, **kwargs) -> GenericResponse:
        reponse = await self.openai_client.beta.threads.runs.steps.list(
            thread_id=thread_id, run_id=run_id, **kwargs)
        return reponse

    async def retrieve(self, thread_id, run_id, step_id, **kwargs) -> GenericResponse:
        response = await self.openai_client.beta.threads.runs.steps.retrieve(
            thread_id=thread_id, run_id=run_id, step_id=step_id, **kwargs)
        return response

