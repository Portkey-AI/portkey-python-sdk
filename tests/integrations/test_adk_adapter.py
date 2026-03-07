from typing import Any, AsyncIterator, Optional

import pytest

pytest.importorskip("google.adk", reason="google-adk extra not installed")

from google.adk.models.llm_request import LlmRequest  # type: ignore
from google.genai import types as genai_types  # type: ignore

from portkey_ai.integrations.adk import (
    PortkeyAdk,
    _normalize_thought_signature,
    _get_reasoning_config,
)


class _FakeReasoningContent:
    def __init__(self, text: str):
        self.type = "reasoning_text"
        self.text = text


class _FakeReasoningSummary:
    def __init__(self, text: str):
        self.type = "summary_text"
        self.text = text


class _FakeReasoningItem:
    def __init__(
        self,
        text: Optional[str] = None,
        encrypted_content: Optional[str] = None,
        summary_text: Optional[str] = None,
        item_id: str = "rs_1",
    ):
        self.type = "reasoning"
        self.id = item_id
        self.encrypted_content = encrypted_content
        self.content = [_FakeReasoningContent(text)] if text is not None else None
        self.summary = [_FakeReasoningSummary(summary_text)] if summary_text else []


class _FakeOutputText:
    def __init__(self, text: str):
        self.type = "output_text"
        self.text = text


class _FakeRefusal:
    def __init__(self, refusal: str):
        self.type = "refusal"
        self.refusal = refusal


class _FakeMessage:
    def __init__(self, text: Optional[str] = None, refusal: Optional[str] = None):
        self.type = "message"
        self.id = "msg_1"
        self.role = "assistant"
        self.status = "completed"
        self.content = []
        if text is not None:
            self.content.append(_FakeOutputText(text))
        if refusal is not None:
            self.content.append(_FakeRefusal(refusal))


class _FakeFunctionCall:
    def __init__(self, name: str, arguments: str, call_id: str = "call_1"):
        self.type = "function_call"
        self.id = call_id
        self.call_id = call_id
        self.name = name
        self.arguments = arguments
        self.status = "completed"


class _FakeUsage:
    def __init__(
        self, input_tokens: int = 1, output_tokens: int = 2, total_tokens: int = 3
    ):
        self.input_tokens = input_tokens
        self.output_tokens = output_tokens
        self.total_tokens = total_tokens


class _FakeResponse:
    def __init__(self, output: list[Any], usage: Optional[_FakeUsage] = None):
        self.output = output
        self.usage = usage or _FakeUsage()


class _FakeReasoningDeltaEvent:
    def __init__(self, delta: str, item_id: str = "rs_1"):
        self.type = "response.reasoning_text.delta"
        self.delta = delta
        self.item_id = item_id


class _FakeTextDeltaEvent:
    def __init__(self, delta: str, item_id: str = "msg_1", content_index: int = 0):
        self.type = "response.output_text.delta"
        self.delta = delta
        self.item_id = item_id
        self.content_index = content_index


class _FakeFunctionArgsDeltaEvent:
    def __init__(self, delta: str, item_id: str = "call_1"):
        self.type = "response.function_call_arguments.delta"
        self.delta = delta
        self.item_id = item_id


class _FakeFunctionArgsDoneEvent:
    def __init__(self, arguments: str, name: str, item_id: str = "call_1"):
        self.type = "response.function_call_arguments.done"
        self.arguments = arguments
        self.name = name
        self.item_id = item_id


class _FakeOutputItemAddedEvent:
    def __init__(self, item: Any, output_index: int = 0):
        self.type = "response.output_item.added"
        self.item = item
        self.output_index = output_index


class _FakeOutputItemDoneEvent:
    def __init__(self, item: Any, output_index: int = 0):
        self.type = "response.output_item.done"
        self.item = item
        self.output_index = output_index


class _FakeCompletedEvent:
    def __init__(self, response: _FakeResponse):
        self.type = "response.completed"
        self.response = response


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
        assert kwargs["input"][0]["content"] == "test"
        return _FakeResponse(output=[_FakeMessage(text="Hello world!")])

    monkeypatch.setattr(llm._client.responses, "create", fake_create)  # type: ignore[attr-defined]

    req = _build_request(model="@openai/gpt-4o-mini", text="test")
    outputs: list[str] = []
    async for resp in llm.generate_content_async(req, stream=False):
        assert not getattr(resp, "partial", False)
        parts = getattr(getattr(resp, "content", None), "parts", []) or []
        for p in parts:
            text = getattr(p, "text", None)
            if text:
                outputs.append(text)
    assert "".join(outputs) == "Hello world!"


@pytest.mark.asyncio
async def test_non_streaming_with_reasoning_and_function_call(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    llm = PortkeyAdk(model="@openai/gpt-4o-mini", api_key="test")

    async def fake_create(**kwargs: Any) -> _FakeResponse:
        assert kwargs["reasoning"]["summary"] == "auto"
        assert kwargs["include"] == ["reasoning.encrypted_content"]
        return _FakeResponse(
            output=[
                _FakeReasoningItem(
                    text="Let me think.",
                    encrypted_content="sig123",
                ),
                _FakeMessage(text="Final answer."),
                _FakeFunctionCall("lookup_weather", '{"city":"SF"}'),
            ]
        )

    monkeypatch.setattr(llm._client.responses, "create", fake_create)  # type: ignore[attr-defined]

    req = LlmRequest(
        model="@openai/gpt-4o-mini",
        contents=[
            genai_types.Content(
                role="user",
                parts=[genai_types.Part.from_text(text="test")],
            )
        ],
        config=genai_types.GenerateContentConfig(
            thinking_config=genai_types.ThinkingConfig(include_thoughts=True)
        ),
    )

    thoughts: list[str] = []
    thought_signatures: list[str] = []
    texts: list[str] = []
    function_names: list[str] = []
    async for resp in llm.generate_content_async(req, stream=False):
        parts = getattr(getattr(resp, "content", None), "parts", []) or []
        for p in parts:
            text = getattr(p, "text", None)
            thought_signature = getattr(p, "thought_signature", None)
            function_call = getattr(p, "function_call", None)
            if getattr(p, "thought", False) and text:
                thoughts.append(text)
                if isinstance(thought_signature, str):
                    thought_signatures.append(thought_signature)
            elif function_call is not None and getattr(function_call, "name", None):
                function_names.append(function_call.name)
            elif text:
                texts.append(text)

    assert "".join(thoughts) == "Let me think."
    assert thought_signatures == ["sig123"]
    assert "".join(texts) == "Final answer."
    assert function_names == ["lookup_weather"]


@pytest.mark.asyncio
async def test_streaming_yields_partials_and_final(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    llm = PortkeyAdk(model="@openai/gpt-4o-mini", api_key="test")

    final_response = _FakeResponse(
        output=[
            _FakeReasoningItem(text="Thinking...", item_id="rs_1"),
            _FakeMessage(text="Answer: 42"),
        ]
    )

    async def fake_stream_gen() -> AsyncIterator[Any]:
        yield _FakeOutputItemAddedEvent(_FakeReasoningItem(text=None, item_id="rs_1"))
        yield _FakeReasoningDeltaEvent("Thinking...")
        yield _FakeTextDeltaEvent("Answer: ")
        yield _FakeTextDeltaEvent("42")
        yield _FakeCompletedEvent(final_response)

    async def fake_create(**kwargs: Any) -> AsyncIterator[Any]:
        assert kwargs["stream"] is True
        return fake_stream_gen()

    monkeypatch.setattr(llm._client.responses, "create", fake_create)  # type: ignore[attr-defined]

    req = _build_request(model="@openai/gpt-4o-mini", text="test")
    partial_thoughts: list[str] = []
    partial_text: list[str] = []
    final_thoughts: list[str] = []
    final_text: list[str] = []

    async for resp in llm.generate_content_async(req, stream=True):
        parts = getattr(getattr(resp, "content", None), "parts", []) or []
        for p in parts:
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
async def test_streaming_function_call_yields_tool_response(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    llm = PortkeyAdk(model="@openai/gpt-4o-mini", api_key="test")
    function_item = _FakeFunctionCall("lookup_weather", '{"city":"SF"}')
    final_response = _FakeResponse(output=[function_item])

    async def fake_stream_gen() -> AsyncIterator[Any]:
        yield _FakeOutputItemAddedEvent(function_item)
        yield _FakeFunctionArgsDeltaEvent('{"city":')
        yield _FakeFunctionArgsDoneEvent('{"city":"SF"}', "lookup_weather")
        yield _FakeOutputItemDoneEvent(function_item)
        yield _FakeCompletedEvent(final_response)

    async def fake_create(**kwargs: Any) -> AsyncIterator[Any]:
        return fake_stream_gen()

    monkeypatch.setattr(llm._client.responses, "create", fake_create)  # type: ignore[attr-defined]

    req = _build_request(model="@openai/gpt-4o-mini", text="test")
    function_names: list[str] = []
    async for resp in llm.generate_content_async(req, stream=True):
        parts = getattr(getattr(resp, "content", None), "parts", []) or []
        for p in parts:
            function_call = getattr(p, "function_call", None)
            if function_call is not None and getattr(function_call, "name", None):
                function_names.append(function_call.name)

    assert function_names == ["lookup_weather"]


def test_normalize_thought_signature_string() -> None:
    assert _normalize_thought_signature("signature_string") == "signature_string"


def test_normalize_thought_signature_bytes() -> None:
    assert _normalize_thought_signature(b"binary_sig") == "YmluYXJ5X3NpZw=="


def test_normalize_thought_signature_none() -> None:
    assert _normalize_thought_signature(None) is None


def test_get_reasoning_config_with_budget() -> None:
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
    result = _get_reasoning_config(req)
    assert result is not None
    assert result["effort"] == "medium"
    assert result["summary"] == "auto"


def test_get_reasoning_config_without_budget() -> None:
    req = LlmRequest(
        model="test",
        contents=[],
        config=genai_types.GenerateContentConfig(
            thinking_config=genai_types.ThinkingConfig(
                include_thoughts=True,
            ),
        ),
    )
    result = _get_reasoning_config(req)
    assert result is not None
    assert result["effort"] == "medium"


def test_get_reasoning_config_none_when_not_configured() -> None:
    req = LlmRequest(model="test", contents=[])
    assert _get_reasoning_config(req) is None


def test_get_reasoning_config_none_when_empty() -> None:
    req = LlmRequest(
        model="test",
        contents=[],
        config=genai_types.GenerateContentConfig(
            thinking_config=genai_types.ThinkingConfig(),
        ),
    )
    assert _get_reasoning_config(req) is None
