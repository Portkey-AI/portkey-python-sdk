import json
from typing import Any, List, Union
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from openai._types import NotGiven, NOT_GIVEN, FileTypes
from portkey_ai.api_resources.client import AsyncPortkey, Portkey
import typing

from portkey_ai.api_resources.types.audio_types import Transcription, Translation


class Audio(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.transcriptions = Transcriptions(client)
        self.translations = Translations(client)
        self.speech = Speech(client)


class Transcriptions(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    @typing.no_type_check
    def create(
        self,
        *,
        file: FileTypes,
        model: str,
        language: Union[str, NotGiven] = NOT_GIVEN,
        prompt: Union[str, NotGiven] = NOT_GIVEN,
        response_format: Union[str, NotGiven] = NOT_GIVEN,
        temperature: Union[float, NotGiven] = NOT_GIVEN,
        timestamp_granularities: Union[List[str], NotGiven] = NOT_GIVEN,
        **kwargs
    ) -> Transcription:
        response = self.openai_client.with_raw_response.audio.transcriptions.create(
            file=file,
            model=model,
            language=language,
            prompt=prompt,
            response_format=response_format,
            temperature=temperature,
            timestamp_granularities=timestamp_granularities,
            **kwargs
        )
        data = Transcription(**json.loads(response.text))
        data._headers = response.headers

        return data


class Translations(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    def create(
        self,
        *,
        file: FileTypes,
        model: str,
        prompt: Union[str, NotGiven] = NOT_GIVEN,
        response_format: Union[str, NotGiven] = NOT_GIVEN,
        temperature: Union[float, NotGiven] = NOT_GIVEN,
        **kwargs
    ) -> Translation:
        response = self.openai_client.with_raw_response.audio.translations.create(
            file=file,
            model=model,
            prompt=prompt,
            response_format=response_format,
            temperature=temperature,
            **kwargs
        )
        data = Translation(**json.loads(response.text))
        data._headers = response.headers

        return data


class Speech(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    @typing.no_type_check
    def create(
        self,
        *,
        input: str,
        model: str,
        voice: str,
        response_format: Union[str, NotGiven] = NOT_GIVEN,
        speed: Union[float, NotGiven] = NOT_GIVEN,
        **kwargs
    ) -> Any:
        response = self.openai_client.audio.speech.create(
            input=input,
            model=model,
            voice=voice,
            response_format=response_format,
            speed=speed,
            **kwargs
        )

        return response


class AsyncAudio(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.transcriptions = AsyncTranscriptions(client)
        self.translations = AsyncTranslations(client)
        self.speech = AsyncSpeech(client)


class AsyncTranscriptions(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    @typing.no_type_check
    async def create(
        self,
        *,
        file: FileTypes,
        model: str,
        language: Union[str, NotGiven] = NOT_GIVEN,
        prompt: Union[str, NotGiven] = NOT_GIVEN,
        response_format: Union[str, NotGiven] = NOT_GIVEN,
        temperature: Union[float, NotGiven] = NOT_GIVEN,
        timestamp_granularities: Union[List[str], NotGiven] = NOT_GIVEN,
        **kwargs
    ) -> Transcription:
        response = (
            await self.openai_client.with_raw_response.audio.transcriptions.create(
                file=file,
                model=model,
                language=language,
                prompt=prompt,
                response_format=response_format,
                temperature=temperature,
                timestamp_granularities=timestamp_granularities,
                **kwargs
            )
        )
        data = Transcription(**json.loads(response.text))
        data._headers = response.headers

        return data


class AsyncTranslations(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    async def create(
        self,
        *,
        file: FileTypes,
        model: str,
        prompt: Union[str, NotGiven] = NOT_GIVEN,
        response_format: Union[str, NotGiven] = NOT_GIVEN,
        temperature: Union[float, NotGiven] = NOT_GIVEN,
        **kwargs
    ) -> Translation:
        response = await self.openai_client.with_raw_response.audio.translations.create(
            file=file,
            model=model,
            prompt=prompt,
            response_format=response_format,
            temperature=temperature,
            **kwargs
        )
        data = Translation(**json.loads(response.text))
        data._headers = response.headers

        return data


class AsyncSpeech(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    @typing.no_type_check
    async def create(
        self,
        *,
        input: str,
        model: str,
        voice: str,
        response_format: Union[str, NotGiven] = NOT_GIVEN,
        speed: Union[float, NotGiven] = NOT_GIVEN,
        **kwargs
    ) -> Any:
        response = await self.openai_client.audio.speech.create(
            input=input,
            model=model,
            voice=voice,
            response_format=response_format,
            speed=speed,
            **kwargs
        )

        data = response

        return data
