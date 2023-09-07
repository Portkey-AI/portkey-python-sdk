import os
from portkey.api_resources import (
    Portkey,
    LLMBase,
    PortkeyModes,
    PortkeyModesLiteral,
    ProviderTypes,
    ProviderTypesLiteral,
    PortkeyCacheType,
    PortkeyCacheLiteral,
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

__version__ = VERSION
__all__ = [
    "Portkey",
    "LLMBase",
    "PortkeyModes",
    "PortkeyResponse",
    "PortkeyModesLiteral",
    "ProviderTypes",
    "ProviderTypesLiteral",
    "PortkeyCacheType",
    "PortkeyCacheLiteral",
    "Message",
    "ChatCompletions",
    "Completions",
    "Params",
    "Config",
    "api_key",
    "base_url",
]
