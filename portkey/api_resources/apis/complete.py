from typing import Mapping, Optional, Union, overload, Literal
from portkey.api_resources.base_client import APIClient
from portkey.api_resources.global_constants import TEXT_COMPLETE_API
from portkey.api_resources.utils import (
    Modes,
    ConfigSlug,
    retrieve_config,
    Params,
    TextCompletion,
    TextCompletionChunk,
)

from portkey.api_resources.streaming import Stream
from portkey.api_resources.apis.api_resource import APIResource


class Completion(APIResource):
    @classmethod
    @overload
    def create(
        cls,
        *,
        prompt: Optional[str] = None,
        config: Optional[Union[Mapping, str]] = None,
        stream: Literal[True],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        **kwargs,
    ) -> Stream[TextCompletionChunk]:
        ...

    @classmethod
    @overload
    def create(
        cls,
        *,
        prompt: Optional[str] = None,
        config: Optional[Union[Mapping, str]] = None,
        stream: Literal[False] = False,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        **kwargs,
    ) -> TextCompletion:
        ...

    @classmethod
    @overload
    def create(
        cls,
        *,
        prompt: Optional[str] = None,
        config: Optional[Union[Mapping, str]] = None,
        stream: bool = False,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        **kwargs,
    ) -> Union[TextCompletion, Stream[TextCompletionChunk]]:
        ...

    @classmethod
    def create(
        cls,
        *,
        provider: str,
        api_key: Optional[str] = None,
        prompt: Optional[str] = None,
        config: Optional[Union[Mapping, str]] = None,
        stream: bool = False,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        **kwargs,
    ) -> Union[TextCompletion, Stream[TextCompletionChunk]]:
        if config is None:
            config = retrieve_config()
        params = Params(
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            top_k=top_k,
            top_p=top_p,
            **kwargs,
        )
        _client = (
            APIClient()
            if isinstance(config, str)
            else APIClient(
                api_key=config.get("api_key"), base_url=config.get("base_url")
            )
        )

        if isinstance(config, str):
            body = ConfigSlug(config=config)
            return cls(_client)._post(
                TEXT_COMPLETE_API,
                body=body,
                params=params,
                cast_to=TextCompletion,
                stream_cls=Stream[TextCompletionChunk],
                stream=stream,
                mode="",
            )

        if config.get("mode") == Modes.SINGLE.value:
            return cls(_client)._post(
                TEXT_COMPLETE_API,
                body=config.get("options"),
                mode=Modes.SINGLE.value,
                params=params,
                cast_to=TextCompletion,
                stream_cls=Stream[TextCompletionChunk],
                stream=stream,
            )
        if config.get("mode") == Modes.FALLBACK.value:
            return cls(_client)._post(
                TEXT_COMPLETE_API,
                body=config.get("options"),
                mode=Modes.FALLBACK,
                params=params,
                cast_to=TextCompletion,
                stream_cls=Stream[TextCompletionChunk],
                stream=stream,
            )
        if config.get("mode") == Modes.AB_TEST.value:
            return cls(_client)._post(
                TEXT_COMPLETE_API,
                body=config.get("options"),
                mode=Modes.AB_TEST,
                params=params,
                cast_to=TextCompletion,
                stream_cls=Stream[TextCompletionChunk],
                stream=stream,
            )
        raise NotImplementedError("Mode not implemented.")
