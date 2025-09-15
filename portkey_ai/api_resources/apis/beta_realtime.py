from typing import Any, Iterable, List, Union
from portkey_ai._vendor.openai.resources.beta.realtime.realtime import (
    AsyncRealtimeConnectionManager,
    RealtimeConnectionManager,
)
from portkey_ai._vendor.openai.types.beta.realtime.transcription_session import (
    TranscriptionSession,
)
from portkey_ai._vendor.openai.types.websocket_connection_options import (
    WebsocketConnectionOptions,
)
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.client import AsyncPortkey, Portkey
from portkey_ai.api_resources.types.beta_realtime import SessionCreateResponse
from ..._vendor.openai._types import NotGiven, NOT_GIVEN


class BetaRealtime(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.sessions = BetaSessions(client)
        self.transcription_sessions = BetaTranscriptionSessions(client)

    def connect(
        self,
        *,
        model: str,
        websocket_connection_options: WebsocketConnectionOptions = {},
        **kwargs,
    ) -> RealtimeConnectionManager:
        return self.openai_client.beta.realtime.connect(
            model=model,
            websocket_connection_options=websocket_connection_options,
            extra_headers=self.openai_client.default_headers,
            **kwargs,
        )


class BetaTranscriptionSessions(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    def create(
        self,
        *,
        client_secret: Union[Any, NotGiven] = NOT_GIVEN,
        include: Union[List[Any], NotGiven] = NOT_GIVEN,
        input_audio_format: Union[Any, NotGiven] = NOT_GIVEN,
        input_audio_noise_reduction: Union[Any, NotGiven] = NOT_GIVEN,
        input_audio_transcription: Union[Any, NotGiven] = NOT_GIVEN,
        modalities: Union[List[Any], NotGiven] = NOT_GIVEN,
        turn_detection: Union[Any, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> TranscriptionSession:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)
        response = self.openai_client.beta.realtime.transcription_sessions.create(
            client_secret=client_secret,
            include=include,
            input_audio_format=input_audio_format,
            input_audio_noise_reduction=input_audio_noise_reduction,
            input_audio_transcription=input_audio_transcription,
            modalities=modalities,
            turn_detection=turn_detection,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body={**(extra_body or {}), **kwargs},
            timeout=timeout,
        )
        return response


class AsyncBetaRealtime(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.sessions = AsyncBetaSessions(client)
        self.transcription_sessions = AsyncBetaTranscriptionSessions(client)

    def connect(
        self,
        *,
        model: str,
        websocket_connection_options: WebsocketConnectionOptions = {},
        **kwargs,
    ) -> AsyncRealtimeConnectionManager:
        return self.openai_client.beta.realtime.connect(
            model=model,
            websocket_connection_options=websocket_connection_options,
            extra_headers=self.openai_client.default_headers,
            **kwargs,
        )


class AsyncBetaTranscriptionSessions(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    async def create(
        self,
        *,
        client_secret: Union[Any, NotGiven] = NOT_GIVEN,
        include: Union[List[Any], NotGiven] = NOT_GIVEN,
        input_audio_format: Union[Any, NotGiven] = NOT_GIVEN,
        input_audio_noise_reduction: Union[Any, NotGiven] = NOT_GIVEN,
        input_audio_transcription: Union[Any, NotGiven] = NOT_GIVEN,
        modalities: Union[List[Any], NotGiven] = NOT_GIVEN,
        turn_detection: Union[Any, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> TranscriptionSession:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)
        response = await self.openai_client.beta.realtime.transcription_sessions.create(
            client_secret=client_secret,
            include=include,
            input_audio_format=input_audio_format,
            input_audio_noise_reduction=input_audio_noise_reduction,
            input_audio_transcription=input_audio_transcription,
            modalities=modalities,
            turn_detection=turn_detection,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body={**(extra_body or {}), **kwargs},
            timeout=timeout,
        )
        return response


class BetaSessions(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    def create(
        self,
        *,
        model: Any = "portkey-default",
        input_audio_format: Union[Any, NotGiven] = NOT_GIVEN,
        input_audio_transcription: Union[Any, NotGiven] = NOT_GIVEN,
        instructions: Union[str, NotGiven] = NOT_GIVEN,
        max_response_output_tokens: Union[int, Any, NotGiven] = NOT_GIVEN,
        modalities: Union[List[Any], NotGiven] = NOT_GIVEN,
        output_audio_format: Union[Any, NotGiven] = NOT_GIVEN,
        temperature: Union[float, NotGiven] = NOT_GIVEN,
        tool_choice: Union[str, NotGiven] = NOT_GIVEN,
        tools: Union[Iterable[Any], NotGiven] = NOT_GIVEN,
        turn_detection: Union[Any, NotGiven] = NOT_GIVEN,
        voice: Union[Any, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> SessionCreateResponse:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)
        response = self.openai_client.beta.realtime.sessions.create(
            model=model,
            input_audio_format=input_audio_format,
            input_audio_transcription=input_audio_transcription,
            instructions=instructions,
            max_response_output_tokens=max_response_output_tokens,
            modalities=modalities,
            output_audio_format=output_audio_format,
            temperature=temperature,
            tool_choice=tool_choice,
            tools=tools,
            turn_detection=turn_detection,
            voice=voice,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body={**(extra_body or {}), **kwargs},
            timeout=timeout,
        )

        return response  # type: ignore[return-value]


class AsyncBetaSessions(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    async def create(
        self,
        *,
        model: Any = "portkey-default",
        input_audio_format: Union[Any, NotGiven] = NOT_GIVEN,
        input_audio_transcription: Union[Any, NotGiven] = NOT_GIVEN,
        instructions: Union[str, NotGiven] = NOT_GIVEN,
        max_response_output_tokens: Union[int, Any, NotGiven] = NOT_GIVEN,
        modalities: Union[List[Any], NotGiven] = NOT_GIVEN,
        output_audio_format: Union[Any, NotGiven] = NOT_GIVEN,
        temperature: Union[float, NotGiven] = NOT_GIVEN,
        tool_choice: Union[str, NotGiven] = NOT_GIVEN,
        tools: Union[Iterable[Any], NotGiven] = NOT_GIVEN,
        turn_detection: Union[Any, NotGiven] = NOT_GIVEN,
        voice: Union[Any, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> SessionCreateResponse:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)
        response = await self.openai_client.beta.realtime.sessions.create(
            model=model,
            input_audio_format=input_audio_format,
            input_audio_transcription=input_audio_transcription,
            instructions=instructions,
            max_response_output_tokens=max_response_output_tokens,
            modalities=modalities,
            output_audio_format=output_audio_format,
            temperature=temperature,
            tool_choice=tool_choice,
            tools=tools,
            turn_detection=turn_detection,
            voice=voice,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body={**(extra_body or {}), **kwargs},
            timeout=timeout,
        )

        return response  # type: ignore[return-value]
