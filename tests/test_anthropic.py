from __future__ import annotations

import os
from typing import Any
import pytest
import portkey
from portkey import TextCompletion, TextCompletionChunk, Config, LLMOptions
from dotenv import load_dotenv

# from tests.utils import assert_matches_type
load_dotenv()
base_url = os.environ.get("PORTKEY_BASE_URL")
api_key = os.environ.get("PORTKEY_API_KEY")
virtual_api_key = os.environ.get("ANTHROPIC_VIRTUAL_KEY")


class TestAnthropicCompletions:
    client = portkey
    client.api_key = api_key
    parametrize = pytest.mark.parametrize("client", [client], ids=["strict"])

    @parametrize
    def test_method_create_non_stream(self, client: Any) -> None:
        config = Config(
            mode="single",
            llms=LLMOptions(
                virtual_key=virtual_api_key,
                provider="anthropic",
                metadata={"_user": "portkey-python-sdk"},
                model="claude-2",
            ),
        )
        client.config = config
        completion = client.Completions.create(
            max_tokens=256,
            prompt="why is the sky blue ?",
        )
        # assert("True", "True")

        # assert_matches_type(TextCompletion, completion, path=["response"])

    @parametrize
    def test_method_create_with_all_params_non_stream(self, client: Any) -> None:
        config = Config(
            mode="single",
            llms=LLMOptions(
                virtual_key=virtual_api_key,
                provider="anthropic",
                metadata={"_user": "portkey-python-sdk"},
                model="claude-2",
            ),
        )
        client.config = config
        completion = client.Completions.create(
            max_tokens=256,
            prompt="why is the sky blue ?",
            stop_sequences=["string", "string", "string"],
            stream=False,
            temperature=1,
            top_k=5,
            top_p=0.7,
        )
        # assert("True", "True")
        # assert_matches_type(TextCompletion, completion, path=["response"])

    @parametrize
    def test_method_create_streaming(self, client: Any) -> None:
        config = Config(
            mode="single",
            llms=LLMOptions(
                virtual_key=virtual_api_key,
                provider="anthropic",
                metadata={"_user": "portkey-python-sdk"},
                model="claude-2",
            ),
        )
        client.config = config
        completion_streaming = client.Completions.create(
            max_tokens=256,
            prompt="why is the sky blue ?",
            stream=True,
        )
        # assert("True", "True")

        # for chunk in completion_streaming:
        #     assert_matches_type(TextCompletionChunk, chunk, path=["response"])

    @parametrize
    def test_method_create_with_all_params_streaming(self, client: Any) -> None:
        config = Config(
            mode="single",
            llms=LLMOptions(
                virtual_key=virtual_api_key,
                provider="anthropic",
                metadata={"_user": "portkey-python-sdk"},
                model="claude-2",
            ),
        )
        client.config = config
        completion_streaming = client.Completions.create(
            max_tokens=256,
            prompt="why is the sky blue ?",
            stream=True,
            stop_sequences=["string", "string", "string"],
            temperature=1,
            top_k=5,
            top_p=0.7,
        )
        # assert("True", "True")


class TestAnthropicChatCompletions:
    client = portkey
    client.api_key = api_key
    parametrize = pytest.mark.parametrize("client", [client], ids=["strict"])

    @parametrize
    def test_method_create_non_stream(self, client: Any) -> None:
        config = Config(
            mode="single",
            llms=LLMOptions(
                virtual_key=virtual_api_key,
                provider="anthropic",
                metadata={"_user": "portkey-python-sdk"},
                model="claude-2",
            ),
        )
        client.config = config
        completion = client.ChatCompletions.create(
            max_tokens=256,
            messages=[{"role": "user", "content": "why is the sky blue ?"}],
        )
        # assert("True", "True")

        # assert_matches_type(TextCompletion, completion, path=["response"])

    @parametrize
    def test_method_create_with_all_params_non_stream(self, client: Any) -> None:
        config = Config(
            mode="single",
            llms=LLMOptions(
                virtual_key=virtual_api_key,
                provider="anthropic",
                metadata={"_user": "portkey-python-sdk"},
                model="claude-2",
            ),
        )
        client.config = config
        completion = client.ChatCompletions.create(
            max_tokens=256,
            messages=[{"role": "user", "content": "why is the sky blue ?"}],
            stop_sequences=["string", "string", "string"],
            stream=False,
            temperature=1,
            top_k=5,
            top_p=0.7,
        )
        # assert("True", "True")
        # assert_matches_type(TextCompletion, completion, path=["response"])

    @parametrize
    def test_method_create_streaming(self, client: Any) -> None:
        config = Config(
            mode="single",
            llms=LLMOptions(
                virtual_key=virtual_api_key,
                provider="anthropic",
                metadata={"_user": "portkey-python-sdk"},
                model="claude-2",
            ),
        )
        client.config = config
        completion_streaming = client.ChatCompletions.create(
            max_tokens=256,
            messages=[{"role": "user", "content": "why is the sky blue ?"}],
            stream=True,
        )
        # assert("True", "True")

        # for chunk in completion_streaming:
        #     assert_matches_type(TextCompletionChunk, chunk, path=["response"])

    @parametrize
    def test_method_create_with_all_params_streaming(self, client: Any) -> None:
        config = Config(
            mode="single",
            llms=LLMOptions(
                virtual_key=virtual_api_key,
                provider="anthropic",
                metadata={"_user": "portkey-python-sdk"},
                model="claude-2",
            ),
        )
        client.config = config
        completion_streaming = client.ChatCompletions.create(
            max_tokens=256,
            messages=[{"role": "user", "content": "why is the sky blue ?"}],
            stream=True,
            stop_sequences=["string", "string", "string"],
            temperature=1,
            top_k=5,
            top_p=0.7,
        )
        # assert("True", "True")


class TestOpenaiGenerations:
    client = portkey
    client.api_key = api_key
    parametrize = pytest.mark.parametrize("client", [client], ids=["strict"])

    @parametrize
    def test_method_create_stream(self, client: Any) -> None:
        config = Config()
        client.config = config
        completion = client.Generations.create(
            prompt_id="",
        )