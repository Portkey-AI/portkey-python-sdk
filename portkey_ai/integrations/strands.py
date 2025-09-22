"""Strands integration: thin adapter over Portkey Async client.

This module is only imported when users explicitly do:

    from portkey_ai.integrations.strands import PortkeyModel

It requires the optional dependency "strands-agents". Recommend install:

    pip install 'portkey-ai[strands]'

Design:
- Keep this adapter tiny. Heavy lifting (OpenAI-compatible streaming, etc.)
  is already provided by Portkey's SDK. We only:
  - Map Strands Messages/Tools -> OpenAI-compatible request.
  - Translate OpenAI-style stream chunks -> Strands StreamEvent.
  - Expose a class compatible with Strands `Model` interface.
"""

from __future__ import annotations

import json
import uuid
from typing import Any, AsyncGenerator, AsyncIterator, Optional, TYPE_CHECKING, cast, List, Type, TypeVar, Union

from portkey_ai import AsyncPortkey

if TYPE_CHECKING:  # Only used for static typing; no runtime import of Strands
    from strands.types.content import Messages
    from strands.types.tools import ToolSpec
    from strands.types.streaming import StreamEvent

T = TypeVar("T")

try:
    from strands.models.model import Model as _StrandsModel  # type: ignore

    _HAS_STRANDS = True
except Exception:
    _HAS_STRANDS = False

    class _StrandsModel:  # type: ignore
        pass


def _map_tools_to_openai(
    tool_specs: Optional[list[ToolSpec]],
) -> Optional[list[dict[str, Any]]]:
    if not tool_specs:
        return None
    tools: list[dict[str, Any]] = []
    for spec in tool_specs:
        json_schema = spec["inputSchema"]["json"]
        properties = json_schema.get("properties", {})
        # Drop default=None fields for OpenAI compatibility
        cleaned_properties = {
            key: {
                k: v
                for k, v in definition.items()
                if not (k == "default" and v is None)
            }
            for key, definition in properties.items()
        }
        tools.append(
            {
                "type": "function",
                "function": {
                    "name": spec["name"],
                    "description": spec.get("description", ""),
                    "parameters": {
                        "type": "object",
                        "properties": cleaned_properties,
                        "required": json_schema.get("required", []),
                    },
                },
            }
        )
    return tools


class _MessageFormatter:
    """Formats Strands messages into OpenAI-compatible messages.

    Tracks current tool use id to correctly emit tool result messages.
    """

    def __init__(self) -> None:
        self._current_tool_use_id: Optional[str] = None

    def format_messages(
        self, messages: "Messages", system_prompt: Optional[str]
    ) -> list[dict[str, Any]]:
        formatted: list[dict[str, Any]] = []

        if system_prompt:
            formatted.append({"role": "system", "content": system_prompt})

        for message in messages:
            role = message.get("role")
            content = message.get("content")
            if role not in ("user", "assistant"):
                continue

            if isinstance(content, str):
                formatted.append({"role": role, "content": content})
                continue

            if isinstance(content, list):
                for part in content:
                    if (
                        isinstance(part, dict)
                        and "text" in part
                        and isinstance(part["text"], str)
                    ):
                        formatted.append({"role": role, "content": part["text"]})
                    elif isinstance(part, dict) and "toolUse" in part:
                        formatted.append(self._format_tool_use_part(part))
                    elif (
                        isinstance(part, dict)
                        and "toolResult" in part
                        and self._current_tool_use_id is not None
                    ):
                        formatted.append(self._format_tool_result_part(part))

        return formatted

    def _format_tool_use_part(self, part: dict[str, Any]) -> dict[str, Any]:
        tool_use = part["toolUse"]
        tool_use_id = tool_use.get("toolUseId") or f"tooluse-{uuid.uuid4().hex[:8]}"
        self._current_tool_use_id = tool_use_id
        return {
            "role": "assistant",
            "tool_calls": [
                {
                    "id": tool_use_id,
                    "type": "function",
                    "function": {
                        "name": tool_use.get("name"),
                        "arguments": json.dumps(tool_use.get("input", {})),
                    },
                }
            ],
            "content": None,
        }

    def _format_tool_result_part(self, part: dict[str, Any]) -> dict[str, Any]:
        # Strands toolResult content is an array of blocks; concatenate text blocks
        content_blocks = part["toolResult"].get("content", [])
        text_parts = [
            blk["text"]
            for blk in content_blocks
            if isinstance(blk, dict) and "text" in blk
        ]
        result_text = " ".join(text_parts)
        return {
            "role": "tool",
            "tool_call_id": self._current_tool_use_id,
            "content": result_text,
        }


def _get_attr(obj: Any, name: str, default: Any = None) -> Any:
    try:
        return getattr(obj, name)
    except Exception:
        return cast(dict, obj).get(name, default)


def _format_chunk_to_stream_event(
    event: Any,
    state: dict[str, Optional[str]],
) -> "StreamEvent":
    """Translate an OpenAI-style ChatCompletionChunk into a Strands StreamEvent.

    Maintains tool use start/accumulation/stop using `state`.
    """
    choices = _get_attr(event, "choices") or [{}]
    choice0 = choices[0] if choices else {}
    delta = _get_attr(choice0, "delta") or {}

    # Tool calls
    tool_calls = _get_attr(delta, "tool_calls")
    if tool_calls:
        tool_call0 = tool_calls[0]
        function = _get_attr(tool_call0, "function") or {}
        tool_name = _get_attr(function, "name")
        arguments_chunk = _get_attr(function, "arguments", "") or ""
        call_type = _get_attr(tool_call0, "type")

        if tool_name and call_type and not state.get("tool_name"):
            state["tool_name"] = tool_name
            state["tool_use_id"] = f"{tool_name}-{uuid.uuid4().hex[:6]}"
            return cast(
                "StreamEvent",
                {
                    "contentBlockStart": {
                        "start": {
                            "toolUse": {
                                "name": tool_name,
                                "toolUseId": state["tool_use_id"],
                            }
                        }
                    }
                },
            )

        if arguments_chunk:
            return cast(
                "StreamEvent",
                {
                    "contentBlockDelta": {
                        "delta": {"toolUse": {"input": arguments_chunk}}
                    }
                },
            )

    finish_reason = str(_get_attr(choice0, "finish_reason", "") or "").lower()
    if finish_reason in ("tool_calls", "tool_use"):
        return cast(
            "StreamEvent",
            {
                "contentBlockStop": {
                    "name": state.get("tool_name"),
                    "toolUseId": state.get("tool_use_id"),
                }
            },
        )

    content_text = _get_attr(delta, "content")
    if content_text:
        return cast(
            "StreamEvent", {"contentBlockDelta": {"delta": {"text": content_text}}}
        )

    usage = _get_attr(event, "usage")
    if usage:
        return cast(
            "StreamEvent",
            {
                "metadata": {
                    "metrics": {"latencyMs": 0},
                    "usage": {
                        "inputTokens": _get_attr(usage, "prompt_tokens", 0) or 0,
                        "outputTokens": _get_attr(usage, "completion_tokens", 0) or 0,
                        "totalTokens": _get_attr(usage, "total_tokens", 0) or 0,
                    },
                }
            },
        )

    return cast("StreamEvent", {})


class PortkeyStrands(_StrandsModel):  # type: ignore[misc]
    """Strands `Model` adapter backed by Portkey Async client."""

    def __init__(self, **config: dict[str, Any]) -> None:  # type: ignore[override]
        if not _HAS_STRANDS:
            raise ImportError(
                "strands-agents is not installed. Install with: pip install 'portkey-ai[strands]'"
            )
        # Store config as-is for Strands get_config/update_config APIs
        self._config: dict[str, Any] = {"streaming": True}
        self.update_config(**config)

        self._provider_name: str = str(self._config.get("provider", "openai")).lower()
        self._client = AsyncPortkey(
            api_key=self._config.get("api_key"),
            virtual_key=self._config.get("virtual_key"),
            base_url=self._config.get("base_url"),
        )

    def update_config(self, **model_config: dict[str, Any]) -> None:  # type: ignore[override]
        self._config.update(model_config)

    def get_config(self) -> dict[str, Any]:  # type: ignore[override]
        return self._config

    def _allow_tool_use(self) -> bool:
        if self._provider_name == "openai":
            return True
        if self._provider_name == "bedrock":
            model_id = str(self._config.get("model_id", "")).lower()
            return "anthropic" in model_id
        return False

    async def stream(
        self,
        messages: "Messages",
        tool_specs: Optional[list["ToolSpec"]] = None,
        system_prompt: Optional[str] = None,
        **kwargs: Any,
    ) -> AsyncGenerator["StreamEvent", None]:  # type: ignore[override]
        formatter = _MessageFormatter()
        formatted_messages = formatter.format_messages(messages, system_prompt)

        request: dict[str, Any] = {
            "messages": formatted_messages,
            "model": self._config.get("model_id"),
            "stream": True,
        }

        if tool_specs and self._allow_tool_use():
            tools = _map_tools_to_openai(tool_specs)
            if tools:
                request["tools"] = tools
                request["tool_choice"] = "auto"

        state: dict[str, Optional[str]] = {"tool_use_id": None, "tool_name": None}

        yield cast("StreamEvent", {"messageStart": {"role": "assistant"}})
        # Await the creation to obtain an async iterator for streaming and cast for mypy
        stream_obj = await self._client.chat.completions.create(**request)  # type: ignore[arg-type]
        stream_iter = cast(AsyncIterator[Any], stream_obj)
        async for chunk in stream_iter:
            event = _format_chunk_to_stream_event(chunk, state)
            if event:
                yield event

            if (
                isinstance(event, dict)
                and "contentBlockStop" in event
                and state.get("tool_use_id")
            ):
                # Signal immediate message stop for tool use to let Strands hand over to tool executor
                yield cast("StreamEvent", {"messageStop": {"stopReason": "tool_use"}})

        # Reset internal state per call
        state["tool_use_id"] = None
        state["tool_name"] = None

    async def structured_output(
        self,
        output_model: "Type[T]",
        prompt: List[dict[str, Any]],
        system_prompt: Optional[str] = None,
        **kwargs: Any,
    ) -> AsyncGenerator[dict[str, Union["T", Any]], None]:  # type: ignore[override]
        """Placeholder to satisfy Strands Model abstract requirements.

        Note: PortkeyStrands currently focuses on streaming text/tool events via `stream`.
        Structured output is not yet implemented. This method exists to allow the
        class to be instantiated by Strands without raising an abstract class error.
        """
        raise NotImplementedError(
            "PortkeyStrands.structured_output is not implemented yet. "
            "Use model.stream(...) for streaming responses."
        )


__all__ = ["PortkeyStrands"]
