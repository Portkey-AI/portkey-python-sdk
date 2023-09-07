from typing import Optional, Union, List, Dict, Any, cast, overload, Literal
import portkey
from portkey.api_resources.base_client import APIClient
from .global_constants import DEFAULT_MAX_RETRIES, DEFAULT_TIMEOUT
from .utils import (
    ProviderTypes,
    PortkeyCacheType,
    LLMBase,
    PortkeyModes,
    Message,
    ProviderTypesLiteral,
    Body,
    PortkeyResponse,
    RetrySettings,
    Function,
    Config,
    ResponseT,
)

from .common_types import StreamT

from .streaming import Stream

__all__ = ["Completions", "ChatCompletions"]


class APIResource:
    _client: APIClient
    # _get: Any
    # _patch: Any
    # _put: Any
    # _delete: Any

    def __init__(self, client: APIClient) -> None:
        self._client = client
        # self._get = client.get
        # self._patch = client.patch
        # self._put = client.put
        # self._delete = client.delete

    def _post(self, *args, **kwargs):
        return self._client.post(*args, **kwargs)


class Completions(APIResource):
    @classmethod
    @overload
    def create(
        cls, *, config: Config, stream: Literal[True]
    ) -> Stream[PortkeyResponse]:
        ...

    @classmethod
    @overload
    def create(
        cls, *, config: Config, stream: Literal[False] = False
    ) -> PortkeyResponse:
        ...

    @classmethod
    @overload
    def create(
        cls, *, config: Config, stream: bool = False
    ) -> Union[PortkeyResponse, Stream[PortkeyResponse]]:
        ...

    @classmethod
    def create(
        cls, *, config: Config, stream: bool = False
    ) -> Union[PortkeyResponse, Stream[PortkeyResponse]]:
        _client = APIClient()
        if config.mode == PortkeyModes.SINGLE.value:
            return cls(_client)._post(
                "/v1/complete",
                body=config.llms,
                mode=PortkeyModes.SINGLE.value,
                params=config.params,
                cast_to=PortkeyResponse,
                stream_cls=Stream[PortkeyResponse],
                stream=stream,
            )
        if config.mode == PortkeyModes.FALLBACK.value:
            return cls(_client)._post(
                "/v1/complete",
                body=config.llms,
                mode=PortkeyModes.FALLBACK,
                params=config.params,
                cast_to=PortkeyResponse,
                stream_cls=Stream[PortkeyResponse],
                stream=stream,
            )
        if config.mode == PortkeyModes.LOADBALANCE.value:
            return cls(_client)._post(
                "/v1/complete",
                body=config.llms,
                mode=PortkeyModes.LOADBALANCE,
                params=config.params,
                cast_to=PortkeyResponse,
                stream_cls=Stream[PortkeyResponse],
                stream=stream,
            )
        raise NotImplementedError("Mode not implemented.")


class ChatCompletions(APIResource):
    @classmethod
    @overload
    def create(
        cls, *, config: Config, stream: Literal[True]
    ) -> Stream[PortkeyResponse]:
        ...

    @classmethod
    @overload
    def create(
        cls, *, config: Config, stream: Literal[False] = False
    ) -> PortkeyResponse:
        ...

    @classmethod
    @overload
    def create(
        cls, *, config: Config, stream: bool = False
    ) -> Union[PortkeyResponse, Stream[PortkeyResponse]]:
        ...

    @classmethod
    def create(
        cls, *, config: Config, stream: bool = False
    ) -> Union[PortkeyResponse, Stream[PortkeyResponse]]:
        _client = APIClient()
        if config.mode == PortkeyModes.SINGLE.value:
            return cls(_client)._post(
                "/v1/chatComplete",
                body=config.llms,
                mode=PortkeyModes.SINGLE.value,
                params=config.params,
                cast_to=PortkeyResponse,
                stream_cls=Stream[PortkeyResponse],
                stream=stream,
            )
        if config.mode == PortkeyModes.FALLBACK.value:
            return cls(_client)._post(
                "/v1/chatComplete",
                body=config.llms,
                mode=PortkeyModes.FALLBACK,
                params=config.params,
                cast_to=PortkeyResponse,
                stream_cls=Stream[PortkeyResponse],
                stream=stream,
            )
        if config.mode == PortkeyModes.LOADBALANCE.value:
            return cls(_client)._post(
                "/v1/chatComplete",
                body=config.llms,
                mode=PortkeyModes.LOADBALANCE,
                params=config.params,
                cast_to=PortkeyResponse,
                stream_cls=Stream[PortkeyResponse],
                stream=stream,
            )
        raise NotImplementedError("Mode not implemented.")
