import os
import json
from typing import List, Dict, Any, Optional, Union, Mapping, Literal, TypeVar, cast
from enum import Enum
from typing_extensions import TypedDict
import httpx
import portkey
from pydantic import BaseModel, validator
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
from .global_constants import (
    MISSING_API_KEY_ERROR_MESSAGE,
    INVALID_PORTKEY_MODE,
    MISSING_BASE_URL,
    MISSING_CONFIG_MESSAGE,
    MISSING_MODE_MESSAGE,
)


class CacheType(str, Enum):
    SEMANTIC = "semantic"
    SIMPLE = "simple"


CacheLiteral = Literal["semantic", "simple"]


ResponseT = TypeVar(
    "ResponseT",
    bound="Union[ChatCompletionChunk, ChatCompletion, TextCompletionChunk, TextCompletion]",
)


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


class Modes(str, Enum):
    """_summary_

    Args:
        Enum (_type_): _description_
    """

    FALLBACK = "fallback"
    AB_TEST = "ab_test"
    SINGLE = "single"
    PROXY = "proxy"


class ApiType(str, Enum):
    COMPLETIONS = "completions"
    CHAT_COMPLETION = "chat_completions"


ModesLiteral = Literal["fallback", "loadbalance", "single", "proxy"]


class PortkeyApiPaths(Enum):
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


class RetrySettings(TypedDict):
    attempts: int
    on_status_codes: list


class ConversationInput(BaseModel):
    prompt: Optional[str] = None
    messages: Optional[List[Message]] = None


class ModelParams(BaseModel):
    model: Optional[str] = None
    suffix: Optional[str] = None
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    top_k: Optional[int] = None
    top_p: Optional[float] = None
    n: Optional[int] = None
    stop_sequences: Optional[List[str]] = None
    timeout: Union[float, None] = None
    retry_settings: Optional[RetrySettings] = None
    functions: Optional[List[Function]] = None
    function_call: Optional[Union[None, str, Function]] = None
    logprobs: Optional[int] = None
    echo: Optional[bool] = None
    stop: Optional[Union[str, List[str]]] = None
    presence_penalty: Optional[int] = None
    frequency_penalty: Optional[int] = None
    best_of: Optional[int] = None
    logit_bias: Optional[Dict[str, int]] = None
    user: Optional[str] = None
    organization: Optional[str] = None


class OverrideParams(ModelParams, ConversationInput):
    ...


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


class Constructs(BaseModel):
    provider: Union[ProviderTypes, ProviderTypesLiteral]
    api_key: Optional[str] = None
    virtual_key: Optional[str] = None
    cache: Optional[bool] = None
    cache_age: Optional[int] = None
    cache_status: Optional[Union[CacheType, CacheLiteral]] = None
    cache_force_refresh: Optional[bool] = None
    trace_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    weight: Optional[float] = None
    retry: Optional[RetrySettings] = None


class LLMOptions(Constructs, ConversationInput, ModelParams):
    @validator("cache_age", always=True)
    @classmethod
    def parse_cache_age(cls, cache_age):
        if cache_age is not None:
            cache_age = f"max-age={cache_age}"
        return cache_age

    @validator("api_key", "virtual_key", always=False)
    @classmethod
    def parse_api_key(cls, api_key, values):
        if api_key is None and values.get("virtual_key") is None:
            # You can access other fields' values via the 'values' dictionary
            provider = values.get("provider", "")
            api_key = apikey_from_env(provider)
        return api_key


class ProviderOptions(Constructs):
    override_params: Optional[OverrideParams] = None


class RequestConfig(BaseModel):
    mode: str
    options: List[ProviderOptions]


class Body(LLMOptions):
    ...


class Params(ConversationInput, ModelParams, extra="forbid"):
    ...


class RequestData(BaseModel):
    config: RequestConfig
    params: Params


class PortkeyResponse(BaseModel):
    model: str
    choices: List[Any]
    raw_body: Dict[str, Any]

    def __str__(self):
        return json.dumps(self.dict(), indent=4)


# Models for Chat Stream
class Delta(BaseModel):
    role: Optional[str] = None
    content: Optional[str] = ""

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


class StreamChoice(BaseModel):
    index: Optional[int] = None
    delta: Union[Delta, Dict[Any, Any]] = {}
    finish_reason: Optional[str] = None

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default

    def __getitem__(self, key):
        return getattr(self, key, None)


class ChatCompletionChunk(BaseModel):
    id: Optional[str] = None
    object: Optional[str] = None
    created: Optional[int] = None
    model: Optional[str] = None
    choices: Union[List[StreamChoice], Dict[Any, Any]] = {}

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


# Models for Chat Non-stream
class ChatChoice(BaseModel):
    index: Optional[int] = None
    message: Optional[Message] = None
    finish_reason: Optional[str] = None

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


class Usage(BaseModel):
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


class ChatCompletion(BaseModel):
    id: Optional[str] = None
    object: Optional[str] = None
    created: Optional[int] = None
    model: Optional[str] = None
    choices: Union[List[ChatChoice], Dict[Any, Any]] = {}
    usage: Optional[Usage] = None

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


# Models for text completion Non-stream
class TextChoice(BaseModel):
    index: Optional[int] = None
    text: Optional[str] = None
    logprobs: Any
    finish_reason: Optional[str] = None

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


class TextCompletion(BaseModel):
    id: Optional[str] = None
    object: Optional[str] = None
    created: Optional[int] = None
    model: Optional[str] = None
    choices: Union[List[TextChoice], Dict[Any, Any]] = {}
    usage: Optional[Usage] = None

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


# Models for text completion stream
class TextCompletionChunk(BaseModel):
    id: Optional[str] = None
    object: Optional[str] = None
    created: Optional[int] = None
    model: Optional[str] = None
    choices: Union[List[TextChoice], Dict[Any, Any]] = {}

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


def apikey_from_env(provider: Union[ProviderTypes, ProviderTypesLiteral]) -> str:
    env_key = f"{provider.upper().replace('-', '_')}_API_KEY"
    if provider is None:
        return ""
    if env_key in os.environ and os.environ[env_key]:
        return os.environ.get(env_key, "")

    raise ValueError(
        f"Did not find '{provider.lower()}' api key, please add an environment variable"
        f" `{env_key}` which contains it, or pass"
        f"  `api_key` as a named parameter in LLMOptions"
    )


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


class Config(BaseModel):
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    mode: Optional[Union[Modes, ModesLiteral]] = "single"
    llms: Union[List[LLMOptions], LLMOptions]

    @validator("mode", always=True)
    @classmethod
    def check_mode(cls, mode):
        if mode is None:
            # You can access other fields' values via the 'values' dictionary
            mode = retrieve_mode()
        if not isinstance(mode, Modes):
            raise ValueError(INVALID_PORTKEY_MODE.format(mode))

        return mode

    @validator("llms", always=True)
    @classmethod
    def parse_llms(cls, llms):
        if isinstance(llms, LLMOptions):
            llms = [llms]
        return llms


def default_api_key() -> str:
    if portkey.api_key:
        return portkey.api_key
    raise ValueError(MISSING_API_KEY_ERROR_MESSAGE)


def default_base_url() -> str:
    if portkey.base_url:
        return portkey.base_url
    raise ValueError(MISSING_BASE_URL)


def retrieve_config() -> Config:
    if portkey.config:
        return portkey.config
    raise ValueError(MISSING_CONFIG_MESSAGE)


def retrieve_mode() -> Union[Modes, ModesLiteral]:
    if portkey.mode:
        return portkey.mode
    raise ValueError(MISSING_MODE_MESSAGE)
