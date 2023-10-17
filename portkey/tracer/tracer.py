import importlib
from typing import Optional
from types import ModuleType
from portkey.api_resources.utils import default_api_key, get_proxy_url
import portkey.tracer.handlers as handlers


def import_package(package_name: str, pypi_name: Optional[str] = None) -> ModuleType:
    """
    Dynamically imports a package.

    Args:
        package_name (str): Name of the package to import.

        pypi_name (Optional[str], optional): Name of the package on PyPI, if different
        from the
        package name.

    Returns:
        ModuleType: The imported package.
    """
    try:
        return importlib.import_module(package_name)
    except ImportError:
        raise ImportError(
            f"The {package_name} package is not installed. "
            f"Install with `pip install {pypi_name or package_name}`."
        )


class Connector:
    """
    Conector - A Request Routing Utility

    The Conector module is a powerful utility designed to seamlessly integrate
    with your AI clients, intercept requests, and route them via Portkey - an AI
    gateway. This tool simplifies the process of connecting your AI applications
    to external services or APIs, allowing for enhanced control, security, and
    customization of request handling.

    Usage:
        The Conector module is easy to use and can be integrated into
        your OpenAI projects with minimal effort. Here's how it works:

        1. Initialization:
        To get started, create an instance of Conector, specifying the
        necessary configuration options. This typically includes the Portkey
        URL, API keys, and any additional settings.

        2. Request Interception:
        Conector is equipped to automatically intercept requests made
        through your AI client. It acts as a middleware, capturing requests
        before they are sent to the AI API.

        3. Routing via Portkey:
        Once a request is intercepted, the Conector will route it through the
        specified Portkey gateway. This is especially useful when you need to apply
        transformations, authentication, or any custom logic to the request before it
        reaches the AI service.

        4. Seamless Integration:
        Conector seamlessly integrates with your existing AI client, making
        it a transparent and non-intrusive addition to your workflow. It ensures a
        smooth and reliable connection between your application and Portkey.

        5. Customization:
        Conector offers various customization options. You can define specific
        rules and transformations to apply to requests, enabling you to adapt the
        behavior according to your needs.

        6. Benefits:
        - Enhanced Security: Securely route requests through Portkey, protecting
        sensitive data and authentication details.
        - Logging and Analytics: Easily log and analyze requests for debugging and
        performance monitoring.

    Example:

        ```python
        # Import the Conector module
        import portkey

        # Use the connector to make requests through Portkey
        response = openai.Completion.create(
            prompt="Translate this English text to French: 'Hello World'",
            model="gpt-3.5-turbo"
        )
        print(response)
        ```
    """

    def __init__(self, api_key=None, base_url=None) -> None:
        self.api_key = api_key or default_api_key()
        self.proxy_url = get_proxy_url(base_url)
        pass

    def initialize(self):
        requests = import_package("requests")
        httpx = import_package("httpx")
        setattr(requests, "Session", handlers.SessionHandler)
        setattr(httpx, "Client", handlers.ClientHandler)
