from typing import Any
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.client import AsyncPortkey, Portkey


class Assistants(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.files = AssistantFiles(client)

    def create(self, **kwargs) -> Any:
        response = self.openai_client.beta.assistants.create(**kwargs)
        return response

    def retrieve(self, assistant_id, **kwargs) -> Any:
        response = self.openai_client.beta.assistants.retrieve(
            assistant_id=assistant_id, **kwargs
        )
        return response

    def update(self, assistant_id, **kwargs) -> Any:
        response = self.openai_client.beta.assistants.update(
            assistant_id=assistant_id, **kwargs
        )
        return response

    def delete(self, assistant_id, **kwargs) -> Any:
        response = self.openai_client.beta.assistants.delete(
            assistant_id=assistant_id, **kwargs
        )
        return response


class AssistantFiles(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    def create(self, **kwargs) -> Any:
        response = self.openai_client.beta.assistants.files.create(**kwargs)
        return response

    def list(self, assistant_id, **kwargs) -> Any:
        response = self.openai_client.beta.assistants.files.list(
            assistant_id=assistant_id, **kwargs
        )
        return response

    def retrieve(self, assistant_id, file_id, **kwargs) -> Any:
        response = self.openai_client.beta.assistants.files.retrieve(
            assistant_id=assistant_id, file_id=file_id, **kwargs
        )
        return response

    def delete(self, assistant_id, file_id, **kwargs) -> Any:
        response = self.openai_client.beta.assistants.files.delete(
            assistant_id=assistant_id, file_id=file_id, **kwargs
        )
        return response


class AsyncAssistants(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.files = AsyncAssistantFiles(client)

    async def create(self, **kwargs) -> Any:
        response = await self.openai_client.beta.assistants.create(**kwargs)
        return response

    async def retrieve(self, assistant_id, **kwargs) -> Any:
        response = await self.openai_client.beta.assistants.retrieve(
            assistant_id=assistant_id, **kwargs
        )
        return response

    async def update(self, assistant_id, **kwargs) -> Any:
        response = await self.openai_client.beta.assistants.update(
            assistant_id=assistant_id, **kwargs
        )
        return response

    async def delete(self, assistant_id, **kwargs) -> Any:
        response = await self.openai_client.beta.assistants.delete(
            assistant_id=assistant_id, **kwargs
        )
        return response


class AsyncAssistantFiles(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    async def create(self, **kwargs) -> Any:
        response = await self.openai_client.beta.assistants.files.create(**kwargs)
        return response

    async def list(self, assistant_id, **kwargs) -> Any:
        response = await self.openai_client.beta.assistants.files.list(
            assistant_id=assistant_id, **kwargs
        )
        return response

    async def retrieve(self, assistant_id, file_id, **kwargs) -> Any:
        response = await self.openai_client.beta.assistants.files.retrieve(
            assistant_id=assistant_id, file_id=file_id, **kwargs
        )
        return response

    async def delete(self, assistant_id, file_id, **kwargs) -> Any:
        response = await self.openai_client.beta.assistants.files.delete(
            assistant_id=assistant_id, file_id=file_id, **kwargs
        )
        return response
