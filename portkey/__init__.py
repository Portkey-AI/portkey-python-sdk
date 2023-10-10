import os
from typing import Optional, Union
from portkey.api_resources import (
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
    Completions,
    Params,
    Config,
    RetrySettings,
    ChatCompletion,
    ChatCompletionChunk,
    TextCompletion,
    TextCompletionChunk,
    Generations,
)
from portkey.version import VERSION
from portkey.api_resources.global_constants import (
    PORTKEY_BASE_URL,
    PORTKEY_API_KEY_ENV,
    PORTKEY_PROXY_ENV,
)

api_key = os.environ.get(PORTKEY_API_KEY_ENV)
base_url = os.environ.get(PORTKEY_PROXY_ENV, PORTKEY_BASE_URL)
config: Optional[Union[Config, str]] = None
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
    "Completions",
    "Params",
    "RetrySettings",
    "ChatCompletion",
    "ChatCompletionChunk",
    "TextCompletion",
    "TextCompletionChunk",
    "Generations",
    "Config",
    "api_key",
    "base_url",
]
