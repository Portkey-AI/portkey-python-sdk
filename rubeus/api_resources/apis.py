from typing import Optional, Union, List, Dict, Any, cast, overload, Literal

from rubeus.api_resources.base_client import APIClient
from .global_constants import DEFAULT_MAX_RETRIES, DEFAULT_TIMEOUT
from .utils import (
    ProviderTypes,
    RubeusCacheType,
    LLMBase,
    RubeusModes,
    Message,
    ProviderTypesLiteral,
    Body,
    RubeusResponse,
    RetrySettings,
    Function,
)

from .streaming import Stream

__all__ = ["Completions", "ChatCompletions"]


class APIResource:
    _client: APIClient

    def __init__(self, client: APIClient) -> None:
        self._client = client
        # self._get = client.get
        self._post = client.post
        # self._patch = client.patch
        # self._put = client.put
        # self._delete = client.delete
        # self._get_api_list = client.get_api_list


class Completions(APIResource):
    @overload
    def create(
        self,
        *,
        prompt: str = "",
        timeout: Union[float, None] = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        provider: Union[ProviderTypes, ProviderTypesLiteral] = ProviderTypes.OPENAI,
        model: str = "gpt-3.5-turbo",
        api_key: str = "",
        temperature: float = 0.1,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        stop_sequences: Optional[List[str]] = None,
        max_tokens: Optional[int] = None,
        trace_id: Optional[str] = None,
        cache_status: Optional[RubeusCacheType] = None,
        cache: Optional[bool] = False,
        metadata: Optional[Dict[str, Any]] = None,
        weight: Optional[float] = 1.0,
        stream: Literal[True],
        retry_settings: Optional[RetrySettings] = None,
        functions: Optional[List[Function]] = None,
        function_call: Optional[Union[None, str, Function]] = None,
        n: Optional[int] = None,
        logprobs: Optional[int] = None,
        echo: Optional[bool] = None,
        stop: Optional[Union[str, List[str]]] = None,
        presence_penalty: Optional[int] = None,
        frequency_penalty: Optional[int] = None,
        best_of: Optional[int] = None,
        logit_bias: Optional[Dict[str, int]] = None,
        user: Optional[str] = None,
    ) -> Stream[RubeusResponse]:
        ...

    @overload
    def create(
        self,
        *,
        prompt: str = "",
        timeout: Union[float, None] = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        provider: Union[ProviderTypes, ProviderTypesLiteral] = ProviderTypes.OPENAI,
        model: str = "gpt-3.5-turbo",
        api_key: str = "",
        temperature: float = 0.1,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        stop_sequences: Optional[List[str]] = None,
        max_tokens: Optional[int] = None,
        trace_id: Optional[str] = None,
        cache_status: Optional[RubeusCacheType] = None,
        cache: Optional[bool] = False,
        metadata: Optional[Dict[str, Any]] = None,
        weight: Optional[float] = 1.0,
        stream: Literal[False] = False,
        retry_settings: Optional[RetrySettings] = None,
        functions: Optional[List[Function]] = None,
        function_call: Optional[Union[None, str, Function]] = None,
        n: Optional[int] = None,
        logprobs: Optional[int] = None,
        echo: Optional[bool] = None,
        stop: Optional[Union[str, List[str]]] = None,
        presence_penalty: Optional[int] = None,
        frequency_penalty: Optional[int] = None,
        best_of: Optional[int] = None,
        logit_bias: Optional[Dict[str, int]] = None,
        user: Optional[str] = None,
    ) -> RubeusResponse:
        ...

    @overload
    def create(
        self,
        *,
        prompt: str = "",
        timeout: Union[float, None] = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        provider: Union[ProviderTypes, ProviderTypesLiteral] = ProviderTypes.OPENAI,
        model: str = "gpt-3.5-turbo",
        api_key: str = "",
        temperature: float = 0.1,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        stop_sequences: Optional[List[str]] = None,
        max_tokens: Optional[int] = None,
        trace_id: Optional[str] = None,
        cache_status: Optional[RubeusCacheType] = None,
        cache: Optional[bool] = False,
        metadata: Optional[Dict[str, Any]] = None,
        weight: Optional[float] = 1.0,
        stream: bool = False,
        retry_settings: Optional[RetrySettings] = None,
        functions: Optional[List[Function]] = None,
        function_call: Optional[Union[None, str, Function]] = None,
        n: Optional[int] = None,
        logprobs: Optional[int] = None,
        echo: Optional[bool] = None,
        stop: Optional[Union[str, List[str]]] = None,
        presence_penalty: Optional[int] = None,
        frequency_penalty: Optional[int] = None,
        best_of: Optional[int] = None,
        logit_bias: Optional[Dict[str, int]] = None,
        user: Optional[str] = None,
    ) -> Union[RubeusResponse, Stream[RubeusResponse]]:
        ...

    def create(
        self,
        *,
        prompt: str = "",
        timeout: Union[float, None] = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        provider: Union[ProviderTypes, ProviderTypesLiteral] = ProviderTypes.OPENAI,
        model: str = "gpt-3.5-turbo",
        api_key: str = "",
        temperature: float = 0.1,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        stop_sequences: Optional[List[str]] = None,
        max_tokens: Optional[int] = None,
        trace_id: Optional[str] = None,
        cache_status: Optional[RubeusCacheType] = None,
        cache: Optional[bool] = False,
        metadata: Optional[Dict[str, Any]] = None,
        weight: Optional[float] = 1.0,
        stream: bool = False,
        retry_settings: Optional[RetrySettings] = None,
        functions: Optional[List[Function]] = None,
        function_call: Optional[Union[None, str, Function]] = None,
        n: Optional[int] = None,
        logprobs: Optional[int] = None,
        echo: Optional[bool] = None,
        stop: Optional[Union[str, List[str]]] = None,
        presence_penalty: Optional[int] = None,
        frequency_penalty: Optional[int] = None,
        best_of: Optional[int] = None,
        logit_bias: Optional[Dict[str, int]] = None,
        user: Optional[str] = None,
    ) -> Union[RubeusResponse, Stream[RubeusResponse]]:
        llm = Body(
            prompt=prompt,
            timeout=timeout,
            max_retries=max_retries,
            provider=provider,
            model=model,
            api_key=api_key,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            stop_sequences=stop_sequences,
            max_tokens=max_tokens,
            trace_id=trace_id,
            cache_status=cache_status,
            cache=cache,
            metadata=metadata,
            weight=weight,
            retry_settings=retry_settings,
            functions=functions,
            function_call=function_call,
            n=n,
            logprobs=logprobs,
            echo=echo,
            stop=stop,
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
            best_of=best_of,
            logit_bias=logit_bias,
            user=user,
        )
        return self._post(
            "/v1/complete",
            body=[llm],
            mode=RubeusModes.SINGLE.value,
            cast_to=RubeusResponse,
            stream_cls=Stream[RubeusResponse],
            stream=stream,
        )

    @overload
    def with_fallbacks(
        self, *, llms: List[LLMBase], stream: Literal[True]
    ) -> Stream[RubeusResponse]:
        ...

    @overload
    def with_fallbacks(
        self, *, llms: List[LLMBase], stream: Literal[False] = False
    ) -> RubeusResponse:
        ...

    @overload
    def with_fallbacks(
        self, *, llms: List[LLMBase], stream: bool = False
    ) -> Union[RubeusResponse, Stream[RubeusResponse]]:
        ...

    def with_fallbacks(
        self, llms: List[LLMBase], stream: bool = False
    ) -> Union[RubeusResponse, Stream[RubeusResponse]]:
        body = []
        for i in llms:
            body.append(cast(Body, i))
        return self._post(
            "/v1/complete",
            body=body,
            mode=RubeusModes.FALLBACK,
            cast_to=RubeusResponse,
            stream_cls=Stream[RubeusResponse],
            stream=stream,
        )

    @overload
    def with_loadbalancing(
        self, llms: List[LLMBase], stream: Literal[True]
    ) -> Stream[RubeusResponse]:
        ...

    @overload
    def with_loadbalancing(
        self, llms: List[LLMBase], stream: Literal[False] = False
    ) -> RubeusResponse:
        ...

    @overload
    def with_loadbalancing(
        self, llms: List[LLMBase], stream: bool = False
    ) -> Union[RubeusResponse, Stream[RubeusResponse]]:
        ...

    def with_loadbalancing(
        self, llms: List[LLMBase], stream: bool = False
    ) -> Union[RubeusResponse, Stream[RubeusResponse]]:
        body = []
        for i in llms:
            body.append(cast(Body, i))
        return self._post(
            "/v1/complete",
            body=body,
            mode=RubeusModes.LOADBALANCE,
            cast_to=RubeusResponse,
            stream_cls=Stream[RubeusResponse],
            stream=stream,
        )

    @overload
    def single(
        self, llms: List[LLMBase], stream: Literal[True]
    ) -> Stream[RubeusResponse]:
        ...

    @overload
    def single(
        self, llms: List[LLMBase], stream: Literal[False] = False
    ) -> RubeusResponse:
        ...

    @overload
    def single(
        self, llms: List[LLMBase], stream: bool = False
    ) -> Union[RubeusResponse, Stream[RubeusResponse]]:
        ...

    def single(
        self, llms: List[LLMBase], stream: bool = False
    ) -> Union[RubeusResponse, Stream[RubeusResponse]]:
        body = []
        for i in llms:
            body.append(cast(Body, i))
        return self._post(
            "/v1/complete",
            body=body,
            mode=RubeusModes.SINGLE,
            cast_to=RubeusResponse,
            stream_cls=Stream[RubeusResponse],
            stream=stream,
        )


class ChatCompletions(APIResource):
    @overload
    def create(
        self,
        *,
        messages: List[Message],
        provider: ProviderTypes = ProviderTypes.OPENAI,
        model: str = "gpt-3.5-turbo",
        api_key: str = "",
        timeout: Union[float, None] = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        temperature: float = 0.1,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        stop_sequences: Optional[List[str]] = None,
        max_tokens: Optional[int] = None,
        trace_id: Optional[str] = "",
        cache_status: Optional[RubeusCacheType] = None,
        cache: Optional[bool] = False,
        metadata: Optional[Dict[str, Any]] = None,
        weight: Optional[float] = 1.0,
        stream: Literal[True],
        retry_settings: Optional[RetrySettings] = None,
        functions: Optional[List[Function]] = None,
        function_call: Optional[Union[None, str, Function]] = None,
        n: Optional[int] = None,
        logprobs: Optional[int] = None,
        echo: Optional[bool] = None,
        stop: Optional[Union[str, List[str]]] = None,
        presence_penalty: Optional[int] = None,
        frequency_penalty: Optional[int] = None,
        best_of: Optional[int] = None,
        logit_bias: Optional[Dict[str, int]] = None,
        user: Optional[str] = None,
    ) -> Stream[RubeusResponse]:
        ...

    @overload
    def create(
        self,
        *,
        messages: List[Message],
        provider: ProviderTypes = ProviderTypes.OPENAI,
        model: str = "gpt-3.5-turbo",
        api_key: str = "",
        timeout: Union[float, None] = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        temperature: float = 0.1,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        stop_sequences: Optional[List[str]] = None,
        max_tokens: Optional[int] = None,
        trace_id: Optional[str] = "",
        cache_status: Optional[RubeusCacheType] = None,
        cache: Optional[bool] = False,
        metadata: Optional[Dict[str, Any]] = None,
        weight: Optional[float] = 1.0,
        stream: Literal[False] = False,
        retry_settings: Optional[RetrySettings] = None,
        functions: Optional[List[Function]] = None,
        function_call: Optional[Union[None, str, Function]] = None,
        n: Optional[int] = None,
        logprobs: Optional[int] = None,
        echo: Optional[bool] = None,
        stop: Optional[Union[str, List[str]]] = None,
        presence_penalty: Optional[int] = None,
        frequency_penalty: Optional[int] = None,
        best_of: Optional[int] = None,
        logit_bias: Optional[Dict[str, int]] = None,
        user: Optional[str] = None,
    ) -> RubeusResponse:
        ...

    @overload
    def create(
        self,
        *,
        messages: List[Message],
        provider: ProviderTypes = ProviderTypes.OPENAI,
        model: str = "gpt-3.5-turbo",
        api_key: str = "",
        timeout: Union[float, None] = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        temperature: float = 0.1,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        stop_sequences: Optional[List[str]] = None,
        max_tokens: Optional[int] = None,
        trace_id: Optional[str] = "",
        cache_status: Optional[RubeusCacheType] = None,
        cache: Optional[bool] = False,
        metadata: Optional[Dict[str, Any]] = None,
        weight: Optional[float] = 1.0,
        stream: bool = False,
        retry_settings: Optional[RetrySettings] = None,
        functions: Optional[List[Function]] = None,
        function_call: Optional[Union[None, str, Function]] = None,
        n: Optional[int] = None,
        logprobs: Optional[int] = None,
        echo: Optional[bool] = None,
        stop: Optional[Union[str, List[str]]] = None,
        presence_penalty: Optional[int] = None,
        frequency_penalty: Optional[int] = None,
        best_of: Optional[int] = None,
        logit_bias: Optional[Dict[str, int]] = None,
        user: Optional[str] = None,
    ) -> Union[RubeusResponse, Stream[RubeusResponse]]:
        ...

    def create(
        self,
        *,
        messages: List[Message],
        provider: ProviderTypes = ProviderTypes.OPENAI,
        model: str = "gpt-3.5-turbo",
        api_key: str = "",
        timeout: Union[float, None] = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        temperature: float = 0.1,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        stop_sequences: Optional[List[str]] = None,
        max_tokens: Optional[int] = None,
        trace_id: Optional[str] = "",
        cache_status: Optional[RubeusCacheType] = None,
        cache: Optional[bool] = False,
        metadata: Optional[Dict[str, Any]] = None,
        weight: Optional[float] = 1.0,
        stream: bool = False,
        retry_settings: Optional[RetrySettings] = None,
        functions: Optional[List[Function]] = None,
        function_call: Optional[Union[None, str, Function]] = None,
        n: Optional[int] = None,
        logprobs: Optional[int] = None,
        echo: Optional[bool] = None,
        stop: Optional[Union[str, List[str]]] = None,
        presence_penalty: Optional[int] = None,
        frequency_penalty: Optional[int] = None,
        best_of: Optional[int] = None,
        logit_bias: Optional[Dict[str, int]] = None,
        user: Optional[str] = None,
    ) -> Union[RubeusResponse, Stream[RubeusResponse]]:
        llm = Body(
            messages=messages,
            timeout=timeout,
            max_retries=max_retries,
            provider=provider,
            model=model,
            api_key=api_key,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            stop_sequences=stop_sequences,
            max_tokens=max_tokens,
            trace_id=trace_id,
            cache_status=cache_status,
            cache=cache,
            metadata=metadata,
            weight=weight,
            retry_settings=retry_settings,
            functions=functions,
            function_call=function_call,
            n=n,
            logprobs=logprobs,
            echo=echo,
            stop=stop,
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
            best_of=best_of,
            logit_bias=logit_bias,
            user=user,
        )
        return self._post(
            "/v1/chatComplete",
            body=[llm],
            mode=RubeusModes.SINGLE.value,
            cast_to=RubeusResponse,
            stream_cls=Stream[RubeusResponse],
            stream=stream,
        )

    @overload
    def with_fallbacks(
        self, *, llms: List[LLMBase], stream: Literal[True]
    ) -> Stream[RubeusResponse]:
        ...

    @overload
    def with_fallbacks(
        self, *, llms: List[LLMBase], stream: Literal[False] = False
    ) -> RubeusResponse:
        ...

    @overload
    def with_fallbacks(
        self, *, llms: List[LLMBase], stream: bool = False
    ) -> Union[RubeusResponse, Stream[RubeusResponse]]:
        ...

    def with_fallbacks(
        self, *, llms: List[LLMBase], stream: bool = False
    ) -> Union[RubeusResponse, Stream[RubeusResponse]]:
        body = []
        for i in llms:
            body.append(cast(Body, i))
        return self._post(
            "/v1/chatComplete",
            body=body,
            mode=RubeusModes.FALLBACK,
            cast_to=RubeusResponse,
            stream_cls=Stream[RubeusResponse],
            stream=stream,
        )

    @overload
    def with_loadbalancing(
        self, llms: List[LLMBase], stream: Literal[True]
    ) -> Stream[RubeusResponse]:
        ...

    @overload
    def with_loadbalancing(
        self, llms: List[LLMBase], stream: Literal[False] = False
    ) -> RubeusResponse:
        ...

    @overload
    def with_loadbalancing(
        self, llms: List[LLMBase], stream: bool = False
    ) -> Union[RubeusResponse, Stream[RubeusResponse]]:
        ...

    def with_loadbalancing(
        self, llms: List[LLMBase], stream: bool = False
    ) -> Union[RubeusResponse, Stream[RubeusResponse]]:
        body = []
        for i in llms:
            body.append(cast(Body, i))
        return self._post(
            "/v1/chatComplete",
            body=body,
            mode=RubeusModes.LOADBALANCE,
            cast_to=RubeusResponse,
            stream_cls=Stream[RubeusResponse],
            stream=stream,
        )

    @overload
    def single(
        self, llms: List[LLMBase], stream: Literal[True]
    ) -> Stream[RubeusResponse]:
        ...

    @overload
    def single(
        self, llms: List[LLMBase], stream: Literal[False] = False
    ) -> RubeusResponse:
        ...

    @overload
    def single(
        self, llms: List[LLMBase], stream: bool = False
    ) -> Union[RubeusResponse, Stream[RubeusResponse]]:
        ...

    def single(
        self, llms: List[LLMBase], stream: bool = False
    ) -> Union[RubeusResponse, Stream[RubeusResponse]]:
        body = []
        for i in llms:
            body.append(cast(Body, i))
        return self._post(
            "/v1/chatComplete",
            body=body,
            mode=RubeusModes.SINGLE,
            cast_to=RubeusResponse,
            stream_cls=Stream[RubeusResponse],
            stream=stream,
        )
