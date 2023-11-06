import json
from typing import Mapping, Optional, Union, overload, Literal, List

from portkey.api_resources.base_client import APIClient
from portkey.api_resources.global_constants import CHAT_COMPLETE_API
from portkey.api_resources.utils import (
    Modes,
    ConfigSlug,
    get_portkey_header,
    retrieve_config,
    Message,
    ChatCompletionChunk,
    ChatCompletions,
)

from portkey.api_resources.streaming import Stream
from portkey.api_resources.apis.api_resource import APIResource


class ChatCompletion(APIResource):
    @classmethod
    @overload
    def create(
        cls,
        *,
        messages: Optional[List[Message]] = None,
        config: Optional[Union[Mapping, str]] = None,
        stream: Literal[True],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        **kwargs,
    ) -> Stream[ChatCompletionChunk]:
        ...

    @classmethod
    @overload
    def create(
        cls,
        *,
        messages: Optional[List[Message]] = None,
        config: Optional[Union[Mapping, str]] = None,
        stream: Literal[False] = False,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        **kwargs,
    ) -> ChatCompletions:
        ...

    @classmethod
    @overload
    def create(
        cls,
        *,
        messages: Optional[List[Message]] = None,
        config: Optional[Union[Mapping, str]] = None,
        stream: bool = False,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        **kwargs,
    ) -> Union[ChatCompletions, Stream[ChatCompletionChunk]]:
        ...

    @classmethod
    def create(
        cls,
        *,
        messages: Optional[List[Message]] = None,
        stream: bool = False,
        config: Optional[Union[Mapping, str]] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        **kwargs,
    ) -> Union[ChatCompletions, Stream[ChatCompletionChunk]]:
        if config is None:
            config = retrieve_config()
        params = dict(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_k=top_k,
            top_p=top_p,
            **kwargs,
        )
        _client = (
            APIClient()
            if isinstance(config, str) or config is None
            else APIClient(
                api_key=config.get("api_key"), base_url=config.get("base_url")
            )
        )

        headers = {get_portkey_header("config"): cls._get_config_string(config)}

        if isinstance(config, str):
            ConfigSlug(config=config)
            return cls(_client)._post(
                CHAT_COMPLETE_API,
                body=params,
                mode="",
                params=params,
                cast_to=ChatCompletion,
                stream_cls=Stream[ChatCompletionChunk],
                stream=stream,
                headers=headers,
            )
        print("config: ", config)

        if config and config.get("mode") == Modes.SINGLE.value:
            return cls(_client)._post(
                CHAT_COMPLETE_API,
                body=params,
                mode=Modes.SINGLE.value,
                params=params,
                cast_to=ChatCompletion,
                stream_cls=Stream[ChatCompletionChunk],
                stream=stream,
                headers=headers,
            )
        if config and config.get("mode") == Modes.FALLBACK.value:
            return cls(_client)._post(
                CHAT_COMPLETE_API,
                body=params,
                mode=Modes.FALLBACK,
                params=params,
                cast_to=ChatCompletion,
                stream_cls=Stream[ChatCompletionChunk],
                stream=stream,
                headers=headers,
            )
        if config and config.get("mode") == Modes.AB_TEST.value:
            return cls(_client)._post(
                CHAT_COMPLETE_API,
                body=params,
                mode=Modes.AB_TEST,
                params=params,
                cast_to=ChatCompletion,
                stream_cls=Stream[ChatCompletionChunk],
                stream=stream,
                headers=headers,
            )
        raise NotImplementedError("Mode not implemented.")

    @classmethod
    def _get_config_string(cls, config: Union[Mapping, str]) -> str:
        return config if isinstance(config, str) else json.dumps(config)
