import json
from typing import Any, Literal, Union
from portkey_ai._vendor.openai._types import NotGiven, NOT_GIVEN
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

    def create(
        self,
        model: Union[str, Any] = "portkey-default",
        description: Union[str, NotGiven] = NOT_GIVEN,
        instructions: Union[str, NotGiven] = NOT_GIVEN,
        metadata: Union[object, NotGiven] = NOT_GIVEN,
        name: Union[str, NotGiven] = NOT_GIVEN,
        response_format: Union[Any, NotGiven] = NOT_GIVEN,
        temperature: Union[float, NotGiven] = NOT_GIVEN,
        tool_resources: Union[Any, NotGiven] = NOT_GIVEN,
        tools: Union[Any, NotGiven] = NOT_GIVEN,
        top_p: Union[float, NotGiven] = NOT_GIVEN,
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
        description: Union[str, NotGiven] = NOT_GIVEN,
        instructions: Union[str, NotGiven] = NOT_GIVEN,
        metadata: Union[object, NotGiven] = NOT_GIVEN,
        model: Union[str, NotGiven] = "portkey-default",
        name: Union[str, NotGiven] = NOT_GIVEN,
        response_format: Union[Any, NotGiven] = NOT_GIVEN,
        temperature: Union[float, NotGiven] = NOT_GIVEN,
        tool_resources: Union[Any, NotGiven] = NOT_GIVEN,
        tools: Union[Any, NotGiven] = NOT_GIVEN,
        top_p: Union[float, NotGiven] = NOT_GIVEN,
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
        after: Union[str, NotGiven] = NOT_GIVEN,
        before: Union[str, NotGiven] = NOT_GIVEN,
        limit: Union[int, NotGiven] = NOT_GIVEN,
        order: Union[NotGiven, Literal["asc", "desc"]] = NOT_GIVEN,
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
        description: Union[str, NotGiven] = NOT_GIVEN,
        instructions: Union[str, NotGiven] = NOT_GIVEN,
        metadata: Union[object, NotGiven] = NOT_GIVEN,
        name: Union[str, NotGiven] = NOT_GIVEN,
        response_format: Union[Any, NotGiven] = NOT_GIVEN,
        temperature: Union[float, NotGiven] = NOT_GIVEN,
        tool_resources: Union[Any, NotGiven] = NOT_GIVEN,
        tools: Union[Any, NotGiven] = NOT_GIVEN,
        top_p: Union[float, NotGiven] = NOT_GIVEN,
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
        description: Union[str, NotGiven] = NOT_GIVEN,
        instructions: Union[str, NotGiven] = NOT_GIVEN,
        metadata: Union[object, NotGiven] = NOT_GIVEN,
        model: Union[str, NotGiven] = "portkey-default",
        name: Union[str, NotGiven] = NOT_GIVEN,
        response_format: Union[Any, NotGiven] = NOT_GIVEN,
        temperature: Union[float, NotGiven] = NOT_GIVEN,
        tool_resources: Union[Any, NotGiven] = NOT_GIVEN,
        tools: Union[Any, NotGiven] = NOT_GIVEN,
        top_p: Union[float, NotGiven] = NOT_GIVEN,
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
        after: Union[str, NotGiven] = NOT_GIVEN,
        before: Union[str, NotGiven] = NOT_GIVEN,
        limit: Union[int, NotGiven] = NOT_GIVEN,
        order: Union[NotGiven, Literal["asc", "desc"]] = NOT_GIVEN,
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
