from typing import Any, AsyncIterator, Optional

import pytest

pytest.importorskip("google.adk", reason="google-adk extra not installed")

from google.adk.models.llm_request import LlmRequest  # type: ignore
from google.genai import types as genai_types  # type: ignore

from portkey_ai.integrations.adk import (
    PortkeyAdk,
    _ensure_strict_json_schema,
    _get_response_inputs,
    _merge_streamed_function_calls,
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
    def __init__(
        self,
        delta: str,
        item_id: str = "call_1",
        output_index: int = 0,
    ):
        self.type = "response.function_call_arguments.delta"
        self.delta = delta
        self.item_id = item_id
        self.output_index = output_index


class _FakeFunctionArgsDoneEvent:
    def __init__(
        self,
        arguments: str,
        name: str,
        item_id: str = "call_1",
        output_index: int = 0,
    ):
        self.type = "response.function_call_arguments.done"
        self.arguments = arguments
        self.name = name
        self.item_id = item_id
        self.output_index = output_index


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


@pytest.mark.asyncio
async def test_streaming_function_call_is_merged_when_final_response_omits_it(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    llm = PortkeyAdk(model="@openai/gpt-4o-mini", api_key="test")
    function_item = _FakeFunctionCall("lookup_weather", "")
    final_response = _FakeResponse(output=[_FakeMessage(text="Done")])

    async def fake_stream_gen() -> AsyncIterator[Any]:
        yield _FakeOutputItemAddedEvent(function_item)
        yield _FakeFunctionArgsDeltaEvent('{"city":"')
        yield _FakeFunctionArgsDeltaEvent('SF"}')
        yield _FakeCompletedEvent(final_response)

    async def fake_create(**kwargs: Any) -> AsyncIterator[Any]:
        return fake_stream_gen()

    monkeypatch.setattr(llm._client.responses, "create", fake_create)  # type: ignore[attr-defined]

    req = _build_request(model="@openai/gpt-4o-mini", text="test")
    function_names: list[str] = []
    function_args: list[Any] = []
    final_text: list[str] = []

    async for resp in llm.generate_content_async(req, stream=True):
        parts = getattr(getattr(resp, "content", None), "parts", []) or []
        for p in parts:
            function_call = getattr(p, "function_call", None)
            text = getattr(p, "text", None)
            if function_call is not None and getattr(function_call, "name", None):
                function_names.append(function_call.name)
                function_args.append(getattr(function_call, "args", None))
            elif text and not getattr(resp, "partial", False):
                final_text.append(text)

    assert function_names == ["lookup_weather"]
    assert function_args == [{"city": "SF"}]
    assert "".join(final_text) == "Done"


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


@pytest.mark.asyncio
async def test_streaming_multiple_parallel_function_calls(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    llm = PortkeyAdk(model="@openai/gpt-4o-mini", api_key="test")
    fc1 = _FakeFunctionCall("get_weather", "", call_id="call_1")
    fc2 = _FakeFunctionCall("get_time", "", call_id="call_2")
    final_response = _FakeResponse(output=[_FakeMessage(text="Here you go")])

    async def fake_stream_gen() -> AsyncIterator[Any]:
        yield _FakeOutputItemAddedEvent(fc1, output_index=0)
        yield _FakeOutputItemAddedEvent(fc2, output_index=1)
        yield _FakeFunctionArgsDeltaEvent('{"city":', item_id="call_1", output_index=0)
        yield _FakeFunctionArgsDeltaEvent('{"tz":', item_id="call_2", output_index=1)
        yield _FakeFunctionArgsDeltaEvent('"SF"}', item_id="call_1", output_index=0)
        yield _FakeFunctionArgsDeltaEvent('"PST"}', item_id="call_2", output_index=1)
        yield _FakeCompletedEvent(final_response)

    async def fake_create(**kwargs: Any) -> AsyncIterator[Any]:
        return fake_stream_gen()

    monkeypatch.setattr(llm._client.responses, "create", fake_create)  # type: ignore[attr-defined]

    req = _build_request(model="@openai/gpt-4o-mini", text="test")
    function_names: list[str] = []
    function_args: list[Any] = []

    async for resp in llm.generate_content_async(req, stream=True):
        parts = getattr(getattr(resp, "content", None), "parts", []) or []
        for p in parts:
            function_call = getattr(p, "function_call", None)
            if function_call is not None and getattr(function_call, "name", None):
                function_names.append(function_call.name)
                function_args.append(getattr(function_call, "args", None))

    assert function_names == ["get_weather", "get_time"]
    assert function_args == [{"city": "SF"}, {"tz": "PST"}]


@pytest.mark.asyncio
async def test_streaming_merge_enriches_incomplete_final_response(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    llm = PortkeyAdk(model="@openai/gpt-4o-mini", api_key="test")
    streamed_item = _FakeFunctionCall("lookup_weather", "", call_id="call_1")
    final_item = _FakeFunctionCall("lookup_weather", "", call_id="call_1")
    final_response = _FakeResponse(output=[final_item])

    async def fake_stream_gen() -> AsyncIterator[Any]:
        yield _FakeOutputItemAddedEvent(streamed_item, output_index=0)
        yield _FakeFunctionArgsDeltaEvent(
            '{"city":"SF"}', item_id="call_1", output_index=0
        )
        yield _FakeCompletedEvent(final_response)

    async def fake_create(**kwargs: Any) -> AsyncIterator[Any]:
        return fake_stream_gen()

    monkeypatch.setattr(llm._client.responses, "create", fake_create)  # type: ignore[attr-defined]

    req = _build_request(model="@openai/gpt-4o-mini", text="test")
    function_args: list[Any] = []

    async for resp in llm.generate_content_async(req, stream=True):
        parts = getattr(getattr(resp, "content", None), "parts", []) or []
        for p in parts:
            function_call = getattr(p, "function_call", None)
            if function_call is not None and getattr(function_call, "name", None):
                function_args.append(getattr(function_call, "args", None))

    assert function_args == [{"city": "SF"}]


def test_ensure_strict_json_schema_nested_objects() -> None:
    schema: dict[str, Any] = {
        "type": "object",
        "properties": {
            "location": {
                "type": "object",
                "properties": {
                    "city": {"type": "string"},
                    "coords": {
                        "type": "object",
                        "properties": {
                            "lat": {"type": "number"},
                            "lon": {"type": "number"},
                        },
                    },
                },
            },
        },
    }
    result = _ensure_strict_json_schema(schema)
    assert result["additionalProperties"] is False
    assert result["properties"]["location"]["additionalProperties"] is False
    assert (
        result["properties"]["location"]["properties"]["coords"]["additionalProperties"]
        is False
    )


def test_ensure_strict_json_schema_array_of_objects() -> None:
    schema: dict[str, Any] = {
        "type": "object",
        "properties": {
            "items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                    },
                },
            },
        },
    }
    result = _ensure_strict_json_schema(schema)
    assert result["additionalProperties"] is False
    inner = result["properties"]["items"]["items"]
    assert inner["additionalProperties"] is False


def test_merge_streamed_function_calls_inserts_missing() -> None:
    response = _FakeResponse(output=[_FakeMessage(text="Done")])
    fc = _FakeFunctionCall("do_thing", '{"x":1}', call_id="call_1")
    result = _merge_streamed_function_calls(response, {0: fc})
    types = [getattr(item, "type", None) for item in result.output]
    assert types == ["function_call", "message"]


def test_merge_streamed_function_calls_enriches_existing() -> None:
    existing_fc = _FakeFunctionCall("do_thing", "", call_id="call_1")
    response = _FakeResponse(output=[existing_fc])
    streamed_fc = _FakeFunctionCall("do_thing", '{"x":1}', call_id="call_1")
    _merge_streamed_function_calls(response, {0: streamed_fc})
    assert existing_fc.arguments == '{"x":1}'


def test_get_response_inputs_adds_additional_properties_false_for_tools() -> None:
    req = LlmRequest(
        model="test",
        contents=[
            genai_types.Content(
                role="user",
                parts=[genai_types.Part.from_text(text="weather")],
            )
        ],
        config=genai_types.GenerateContentConfig(
            tools=[
                genai_types.Tool(
                    function_declarations=[
                        genai_types.FunctionDeclaration(
                            name="get_demo_weather",
                            description="Return canned weather information.",
                            parameters=genai_types.Schema(
                                type="OBJECT",
                                properties={
                                    "city": genai_types.Schema(
                                        type="STRING",
                                        description="City name",
                                    )
                                },
                                required=["city"],
                            ),
                        )
                    ]
                )
            ]
        ),
    )

    _, tools, _, _ = _get_response_inputs(req)

    assert tools is not None
    assert tools[0]["strict"] is True
    assert tools[0]["parameters"]["additionalProperties"] is False
