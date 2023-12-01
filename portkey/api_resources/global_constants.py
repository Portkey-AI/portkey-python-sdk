MISSING_API_KEY_ERROR_MESSAGE = """No API key found for Portkey.
Please set either the PORTKEY_API_KEY environment variable or \
pass the api_key prior to initialization of Portkey.
API keys can be found or created at Portkey Dashboard \

Here's how you get it:
1. Visit https://app.portkey.ai/
1. Click on your profile icon on the top left
2. From the dropdown menu, click on "Copy API Key"
"""

MISSING_BASE_URL = """No Base url provided. Please provide a valid base url.
For example: https://api.portkey.ai
"""

MISSING_CONFIG_MESSAGE = (
    """The 'config' parameter is not set. Please provide a valid Config object."""
)
MISSING_MODE_MESSAGE = (
    """The 'mode' parameter is not set. Please provide a valid mode literal."""
)

INVALID_PORTKEY_MODE = """
Argument of type '{}' cannot be assigned to parameter "mode" of \
    type "ModesLiteral | Modes | None"
"""

DEFAULT_MAX_RETRIES = 2
VERSION = "0.1.0"
DEFAULT_TIMEOUT = 60
PORTKEY_HEADER_PREFIX = "x-portkey-"
PORTKEY_BASE_URL = "https://api.portkey.ai"
PORTKEY_GATEWAY_URL = f"{PORTKEY_BASE_URL}/v1"
PORTKEY_API_KEY_ENV = "PORTKEY_API_KEY"
PORTKEY_PROXY_ENV = "PORTKEY_PROXY"
