import json
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.client import AsyncPortkey, Portkey
from portkey_ai.api_resources.types.assistant_type import (
    Assistant,
    AssistantList,
    AssistantDeleted,
)


class Assistants(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    def create(self, **kwargs) -> Assistant:
        response = self.openai_client.with_raw_response.beta.assistants.create(**kwargs)
        data = Assistant(**json.loads(response.text))
        data._headers = response.headers

        return data

    def retrieve(self, assistant_id, **kwargs) -> Assistant:
        response = self.openai_client.with_raw_response.beta.assistants.retrieve(
            assistant_id=assistant_id, **kwargs
        )
        data = Assistant(**json.loads(response.text))
        data._headers = response.headers

        return data

    def update(self, assistant_id, **kwargs) -> Assistant:
        response = self.openai_client.with_raw_response.beta.assistants.update(
            assistant_id=assistant_id, **kwargs
        )
        data = Assistant(**json.loads(response.text))
        data._headers = response.headers

        return data

    def list(self, **kwargs) -> AssistantList:
        response = self.openai_client.with_raw_response.beta.assistants.list(**kwargs)
        data = AssistantList(**json.loads(response.text))
        data._headers = response.headers

        return data

    def delete(self, assistant_id, **kwargs) -> AssistantDeleted:
        response = self.openai_client.with_raw_response.beta.assistants.delete(
            assistant_id=assistant_id, **kwargs
        )
        data = AssistantDeleted(**json.loads(response.text))
        data._headers = response.headers

        return data


class AsyncAssistants(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    async def create(self, **kwargs) -> Assistant:
        response = await self.openai_client.with_raw_response.beta.assistants.create(
            **kwargs
        )
        data = Assistant(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def retrieve(self, assistant_id, **kwargs) -> Assistant:
        response = await self.openai_client.with_raw_response.beta.assistants.retrieve(
            assistant_id=assistant_id, **kwargs
        )
        data = Assistant(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def update(self, assistant_id, **kwargs) -> Assistant:
        response = await self.openai_client.with_raw_response.beta.assistants.update(
            assistant_id=assistant_id, **kwargs
        )
        data = Assistant(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def list(self, **kwargs) -> AssistantList:
        response = await self.openai_client.with_raw_response.beta.assistants.list(
            **kwargs
        )
        data = AssistantList(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def delete(self, assistant_id, **kwargs) -> AssistantDeleted:
        response = await self.openai_client.with_raw_response.beta.assistants.delete(
            assistant_id=assistant_id, **kwargs
        )
        data = AssistantDeleted(**json.loads(response.text))
        data._headers = response.headers

        return data
