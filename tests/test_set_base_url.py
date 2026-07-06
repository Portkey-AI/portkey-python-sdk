import pytest

from portkey_ai.api_resources.global_constants import (
    LOCAL_BASE_URL,
    PORTKEY_BASE_URL,
)
from portkey_ai.api_resources.utils import set_base_url


@pytest.fixture(autouse=True)
def clear_base_url_env(monkeypatch):
    # set_base_url reads process env vars; isolate the test from the ambient
    # environment so PORTKEY_BASE_URL / PORTKEY_PROXY / PORTKEY_API_KEY do not leak in.
    monkeypatch.delenv("PORTKEY_BASE_URL", raising=False)
    monkeypatch.delenv("PORTKEY_PROXY", raising=False)
    monkeypatch.delenv("PORTKEY_API_KEY", raising=False)


class TestSetBaseUrl:
    def test_explicit_base_url_takes_precedence(self, monkeypatch):
        monkeypatch.setenv("PORTKEY_BASE_URL", "https://env-gateway.example/v1")
        assert (
            set_base_url("https://explicit.example/v1", None)
            == "https://explicit.example/v1"
        )

    def test_portkey_base_url_env_is_honored_without_api_key(self, monkeypatch):
        monkeypatch.setenv("PORTKEY_BASE_URL", "https://env-gateway.example/v1")
        assert set_base_url(None, None) == "https://env-gateway.example/v1"

    def test_portkey_base_url_env_is_honored_with_api_key(self, monkeypatch):
        monkeypatch.setenv("PORTKEY_BASE_URL", "https://env-gateway.example/v1")
        assert set_base_url(None, "pk-fakekey") == "https://env-gateway.example/v1"

    def test_portkey_base_url_env_wins_over_portkey_proxy_env(self, monkeypatch):
        monkeypatch.setenv("PORTKEY_BASE_URL", "https://env-gateway.example/v1")
        monkeypatch.setenv("PORTKEY_PROXY", "https://proxy.example/v1")
        assert set_base_url(None, None) == "https://env-gateway.example/v1"

    def test_portkey_proxy_env_used_when_base_url_env_absent(self, monkeypatch):
        monkeypatch.setenv("PORTKEY_PROXY", "https://proxy.example/v1")
        assert set_base_url(None, None) == "https://proxy.example/v1"

    def test_defaults_to_localhost_without_api_key(self):
        assert set_base_url(None, None) == LOCAL_BASE_URL

    def test_defaults_to_portkey_base_url_with_api_key(self):
        assert set_base_url(None, "pk-fakekey") == PORTKEY_BASE_URL
