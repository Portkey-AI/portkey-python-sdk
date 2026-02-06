"""Google ADK integration: thin adapter over Portkey Async client.

This module is only imported when users explicitly do:

    from portkey_ai.integrations.adk import PortkeyAdk

It requires the optional dependency "google-adk" (and its deps). Recommended install:

    pip install 'portkey-ai[adk]'

Design:
- Keep this adapter tiny. Heavy lifting (OpenAI-compatible streaming, etc.)
  is already provided by Portkey's SDK. We only:
  - Map ADK `google.genai.types.Content`/tools -> OpenAI-compatible request.
  - Translate OpenAI-style stream chunks -> ADK `LlmResponse` objects.
  - Expose a class compatible with ADK `BaseLlm` interface.
"""

from __future__ import annotations

from typing import (
    Any,
    AsyncGenerator,
    AsyncIterator,
    Optional,
    TYPE_CHECKING,
    Iterable,
    Union,
    Tuple,
    Generator,
    Literal,
    cast,
)
import json
import base64
import logging

from portkey_ai import AsyncPortkey

logger = logging.getLogger("portkey_ai.integrations.adk")

if TYPE_CHECKING:  # Only for static typing, never imported at runtime automatically
    from google.adk.models.base_llm import BaseLlm as _AdkBaseLlm  # type: ignore
    from google.adk.models.llm_request import LlmRequest  # type: ignore
    from google.adk.models.llm_response import LlmResponse  # type: ignore

try:
    # Attempt runtime import so we can subclass the ADK BaseLlm and construct ADK types.
    from google.adk.models.base_llm import BaseLlm as _AdkBaseLlm  # type: ignore

    _HAS_ADK = True
except Exception:  # pragma: no cover - when ADK not installed
    _HAS_ADK = False

    class _AdkBaseLlm:  # type: ignore
        """Fallback to allow import of this module without ADK installed."""

        pass


# ------------------------------- helpers ------------------------------------


class _FunctionChunk:
    def __init__(
        self,
        id: Optional[str],
        name: Optional[str],
        args: Optional[str],
        index: Optional[int] = 0,
    ) -> None:
        self.id = id
        self.name = name
        self.args = args
        self.index = index or 0


class _TextChunk:
    def __init__(self, text: str, thought_signature: Optional[str] = None) -> None:
        self.text = text
        self.thought_signature = thought_signature


class _ThoughtChunk:
    def __init__(self, text: str, thought_signature: Optional[str] = None) -> None:
        self.text = text
        self.thought_signature = thought_signature


class _UsageMetadataChunk:
    def __init__(
        self, prompt_tokens: int, completion_tokens: int, total_tokens: int
    ) -> None:
        self.prompt_tokens = prompt_tokens
        self.completion_tokens = completion_tokens
        self.total_tokens = total_tokens


def _get_anthropic_content_blocks(message: Any) -> Optional[list[dict[str, Any]]]:
    """Extract content_blocks from a message, falling back to list-typed content.

    Portkey returns thinking/reasoning via content_blocks when
    strict_open_ai_compliance=False. Some providers put them directly in
    content as a list instead.
    """
    content_blocks = getattr(message, "content_blocks", None)
    if content_blocks is None:
        content = getattr(message, "content", None)
        if isinstance(content, list):
            content_blocks = content
    return content_blocks


def _iter_anthropic_content_blocks(
    content_blocks: Optional[list[dict[str, Any]]],
) -> Iterable[tuple[str, str, Optional[str]]]:
    """Yields (block_type, text, thought_signature) from content blocks.

    Handles both non-streaming format (type/thinking/text keys) and
    streaming delta format (delta dict with thinking/text keys).
    """
    if not content_blocks:
        return []
    items: list[tuple[str, str, Optional[str]]] = []
    for block in content_blocks:
        block_type = block.get("type")
        thought_signature = _get_gemini_thought_signature(
            block.get("thought_signature")
        )
        if block_type == "thinking":
            text = block.get("thinking")
            if text:
                items.append(("thinking", text, thought_signature))
        elif block_type == "text":
            text = block.get("text")
            if text:
                items.append(("text", text, thought_signature))
        elif "delta" in block:
            delta = block.get("delta", {})
            if delta.get("thinking"):
                items.append(("thinking", delta["thinking"], thought_signature))
            elif delta.get("text"):
                items.append(("text", delta["text"], thought_signature))
    return items


def _get_gemini_thought_signature(value: Any) -> Optional[str]:
    """Normalize thought_signature to str. Gemini returns bytes, Portkey returns str."""
    if value is None:
        return None
    if isinstance(value, bytes):
        return base64.b64encode(value).decode("utf-8")
    if isinstance(value, str):
        return value
    return None


def _build_content_blocks(
    thought_text: str,
    thought_signature: Optional[str],
    text: str,
    text_signature: Optional[str],
) -> Optional[list[dict[str, Any]]]:
    """Build content_blocks for aggregated streaming responses, omitting empty blocks."""
    blocks: list[dict[str, Any]] = []
    if thought_text:
        blocks.append(
            {
                "type": "thinking",
                "thinking": thought_text,
                "thought_signature": thought_signature,
            }
        )
    if text:
        blocks.append(
            {
                "type": "text",
                "text": text,
                "thought_signature": text_signature,
            }
        )
    return blocks or None


def _safe_json_serialize(obj: Any) -> str:
    try:
        return json.dumps(obj, ensure_ascii=False)
    except (TypeError, OverflowError):
        return str(obj)


def _to_portkey_role(role: Optional[str]) -> Literal["user", "assistant"]:
    if role in ["model", "assistant"]:
        return "assistant"
    return "user"


def _get_content(parts: Iterable[Any]) -> Union[list[dict], str]:
    """Convert ADK parts to Portkey/OpenAI-compatible content.

    Note: we import google.genai.types lazily to avoid runtime import when ADK isn't installed.
    """
    content_objects: list[dict] = []
    # We treat `parts` as an iterable of objects with attributes: text, inline_data(data,mime_type)
    for part in parts:
        text = getattr(part, "text", None)
        inline_data = getattr(part, "inline_data", None)
        thought_signature = _get_gemini_thought_signature(
            getattr(part, "thought_signature", None)
        )
        if text:
            # Return simple string when it's a single text part
            if isinstance(parts, list) and len(parts) == 1:
                return text
            content_object: dict[str, Any] = {"type": "text", "text": text}
            if thought_signature:
                content_object["thought_signature"] = thought_signature
            content_objects.append(content_object)
        elif (
            inline_data
            and getattr(inline_data, "data", None)
            and getattr(inline_data, "mime_type", None)
        ):
            b64 = base64.b64encode(inline_data.data).decode("utf-8")
            data_uri = f"data:{inline_data.mime_type};base64,{b64}"
            if inline_data.mime_type.startswith("image"):
                content_objects.append(
                    {
                        "type": "image_url",
                        "image_url": {"url": data_uri},
                    }
                )
            elif inline_data.mime_type.startswith("video"):
                content_objects.append(
                    {
                        "type": "video_url",
                        "video_url": {"url": data_uri},
                    }
                )
            elif inline_data.mime_type.startswith("audio"):
                content_objects.append(
                    {
                        "type": "audio_url",
                        "audio_url": {"url": data_uri},
                    }
                )
            elif inline_data.mime_type == "application/pdf":
                content_objects.append(
                    {
                        "type": "file",
                        "file": {
                            "file_data": data_uri,
                            "format": inline_data.mime_type,
                        },
                    }
                )
            else:
                raise ValueError("Portkey(ADK) does not support this content part.")
    return content_objects


def _content_to_message_param(content: Any) -> Union[dict, list[dict]]:
    """Convert ADK `types.Content` to OpenAI-compatible message dict(s)."""
    tool_messages: list[dict] = []
    for part in getattr(content, "parts", []) or []:
        function_response = getattr(part, "function_response", None)
        if function_response:
            tool_messages.append(
                {
                    "role": "tool",
                    "tool_call_id": getattr(function_response, "id", None),
                    "content": _safe_json_serialize(
                        getattr(function_response, "response", None)
                    ),
                }
            )
    if tool_messages:
        return tool_messages if len(tool_messages) > 1 else tool_messages[0]

    role = _to_portkey_role(getattr(content, "role", None))
    message_content = _get_content(getattr(content, "parts", []) or []) or None

    if role == "user":
        return {"role": "user", "content": message_content}

    # assistant/model
    tool_calls: list[dict] = []
    content_present = False
    for part in getattr(content, "parts", []) or []:
        function_call = getattr(part, "function_call", None)
        if function_call:
            tool_call: dict[str, Any] = {
                "type": "function",
                "id": getattr(function_call, "id", None),
                "function": {
                    "name": getattr(function_call, "name", None),
                    "arguments": _safe_json_serialize(
                        getattr(function_call, "args", None)
                    ),
                },
            }
            thought_signature = _get_gemini_thought_signature(
                getattr(part, "thought_signature", None)
            )
            if thought_signature:
                tool_call["thought_signature"] = thought_signature
            tool_calls.append(tool_call)
        elif getattr(part, "text", None) or getattr(part, "inline_data", None):
            content_present = True

    final_content = message_content if content_present else None
    if (
        isinstance(final_content, list)
        and final_content
        and final_content[0].get("type") == "text"
    ):
        # Some providers require a plain string when only a single text block
        final_content = final_content[0].get("text", "")

    msg: dict[str, Any] = {"role": role, "content": final_content}
    if tool_calls:
        msg["tool_calls"] = tool_calls
    return msg


def _schema_to_dict(schema: Any) -> dict:
    """Recursively convert ADK Schema to a plain JSON schema dict."""
    schema_dict = schema.model_dump(exclude_none=True)
    if "type" in schema_dict:
        t = schema_dict["type"]
        schema_dict["type"] = (t.value if hasattr(t, "value") else t).lower()
    if "items" in schema_dict:
        items = schema_dict["items"]
        if isinstance(items, dict):
            # Rebuild a Schema object then recurse
            try:
                from google.genai import types as genai_types  # type: ignore

                schema_dict["items"] = _schema_to_dict(
                    genai_types.Schema.model_validate(items)
                )
            except Exception:
                schema_dict["items"] = items
        elif hasattr(items, "type"):
            schema_dict["items"] = _schema_to_dict(items)
    if "properties" in schema_dict:
        new_props: dict[str, Any] = {}
        for key, value in schema_dict["properties"].items():
            if hasattr(value, "model_dump"):
                new_props[key] = _schema_to_dict(value)
            elif isinstance(value, dict):
                new_props[key] = value
                if "type" in new_props[key]:
                    new_props[key]["type"] = str(new_props[key]["type"]).lower()
            else:
                new_props[key] = value
        schema_dict["properties"] = new_props
    return schema_dict


def _function_declaration_to_tool_param(function_declaration: Any) -> dict:
    """Convert ADK FunctionDeclaration to OpenAI tool param dict."""
    name = getattr(function_declaration, "name", None)
    assert name

    properties: dict[str, Any] = {}
    params = getattr(function_declaration, "parameters", None)
    if params and getattr(params, "properties", None):
        for key, value in params.properties.items():
            properties[key] = _schema_to_dict(value)

    tool = {
        "type": "function",
        "function": {
            "name": name,
            "description": getattr(function_declaration, "description", "") or "",
            "parameters": {
                "type": "object",
                "properties": properties,
            },
        },
    }

    if params and getattr(params, "required", None):
        # Help mypy understand nested dict mutation
        params_dict = cast(dict, tool["function"]["parameters"])  # type: ignore[index]
        params_dict["required"] = params.required

    return tool


def _model_response_to_chunk(
    response: Any,
) -> Generator[
    Tuple[
        Optional[Union[_TextChunk, _FunctionChunk, _UsageMetadataChunk, _ThoughtChunk]],
        Optional[str],
    ],
    None,
    None,
]:
    """Convert Portkey ChatCompletion response/chunk to ADK-friendly chunks."""
    message = None
    finish_reason = None
    if getattr(response, "choices", None):
        choice0 = response.choices[0]
        finish_reason = getattr(choice0, "finish_reason", None)
        if getattr(choice0, "delta", None):
            message = choice0.delta
        elif getattr(choice0, "message", None):
            message = choice0.message

        if message:
            reasoning_content = getattr(message, "reasoning_content", None)
            if reasoning_content:
                yield _ThoughtChunk(text=reasoning_content), finish_reason

            content_blocks = _get_anthropic_content_blocks(message)
            has_content_blocks = bool(content_blocks)
            for block_type, text, thought_signature in _iter_anthropic_content_blocks(
                content_blocks
            ):
                if block_type == "thinking":
                    yield (
                        _ThoughtChunk(text=text, thought_signature=thought_signature),
                        finish_reason,
                    )
                elif block_type == "text":
                    yield (
                        _TextChunk(text=text, thought_signature=thought_signature),
                        finish_reason,
                    )

            if not has_content_blocks and getattr(message, "content", None):
                yield _TextChunk(text=message.content), finish_reason

            tool_calls = getattr(message, "tool_calls", None)
            if tool_calls:
                for tool_call in tool_calls:
                    if getattr(tool_call, "type", None) == "function":
                        yield (
                            _FunctionChunk(
                                id=getattr(tool_call, "id", None),
                                name=getattr(
                                    getattr(tool_call, "function", None), "name", None
                                ),
                                args=getattr(
                                    getattr(tool_call, "function", None),
                                    "arguments",
                                    None,
                                ),
                                index=getattr(tool_call, "index", 0),
                            ),
                            finish_reason,
                        )

            if finish_reason and not (
                (getattr(message, "content", None))
                or (getattr(message, "tool_calls", None))
                or reasoning_content
                or has_content_blocks
            ):
                yield None, finish_reason

    if not message:
        yield None, None

    usage = getattr(response, "usage", None)
    if usage:
        yield (
            _UsageMetadataChunk(
                prompt_tokens=getattr(usage, "prompt_tokens", 0),
                completion_tokens=getattr(usage, "completion_tokens", 0),
                total_tokens=getattr(usage, "total_tokens", 0),
            ),
            None,
        )


def _message_to_generate_content_response(
    message: Any, is_partial: bool = False
) -> "LlmResponse":  # type: ignore[name-defined]
    """Convert a Portkey-style message object to ADK LlmResponse."""
    from google.genai import types as genai_types  # type: ignore
    from google.adk.models.llm_response import LlmResponse  # type: ignore

    parts: list[Any] = []

    content_blocks = _get_anthropic_content_blocks(message)
    if content_blocks:
        # content_blocks take priority; they carry both thinking and text with signatures
        for block_type, text, thought_signature in _iter_anthropic_content_blocks(
            content_blocks
        ):
            if block_type == "thinking":
                thought_part = genai_types.Part.from_text(text=text)
                thought_part.thought = True
                if thought_signature:
                    # stubs say bytes | None but _get_gemini_thought_signature
                    # and _iter_anthropic_content_blocks return str; works at runtime
                    thought_part.thought_signature = thought_signature  # type: ignore[assignment]
                parts.append(thought_part)
            elif block_type == "text":
                text_part = genai_types.Part.from_text(text=text)
                if thought_signature:
                    # stubs say bytes | None but _get_gemini_thought_signature
                    # and _iter_anthropic_content_blocks return str; works at runtime
                    text_part.thought_signature = thought_signature  # type: ignore[assignment]
                parts.append(text_part)
    else:
        reasoning_content = getattr(message, "reasoning_content", None)
        if reasoning_content:
            thought_part = genai_types.Part.from_text(text=reasoning_content)
            thought_part.thought = True
            parts.append(thought_part)
        if getattr(message, "content", None):
            parts.append(genai_types.Part.from_text(text=message.content))

    if getattr(message, "tool_calls", None):
        for tool_call in message.tool_calls:
            if getattr(tool_call, "type", None) == "function":
                part = genai_types.Part.from_function_call(
                    name=getattr(getattr(tool_call, "function", None), "name", None),  # type: ignore[arg-type]
                    args=json.loads(
                        getattr(getattr(tool_call, "function", None), "arguments", "{}")
                        or "{}"
                    ),
                )
                # Attach tool_call id if present
                try:
                    part.function_call.id = getattr(tool_call, "id", None)  # type: ignore[union-attr]
                except Exception:
                    pass
                parts.append(part)

    return LlmResponse(
        content=genai_types.Content(role="model", parts=parts), partial=is_partial
    )


def _model_response_to_generate_content_response(response: Any) -> "LlmResponse":  # type: ignore[name-defined]
    from google.genai import types as genai_types  # type: ignore

    message = None
    if getattr(response, "choices", None):
        message = response.choices[0].message

    if not message:
        raise ValueError("No message in response")

    llm_response = _message_to_generate_content_response(message)
    usage = getattr(response, "usage", None)
    if usage:
        llm_response.usage_metadata = genai_types.GenerateContentResponseUsageMetadata(
            prompt_token_count=getattr(usage, "prompt_tokens", 0),
            candidates_token_count=getattr(usage, "completion_tokens", 0),
            total_token_count=getattr(usage, "total_tokens", 0),
        )
    return llm_response


def _get_completion_inputs(
    llm_request: "LlmRequest", system_role: str = "developer"
) -> tuple[list[dict], Optional[list[dict]], Optional[dict]]:  # type: ignore[name-defined]
    """Convert ADK LlmRequest into OpenAI-compatible inputs for Portkey.

    Args:
        llm_request: The ADK request object.
        system_role: Which role to use for the system instruction. One of
            "developer" (default, aligned with ADK/LiteLLM) or "system"
            (for providers that strictly expect a system role).
    """
    # 1) Messages
    messages: list[dict] = []
    for content in getattr(llm_request, "contents", []) or []:
        msg_or_list = _content_to_message_param(content)
        if isinstance(msg_or_list, list):
            messages.extend(msg_or_list)
        elif msg_or_list:
            messages.append(msg_or_list)

    # Insert system/developer instruction
    config = getattr(llm_request, "config", None)
    system_instruction = getattr(config, "system_instruction", None) if config else None
    if system_instruction:
        role = system_role if system_role in ("developer", "system") else "developer"
        messages.insert(0, {"role": role, "content": system_instruction})

    # 2) Tools
    tools: Optional[list[dict]] = None
    if config and getattr(config, "tools", None):
        # Avoid indexing a Collection directly; use next(iter(...)) for mypy compatibility
        tool0 = next(iter(getattr(config, "tools", []) or []), None)
        function_declarations = (
            getattr(tool0, "function_declarations", None) if tool0 else None
        )
        if function_declarations:
            tools = [
                _function_declaration_to_tool_param(fd) for fd in function_declarations
            ]

    # 3) Response format (convert ADK schema to OpenAI json_schema where possible)
    response_format: Optional[dict] = None
    response_schema = getattr(config, "response_schema", None) if config else None
    if response_schema:
        try:
            json_schema = _schema_to_dict(response_schema)
            response_format = {
                "type": "json_schema",
                "json_schema": {"name": "adk_response", "schema": json_schema},
            }
        except Exception:
            # Best effort: ignore if schema cannot be converted
            response_format = None

    return messages, tools, response_format


def _get_thinking_config(llm_request: "LlmRequest") -> Optional[dict[str, Any]]:  # type: ignore[name-defined]
    config = getattr(llm_request, "config", None)
    thinking_config = getattr(config, "thinking_config", None) if config else None
    if not thinking_config:
        return None
    include_thoughts = getattr(thinking_config, "include_thoughts", None)
    thinking_budget = getattr(thinking_config, "thinking_budget", None)
    if not include_thoughts:
        return None
    result: dict[str, Any] = {"type": "enabled"}
    if thinking_budget:
        result["budget_tokens"] = thinking_budget
    return result


# ----------------------------- main adapter ---------------------------------


class PortkeyAdk(_AdkBaseLlm):  # type: ignore[misc]
    """ADK `BaseLlm` adapter backed by Portkey Async client."""

    def __init__(
        self, model: str, api_key: Optional[str] = None, **kwargs: Any
    ) -> None:  # type: ignore[override]
        if not _HAS_ADK:
            raise ImportError(
                "google-adk is not installed. Install with: pip install 'portkey-ai[adk]'"
            )
        # Initialize ADK BaseLlm (Pydantic BaseModel) so `model` is recorded
        # Extract system instruction role preference before BaseLlm init
        sys_role = str(kwargs.pop("system_role", "developer")).lower()
        self._system_role = (
            sys_role if sys_role in ("developer", "system") else "developer"
        )

        super().__init__(
            model=model, **{k: v for k, v in kwargs.items() if k != "model"}
        )  # type: ignore[misc]

        # Set up Portkey client
        client_args: dict[str, Any] = {}
        if api_key:
            client_args["api_key"] = api_key
        # Common options: virtual key / base_url / provider + Authorization, etc.
        if "virtual_key" in kwargs:
            client_args["virtual_key"] = kwargs.pop("virtual_key")
        if "base_url" in kwargs:
            client_args["base_url"] = kwargs.pop("base_url")
        if "config" in kwargs:
            client_args["config"] = kwargs.pop("config")
        if "provider" in kwargs:
            client_args["provider"] = kwargs.pop("provider")
        if "Authorization" in kwargs:
            client_args["Authorization"] = kwargs.pop("Authorization")
        client_args["strict_open_ai_compliance"] = kwargs.pop(
            "strict_open_ai_compliance", False
        )

        self._client = AsyncPortkey(**client_args)  # type: ignore[arg-type]

        # Remaining args are passed through to completion calls (temperature, top_p, etc.)
        self._additional_args: dict[str, Any] = dict(kwargs)
        # Guard against reserved keys managed by us
        self._additional_args.pop("messages", None)
        self._additional_args.pop("tools", None)
        self._additional_args.pop("stream", None)

    async def generate_content_async(
        self, llm_request: "LlmRequest", stream: bool = False
    ) -> AsyncGenerator["LlmResponse", None]:  # type: ignore[override,name-defined]
        """Generate ADK LlmResponse objects using Portkey Chat Completions."""
        # Use ADK BaseLlm helper to ensure a user message exists so model can respond
        self._maybe_append_user_content(llm_request)

        messages, tools, response_format = _get_completion_inputs(
            llm_request, getattr(self, "_system_role", "developer")
        )
        thinking_config = _get_thinking_config(llm_request)

        completion_args: dict[str, Any] = {
            "model": getattr(self, "model", None),
            "messages": messages,
            "tools": tools,
            # Only include response_format if we successfully converted it
            **({"response_format": response_format} if response_format else {}),
        }
        if thinking_config:
            completion_args["thinking"] = thinking_config
        completion_args.update(self._additional_args)
        if tools and "tool_choice" not in completion_args:
            # Encourage tool use when functions are provided, mirroring Strands behavior
            completion_args["tool_choice"] = "auto"

        if stream:
            # Aggregate streaming text and tool calls to yield ADK LlmResponse objects
            text_accum = ""
            thought_accum = ""
            text_signature = None
            thought_signature = None
            function_calls: dict[int, dict[str, Any]] = {}
            fallback_index = 0
            usage_metadata = None
            aggregated_llm_response = None
            aggregated_llm_response_with_tool_call = None

            # Await the creation to obtain an async iterator for streaming
            stream_obj = await self._client.chat.completions.create(
                stream=True, **completion_args
            )  # type: ignore[arg-type]
            stream_iter = cast(AsyncIterator[Any], stream_obj)
            async for part in stream_iter:
                for chunk, finish_reason in _model_response_to_chunk(part):
                    if isinstance(chunk, _FunctionChunk):
                        idx = chunk.index or fallback_index
                        if idx not in function_calls:
                            function_calls[idx] = {"name": "", "args": "", "id": None}
                        if chunk.name:
                            function_calls[idx]["name"] += chunk.name
                        if chunk.args:
                            function_calls[idx]["args"] += chunk.args
                            # If args parses as JSON, advance fallback index (handles providers that omit indices)
                            try:
                                json.loads(function_calls[idx]["args"])
                                fallback_index += 1
                            except json.JSONDecodeError:
                                pass
                        function_calls[idx]["id"] = (
                            chunk.id or function_calls[idx]["id"] or str(idx)
                        )
                    elif isinstance(chunk, _ThoughtChunk):
                        thought_accum += chunk.text
                        if chunk.thought_signature:
                            thought_signature = chunk.thought_signature
                        yield _message_to_generate_content_response(
                            type(
                                "Msg",
                                (),
                                {
                                    "content": None,
                                    "reasoning_content": chunk.text,
                                    "content_blocks": [
                                        {
                                            "type": "thinking",
                                            "thinking": chunk.text,
                                            "thought_signature": chunk.thought_signature,
                                        }
                                    ],
                                    "tool_calls": None,
                                },
                            )(),
                            is_partial=True,
                        )
                    elif isinstance(chunk, _TextChunk):
                        text_accum += chunk.text
                        if chunk.thought_signature:
                            text_signature = chunk.thought_signature
                        # Yield partials for better interactivity
                        yield _message_to_generate_content_response(
                            type(
                                "Msg",
                                (),
                                {
                                    "content": chunk.text,
                                    "reasoning_content": None,
                                    "content_blocks": [
                                        {
                                            "type": "text",
                                            "text": chunk.text,
                                            "thought_signature": chunk.thought_signature,
                                        }
                                    ],
                                    "tool_calls": None,
                                },
                            )(),
                            is_partial=True,
                        )
                    elif isinstance(chunk, _UsageMetadataChunk):
                        from google.genai import types as genai_types  # type: ignore

                        usage_metadata = (
                            genai_types.GenerateContentResponseUsageMetadata(
                                prompt_token_count=chunk.prompt_tokens,
                                candidates_token_count=chunk.completion_tokens,
                                total_token_count=chunk.total_tokens,
                            )
                        )

                    if (finish_reason in ("tool_calls", "stop")) and function_calls:
                        # Flush tool calls as a single LlmResponse
                        tool_calls = []
                        for idx, data in function_calls.items():
                            if data.get("id"):
                                tool_calls.append(
                                    type(
                                        "ToolCall",
                                        (),
                                        {
                                            "type": "function",
                                            "id": data["id"],
                                            "function": type(
                                                "Function",
                                                (),
                                                {
                                                    "name": data["name"],
                                                    "arguments": data["args"],
                                                },
                                            )(),
                                            "index": idx,
                                        },
                                    )()
                                )
                        aggregated_llm_response_with_tool_call = (
                            _message_to_generate_content_response(
                                type(
                                    "Msg",
                                    (),
                                    {
                                        "content": "",
                                        "reasoning_content": thought_accum or None,
                                        "content_blocks": _build_content_blocks(
                                            thought_accum,
                                            thought_signature,
                                            text_accum,
                                            text_signature,
                                        ),
                                        "tool_calls": tool_calls,
                                    },
                                )()
                            )
                        )
                        function_calls.clear()
                    elif finish_reason == "stop" and (text_accum or thought_accum):
                        aggregated_llm_response = _message_to_generate_content_response(
                            type(
                                "Msg",
                                (),
                                {
                                    "content": text_accum or None,
                                    "reasoning_content": thought_accum or None,
                                    "content_blocks": _build_content_blocks(
                                        thought_accum,
                                        thought_signature,
                                        text_accum,
                                        text_signature,
                                    ),
                                    "tool_calls": None,
                                },
                            )()
                        )
                        text_accum = ""
                        thought_accum = ""
                        text_signature = None
                        thought_signature = None

            # End of stream: yield aggregated responses (attach usage if available)
            if aggregated_llm_response:
                if usage_metadata is not None:
                    aggregated_llm_response.usage_metadata = usage_metadata
                    usage_metadata = None
                yield aggregated_llm_response

            if aggregated_llm_response_with_tool_call:
                if usage_metadata is not None:
                    aggregated_llm_response_with_tool_call.usage_metadata = (
                        usage_metadata
                    )
                yield aggregated_llm_response_with_tool_call
        else:
            response = await self._client.chat.completions.create(**completion_args)
            yield _model_response_to_generate_content_response(response)


__all__ = ["PortkeyAdk"]
