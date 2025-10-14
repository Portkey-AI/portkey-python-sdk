import json
from typing import Any, Literal, Optional, Union
from portkey_ai.api_resources.types.shared_types import Body, Headers, Query
from ..._vendor.openai._types import (
    FileTypes,
    NotGiven,
    Omit,
    not_given,
    omit,
)
import httpx
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.client import AsyncPortkey, Portkey
from portkey_ai._vendor.openai.types.beta.chatkit.chat_session_chatkit_configuration_param import (
    ChatSessionChatKitConfigurationParam,
)
from portkey_ai._vendor.openai.types.beta.chatkit.chat_session_expires_after_param import (
    ChatSessionExpiresAfterParam,
)
from portkey_ai._vendor.openai.types.beta.chatkit.chat_session_rate_limits_param import (
    ChatSessionRateLimitsParam,
)
from portkey_ai._vendor.openai.types.beta.chatkit.chat_session_workflow_param import (
    ChatSessionWorkflowParam,
)
from portkey_ai._vendor.openai.types.beta.chatkit_upload_file_response import (
    ChatKitUploadFileResponse,
)
from portkey_ai.api_resources.types.chatkit_type import (
    ChatKitThread,
    ChatKitThreadList,
    ChatSession,
    ThreadDeleteResponse,
)


class ChatKit(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.sessions = ChatKitSessions(client)
        self.threads = ChatKitThreads(client)

    def upload_file(
        self,
        *,
        file: FileTypes,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Union[Optional[float], httpx.Timeout, NotGiven] = not_given,
    ) -> ChatKitUploadFileResponse:
        response = self.openai_client.beta.chatkit.upload_file(
            file=file,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return response


class ChatKitSessions(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    def create(
        self,
        *,
        user: str,
        workflow: ChatSessionWorkflowParam,
        chatkit_configuration: Union[ChatSessionChatKitConfigurationParam, Omit] = omit,
        expires_after: Union[ChatSessionExpiresAfterParam, Omit] = omit,
        rate_limits: Union[ChatSessionRateLimitsParam, Omit] = omit,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Union[Optional[float], httpx.Timeout, NotGiven] = not_given,
    ) -> ChatSession:
        response = self.openai_client.with_raw_response.beta.chatkit.sessions.create(
            user=user,
            workflow=workflow,
            chatkit_configuration=chatkit_configuration,
            expires_after=expires_after,
            rate_limits=rate_limits,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        data = ChatSession(**json.loads(response.text))
        data._headers = response.headers

        return data

    def cancel(
        self,
        session_id: str,
        *,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Union[Optional[float], httpx.Timeout, NotGiven] = not_given,
    ) -> ChatSession:
        response = self.openai_client.with_raw_response.beta.chatkit.sessions.cancel(
            session_id=session_id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        data = ChatSession(**json.loads(response.text))
        data._headers = response.headers

        return data


class ChatKitThreads(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    def retrieve(
        self,
        thread_id: str,
        *,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Union[Optional[float], httpx.Timeout, NotGiven] = not_given,
    ) -> ChatKitThread:
        response = self.openai_client.with_raw_response.beta.chatkit.threads.retrieve(
            thread_id=thread_id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        data = ChatKitThread(**json.loads(response.text))
        data._headers = response.headers
        return data

    def list(
        self,
        *,
        after: Union[str, Omit] = omit,
        before: Union[str, Omit] = omit,
        limit: Union[int, Omit] = omit,
        order: Union[Omit, Literal["asc", "desc"]] = omit,
        user: Union[str, Omit] = omit,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Union[Optional[float], httpx.Timeout, NotGiven] = not_given,
    ) -> ChatKitThreadList:
        response = self.openai_client.with_raw_response.beta.chatkit.threads.list(
            after=after,
            before=before,
            limit=limit,
            order=order,
            user=user,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        data = ChatKitThreadList(**json.loads(response.text))
        data._headers = response.headers
        return data

    def delete(
        self,
        thread_id: str,
        *,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Union[Optional[float], httpx.Timeout, NotGiven] = not_given,
    ) -> ThreadDeleteResponse:
        response = self.openai_client.with_raw_response.beta.chatkit.threads.delete(
            thread_id=thread_id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        data = ThreadDeleteResponse(**json.loads(response.text))
        data._headers = response.headers
        return data

    def list_items(
        self,
        thread_id: str,
        *,
        after: Union[str, Omit] = omit,
        before: Union[str, Omit] = omit,
        limit: Union[int, Omit] = omit,
        order: Union[Omit, Literal["asc", "desc"]] = omit,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Union[Optional[float], httpx.Timeout, NotGiven] = not_given,
    ) -> Any:
        response = self.openai_client.beta.chatkit.threads.list_items(
            thread_id=thread_id,
            after=after,
            before=before,
            limit=limit,
            order=order,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return response


class AsyncChatKit(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.sessions = AsyncChatKitSessions(client)
        self.threads = AsyncChatKitThreads(client)

    async def upload_file(
        self,
        *,
        file: FileTypes,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Union[Optional[float], httpx.Timeout, NotGiven] = not_given,
    ) -> ChatKitUploadFileResponse:
        response = await self.openai_client.beta.chatkit.upload_file(
            file=file,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return response


class AsyncChatKitSessions(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    async def create(
        self,
        *,
        user: str,
        workflow: ChatSessionWorkflowParam,
        chatkit_configuration: Union[ChatSessionChatKitConfigurationParam, Omit] = omit,
        expires_after: Union[ChatSessionExpiresAfterParam, Omit] = omit,
        rate_limits: Union[ChatSessionRateLimitsParam, Omit] = omit,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Union[Optional[float], httpx.Timeout, NotGiven] = not_given,
    ) -> ChatSession:
        response = (
            await self.openai_client.with_raw_response.beta.chatkit.sessions.create(
                user=user,
                workflow=workflow,
                chatkit_configuration=chatkit_configuration,
                expires_after=expires_after,
                rate_limits=rate_limits,
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            )
        )
        data = ChatSession(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def cancel(
        self,
        session_id: str,
        *,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Union[Optional[float], httpx.Timeout, NotGiven] = not_given,
    ) -> ChatSession:
        response = (
            await self.openai_client.with_raw_response.beta.chatkit.sessions.cancel(
                session_id=session_id,
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            )
        )
        data = ChatSession(**json.loads(response.text))
        data._headers = response.headers

        return data


class AsyncChatKitThreads(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    async def retrieve(
        self,
        thread_id: str,
        *,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Union[Optional[float], httpx.Timeout, NotGiven] = not_given,
    ) -> ChatKitThread:
        response = (
            await self.openai_client.with_raw_response.beta.chatkit.threads.retrieve(
                thread_id=thread_id,
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            )
        )
        data = ChatKitThread(**json.loads(response.text))
        data._headers = response.headers
        return data

    async def list(
        self,
        *,
        after: Union[str, Omit] = omit,
        before: Union[str, Omit] = omit,
        limit: Union[int, Omit] = omit,
        order: Union[Omit, Literal["asc", "desc"]] = omit,
        user: Union[str, Omit] = omit,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Union[Optional[float], httpx.Timeout, NotGiven] = not_given,
    ) -> ChatKitThreadList:
        response = await self.openai_client.with_raw_response.beta.chatkit.threads.list(
            after=after,
            before=before,
            limit=limit,
            order=order,
            user=user,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        data = ChatKitThreadList(**json.loads(response.text))
        data._headers = response.headers
        return data

    async def delete(
        self,
        thread_id: str,
        *,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Union[Optional[float], httpx.Timeout, NotGiven] = not_given,
    ) -> ThreadDeleteResponse:
        response = (
            await self.openai_client.with_raw_response.beta.chatkit.threads.delete(
                thread_id=thread_id,
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            )
        )
        data = ThreadDeleteResponse(**json.loads(response.text))
        data._headers = response.headers
        return data

    async def list_items(
        self,
        thread_id: str,
        *,
        after: Union[str, Omit] = omit,
        before: Union[str, Omit] = omit,
        limit: Union[int, Omit] = omit,
        order: Union[Omit, Literal["asc", "desc"]] = omit,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Union[Optional[float], httpx.Timeout, NotGiven] = not_given,
    ) -> Any:
        response = await self.openai_client.beta.chatkit.threads.list_items(
            thread_id=thread_id,
            after=after,
            before=before,
            limit=limit,
            order=order,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return response
