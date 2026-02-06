from typing import Any, AsyncIterator, Optional

import pytest

# Skip these tests unless google-adk is installed
pytest.importorskip("google.adk", reason="google-adk extra not installed")

from google.adk.models.llm_request import LlmRequest  # type: ignore
from google.genai import types as genai_types  # type: ignore

from portkey_ai.integrations.adk import (
    PortkeyAdk,
    _get_anthropic_content_blocks,
    _iter_anthropic_content_blocks,
    _get_gemini_thought_signature,
    _get_thinking_config,
)


class _FakeDelta:
    def __init__(
        self,
        content: Optional[str] = None,
        reasoning_content: Optional[str] = None,
        content_blocks: Optional[list[dict[str, Any]]] = None,
    ):
        self.content = content
        self.reasoning_content = reasoning_content
        if content_blocks is not None:
            self.content_blocks = content_blocks


class _FakeMessage:
    def __init__(
        self,
        content: Optional[str] = None,
        reasoning_content: Optional[str] = None,
        content_blocks: Optional[list[dict[str, Any]]] = None,
    ):
        self.content = content
        self.reasoning_content = reasoning_content
        if content_blocks is not None:
            self.content_blocks = content_blocks
        self.tool_calls = None


class _FakeChoice:
    def __init__(
        self,
        delta: Optional[_FakeDelta] = None,
        message: Optional[_FakeMessage] = None,
        finish_reason: Optional[str] = None,
    ):
        self.delta = delta
        self.message = message
        self.finish_reason = finish_reason


class _FakeResponse:
    def __init__(
        self,
        message_text: str,
        reasoning_content: Optional[str] = None,
        content_blocks: Optional[list[dict[str, Any]]] = None,
    ):
        self.choices = [
            _FakeChoice(
                message=_FakeMessage(
                    message_text,
                    reasoning_content=reasoning_content,
                    content_blocks=content_blocks,
                ),
                finish_reason="stop",
            )
        ]
        self.usage = type(
            "Usage", (), {"prompt_tokens": 1, "completion_tokens": 2, "total_tokens": 3}
        )()


def _build_request(model: str, text: str = "Hello") -> LlmRequest:
    return LlmRequest(
        model=model,
        contents=[
            genai_types.Content(
                role="user",
                parts=[genai_types.Part.from_text(text=text)],
            )
        ],
    )


@pytest.mark.asyncio
async def test_non_streaming_simple(monkeypatch: pytest.MonkeyPatch) -> None:
    llm = PortkeyAdk(model="@openai/gpt-4o-mini", api_key="test")

    async def fake_create(**kwargs: Any) -> _FakeResponse:
        assert not kwargs.get("stream"), "Non-streaming path should not request stream"
        return _FakeResponse(message_text="Hello world!")

    # Patch the underlying client create method
    monkeypatch.setattr(llm._client.chat.completions, "create", fake_create)  # type: ignore[attr-defined]

    req = _build_request(model="@openai/gpt-4o-mini", text="test")
    outputs: list[str] = []
    async for resp in llm.generate_content_async(req, stream=False):
        assert not getattr(resp, "partial", False)
        assert resp.content and resp.content.parts
        for p in resp.content.parts:
            text = getattr(p, "text", None)
            if text:
                outputs.append(text)
    assert "".join(outputs).strip() == "Hello world!"


@pytest.mark.asyncio
async def test_streaming_accumulates_and_final(monkeypatch: pytest.MonkeyPatch) -> None:
    llm = PortkeyAdk(model="@openai/gpt-4o-mini", api_key="test")

    part1 = type("Chunk", (), {"choices": [_FakeChoice(delta=_FakeDelta("Hello "))]})()
    part2 = type("Chunk", (), {"choices": [_FakeChoice(delta=_FakeDelta("world!"))]})()
    part3 = type(
        "Chunk",
        (),
        {"choices": [_FakeChoice(message=_FakeMessage(None), finish_reason="stop")]},
    )()

    async def fake_stream_gen() -> AsyncIterator[Any]:
        yield part1
        yield part2
        yield part3

    async def fake_create(**kwargs: Any) -> AsyncIterator[Any] | _FakeResponse:
        if kwargs.get("stream"):
            return fake_stream_gen()
        return _FakeResponse(message_text="unused")

    monkeypatch.setattr(llm._client.chat.completions, "create", fake_create)  # type: ignore[attr-defined]

    req = _build_request(model="@openai/gpt-4o-mini", text="test")
    partial_text = []
    final_text = []

    async for resp in llm.generate_content_async(req, stream=True):
        assert resp.content and resp.content.parts
        text_parts = [
            p.text for p in resp.content.parts if getattr(p, "text", None) is not None
        ]
        if getattr(resp, "partial", False):
            partial_text.extend([t for t in text_parts if t])
        else:
            final_text.extend([t for t in text_parts if t])

    assert "".join(partial_text) == "Hello world!"
    assert "".join(final_text) == "Hello world!"


@pytest.mark.asyncio
async def test_non_streaming_with_reasoning_content(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    llm = PortkeyAdk(model="@openai/gpt-4o-mini", api_key="test")

    async def fake_create(**kwargs: Any) -> _FakeResponse:
        return _FakeResponse(
            message_text="The answer is 42.",
            reasoning_content="Let me think about this step by step...",
        )

    monkeypatch.setattr(llm._client.chat.completions, "create", fake_create)  # type: ignore[attr-defined]

    req = _build_request(model="@openai/gpt-4o-mini", text="test")
    thought_parts: list[str] = []
    text_parts: list[str] = []

    async for resp in llm.generate_content_async(req, stream=False):
        assert resp.content and resp.content.parts
        for p in resp.content.parts:
            text = getattr(p, "text", None)
            if getattr(p, "thought", False) and text:
                thought_parts.append(text)
            elif text:
                text_parts.append(text)

    assert "".join(thought_parts) == "Let me think about this step by step..."
    assert "".join(text_parts) == "The answer is 42."


@pytest.mark.asyncio
async def test_streaming_with_reasoning_content(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    llm = PortkeyAdk(model="@openai/gpt-4o-mini", api_key="test")

    part1 = type(
        "Chunk",
        (),
        {"choices": [_FakeChoice(delta=_FakeDelta(reasoning_content="Thinking..."))]},
    )()
    part2 = type(
        "Chunk", (), {"choices": [_FakeChoice(delta=_FakeDelta(content="Answer: 42"))]}
    )()
    part3 = type(
        "Chunk",
        (),
        {"choices": [_FakeChoice(message=_FakeMessage(None), finish_reason="stop")]},
    )()

    async def fake_stream_gen() -> AsyncIterator[Any]:
        yield part1
        yield part2
        yield part3

    async def fake_create(**kwargs: Any) -> AsyncIterator[Any] | _FakeResponse:
        if kwargs.get("stream"):
            return fake_stream_gen()
        return _FakeResponse(message_text="unused")

    monkeypatch.setattr(llm._client.chat.completions, "create", fake_create)  # type: ignore[attr-defined]

    req = _build_request(model="@openai/gpt-4o-mini", text="test")
    partial_thoughts: list[str] = []
    partial_text: list[str] = []
    final_thoughts: list[str] = []
    final_text: list[str] = []

    async for resp in llm.generate_content_async(req, stream=True):
        assert resp.content and resp.content.parts
        for p in resp.content.parts:
            text = getattr(p, "text", None)
            if getattr(p, "thought", False) and text:
                if getattr(resp, "partial", False):
                    partial_thoughts.append(text)
                else:
                    final_thoughts.append(text)
            elif text:
                if getattr(resp, "partial", False):
                    partial_text.append(text)
                else:
                    final_text.append(text)

    assert "".join(partial_thoughts) == "Thinking..."
    assert "".join(partial_text) == "Answer: 42"
    assert "".join(final_thoughts) == "Thinking..."
    assert "".join(final_text) == "Answer: 42"


@pytest.mark.asyncio
async def test_non_streaming_without_reasoning_content(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    llm = PortkeyAdk(model="@openai/gpt-4o-mini", api_key="test")

    async def fake_create(**kwargs: Any) -> _FakeResponse:
        return _FakeResponse(message_text="Simple response")

    monkeypatch.setattr(llm._client.chat.completions, "create", fake_create)  # type: ignore[attr-defined]

    req = _build_request(model="@openai/gpt-4o-mini", text="test")
    thought_parts: list[str] = []
    text_parts: list[str] = []

    async for resp in llm.generate_content_async(req, stream=False):
        assert resp.content and resp.content.parts
        for p in resp.content.parts:
            text = getattr(p, "text", None)
            if getattr(p, "thought", False) and text:
                thought_parts.append(text)
            elif text:
                text_parts.append(text)

    assert thought_parts == []
    assert "".join(text_parts) == "Simple response"


@pytest.mark.asyncio
async def test_non_streaming_with_content_blocks(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    llm = PortkeyAdk(model="gemini-2.5-pro", api_key="test")

    content_blocks = [
        {"type": "thinking", "thinking": "Let me analyze this problem..."},
        {"type": "text", "text": "The answer is 4."},
    ]

    async def fake_create(**kwargs: Any) -> _FakeResponse:
        return _FakeResponse(
            message_text="The answer is 4.",
            content_blocks=content_blocks,
        )

    monkeypatch.setattr(llm._client.chat.completions, "create", fake_create)  # type: ignore[attr-defined]

    req = _build_request(model="gemini-2.5-pro", text="What is 2+2?")
    thought_parts: list[str] = []
    text_parts: list[str] = []

    async for resp in llm.generate_content_async(req, stream=False):
        assert resp.content and resp.content.parts
        for p in resp.content.parts:
            text = getattr(p, "text", None)
            if getattr(p, "thought", False) and text:
                thought_parts.append(text)
            elif text:
                text_parts.append(text)

    assert "".join(thought_parts) == "Let me analyze this problem..."
    assert "".join(text_parts) == "The answer is 4."


@pytest.mark.asyncio
async def test_streaming_with_content_blocks_delta_format(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    llm = PortkeyAdk(model="gemini-2.5-pro", api_key="test")

    part1 = type(
        "Chunk",
        (),
        {
            "choices": [
                _FakeChoice(
                    delta=_FakeDelta(
                        content_blocks=[
                            {"index": 0, "delta": {"thinking": "Thinking part 1..."}}
                        ]
                    )
                )
            ]
        },
    )()
    part2 = type(
        "Chunk",
        (),
        {
            "choices": [
                _FakeChoice(
                    delta=_FakeDelta(
                        content_blocks=[
                            {"index": 0, "delta": {"thinking": "Thinking part 2..."}}
                        ]
                    )
                )
            ]
        },
    )()
    part3 = type(
        "Chunk",
        (),
        {
            "choices": [
                _FakeChoice(
                    delta=_FakeDelta(
                        content_blocks=[{"index": 1, "delta": {"text": "Answer: 42"}}]
                    )
                )
            ]
        },
    )()
    part4 = type(
        "Chunk",
        (),
        {"choices": [_FakeChoice(message=_FakeMessage(None), finish_reason="stop")]},
    )()

    async def fake_stream_gen() -> AsyncIterator[Any]:
        yield part1
        yield part2
        yield part3
        yield part4

    async def fake_create(**kwargs: Any) -> AsyncIterator[Any] | _FakeResponse:
        if kwargs.get("stream"):
            return fake_stream_gen()
        return _FakeResponse(message_text="unused")

    monkeypatch.setattr(llm._client.chat.completions, "create", fake_create)  # type: ignore[attr-defined]

    req = _build_request(model="gemini-2.5-pro", text="test")
    partial_thoughts: list[str] = []
    partial_text: list[str] = []
    final_thoughts: list[str] = []
    final_text: list[str] = []

    async for resp in llm.generate_content_async(req, stream=True):
        assert resp.content and resp.content.parts
        for p in resp.content.parts:
            text = getattr(p, "text", None)
            if getattr(p, "thought", False) and text:
                if getattr(resp, "partial", False):
                    partial_thoughts.append(text)
                else:
                    final_thoughts.append(text)
            elif text:
                if getattr(resp, "partial", False):
                    partial_text.append(text)
                else:
                    final_text.append(text)

    assert "".join(partial_thoughts) == "Thinking part 1...Thinking part 2..."
    assert "".join(partial_text) == "Answer: 42"


@pytest.mark.asyncio
async def test_non_streaming_with_thought_signature(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    llm = PortkeyAdk(model="gemini-2.5-pro", api_key="test")

    content_blocks = [
        {
            "type": "thinking",
            "thinking": "Deep thinking...",
            "thought_signature": "sig123abc",
        },
        {"type": "text", "text": "Final answer."},
    ]

    async def fake_create(**kwargs: Any) -> _FakeResponse:
        return _FakeResponse(
            message_text="Final answer.",
            content_blocks=content_blocks,
        )

    monkeypatch.setattr(llm._client.chat.completions, "create", fake_create)  # type: ignore[attr-defined]

    req = _build_request(model="gemini-2.5-pro", text="test")
    thought_signatures: list[str] = []

    async for resp in llm.generate_content_async(req, stream=False):
        assert resp.content and resp.content.parts
        for p in resp.content.parts:
            sig = getattr(p, "thought_signature", None)
            if sig:
                thought_signatures.append(sig)

    assert "sig123abc" in thought_signatures


@pytest.mark.asyncio
async def test_thinking_config_passed_to_request(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    llm = PortkeyAdk(model="gemini-2.5-pro", api_key="test")
    captured_kwargs: dict[str, Any] = {}

    async def fake_create(**kwargs: Any) -> _FakeResponse:
        captured_kwargs.update(kwargs)
        return _FakeResponse(message_text="response")

    monkeypatch.setattr(llm._client.chat.completions, "create", fake_create)  # type: ignore[attr-defined]

    req = LlmRequest(
        model="gemini-2.5-pro",
        contents=[
            genai_types.Content(
                role="user",
                parts=[genai_types.Part.from_text(text="test")],
            )
        ],
        config=genai_types.GenerateContentConfig(
            thinking_config=genai_types.ThinkingConfig(
                include_thoughts=True,
                thinking_budget=1024,
            ),
        ),
    )

    async for _ in llm.generate_content_async(req, stream=False):
        pass

    assert "thinking" in captured_kwargs
    assert captured_kwargs["thinking"]["type"] == "enabled"
    assert captured_kwargs["thinking"]["budget_tokens"] == 1024


def test_get_anthropic_content_blocks_from_attribute() -> None:
    msg = _FakeMessage(
        content="text",
        content_blocks=[{"type": "text", "text": "hello"}],
    )
    blocks = _get_anthropic_content_blocks(msg)
    assert blocks is not None
    assert len(blocks) == 1
    assert blocks[0]["type"] == "text"


def test_get_anthropic_content_blocks_from_list_content() -> None:
    msg = type(
        "Msg",
        (),
        {
            "content": [{"type": "thinking", "thinking": "thought"}],
            "content_blocks": None,
        },
    )()
    blocks = _get_anthropic_content_blocks(msg)
    assert blocks is not None
    assert len(blocks) == 1
    assert blocks[0]["type"] == "thinking"


def test_get_anthropic_content_blocks_returns_none_for_string() -> None:
    msg = type("Msg", (), {"content": "plain string", "content_blocks": None})()
    blocks = _get_anthropic_content_blocks(msg)
    assert blocks is None


def test_iter_anthropic_content_blocks_non_streaming_format() -> None:
    blocks = [
        {"type": "thinking", "thinking": "thought text", "thought_signature": "sig1"},
        {"type": "text", "text": "response text"},
    ]
    result = list(_iter_anthropic_content_blocks(blocks))
    assert len(result) == 2
    assert result[0] == ("thinking", "thought text", "sig1")
    assert result[1] == ("text", "response text", None)


def test_iter_anthropic_content_blocks_streaming_delta_format() -> None:
    blocks = [
        {"index": 0, "delta": {"thinking": "streaming thought"}},
        {"index": 1, "delta": {"text": "streaming text"}},
    ]
    result = list(_iter_anthropic_content_blocks(blocks))
    assert len(result) == 2
    assert result[0] == ("thinking", "streaming thought", None)
    assert result[1] == ("text", "streaming text", None)


def test_iter_anthropic_content_blocks_empty_delta() -> None:
    blocks = [{"index": 0, "delta": {}}]
    result = list(_iter_anthropic_content_blocks(blocks))
    assert len(result) == 0


def test_iter_anthropic_content_blocks_none_input() -> None:
    result = list(_iter_anthropic_content_blocks(None))
    assert result == []


def test_get_gemini_thought_signature_string() -> None:
    result = _get_gemini_thought_signature("signature_string")
    assert result == "signature_string"


def test_get_gemini_thought_signature_bytes() -> None:
    result = _get_gemini_thought_signature(b"binary_sig")
    assert result == "YmluYXJ5X3NpZw=="


def test_get_gemini_thought_signature_none() -> None:
    result = _get_gemini_thought_signature(None)
    assert result is None


def test_get_thinking_config_with_budget() -> None:
    req = LlmRequest(
        model="test",
        contents=[],
        config=genai_types.GenerateContentConfig(
            thinking_config=genai_types.ThinkingConfig(
                include_thoughts=True,
                thinking_budget=2048,
            ),
        ),
    )
    result = _get_thinking_config(req)
    assert result is not None
    assert result["type"] == "enabled"
    assert result["budget_tokens"] == 2048


def test_get_thinking_config_without_budget() -> None:
    req = LlmRequest(
        model="test",
        contents=[],
        config=genai_types.GenerateContentConfig(
            thinking_config=genai_types.ThinkingConfig(
                include_thoughts=True,
            ),
        ),
    )
    result = _get_thinking_config(req)
    assert result is not None
    assert result["type"] == "enabled"
    assert "budget_tokens" not in result


def test_get_thinking_config_none_when_not_configured() -> None:
    req = LlmRequest(model="test", contents=[])
    result = _get_thinking_config(req)
    assert result is None


def test_get_thinking_config_none_when_empty() -> None:
    req = LlmRequest(
        model="test",
        contents=[],
        config=genai_types.GenerateContentConfig(
            thinking_config=genai_types.ThinkingConfig(),
        ),
    )
    result = _get_thinking_config(req)
    assert result is None
