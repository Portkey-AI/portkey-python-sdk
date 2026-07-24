from portkey_ai.api_resources.utils import apikey_from_env


def test_apikey_from_env_none_returns_empty():
    # A None provider must return "" (the guard used to sit after
    # provider.upper(), so this raised AttributeError instead).
    assert apikey_from_env(None) == ""


def test_apikey_from_env_reads_environment(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-123")
    assert apikey_from_env("openai") == "sk-test-123"


def test_apikey_from_env_normalizes_dashes(monkeypatch):
    monkeypatch.setenv("AZURE_OPENAI_API_KEY", "sk-azure")
    assert apikey_from_env("azure-openai") == "sk-azure"
