import os
from enum import Enum
import httpx
from typing import List, Dict, Any, Optional, Union, Mapping, Literal, TypeVar, cast
from typing_extensions import TypedDict
from pydantic import BaseModel
from .exceptions import (
    APIStatusError,
    BadRequestError,
    AuthenticationError,
    PermissionDeniedError,
    NotFoundError,
    ConflictError,
    UnprocessableEntityError,
    RateLimitError,
    InternalServerError,
)


class RubeusCacheType(Enum):
    SEMANTIC = "semantic"
    SIMPLE = "simple"


RubeusCacheLiteral = Literal["semantic", "simple"]


ResponseT = TypeVar("ResponseT", bound="RubeusResponse")


class ProviderTypes(str, Enum):
    """_summary_

    Args:
        Enum (_type_): _description_

    Returns:
        _type_: _description_
    """

    OPENAI = "openai"
    COHERE = "cohere"
    ANTHROPIC = "anthropic"
    AZURE_OPENAI = "azure-openai"
    HUGGING_FACE = "huggingface"


ProviderTypesLiteral = Literal[
    "openai", "cohere", "anthropic", "azure-openai", "huggingface"
]


class RubeusModes(str, Enum):
    """_summary_

    Args:
        Enum (_type_): _description_
    """

    FALLBACK = "fallback"
    LOADBALANCE = "loadbalance"
    SINGLE = "single"
    PROXY = "proxy"


RubeusModesLiteral = Literal["fallback", "loadbalance", "single", "proxy"]


class RubeusApiPaths(Enum):
    CHAT_COMPLETION = "/v1/chatComplete"
    COMPLETION = "/v1/complete"


class Options(BaseModel):
    method: str
    url: str
    params: Optional[Mapping[str, str]] = None
    headers: Optional[Mapping[str, str]] = None
    max_retries: Optional[int] = None
    timeout: Optional[float] = None
    # stringified json
    data: Optional[Mapping[str, Any]] = None
    # json structure
    json_body: Optional[Mapping[str, Any]] = None


class Message(TypedDict):
    role: str
    content: str


class Function(BaseModel):
    name: str
    description: str
    parameters: str


class RetrySettings(BaseModel):
    attempts: int
    on_status_codes: list


class OverrideParams(TypedDict, total=False):
    provider: Optional[Union[ProviderTypes, ProviderTypesLiteral]]
    prompt: Optional[str]
    messages: Optional[List[Message]]
    temperature: Optional[float]
    max_tokens: Optional[int]
    max_retries: Optional[int]
    trace_id: Optional[str]
    cache_status: Optional[Union[RubeusCacheType, RubeusCacheLiteral]]
    cache: Optional[bool]
    metadata: Optional[Dict[str, Any]]
    weight: Optional[float]
    top_k: Optional[int]
    top_p: Optional[float]
    stop_sequences: Optional[List[str]]
    timeout: Union[float, None]
    retry_settings: Optional[RetrySettings]
    model: Optional[str]
    api_key: Optional[str]
    stream: Optional[bool]
    functions: Optional[List[Function]]
    function_call: Optional[Union[None, str, Function]]
    n: Optional[int]
    logprobs: Optional[int]
    echo: Optional[bool]
    stop: Optional[Union[str, List[str]]]
    presence_penalty: Optional[int]
    frequency_penalty: Optional[int]
    best_of: Optional[int]
    logit_bias: Optional[Mapping[str, int]]
    user: Optional[str]


class ProviderOptions(BaseModel):
    provider: Optional[str]
    apiKey: Optional[str]
    weight: Optional[float]
    override_params: Optional[OverrideParams]
    retry: Optional[RetrySettings]


class Config(BaseModel):
    mode: str
    options: List[ProviderOptions]


def remove_empty_values(
    data: Union[Dict[str, Any], Mapping[str, Any]]
) -> Dict[str, Any]:
    if isinstance(data, dict):
        cleaned_dict = {}
        for key, value in data.items():
            if value is not None and value != "":
                cleaned_value = remove_empty_values(value)
                if cleaned_value is not None and cleaned_value != "":
                    cleaned_dict[key] = cleaned_value
        return cleaned_dict
    elif isinstance(data, list):
        cleaned_list = []

        for item in data:  # type: ignore
            cleaned_item = remove_empty_values(item)
            if cleaned_item is not None and cleaned_item != "":
                cleaned_list.append(cleaned_item)
        return cleaned_list  # type: ignore
    else:
        return cast(dict, data)


# class DefaultHeaders(TypedDict. total=false)


class DefaultParams(BaseModel):
    provider: Optional[Union[ProviderTypes, ProviderTypesLiteral]] = None
    prompt: Optional[str] = None
    messages: Optional[List[Message]] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    max_retries: Optional[int] = None
    trace_id: Optional[str] = None
    cache_status: Optional[Union[RubeusCacheType, RubeusCacheLiteral]] = None
    cache: Optional[bool] = None
    metadata: Optional[Dict[str, Any]] = None
    weight: Optional[float] = None
    top_k: Optional[int] = None
    top_p: Optional[float] = None
    stop_sequences: Optional[List[str]] = None
    timeout: Union[float, None] = None
    retry_settings: Optional[RetrySettings] = None
    model: Optional[str] = None
    api_key: Optional[str] = None
    stream: Optional[bool] = False
    functions: Optional[List[Function]]
    function_call: Optional[Union[None, str, Function]]
    n: Optional[int]
    logprobs: Optional[int]
    echo: Optional[bool]
    stop: Optional[Union[str, List[str]]]
    presence_penalty: Optional[int]
    frequency_penalty: Optional[int]
    best_of: Optional[int]
    logit_bias: Optional[Dict[str, int]]
    user: Optional[str]

    def __init__(
        self,
        *,
        prompt: Optional[str] = None,
        messages: Optional[List[Message]] = None,
        provider: Optional[Union[ProviderTypes, ProviderTypesLiteral]] = None,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        max_retries: Optional[int] = None,
        trace_id: Optional[str] = None,
        cache_status: Optional[Union[RubeusCacheType, RubeusCacheLiteral]] = None,
        cache: Optional[bool] = None,
        metadata: Optional[Dict[str, Any]] = None,
        weight: Optional[float] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        stop_sequences: Optional[List[str]] = None,
        stream: Optional[bool] = False,
        timeout: Union[float, None] = None,
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
    ):
        api_key = api_key or apikey_from_env(provider)
        super().__init__(
            prompt=prompt,
            messages=messages,
            provider=provider,
            model=model,
            api_key=api_key,
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
            stop_sequences=stop_sequences,
            stream=stream,
            timeout=timeout,
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


class LLMBase(BaseModel):
    """
    provider (Optional[ProviderTypes]): The LLM provider to be used for the Portkey
    integration.
        Eg: openai, anthropic etc.
        NOTE: Check the ProviderTypes to see the supported list of LLMs.
    model (str): The name of the language model to use (default: "gpt-3.5-turbo").
    temperature (float): The temperature parameter for text generation (default: 0.1).
    max_tokens (Optional[int]): The maximum number of tokens in the generated text.
    max_retries (int): The maximum number of retries for failed requests (default: 5).
    trace_id (Optional[str]): A unique identifier for tracing requests.
    cache_status (Optional[Union[RubeusCacheType,  RubeusCacheLiteral]]): The type of c
    ache to use (default: "").
        If cache_status is set, then cache is automatically set to True
    cache (Optional[bool]): Whether to use caching (default: False).
    metadata (Optional[Dict[str, Any]]): Metadata associated with the request
    (default: {}).
    weight (Optional[float]): The weight of the LLM in the ensemble (default: 1.0).
    """

    prompt: Optional[str] = None
    messages: Optional[List[Message]] = None
    provider: Union[ProviderTypes, ProviderTypesLiteral]
    model: str
    api_key: str
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    max_retries: Optional[int] = None
    trace_id: Optional[str] = None
    cache_status: Optional[Union[RubeusCacheType, RubeusCacheLiteral]] = None
    cache: Optional[bool] = None
    metadata: Optional[Dict[str, Any]] = None
    weight: Optional[float] = None
    top_k: Optional[int] = None
    top_p: Optional[float] = None
    stop_sequences: Optional[List[str]] = None
    timeout: Union[float, None] = None
    retry_settings: Optional[RetrySettings] = None
    functions: Optional[List[Function]]
    function_call: Optional[Union[None, str, Function]]
    n: Optional[int]
    logprobs: Optional[int]
    echo: Optional[bool]
    stop: Optional[Union[str, List[str]]]
    presence_penalty: Optional[int]
    frequency_penalty: Optional[int]
    best_of: Optional[int]
    logit_bias: Optional[Dict[str, int]]
    user: Optional[str]

    # NOTE: We do not support streaming in over-ride params.
    def __init__(
        self,
        *,
        prompt: Optional[str] = None,
        messages: Optional[List[Message]] = None,
        provider: Union[ProviderTypes, ProviderTypesLiteral],
        model: str,
        api_key: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        max_retries: Optional[int] = None,
        trace_id: Optional[str] = None,
        cache_status: Optional[RubeusCacheType] = None,
        cache: Optional[bool] = None,
        metadata: Optional[Dict[str, Any]] = None,
        weight: Optional[float] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        stop_sequences: Optional[List[str]] = None,
        timeout: Union[float, None] = None,
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
    ):
        api_key = api_key or apikey_from_env(provider)
        super().__init__(
            prompt=prompt,
            messages=messages,
            provider=provider,
            model=model,
            api_key=api_key,
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
            stop_sequences=stop_sequences,
            timeout=timeout,
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

    def override_params(self) -> OverrideParams:
        return {
            "prompt": self.prompt,
            "messages": self.messages,
            "provider": self.provider,
            "model": self.model,
            "api_key": self.api_key,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "max_retries": self.max_retries,
            "trace_id": self.trace_id,
            "cache_status": self.cache_status,
            "cache": self.cache,
            "metadata": self.metadata,
            "weight": self.weight,
            "top_k": self.top_k,
            "top_p": self.top_p,
            "stop_sequences": self.stop_sequences,
            "timeout": self.timeout,
            "retry_settings": self.retry_settings,
            "functions": self.functions,
            "function_call": self.function_call,
            "n": self.n,
            "logprobs": self.logprobs,
            "echo": self.echo,
            "stop": self.stop,
            "presence_penalty": self.presence_penalty,
            "frequency_penalty": self.frequency_penalty,
            "best_of": self.best_of,
            "logit_bias": self.logit_bias,
            "user": self.user,
        }


class Body(LLMBase):
    pass


class Params(LLMBase):
    pass


class RequestData(BaseModel):
    config: Config
    params: Params


class RubeusResponse(BaseModel):
    model: str
    choices: List[Any]
    raw_body: Dict[str, Any]


def apikey_from_env(provider: Union[ProviderTypes, ProviderTypesLiteral, None]) -> str:
    if provider == ProviderTypes.OPENAI:
        return os.environ.get("OPENAI_API_KEY", "")
    elif provider == ProviderTypes.COHERE:
        return os.environ.get("COHERE_API_KEY", "")
    elif provider == ProviderTypes.AZURE_OPENAI:
        return os.environ.get("AZURE_OPENAI_API_KEY", "")
    elif provider == ProviderTypes.HUGGING_FACE:
        return os.environ.get("HUGGINGFACE_API_KEY", "")
    elif provider == ProviderTypes.HUGGING_FACE:
        return os.environ.get("ANTHROPIC_API_KEY", "")
    return ""


def make_status_error(
    err_msg: str,
    *,
    body: object,
    request: httpx.Request,
    response: httpx.Response,
) -> APIStatusError:
    if response.status_code == 400:
        return BadRequestError(err_msg, request=request, response=response, body=body)
    if response.status_code == 401:
        return AuthenticationError(
            err_msg, request=request, response=response, body=body
        )
    if response.status_code == 403:
        return PermissionDeniedError(
            err_msg, request=request, response=response, body=body
        )
    if response.status_code == 404:
        return NotFoundError(err_msg, request=request, response=response, body=body)
    if response.status_code == 409:
        return ConflictError(err_msg, request=request, response=response, body=body)
    if response.status_code == 422:
        return UnprocessableEntityError(
            err_msg, request=request, response=response, body=body
        )
    if response.status_code == 429:
        return RateLimitError(err_msg, request=request, response=response, body=body)
    if response.status_code >= 500:
        return InternalServerError(
            err_msg, request=request, response=response, body=body
        )
    return APIStatusError(err_msg, request=request, response=response, body=body)
