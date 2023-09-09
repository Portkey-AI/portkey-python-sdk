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
)
from portkey.version import VERSION

api_key = os.environ.get("PORTKEY_API_KEY", "")
base_url = os.environ.get("PORTKEY_PROXY", "https://api.portkey.ai")
config: Optional[Config] = None
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
    "Config",
    "api_key",
    "base_url",
]
