import json
from typing import Any, Iterable, List, Union
from portkey_ai._vendor.openai.resources.beta.realtime.realtime import (
    AsyncRealtimeConnectionManager,
    RealtimeConnectionManager,
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
            **kwargs,
        )


class AsyncBetaRealtime(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.sessions = AsyncBetaSessions(client)

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
            **kwargs,
        )


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
    ) -> SessionCreateResponse:
        response = self.openai_client.with_raw_response.beta.realtime.sessions.create(
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
        )
        data = SessionCreateResponse(**json.loads(response.text))
        data._headers = response.headers
        return data


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
    ) -> SessionCreateResponse:
        response = (
            await self.openai_client.with_raw_response.beta.realtime.sessions.create(
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
            )
        )
        data = SessionCreateResponse(**json.loads(response.text))
        data._headers = response.headers
        return data
