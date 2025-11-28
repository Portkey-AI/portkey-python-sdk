from __future__ import annotations

import json
import os
from typing import List, Dict, Any, Optional, Union, Mapping, Literal, TypeVar, cast
from enum import Enum, EnumMeta
from typing_extensions import TypedDict, NotRequired
import httpx
import portkey_ai
from pydantic import BaseModel
from .._vendor.openai._types import NOT_GIVEN

from portkey_ai.api_resources.types.chat_complete_type import (
    ChatCompletionChunk,
    ChatCompletions,
)
from portkey_ai.api_resources.types.complete_type import (
    TextCompletionChunk,
    TextCompletion,
)
from portkey_ai.api_resources.types.feedback_type import FeedbackResponse
from portkey_ai.api_resources.types.generation_type import (
    PromptCompletion,
    PromptCompletionChunk,
    PromptRender,
)
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
    LOCAL_BASE_URL,
    MISSING_API_KEY_ERROR_MESSAGE,
    MISSING_BASE_URL,
    MISSING_MODE_MESSAGE,
    PORTKEY_BASE_URL,
    PORTKEY_API_KEY_ENV,
    PORTKEY_HEADER_PREFIX,
    PORTKEY_PROXY_ENV,
)


class MetaEnum(EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        return True


class CacheType(str, Enum, metaclass=MetaEnum):
    SEMANTIC = "semantic"
    SIMPLE = "simple"


CacheLiteral = Literal["semantic", "simple"]


ResponseT = TypeVar(
    "ResponseT",
    bound="Union[ChatCompletionChunk, ChatCompletions, TextCompletion, TextCompletionChunk, GenericResponse, PromptCompletion, PromptCompletionChunk, PromptRender, FeedbackResponse, httpx.Response]",  # noqa: E501
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


class Modes(str, Enum, metaclass=MetaEnum):
    """_summary_

    Args:
        Enum (_type_): _description_
    """

    FALLBACK = "fallback"
    AB_TEST = "ab_test"
    SINGLE = "single"
    PROXY = "proxy"


class ApiType(str, Enum, metaclass=MetaEnum):
    COMPLETIONS = "completions"
    CHAT_COMPLETION = "chat_completions"


ModesLiteral = Literal["fallback", "ab_test", "single", "proxy"]


class PortkeyApiPaths(str, Enum, metaclass=MetaEnum):
    GENERATION = "/prompts/{prompt_id}/generate"
    CHAT_COMPLETE_API = "/chat/completions"
    TEXT_COMPLETE_API = "/completions"
    PROMPT_API = "/prompt/complete"
    FEEDBACK_API = "/feedback"
    EMBEDDING_API = "/embeddings"
    USER_API = "/admin/users"
    INVITE_API = "/admin/users/invites"
    WORKSPACE_API = "/admin/workspaces"
    CONFIG_API = "/configs"
    API_KEYS_API = "/api-keys"
    VIRTUAL_KEYS_API = "/virtual-keys"
    LOGS_EXPORT_API = "/logs/exports"
    LOGS_API = "/logs"
    LABELS_API = "/labels"
    COLLECTIONS_API = "/collections"
    PROMPTS_API = "/prompts"
    PROMPTS_PARTIALS_API = "/prompts/partials"
    INTEGRATIONS_API = "/integrations"
    PROVIDERS_API = "/providers"
    GUARDRAILS_API = "/guardrails"

    def __str__(self):
        return self.value


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
    files: Any = None


class FunctionCall(BaseModel):
    name: str
    arguments: str


class ToolCall(BaseModel):
    id: str
    function: FunctionCall
    type: str


class DeltaToolCallFunction(BaseModel):
    arguments: Optional[str] = None
    name: Optional[str] = None


class DeltaToolCall(BaseModel):
    index: int
    id: Optional[str] = None
    function: Optional[DeltaToolCallFunction] = None
    type: Optional[str] = None


class Message(TypedDict):
    role: str
    content: NotRequired[Union[None, str]]
    tool_calls: NotRequired[Union[None, List[ToolCall]]]


class Function(BaseModel):
    name: str
    description: str
    parameters: Dict[str, object]


class Tool(BaseModel):
    function: Function
    type: str


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
    functions: Optional[List[Function]] = None
    function_call: Optional[Union[None, str, Function]] = None
    logprobs: Optional[bool] = None
    top_logprobs: Optional[int] = None
    echo: Optional[bool] = None
    stop: Optional[Union[str, List[str]]] = None
    presence_penalty: Optional[int] = None
    frequency_penalty: Optional[int] = None
    best_of: Optional[int] = None
    logit_bias: Optional[Dict[str, int]] = None
    user: Optional[str] = None
    organization: Optional[str] = None
    tool_choice: Optional[Union[None, str]] = None
    tools: Optional[List[Tool]] = None


class OverrideParams(ModelParams, ConversationInput):
    ...


def remove_empty_values(
    data: Union[Dict[str, Any], Mapping[str, Any]]
) -> Dict[str, Any]:
    if isinstance(data, dict):
        cleaned_dict = {}
        for key, value in data.items():
            if value is not NOT_GIVEN and value != "":
                cleaned_value = remove_empty_values(value)
                if cleaned_value is not NOT_GIVEN and cleaned_value != "":
                    cleaned_dict[key] = cleaned_value
        return cleaned_dict
    elif isinstance(data, list):
        cleaned_list = []

        for item in data:  # type: ignore
            cleaned_item = remove_empty_values(item)
            if cleaned_item is not NOT_GIVEN and cleaned_item != "":
                cleaned_list.append(cleaned_item)
        return cleaned_list  # type: ignore
    else:
        return cast(dict, data)


class Constructs(BaseModel):
    provider: Union[ProviderTypes, ProviderTypesLiteral, str]
    api_key: Optional[str] = None
    virtual_key: Optional[str] = None
    cache: Optional[bool] = None
    cache_age: Optional[int] = None
    cache_status: Optional[Union[CacheType, CacheLiteral]] = None
    cache_force_refresh: Optional[bool] = None
    trace_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    debug: Optional[bool] = None
    custom_host: Optional[str] = None
    forward_headers: Optional[str] = None
    instrumentation: Optional[bool] = None
    weight: Optional[float] = None
    retry: Optional[RetrySettings] = None
    deployment_id: Optional[str] = None
    resource_name: Optional[str] = None
    api_version: Optional[str] = None
    openai_project: Optional[str] = None
    openai_organization: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_access_key_id: Optional[str] = None
    aws_session_token: Optional[str] = None
    aws_region: Optional[str] = None
    vertex_project_id: Optional[str] = None
    vertex_region: Optional[str] = None
    workers_ai_account_id: Optional[str] = None
    azure_resource_name: Optional[str] = None
    azure_deployment_id: Optional[str] = None
    azure_api_version: Optional[str] = None
    azure_endpoint_name: Optional[str] = None
    huggingface_base_url: Optional[str] = None
    cache_namespace: Optional[str] = None
    request_timeout: Optional[int] = None
    anthropic_beta: Optional[str] = None
    anthropic_version: Optional[str] = None
    mistral_fim_completion: Optional[bool] = None
    vertex_storage_bucket_name: Optional[str] = None
    provider_file_name: Optional[str] = None
    provider_model: Optional[str] = None
    aws_s3_bucket: Optional[str] = None
    aws_s3_object_key: Optional[str] = None
    aws_bedrock_model: Optional[str] = None
    fireworks_account_id: Optional[str] = None


class LLMOptions(Constructs, ConversationInput, ModelParams):
    @classmethod
    def parse_api_key(cls, api_key, values):
        if api_key is None and values.get("virtual_key") is None:
            # You can access other fields' values via the 'values' dictionary
            provider = values.get("provider", "")
            api_key = apikey_from_env(provider)
        return api_key


class ProviderOptions(Constructs):
    override_params: Optional[OverrideParams] = None

    @classmethod
    def parse_cache_age(cls, cache_age):
        if cache_age is not None:
            cache_age = f"max-age={cache_age}"
        return cache_age


class RequestConfig(BaseModel):
    mode: str
    options: List[ProviderOptions]


class Body(LLMOptions):
    ...


class ConfigSlug(BaseModel):
    config: str


class Params(Constructs, ConversationInput, ModelParams, extra="forbid"):
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


class Usage(BaseModel, extra="allow"):
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None

    def __str__(self):
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


class GenericResponse(BaseModel, extra="allow"):
    success: Optional[bool] = None
    data: Optional[Any] = None
    warning: Optional[str] = None
    _headers: Optional[httpx.Headers] = None

    def __str__(self):
        del self._headers
        return json.dumps(self.dict(), indent=4)

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers_generic(self._headers)


def apikey_from_env(provider: Union[ProviderTypes, ProviderTypesLiteral, str]) -> str:
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
    mode: Optional[Union[Modes, ModesLiteral, str]] = None
    llms: Optional[Union[List[LLMOptions], LLMOptions]] = None

    @classmethod
    def check_mode(cls, mode):
        if mode is None:
            # You can access other fields' values via the 'values' dictionary
            mode = retrieve_mode()

        return mode

    @classmethod
    def parse_llms(cls, llms):
        if isinstance(llms, LLMOptions):
            llms = [llms]
        return llms


def default_api_key(base_url, api_key) -> str:
    if api_key:
        return api_key
    env_api_key = os.environ.get(PORTKEY_API_KEY_ENV, "")
    if base_url == PORTKEY_BASE_URL:
        if env_api_key:
            return env_api_key
        raise ValueError(MISSING_API_KEY_ERROR_MESSAGE)
    else:
        return env_api_key


def default_base_url() -> str:
    if portkey_ai.base_url:
        return portkey_ai.base_url

    env_base_url = os.environ.get(PORTKEY_PROXY_ENV, PORTKEY_BASE_URL)
    if env_base_url:
        return env_base_url
    raise ValueError(MISSING_BASE_URL)


def retrieve_config() -> Union[Mapping, str]:
    if portkey_ai.config:
        return portkey_ai.config
    # raise ValueError(MISSING_CONFIG_MESSAGE)
    return {}


def retrieve_mode() -> Union[Modes, ModesLiteral, str]:
    if portkey_ai.mode:
        return portkey_ai.mode
    raise ValueError(MISSING_MODE_MESSAGE)


def get_portkey_header(key: str) -> str:
    return f"{PORTKEY_HEADER_PREFIX}{key}"


def parse_headers_generic(headers: Optional[httpx.Headers]) -> dict:
    if headers is None:
        return {}

    _headers = {}
    for k, v in headers.items():
        if k.startswith(PORTKEY_HEADER_PREFIX):
            k = k.replace(PORTKEY_HEADER_PREFIX, "")
            _headers[k] = v

    return _headers


def set_base_url(base_url, api_key):
    if base_url:
        return base_url

    env_base_url = os.environ.get(PORTKEY_BASE_URL) or os.environ.get(PORTKEY_PROXY_ENV)

    if env_base_url:
        return env_base_url
    api_key = api_key or os.environ.get(PORTKEY_API_KEY_ENV)
    return PORTKEY_BASE_URL if api_key else LOCAL_BASE_URL


def create_model_instance(model_class):
    """
    Create a model instance that's compatible with both Pydantic v1 and v2.

    This function provides backward compatibility for the transition from Pydantic v1
    to Pydantic v2. In Pydantic v1, the method was called `construct()`, while in
    Pydantic v2, it was renamed to `model_construct()`.
    """
    try:
        # Try Pydantic v2 method first
        return model_class.model_construct()
    except AttributeError:
        # Fall back to Pydantic v1 method
        return model_class.construct()


def extract_extra_params(kwargs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract and process extra_body, extra_headers, extra_query, and timeout from kwargs.

    This function properly handles the extra_body parameter to match OpenAI SDK behavior.
    When a user passes extra_body={'a': 'b'}, the contents should be merged at the top
    level of the request body, not nested under an 'extra_body' key.

    Args:
        kwargs: The keyword arguments dict (will be mutated - special params removed)

    Returns:
        A dict with keys: extra_headers, extra_query, extra_body, timeout
        ready to be passed to the OpenAI client methods.
    """
    extra_headers = kwargs.pop("extra_headers", None)
    extra_query = kwargs.pop("extra_query", None)
    timeout = kwargs.pop("timeout", None)
    user_extra_body = kwargs.pop("extra_body", None) or {}

    # Merge user's extra_body with remaining kwargs
    # This ensures extra_body={'a': 'b'} results in 'a' at top level, not 'extra_body': {'a': 'b'}
    merged_extra_body = {**user_extra_body, **kwargs}

    return {
        "extra_headers": extra_headers,
        "extra_query": extra_query,
        "extra_body": merged_extra_body if merged_extra_body else None,
        "timeout": timeout,
    }
