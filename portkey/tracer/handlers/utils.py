import yaml
from typing import Any, Tuple, Mapping, Dict, Optional
from portkey.api_resources.utils import get_proxy_url, default_api_key


def merge_headers(
    obj1: Mapping[str, Any],
    obj2: Mapping[str, Any],
) -> Dict[str, Any]:
    """Merge two headers of the given type
    In cases with duplicate keys the second mapping takes precedence.
    """
    return {**obj1, **obj2}


def check_api_signature(
    method: str | bytes, url: str | bytes
) -> Tuple[bool, dict[str, Any]]:
    config = read_signature_configs()
    if config:
        for item in config:
            if item["url"] == url and item["method"] == method:
                return True, item
    return False, {}


def update_url(url: str | bytes, config: Dict[str, Any]) -> str | bytes:
    base_url = config["base_url"]
    url = url.decode("utf-8") if isinstance(url, bytes) else str(url)
    proxy_url = get_proxy_url()
    new_url = url.replace(base_url, proxy_url)
    return new_url


def update_headers(
    headers: Optional[Mapping[str, str]], config: Dict[str, Any]
) -> Mapping[str, str]:
    api_key = default_api_key()
    mode = config["mode"]
    if not headers:
        headers = {}
    headers = {
        **headers,
        "x-portkey-api-key": api_key,
        "x-portkey-mode": f"proxy {mode}",
    }
    return headers


def intitiate_tracing(
    method: str | bytes, url: str | bytes, headers: Optional[Mapping[str, str]] = None
) -> Tuple[str | bytes, Optional[Dict[str, str] | Mapping[str, str]]]:
    is_signature_match, config = check_api_signature(method, url)
    if is_signature_match:
        new_url = update_url(url, config)
        new_headers = update_headers(headers, config)
        return new_url, new_headers
    return url, headers


def read_signature_configs():
    config = []
    # TODO: Get the config files from users to customise this signature validation on portkey.
    with open("portkey/tracer/config.yaml", "r") as config_file:
        configs_file = yaml.safe_load(config_file)
        for i in configs_file["routes"]:
            paths = i["paths"]
            base_url = i["base_url"]
            mode = i["mode"]
            _configs = [
                {
                    "base_url": base_url,
                    "url": f"{base_url}{k['path']}",
                    "mode": mode,
                    "method": k["method"],
                }
                for k in paths
            ]
            config.extend(_configs)
    return config
