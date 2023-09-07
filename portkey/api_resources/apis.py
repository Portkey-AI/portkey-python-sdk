from typing import Optional, Union, overload, Literal
from portkey.api_resources.base_client import APIClient
from .utils import PortkeyModes, PortkeyResponse, Config, retrieve_config, Params
import portkey

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
        cls, *, config: Optional[Config] = None, stream: Literal[True], **kwargs
    ) -> Stream[PortkeyResponse]:
        ...

    @classmethod
    @overload
    def create(
        cls,
        *,
        config: Optional[Config] = None,
        stream: Literal[False] = False,
        **kwargs
    ) -> PortkeyResponse:
        ...

    @classmethod
    @overload
    def create(
        cls, *, config: Optional[Config] = None, stream: bool = False, **kwargs
    ) -> Union[PortkeyResponse, Stream[PortkeyResponse]]:
        ...

    @classmethod
    def create(
        cls, *, config: Optional[Config] = None, stream: bool = False, **kwargs
    ) -> Union[PortkeyResponse, Stream[PortkeyResponse]]:
        _client = APIClient()
        if config is None:
            config = retrieve_config()
        params = portkey.params or Params(**kwargs)
        if config.mode == PortkeyModes.SINGLE.value:
            return cls(_client)._post(
                "/v1/complete",
                body=config.llms,
                mode=PortkeyModes.SINGLE.value,
                params=params,
                cast_to=PortkeyResponse,
                stream_cls=Stream[PortkeyResponse],
                stream=stream,
            )
        if config.mode == PortkeyModes.FALLBACK.value:
            return cls(_client)._post(
                "/v1/complete",
                body=config.llms,
                mode=PortkeyModes.FALLBACK,
                params=params,
                cast_to=PortkeyResponse,
                stream_cls=Stream[PortkeyResponse],
                stream=stream,
            )
        if config.mode == PortkeyModes.LOADBALANCE.value:
            return cls(_client)._post(
                "/v1/complete",
                body=config.llms,
                mode=PortkeyModes.LOADBALANCE,
                params=params,
                cast_to=PortkeyResponse,
                stream_cls=Stream[PortkeyResponse],
                stream=stream,
            )
        raise NotImplementedError("Mode not implemented.")


class ChatCompletions(APIResource):
    @classmethod
    @overload
    def create(
        cls, *, config: Optional[Config] = None, stream: Literal[True], **kwargs
    ) -> Stream[PortkeyResponse]:
        ...

    @classmethod
    @overload
    def create(
        cls,
        *,
        config: Optional[Config] = None,
        stream: Literal[False] = False,
        **kwargs
    ) -> PortkeyResponse:
        ...

    @classmethod
    @overload
    def create(
        cls, *, config: Optional[Config] = None, stream: bool = False, **kwargs
    ) -> Union[PortkeyResponse, Stream[PortkeyResponse]]:
        ...

    @classmethod
    def create(
        cls, *, config: Optional[Config] = None, stream: bool = False, **kwargs
    ) -> Union[PortkeyResponse, Stream[PortkeyResponse]]:
        _client = APIClient()
        if config is None:
            config = retrieve_config()
        params = portkey.params or Params(**kwargs)
        if config.mode == PortkeyModes.SINGLE.value:
            return cls(_client)._post(
                "/v1/chatComplete",
                body=config.llms,
                mode=PortkeyModes.SINGLE.value,
                params=params,
                cast_to=PortkeyResponse,
                stream_cls=Stream[PortkeyResponse],
                stream=stream,
            )
        if config.mode == PortkeyModes.FALLBACK.value:
            return cls(_client)._post(
                "/v1/chatComplete",
                body=config.llms,
                mode=PortkeyModes.FALLBACK,
                params=params,
                cast_to=PortkeyResponse,
                stream_cls=Stream[PortkeyResponse],
                stream=stream,
            )
        if config.mode == PortkeyModes.LOADBALANCE.value:
            return cls(_client)._post(
                "/v1/chatComplete",
                body=config.llms,
                mode=PortkeyModes.LOADBALANCE,
                params=params,
                cast_to=PortkeyResponse,
                stream_cls=Stream[PortkeyResponse],
                stream=stream,
            )
        raise NotImplementedError("Mode not implemented.")
