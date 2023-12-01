import os
from typing import Mapping, Optional, Union
from portkey_ai.api_resources import (
    LLMOptions,
    Modes,
    ModesLiteral,
    ProviderTypes,
    ProviderTypesLiteral,
    CacheType,
    CacheLiteral,
    Message,
    PortkeyResponse,
    ChatCompletions,
    Completion,
    Params,
    Config,
    RetrySettings,
    ChatCompletion,
    ChatCompletionChunk,
    TextCompletion,
    TextCompletionChunk,
    createHeaders,
    Prompt,
    Portkey,
)
from portkey_ai.version import VERSION
from portkey_ai.api_resources.global_constants import (
    PORTKEY_BASE_URL,
    PORTKEY_API_KEY_ENV,
    PORTKEY_PROXY_ENV,
    PORTKEY_GATEWAY_URL,
)

api_key = os.environ.get(PORTKEY_API_KEY_ENV)
base_url = os.environ.get(PORTKEY_PROXY_ENV, PORTKEY_BASE_URL)
config: Optional[Union[Mapping, str]] = None
mode: Optional[Union[Modes, ModesLiteral]] = None

__version__ = VERSION
__all__ = [
    "LLMOptions",
    "Modes",
    "PortkeyResponse",
    "ModesLiteral",
    "ProviderTypes",
    "ProviderTypesLiteral",
    "CacheType",
    "CacheLiteral",
    "Message",
    "ChatCompletions",
    "Completion",
    "Params",
    "RetrySettings",
    "ChatCompletion",
    "ChatCompletionChunk",
    "TextCompletion",
    "TextCompletionChunk",
    "Config",
    "api_key",
    "base_url",
    "PORTKEY_GATEWAY_URL",
    "createHeaders",
    "Prompt",
    "Portkey",
]
