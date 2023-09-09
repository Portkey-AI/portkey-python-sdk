from typing import Optional, Union, overload, Literal, Dict, Any
from portkey.api_resources.base_client import APIClient
import portkey
from .utils import (
    PortkeyModes,
    PortkeyResponse,
    Config,
    retrieve_config,
    Params,
    PortkeyCacheType,
    PortkeyCacheLiteral,
)

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
        cls,
        *,
        config: Optional[Config] = None,
        stream: Literal[True],
        virtual_key: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        max_retries: Optional[int] = None,
        trace_id: Optional[str] = None,
        cache_status: Optional[Union[PortkeyCacheType, PortkeyCacheLiteral]] = None,
        cache: Optional[bool] = None,
        metadata: Optional[Dict[str, Any]] = None,
        weight: Optional[float] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        **kwargs
    ) -> Stream[PortkeyResponse]:
        ...

    @classmethod
    @overload
    def create(
        cls,
        *,
        config: Optional[Config] = None,
        stream: Literal[False] = False,
        virtual_key: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        max_retries: Optional[int] = None,
        trace_id: Optional[str] = None,
        cache_status: Optional[Union[PortkeyCacheType, PortkeyCacheLiteral]] = None,
        cache: Optional[bool] = None,
        metadata: Optional[Dict[str, Any]] = None,
        weight: Optional[float] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        **kwargs
    ) -> PortkeyResponse:
        ...

    @classmethod
    @overload
    def create(
        cls,
        *,
        config: Optional[Config] = None,
        stream: bool = False,
        virtual_key: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        max_retries: Optional[int] = None,
        trace_id: Optional[str] = None,
        cache_status: Optional[Union[PortkeyCacheType, PortkeyCacheLiteral]] = None,
        cache: Optional[bool] = None,
        metadata: Optional[Dict[str, Any]] = None,
        weight: Optional[float] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        **kwargs
    ) -> Union[PortkeyResponse, Stream[PortkeyResponse]]:
        ...

    @classmethod
    def create(
        cls,
        *,
        config: Optional[Config] = None,
        stream: bool = False,
        virtual_key: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        max_retries: Optional[int] = None,
        trace_id: Optional[str] = None,
        cache_status: Optional[Union[PortkeyCacheType, PortkeyCacheLiteral]] = None,
        cache: Optional[bool] = None,
        metadata: Optional[Dict[str, Any]] = None,
        weight: Optional[float] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        **kwargs
    ) -> Union[PortkeyResponse, Stream[PortkeyResponse]]:
        _client = APIClient()
        if config is None:
            config = retrieve_config()
        params = portkey.params or Params(
            virtual_key=virtual_key,
            temperature=temperature,
            max_tokens=max_tokens,
            max_retries=max_retries,
            trace_id=trace_id,
            cache_status=cache_status,
            cache=cache,
            metadata=metadata,
            weight=weight,
            top_k=top_k,
            top_p=top_p,
            **kwargs
        )
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
        cls,
        *,
        config: Optional[Config] = None,
        stream: Literal[True],
        virtual_key: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        max_retries: Optional[int] = None,
        trace_id: Optional[str] = None,
        cache_status: Optional[Union[PortkeyCacheType, PortkeyCacheLiteral]] = None,
        cache: Optional[bool] = None,
        metadata: Optional[Dict[str, Any]] = None,
        weight: Optional[float] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        **kwargs
    ) -> Stream[PortkeyResponse]:
        ...

    @classmethod
    @overload
    def create(
        cls,
        *,
        config: Optional[Config] = None,
        stream: Literal[False] = False,
        virtual_key: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        max_retries: Optional[int] = None,
        trace_id: Optional[str] = None,
        cache_status: Optional[Union[PortkeyCacheType, PortkeyCacheLiteral]] = None,
        cache: Optional[bool] = None,
        metadata: Optional[Dict[str, Any]] = None,
        weight: Optional[float] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        **kwargs
    ) -> PortkeyResponse:
        ...

    @classmethod
    @overload
    def create(
        cls,
        *,
        config: Optional[Config] = None,
        stream: bool = False,
        virtual_key: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        max_retries: Optional[int] = None,
        trace_id: Optional[str] = None,
        cache_status: Optional[Union[PortkeyCacheType, PortkeyCacheLiteral]] = None,
        cache: Optional[bool] = None,
        metadata: Optional[Dict[str, Any]] = None,
        weight: Optional[float] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        **kwargs
    ) -> Union[PortkeyResponse, Stream[PortkeyResponse]]:
        ...

    @classmethod
    def create(
        cls,
        *,
        config: Optional[Config] = None,
        stream: bool = False,
        virtual_key: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        max_retries: Optional[int] = None,
        trace_id: Optional[str] = None,
        cache_status: Optional[Union[PortkeyCacheType, PortkeyCacheLiteral]] = None,
        cache: Optional[bool] = None,
        metadata: Optional[Dict[str, Any]] = None,
        weight: Optional[float] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        **kwargs
    ) -> Union[PortkeyResponse, Stream[PortkeyResponse]]:
        _client = APIClient()
        if config is None:
            config = retrieve_config()
        params = portkey.params or Params(
            virtual_key=virtual_key,
            temperature=temperature,
            max_tokens=max_tokens,
            max_retries=max_retries,
            trace_id=trace_id,
            cache_status=cache_status,
            cache=cache,
            metadata=metadata,
            weight=weight,
            top_k=top_k,
            top_p=top_p,
            **kwargs
        )
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
