import json
from typing import Any, List, Union
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.global_constants import AUDIO_FILE_DURATION_HEADER
from portkey_ai.api_resources.get_audio_duration import get_audio_file_duration
from ..._vendor.openai._types import NotGiven, NOT_GIVEN, FileTypes
from portkey_ai.api_resources.client import AsyncPortkey, Portkey
import typing

from portkey_ai.api_resources.types.audio_types import (
    Transcription,
    TranscriptionVerbose,
    Translation,
    TranslationVerbose,
)


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
        stream: Union[bool, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> Union[Transcription, TranscriptionVerbose, str]:
        extra_headers = kwargs.pop("extra_headers", {})
        if file.name and self._client.calculate_audio_duration:
            duration = get_audio_file_duration(file.name)
            print(f"duration: {duration}")
            if duration is not None:
                extra_headers[AUDIO_FILE_DURATION_HEADER] = duration
        if stream:
            return self.openai_client.audio.transcriptions.create(
                file=file,
                model=model,
                language=language,
                prompt=prompt,
                response_format=response_format,
                temperature=temperature,
                timestamp_granularities=timestamp_granularities,
                stream=stream,
                extra_headers=extra_headers,
                extra_body=kwargs,
            )
        else:
            response = self.openai_client.with_raw_response.audio.transcriptions.create(
                file=file,
                model=model,
                language=language,
                prompt=prompt,
                response_format=response_format,
                temperature=temperature,
                timestamp_granularities=timestamp_granularities,
                extra_headers=extra_headers,
                extra_body=kwargs,
            )

            if response_format == "verbose_json":
                data = TranscriptionVerbose(**json.loads(response.text))
                data._headers = response.headers
            elif response_format == "json":
                data = Transcription(**json.loads(response.text))
                data._headers = response.headers
            else:
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
        temperature: Union[float, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> Union[Translation, TranslationVerbose, str]:
        extra_headers = kwargs.pop("extra_headers", {})
        if file.name and self._client.calculate_audio_duration:  # type: ignore[union-attr]
            duration = get_audio_file_duration(file.name)  # type: ignore[union-attr]
            if duration is not None:
                extra_headers[AUDIO_FILE_DURATION_HEADER] = duration
        response = self.openai_client.with_raw_response.audio.translations.create(
            file=file,
            model=model,
            prompt=prompt,
            temperature=temperature,
            extra_headers=extra_headers,
            extra_body=kwargs,
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
        stream: Union[bool, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> Any:
        if stream is True:
            self.openai_client = self.openai_client.with_streaming_response
        extra_headers = kwargs.pop("extra_headers", {})
        response = self.openai_client.audio.speech.create(
            input=input,
            model=model,
            voice=voice,
            response_format=response_format,
            speed=speed,
            extra_headers=extra_headers,
            extra_body=kwargs,
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
        stream: Union[bool, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> Union[Transcription, TranscriptionVerbose, str]:
        extra_headers = kwargs.pop("extra_headers", {})
        if file.name and self._client.calculate_audio_duration:
            duration = get_audio_file_duration(file.name)
            if duration is not None:
                extra_headers[AUDIO_FILE_DURATION_HEADER] = duration
        if stream:
            return await self.openai_client.audio.transcriptions.create(
                file=file,
                model=model,
                language=language,
                prompt=prompt,
                response_format=response_format,
                temperature=temperature,
                timestamp_granularities=timestamp_granularities,
                stream=stream,
                extra_headers=extra_headers,
                extra_body=kwargs,
            )
        else:
            response = (
                await self.openai_client.with_raw_response.audio.transcriptions.create(
                    file=file,
                    model=model,
                    language=language,
                    prompt=prompt,
                    response_format=response_format,
                    temperature=temperature,
                    timestamp_granularities=timestamp_granularities,
                    extra_headers=extra_headers,
                    extra_body=kwargs,
                )
            )

            if response_format == "verbose_json":
                data = TranscriptionVerbose(**json.loads(response.text))
                data._headers = response.headers
            elif response_format == "json":
                data = Transcription(**json.loads(response.text))
                data._headers = response.headers
            else:
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
        temperature: Union[float, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> Union[Translation, TranslationVerbose, str]:
        extra_headers = kwargs.pop("extra_headers", {})
        if file.name and self._client.calculate_audio_duration:  # type: ignore[union-attr]
            duration = get_audio_file_duration(file.name)  # type: ignore[union-attr]
            if duration is not None:
                extra_headers[AUDIO_FILE_DURATION_HEADER] = duration
        response = await self.openai_client.with_raw_response.audio.translations.create(
            file=file,
            model=model,
            prompt=prompt,
            temperature=temperature,
            extra_headers=extra_headers,
            extra_body=kwargs,
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
        stream: Union[bool, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> Any:
        if stream is True:
            self.openai_client = await self.openai_client.with_streaming_response
        extra_headers = kwargs.pop("extra_headers", {})
        response = await self.openai_client.audio.speech.create(
            input=input,
            model=model,
            voice=voice,
            response_format=response_format,
            speed=speed,
            extra_headers=extra_headers,
            extra_body=kwargs,
        )

        data = response

        return data
