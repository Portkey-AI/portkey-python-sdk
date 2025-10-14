import json
from typing import Any, Iterable, List, Literal, Optional, Union
from portkey_ai._vendor.openai.types.responses.response_includable import (
    ResponseIncludable,
)
from portkey_ai._vendor.openai.types.responses.response_input_item_param import (
    ResponseInputItemParam,
)
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.client import AsyncPortkey, Portkey
from portkey_ai.api_resources.types.conversation_type import (
    Conversation,
    ConversationDeletedResource,
)
from portkey_ai.api_resources.types.shared_types import Headers, Metadata, Query
from ..._vendor.openai._types import NOT_GIVEN, Body, NotGiven, Omit, omit
import httpx


class Conversations(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.items = ConversationsItems(client)

    def create(
        self,
        *,
        items: Union[Optional[Iterable[ResponseInputItemParam]], Omit] = omit,
        metadata: Union[Optional[Metadata], Omit] = omit,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Union[float, httpx.Timeout, NotGiven] = NOT_GIVEN,
    ) -> Conversation:
        response = self.openai_client.with_raw_response.conversations.create(
            items=items,
            metadata=metadata,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        data = Conversation(**json.loads(response.text))
        data._headers = response.headers

        return data

    def retrieve(
        self,
        conversation_id: str,
        *,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Union[float, httpx.Timeout, NotGiven] = NOT_GIVEN,
    ) -> Conversation:
        response = self.openai_client.with_raw_response.conversations.retrieve(
            conversation_id=conversation_id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        data = Conversation(**json.loads(response.text))
        data._headers = response.headers

        return data

    def update(
        self,
        conversation_id: str,
        *,
        metadata: Metadata,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Union[float, httpx.Timeout, NotGiven] = NOT_GIVEN,
    ) -> Conversation:
        response = self.openai_client.with_raw_response.conversations.update(
            conversation_id=conversation_id,
            metadata=metadata,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        data = Conversation(**json.loads(response.text))
        data._headers = response.headers

        return data

    def delete(
        self,
        conversation_id: str,
        *,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Union[float, httpx.Timeout, NotGiven] = NOT_GIVEN,
    ) -> ConversationDeletedResource:
        response = self.openai_client.with_raw_response.conversations.delete(
            conversation_id=conversation_id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        data = ConversationDeletedResource(**json.loads(response.text))
        data._headers = response.headers

        return data


class AsyncConversations(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.items = AsyncConversationsItems(client)

    async def create(
        self,
        *,
        items: Union[Optional[Iterable[ResponseInputItemParam]], Omit] = omit,
        metadata: Union[Optional[Metadata], Omit] = omit,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Union[float, httpx.Timeout, NotGiven] = NOT_GIVEN,
    ) -> Conversation:
        response = await self.openai_client.with_raw_response.conversations.create(
            items=items,
            metadata=metadata,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        data = Conversation(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def retrieve(
        self,
        conversation_id: str,
        *,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Union[float, httpx.Timeout, NotGiven] = NOT_GIVEN,
    ) -> Conversation:
        response = await self.openai_client.with_raw_response.conversations.retrieve(
            conversation_id=conversation_id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        data = Conversation(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def update(
        self,
        conversation_id: str,
        *,
        metadata: Metadata,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Union[float, httpx.Timeout, NotGiven] = NOT_GIVEN,
    ) -> Conversation:
        response = await self.openai_client.with_raw_response.conversations.update(
            conversation_id=conversation_id,
            metadata=metadata,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        data = Conversation(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def delete(
        self,
        conversation_id: str,
        *,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Union[float, httpx.Timeout, NotGiven] = NOT_GIVEN,
    ) -> ConversationDeletedResource:
        response = await self.openai_client.with_raw_response.conversations.delete(
            conversation_id=conversation_id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        data = ConversationDeletedResource(**json.loads(response.text))
        data._headers = response.headers

        return data


class ConversationsItems(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    def create(
        self,
        conversation_id: str,
        *,
        items: Iterable[ResponseInputItemParam],
        include: Union[List[ResponseIncludable], Omit] = omit,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Union[float, httpx.Timeout, NotGiven] = NOT_GIVEN,
    ) -> Any:
        response = self.openai_client.conversations.items.create(
            conversation_id=conversation_id,
            items=items,
            include=include,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )

        return response

    def retrieve(
        self,
        item_id: str,
        *,
        conversation_id: str,
        include: Union[List[ResponseIncludable], Omit] = omit,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Union[float, httpx.Timeout, NotGiven] = NOT_GIVEN,
    ) -> Any:
        response = self.openai_client.conversations.items.retrieve(
            item_id=item_id,
            conversation_id=conversation_id,
            include=include,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )

        return response

    def list(
        self,
        conversation_id: str,
        *,
        after: Union[str, Omit] = omit,
        include: Union[List[ResponseIncludable], Omit] = omit,
        limit: Union[int, Omit] = omit,
        order: Union[Omit, Literal["asc", "desc"]] = omit,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Union[float, httpx.Timeout, NotGiven] = NOT_GIVEN,
    ) -> Any:
        response = self.openai_client.conversations.items.list(
            conversation_id=conversation_id,
            after=after,
            include=include,
            limit=limit,
            order=order,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )

        return response

    def delete(
        self,
        item_id: str,
        *,
        conversation_id: str,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Union[float, httpx.Timeout, NotGiven] = NOT_GIVEN,
    ) -> Any:
        response = self.openai_client.conversations.items.delete(
            item_id=item_id,
            conversation_id=conversation_id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )

        return response


class AsyncConversationsItems(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    async def create(
        self,
        conversation_id: str,
        *,
        items: Iterable[ResponseInputItemParam],
        include: Union[List[ResponseIncludable], Omit] = omit,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Union[float, httpx.Timeout, NotGiven] = NOT_GIVEN,
    ) -> Any:
        response = await self.openai_client.conversations.items.create(
            conversation_id=conversation_id,
            items=items,
            include=include,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )

        return response

    async def retrieve(
        self,
        item_id: str,
        *,
        conversation_id: str,
        include: Union[List[ResponseIncludable], Omit] = omit,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Union[float, httpx.Timeout, NotGiven] = NOT_GIVEN,
    ) -> Any:
        response = await self.openai_client.conversations.items.retrieve(
            item_id=item_id,
            conversation_id=conversation_id,
            include=include,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )

        return response

    async def list(
        self,
        conversation_id: str,
        *,
        after: Union[str, Omit] = omit,
        include: Union[List[ResponseIncludable], Omit] = omit,
        limit: Union[int, Omit] = omit,
        order: Union[Omit, Literal["asc", "desc"]] = omit,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Union[float, httpx.Timeout, NotGiven] = NOT_GIVEN,
    ) -> Any:
        response = await self.openai_client.conversations.items.list(
            conversation_id=conversation_id,
            after=after,
            include=include,
            limit=limit,
            order=order,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )

        return response

    async def delete(
        self,
        item_id: str,
        *,
        conversation_id: str,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Union[float, httpx.Timeout, NotGiven] = NOT_GIVEN,
    ) -> Any:
        response = await self.openai_client.conversations.items.delete(
            item_id=item_id,
            conversation_id=conversation_id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )

        return response
