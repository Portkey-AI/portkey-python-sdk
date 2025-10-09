import json
from typing import Any, Literal, Optional, Union
from portkey_ai._vendor.openai._types import Omit, omit
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.client import AsyncPortkey, Portkey
from portkey_ai.api_resources.types.assistant_type import (
    Assistant,
    AssistantList,
    AssistantDeleted,
)
from portkey_ai.api_resources.types.shared_types import Metadata


class Assistants(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    def create(
        self,
        model: Union[str, Any] = "portkey-default",
        description: Union[str, Omit] = omit,
        instructions: Union[str, Omit] = omit,
        metadata: Union[Optional[Metadata], Omit] = omit,
        name: Union[str, Omit] = omit,
        response_format: Union[Any, Omit] = omit,
        temperature: Union[float, Omit] = omit,
        tool_resources: Union[Any, Omit] = omit,
        tools: Union[Any, Omit] = omit,
        top_p: Union[float, Omit] = omit,
        **kwargs
    ) -> Assistant:
        response = self.openai_client.with_raw_response.beta.assistants.create(
            model=model,
            description=description,
            instructions=instructions,
            metadata=metadata,
            name=name,
            response_format=response_format,
            temperature=temperature,
            tool_resources=tool_resources,
            tools=tools,
            top_p=top_p,
            extra_body=kwargs,
        )
        data = Assistant(**json.loads(response.text))
        data._headers = response.headers

        return data

    def retrieve(self, assistant_id, **kwargs) -> Assistant:
        if kwargs:
            response = self.openai_client.with_raw_response.beta.assistants.retrieve(
                assistant_id=assistant_id, extra_body=kwargs
            )
        else:
            response = self.openai_client.with_raw_response.beta.assistants.retrieve(
                assistant_id=assistant_id
            )
        data = Assistant(**json.loads(response.text))
        data._headers = response.headers

        return data

    def update(
        self,
        assistant_id,
        *,
        description: Union[str, Omit] = omit,
        instructions: Union[str, Omit] = omit,
        metadata: Union[Optional[Metadata], Omit] = omit,
        model: Union[str, Omit] = "portkey-default",
        name: Union[str, Omit] = omit,
        response_format: Union[Any, Omit] = omit,
        temperature: Union[float, Omit] = omit,
        tool_resources: Union[Any, Omit] = omit,
        tools: Union[Any, Omit] = omit,
        top_p: Union[float, Omit] = omit,
        **kwargs
    ) -> Assistant:
        response = self.openai_client.with_raw_response.beta.assistants.update(
            assistant_id=assistant_id,
            description=description,
            instructions=instructions,
            metadata=metadata,
            model=model,
            name=name,
            response_format=response_format,
            temperature=temperature,
            tool_resources=tool_resources,
            tools=tools,
            top_p=top_p,
            extra_body=kwargs,
        )
        data = Assistant(**json.loads(response.text))
        data._headers = response.headers

        return data

    def list(
        self,
        *,
        after: Union[str, Omit] = omit,
        before: Union[str, Omit] = omit,
        limit: Union[int, Omit] = omit,
        order: Union[Omit, Literal["asc", "desc"]] = omit,
        **kwargs
    ) -> AssistantList:
        response = self.openai_client.with_raw_response.beta.assistants.list(
            after=after, before=before, limit=limit, order=order
        )
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

    async def create(
        self,
        model: Union[str, Any] = "portkey-default",
        description: Union[str, Omit] = omit,
        instructions: Union[str, Omit] = omit,
        metadata: Union[Optional[Metadata], Omit] = omit,
        name: Union[str, Omit] = omit,
        response_format: Union[Any, Omit] = omit,
        temperature: Union[float, Omit] = omit,
        tool_resources: Union[Any, Omit] = omit,
        tools: Union[Any, Omit] = omit,
        top_p: Union[float, Omit] = omit,
        **kwargs
    ) -> Assistant:
        response = await self.openai_client.with_raw_response.beta.assistants.create(
            model=model,
            description=description,
            instructions=instructions,
            metadata=metadata,
            name=name,
            response_format=response_format,
            temperature=temperature,
            tool_resources=tool_resources,
            tools=tools,
            top_p=top_p,
            extra_body=kwargs,
        )
        data = Assistant(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def retrieve(self, assistant_id, **kwargs) -> Assistant:
        if kwargs:
            response = (
                await self.openai_client.with_raw_response.beta.assistants.retrieve(
                    assistant_id=assistant_id, extra_body=kwargs
                )
            )
        else:
            response = (
                await self.openai_client.with_raw_response.beta.assistants.retrieve(
                    assistant_id=assistant_id
                )
            )
        data = Assistant(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def update(
        self,
        assistant_id,
        *,
        description: Union[str, Omit] = omit,
        instructions: Union[str, Omit] = omit,
        metadata: Union[Optional[Metadata], Omit] = omit,
        model: Union[str, Omit] = "portkey-default",
        name: Union[str, Omit] = omit,
        response_format: Union[Any, Omit] = omit,
        temperature: Union[float, Omit] = omit,
        tool_resources: Union[Any, Omit] = omit,
        tools: Union[Any, Omit] = omit,
        top_p: Union[float, Omit] = omit,
        **kwargs
    ) -> Assistant:
        response = await self.openai_client.with_raw_response.beta.assistants.update(
            assistant_id=assistant_id,
            description=description,
            instructions=instructions,
            metadata=metadata,
            model=model,
            name=name,
            response_format=response_format,
            temperature=temperature,
            tool_resources=tool_resources,
            tools=tools,
            top_p=top_p,
            extra_body=kwargs,
        )
        data = Assistant(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def list(
        self,
        *,
        after: Union[str, Omit] = omit,
        before: Union[str, Omit] = omit,
        limit: Union[int, Omit] = omit,
        order: Union[Omit, Literal["asc", "desc"]] = omit,
        **kwargs
    ) -> AssistantList:
        response = await self.openai_client.with_raw_response.beta.assistants.list(
            after=after, before=before, limit=limit, order=order
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
