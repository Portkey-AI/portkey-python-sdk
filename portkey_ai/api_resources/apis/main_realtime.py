from typing import Any, List, Literal, Optional, Union

import httpx
from portkey_ai._vendor.openai._types import NotGiven, Omit, not_given, omit
from portkey_ai._vendor.openai.resources.realtime.realtime import (
    AsyncRealtimeConnectionManager,
    RealtimeConnectionManager,
)
from portkey_ai._vendor.openai.types.realtime.realtime_audio_config_param import (
    RealtimeAudioConfigParam,
)
from portkey_ai._vendor.openai.types.realtime.realtime_session_create_request_param import (
    RealtimeSessionCreateRequestParam,
)
from portkey_ai._vendor.openai.types.realtime.realtime_tool_choice_config_param import (
    RealtimeToolChoiceConfigParam,
)
from portkey_ai._vendor.openai.types.realtime.realtime_tools_config_param import (
    RealtimeToolsConfigParam,
)
from portkey_ai._vendor.openai.types.realtime.realtime_tracing_config_param import (
    RealtimeTracingConfigParam,
)
from portkey_ai._vendor.openai.types.realtime.realtime_truncation_param import (
    RealtimeTruncationParam,
)
from portkey_ai._vendor.openai.types.responses.response_prompt_param import (
    ResponsePromptParam,
)
from portkey_ai._vendor.openai.types.websocket_connection_options import (
    WebsocketConnectionOptions,
)
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.client import AsyncPortkey, Portkey
from portkey_ai.api_resources.types.shared_types import Headers, Query, Body


class MainRealtime(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.client_secrets = ClientSecrets(client)
        self.calls = Calls(client)

    def connect(
        self,
        *,
        model: str,
        extra_query: Query = {},
        extra_headers: Headers = {},
        websocket_connection_options: WebsocketConnectionOptions = {},
    ) -> RealtimeConnectionManager:
        return self.openai_client.realtime.connect(
            model=model,
            extra_query=extra_query,
            extra_headers=extra_headers,
            websocket_connection_options=websocket_connection_options,
        )


class AsyncMainRealtime(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.client_secrets = AsyncClientSecrets(client)
        self.calls = AsyncCalls(client)

    def connect(
        self,
        *,
        model: str,
        extra_query: Query = {},
        extra_headers: Headers = {},
        websocket_connection_options: WebsocketConnectionOptions = {},
    ) -> AsyncRealtimeConnectionManager:
        return self.openai_client.realtime.connect(
            model=model,
            extra_query=extra_query,
            extra_headers=extra_headers,
            websocket_connection_options=websocket_connection_options,
        )


class ClientSecrets(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    def create(
        self,
        *,
        expires_after: Any,
        session: Any,
        **kwargs: Any,
    ) -> Any:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)

        return self.openai_client.realtime.client_secrets.create(
            expires_after=expires_after,
            session=session,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body={**(extra_body or {}), **kwargs},
            timeout=timeout,
        )


class AsyncClientSecrets(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    async def create(
        self,
        *,
        expires_after: Any,
        session: Any,
        **kwargs: Any,
    ) -> Any:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)

        return await self.openai_client.realtime.client_secrets.create(
            expires_after=expires_after,
            session=session,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body={**(extra_body or {}), **kwargs},
            timeout=timeout,
        )


class Calls(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    def create(
        self,
        *,
        sdp: str,
        session: Union[RealtimeSessionCreateRequestParam, Omit] = omit,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Union[Optional[float], httpx.Timeout, NotGiven] = not_given,
    ) -> Any:
        return self.openai_client.realtime.calls.create(
            sdp=sdp,
            session=session,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )

    def accept(
        self,
        call_id: str,
        *,
        type: Literal["realtime"],
        audio: Union[RealtimeAudioConfigParam, Omit] = omit,
        include: Union[
            List[Literal["item.input_audio_transcription.logprobs"]], Omit
        ] = omit,
        instructions: Union[str, Omit] = omit,
        max_output_tokens: Union[int, Literal["inf"], Omit] = omit,
        model: Union[
            str,
            Literal[
                "gpt-realtime",
                "gpt-realtime-2025-08-28",
                "gpt-4o-realtime-preview",
                "gpt-4o-realtime-preview-2024-10-01",
                "gpt-4o-realtime-preview-2024-12-17",
                "gpt-4o-realtime-preview-2025-06-03",
                "gpt-4o-mini-realtime-preview",
                "gpt-4o-mini-realtime-preview-2024-12-17",
                "gpt-realtime-mini",
                "gpt-realtime-mini-2025-10-06",
                "gpt-audio-mini",
                "gpt-audio-mini-2025-10-06",
            ],
            Omit,
        ] = omit,
        output_modalities: Union[List[Literal["text", "audio"]], Omit] = omit,
        prompt: Union[Optional[ResponsePromptParam], Omit] = omit,
        tool_choice: Union[RealtimeToolChoiceConfigParam, Omit] = omit,
        tools: Union[RealtimeToolsConfigParam, Omit] = omit,
        tracing: Union[Optional[RealtimeTracingConfigParam], Omit] = omit,
        truncation: Union[RealtimeTruncationParam, Omit] = omit,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Union[Optional[float], httpx.Timeout, NotGiven] = not_given,
    ) -> None:
        return self.openai_client.realtime.calls.accept(
            call_id=call_id,
            type=type,
            audio=audio,
            include=include,
            instructions=instructions,
            max_output_tokens=max_output_tokens,
            model=model,
            output_modalities=output_modalities,
            prompt=prompt,
            tool_choice=tool_choice,
            tools=tools,
            tracing=tracing,
            truncation=truncation,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )

    def hangup(
        self,
        call_id: str,
        *,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Union[Optional[float], httpx.Timeout, NotGiven] = not_given,
    ) -> None:
        return self.openai_client.realtime.calls.hangup(
            call_id=call_id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )

    def refer(
        self,
        call_id: str,
        *,
        target_uri: str,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Union[Optional[float], httpx.Timeout, NotGiven] = not_given,
    ) -> None:
        return self.openai_client.realtime.calls.refer(
            call_id=call_id,
            target_uri=target_uri,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )

    def reject(
        self,
        call_id: str,
        *,
        status_code: Union[int, Omit] = omit,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Union[Optional[float], httpx.Timeout, NotGiven] = not_given,
    ) -> None:
        return self.openai_client.realtime.calls.reject(
            call_id=call_id,
            status_code=status_code,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )


class AsyncCalls(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    async def create(
        self,
        *,
        sdp: str,
        session: Union[RealtimeSessionCreateRequestParam, Omit] = omit,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Union[Optional[float], httpx.Timeout, NotGiven] = not_given,
    ) -> Any:
        return await self.openai_client.realtime.calls.create(
            sdp=sdp,
            session=session,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )

    async def accept(
        self,
        call_id: str,
        *,
        type: Literal["realtime"],
        audio: Union[RealtimeAudioConfigParam, Omit] = omit,
        include: Union[
            List[Literal["item.input_audio_transcription.logprobs"]], Omit
        ] = omit,
        instructions: Union[str, Omit] = omit,
        max_output_tokens: Union[int, Literal["inf"], Omit] = omit,
        model: Union[
            str,
            Literal[
                "gpt-realtime",
                "gpt-realtime-2025-08-28",
                "gpt-4o-realtime-preview",
                "gpt-4o-realtime-preview-2024-10-01",
                "gpt-4o-realtime-preview-2024-12-17",
                "gpt-4o-realtime-preview-2025-06-03",
                "gpt-4o-mini-realtime-preview",
                "gpt-4o-mini-realtime-preview-2024-12-17",
                "gpt-realtime-mini",
                "gpt-realtime-mini-2025-10-06",
                "gpt-audio-mini",
                "gpt-audio-mini-2025-10-06",
            ],
            Omit,
        ] = omit,
        output_modalities: Union[List[Literal["text", "audio"]], Omit] = omit,
        prompt: Union[Optional[ResponsePromptParam], Omit] = omit,
        tool_choice: Union[RealtimeToolChoiceConfigParam, Omit] = omit,
        tools: Union[RealtimeToolsConfigParam, Omit] = omit,
        tracing: Union[Optional[RealtimeTracingConfigParam], Omit] = omit,
        truncation: Union[RealtimeTruncationParam, Omit] = omit,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Union[Optional[float], httpx.Timeout, NotGiven] = not_given,
    ) -> None:
        return await self.openai_client.realtime.calls.accept(
            call_id=call_id,
            type=type,
            audio=audio,
            include=include,
            instructions=instructions,
            max_output_tokens=max_output_tokens,
            model=model,
            output_modalities=output_modalities,
            prompt=prompt,
            tool_choice=tool_choice,
            tools=tools,
            tracing=tracing,
            truncation=truncation,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )

    async def hangup(
        self,
        call_id: str,
        *,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Union[Optional[float], httpx.Timeout, NotGiven] = not_given,
    ) -> None:
        return await self.openai_client.realtime.calls.hangup(
            call_id=call_id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )

    async def refer(
        self,
        call_id: str,
        *,
        target_uri: str,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Union[Optional[float], httpx.Timeout, NotGiven] = not_given,
    ) -> None:
        return await self.openai_client.realtime.calls.refer(
            call_id=call_id,
            target_uri=target_uri,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )

    async def reject(
        self,
        call_id: str,
        *,
        status_code: Union[int, Omit] = omit,
        extra_headers: Optional[Headers] = None,
        extra_query: Optional[Query] = None,
        extra_body: Optional[Body] = None,
        timeout: Union[Optional[float], httpx.Timeout, NotGiven] = not_given,
    ) -> None:
        return await self.openai_client.realtime.calls.reject(
            call_id=call_id,
            status_code=status_code,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
