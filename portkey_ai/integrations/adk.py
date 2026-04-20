"""Google ADK integration: thin adapter over Portkey Async client.

This module is only imported when users explicitly do:

    from portkey_ai.integrations.adk import PortkeyAdk

It requires the optional dependency "google-adk" (and its deps). Recommended install:

    pip install 'portkey-ai[adk]'

Design:
- Keep this adapter tiny. Heavy lifting (Responses API transport, etc.)
  is already provided by Portkey's SDK. We only:
  - Map ADK `google.genai.types.Content`/tools -> Responses API input.
  - Translate Responses output and streaming events -> ADK `LlmResponse` objects.
  - Expose a class compatible with ADK `BaseLlm` interface.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, AsyncGenerator, Iterable, Optional
import base64
import json

from portkey_ai import AsyncPortkey

if TYPE_CHECKING:
    from google.adk.models.llm_request import LlmRequest  # type: ignore  # no py.typed
    from google.adk.models.llm_response import LlmResponse  # type: ignore[import-untyped]  # no py.typed

try:
    from google.adk.models.base_llm import BaseLlm as _AdkBaseLlm  # type: ignore  # no py.typed

    _HAS_ADK = True
except Exception:  # pragma: no cover
    _HAS_ADK = False

    class _AdkBaseLlm:  # type: ignore[no-redef]  # stub used when google-adk is absent
        pass


def _safe_json_serialize(obj: Any) -> str:
    try:
        return json.dumps(obj, ensure_ascii=False)
    except (TypeError, ValueError, OverflowError):
        return str(obj)


def _to_input_role(role: Optional[str], system_role: str) -> str:
    if role in ("model", "assistant"):
        return "assistant"
    if role in ("system", "developer"):
        return system_role if system_role in ("system", "developer") else "developer"
    return "user"


def _normalize_thought_signature(value: Any) -> Optional[str]:
    """Normalize thought_signature to ``str``.

    Gemini returns raw ``bytes``; Responses API returns a base-64 ``str``.
    """
    if value is None:
        return None
    if isinstance(value, bytes):
        return base64.b64encode(value).decode("utf-8")
    if isinstance(value, str):
        return value
    return None


def _schema_to_dict(schema: Any) -> dict[str, Any]:
    """Recursively convert ADK Schema to a plain JSON schema dict."""
    schema_dict = schema.model_dump(exclude_none=True)
    if "type" in schema_dict:
        schema_type = schema_dict["type"]
        schema_dict["type"] = (
            schema_type.value if hasattr(schema_type, "value") else schema_type
        ).lower()
    if "items" in schema_dict:
        items = schema_dict["items"]
        if isinstance(items, dict):
            try:
                from google.genai import types as genai_types  # type: ignore[import-untyped]  # no py.typed

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


def _ensure_strict_json_schema(schema: Any) -> Any:
    if isinstance(schema, dict):
        schema_type = schema.get("type")
        is_object = schema_type == "object" or (
            isinstance(schema_type, list) and "object" in schema_type
        )
        if is_object:
            schema.setdefault("additionalProperties", False)
        for key, value in list(schema.items()):
            if isinstance(value, (dict, list)):
                schema[key] = _ensure_strict_json_schema(value)
        return schema
    if isinstance(schema, list):
        return [_ensure_strict_json_schema(item) for item in schema]
    return schema


def _build_input_content(parts: Iterable[Any]) -> list[dict[str, Any]] | str:
    content_objects: list[dict[str, Any]] = []
    for part in parts:
        text = getattr(part, "text", None)
        inline_data = getattr(part, "inline_data", None)
        if text:
            if isinstance(parts, list) and len(parts) == 1:
                return text
            content_objects.append({"type": "input_text", "text": text})
            continue
        if not (
            inline_data
            and getattr(inline_data, "data", None)
            and getattr(inline_data, "mime_type", None)
        ):
            continue

        b64 = base64.b64encode(inline_data.data).decode("utf-8")
        mime_type = inline_data.mime_type
        data_uri = f"data:{mime_type};base64,{b64}"
        if mime_type.startswith("image"):
            content_objects.append(
                {"type": "input_image", "image_url": data_uri, "detail": "auto"}
            )
        elif mime_type.startswith("audio"):
            audio_format = mime_type.split("/")[-1].lower()
            if audio_format not in ("mp3", "wav"):
                raise ValueError(
                    "Portkey(ADK) Responses adapter only supports mp3/wav audio inputs."
                )
            content_objects.append(
                {
                    "type": "input_audio",
                    "input_audio": {"data": b64, "format": audio_format},
                }
            )
        elif mime_type.startswith("video"):
            raise ValueError(
                "Portkey(ADK) Responses adapter does not support video input."
            )
        else:
            content_objects.append(
                {
                    "type": "input_file",
                    "file_data": data_uri,
                    "filename": "attachment",
                }
            )
    return content_objects


def _content_to_input_items(content: Any, system_role: str) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []

    tool_outputs = []
    for part in getattr(content, "parts", None) or []:
        function_response = getattr(part, "function_response", None)
        if not function_response:
            continue
        call_id = getattr(function_response, "id", None)
        if not call_id:
            raise ValueError(
                "FunctionResponse is missing 'id' — cannot build call_id "
                "for function_call_output item in Responses API request."
            )
        tool_outputs.append(
            {
                "type": "function_call_output",
                "call_id": call_id,
                "output": _safe_json_serialize(
                    getattr(function_response, "response", None)
                ),
            }
        )
    if tool_outputs:
        return tool_outputs

    role = _to_input_role(getattr(content, "role", None), system_role)
    input_parts = getattr(content, "parts", None) or []

    text_or_media_present = False
    for part in input_parts:
        function_call = getattr(part, "function_call", None)
        if function_call:
            fc_name = getattr(function_call, "name", None)
            fc_id = getattr(function_call, "id", None)
            if not fc_name:
                raise ValueError(
                    "FunctionCall is missing 'name' — cannot build "
                    "function_call item for Responses API request."
                )
            if not fc_id:
                raise ValueError(
                    "FunctionCall is missing 'id' — cannot build "
                    "call_id for function_call item in Responses API request."
                )
            items.append(
                {
                    "type": "function_call",
                    "id": fc_id,
                    "call_id": fc_id,
                    "name": fc_name,
                    "arguments": _safe_json_serialize(
                        getattr(function_call, "args", None)
                    ),
                }
            )
            continue

        text = getattr(part, "text", None)
        inline_data = getattr(part, "inline_data", None)
        thought = getattr(part, "thought", False)
        thought_signature = _normalize_thought_signature(
            getattr(part, "thought_signature", None)
        )

        if thought and text:
            reasoning_item: dict[str, Any] = {
                "id": thought_signature or f"reasoning_{len(items)}",
                "type": "reasoning",
                "summary": [],
                "content": [{"type": "reasoning_text", "text": text}],
            }
            if thought_signature:
                reasoning_item["encrypted_content"] = thought_signature
            items.append(reasoning_item)
            continue

        if text or inline_data:
            text_or_media_present = True

    if text_or_media_present:
        message_parts_or_text = _build_input_content(input_parts)
        items.append(
            {"type": "message", "role": role, "content": message_parts_or_text}
        )

    return items


def _function_declaration_to_tool_param(function_declaration: Any) -> dict[str, Any]:
    name = getattr(function_declaration, "name", None)
    assert name

    properties: dict[str, Any] = {}
    params = getattr(function_declaration, "parameters", None)
    if params and getattr(params, "properties", None):
        for key, value in params.properties.items():
            properties[key] = _schema_to_dict(value)

    parameters: dict[str, Any] = {
        "type": "object",
        "properties": properties,
    }
    if params and getattr(params, "required", None):
        parameters["required"] = params.required
    parameters = _ensure_strict_json_schema(parameters)

    tool: dict[str, Any] = {
        "type": "function",
        "name": name,
        "description": getattr(function_declaration, "description", "") or "",
        "parameters": parameters,
        "strict": True,
    }
    return tool


def _get_response_inputs(
    llm_request: "LlmRequest", system_role: str = "developer"
) -> tuple[
    list[dict[str, Any]],
    Optional[list[dict[str, Any]]],
    Optional[dict[str, Any]],
    Optional[str],
]:
    input_items: list[dict[str, Any]] = []
    for content in getattr(llm_request, "contents", None) or []:
        input_items.extend(_content_to_input_items(content, system_role))

    config = getattr(llm_request, "config", None)
    system_instruction = getattr(config, "system_instruction", None) if config else None
    instructions = str(system_instruction) if system_instruction else None

    tools: Optional[list[dict[str, Any]]] = None
    if config and getattr(config, "tools", None):
        tool0 = next(iter(getattr(config, "tools", None) or []), None)
        function_declarations = (
            getattr(tool0, "function_declarations", None) if tool0 else None
        )
        if function_declarations:
            tools = [
                _function_declaration_to_tool_param(fd) for fd in function_declarations
            ]

    text_config: Optional[dict[str, Any]] = None
    response_schema = getattr(config, "response_schema", None) if config else None
    if response_schema:
        try:
            json_schema = _schema_to_dict(response_schema)
            text_config = {
                "format": {
                    "type": "json_schema",
                    "name": "adk_response",
                    "schema": json_schema,
                    "strict": True,
                }
            }
        except Exception:
            text_config = None

    return input_items, tools, text_config, instructions


def _get_reasoning_config(llm_request: "LlmRequest") -> Optional[dict[str, Any]]:
    """Map ADK thinking_config to Portkey Responses ``reasoning`` dict.

    The Portkey Responses API accepts ``reasoning.effort`` as a string
    ("low" | "medium" | "high") for **all** providers — Portkey translates
    this to each provider's native reasoning mechanism server-side (e.g.
    Anthropic's ``budget_tokens``, Google's ``thinking_budget``).

    ADK exposes an integer ``thinking_budget`` (token count), so we map it
    to the closest effort level. The thresholds below are best-effort
    heuristics; some models may not support every effort level (e.g.
    GPT-5.3 only supports "medium").  In those cases the provider returns
    a clear error indicating the supported values.
    """
    config = getattr(llm_request, "config", None)
    thinking_config = getattr(config, "thinking_config", None) if config else None
    if not thinking_config or not getattr(thinking_config, "include_thoughts", None):
        return None

    budget = getattr(thinking_config, "thinking_budget", None)
    effort = "medium"
    if budget is not None:
        if budget <= 1024:
            effort = "low"
        elif budget <= 4096:
            effort = "medium"
        else:
            effort = "high"
    return {"effort": effort, "summary": "auto"}


def _usage_to_metadata(usage: Any) -> Any:
    from google.genai import types as genai_types  # type: ignore[import-untyped]  # no py.typed

    if not usage:
        return None
    return genai_types.GenerateContentResponseUsageMetadata(
        prompt_token_count=getattr(usage, "input_tokens", 0),
        candidates_token_count=getattr(usage, "output_tokens", 0),
        total_token_count=getattr(usage, "total_tokens", 0),
    )


def _build_text_part(
    text: str, thought: bool = False, thought_signature: Optional[str] = None
) -> Any:
    from google.genai import types as genai_types  # type: ignore[import-untyped]  # no py.typed

    part = genai_types.Part.from_text(text=text)
    if thought:
        part.thought = True
    if thought_signature:
        part.thought_signature = thought_signature  # type: ignore[assignment]  # Part.thought_signature typed as bytes but Responses API uses str
    return part


def _function_call_to_part(item: Any) -> Any:
    from google.genai import types as genai_types  # type: ignore[import-untyped]  # no py.typed

    args_str = getattr(item, "arguments", "{}") or "{}"
    name = getattr(item, "name", None) or "function_call"
    try:
        parsed_args = json.loads(args_str)
    except json.JSONDecodeError:
        parsed_args = {}
    part = genai_types.Part.from_function_call(
        name=name,
        args=parsed_args,
    )
    function_call = getattr(part, "function_call", None)
    if function_call is not None:
        function_call.id = getattr(item, "call_id", None) or getattr(item, "id", None)
    return part


def _response_output_to_parts(output: Iterable[Any]) -> list[Any]:
    parts: list[Any] = []
    for item in output:
        item_type = getattr(item, "type", None)
        if item_type == "reasoning":
            thought_signature = _normalize_thought_signature(
                getattr(item, "encrypted_content", None)
            )
            for content in getattr(item, "content", None) or []:
                if getattr(content, "type", None) == "reasoning_text":
                    parts.append(
                        _build_text_part(
                            getattr(content, "text", ""),
                            thought=True,
                            thought_signature=thought_signature,
                        )
                    )
            if not getattr(item, "content", None):
                for summary in getattr(item, "summary", None) or []:
                    parts.append(
                        _build_text_part(getattr(summary, "text", ""), thought=True)
                    )
        elif item_type == "message":
            for content in getattr(item, "content", None) or []:
                content_type = getattr(content, "type", None)
                if content_type == "output_text":
                    parts.append(_build_text_part(getattr(content, "text", "")))
                elif content_type == "refusal":
                    parts.append(_build_text_part(getattr(content, "refusal", "")))
        elif item_type == "function_call":
            parts.append(_function_call_to_part(item))
    return parts


def _function_call_key(item: Any) -> Optional[str]:
    key = getattr(item, "call_id", None) or getattr(item, "id", None)
    return str(key) if key is not None else None


def _merge_function_call_item(target: Any, source: Any) -> None:
    source_name = getattr(source, "name", None)
    if source_name and not getattr(target, "name", None):
        target.name = source_name

    source_arguments = getattr(source, "arguments", None)
    if source_arguments and (
        not getattr(target, "arguments", None)
        or len(str(source_arguments)) > len(str(getattr(target, "arguments", "")))
    ):
        target.arguments = source_arguments

    source_call_id = getattr(source, "call_id", None)
    if source_call_id and not getattr(target, "call_id", None):
        target.call_id = source_call_id

    source_id = getattr(source, "id", None)
    if source_id and not getattr(target, "id", None):
        target.id = source_id

    source_status = getattr(source, "status", None)
    if source_status and not getattr(target, "status", None):
        target.status = source_status


def _merge_streamed_function_calls(
    response: Any, streamed_function_calls: dict[int, Any]
) -> Any:
    output = list(getattr(response, "output", None) or [])
    existing_by_key: dict[str, Any] = {}

    for item in output:
        if getattr(item, "type", None) != "function_call":
            continue
        key = _function_call_key(item)
        if key:
            existing_by_key[key] = item

    for output_index, item in sorted(streamed_function_calls.items()):
        key = _function_call_key(item)
        if key and key in existing_by_key:
            _merge_function_call_item(existing_by_key[key], item)
            continue

        insert_at = min(output_index, len(output))
        output.insert(insert_at, item)
        if key:
            existing_by_key[key] = item

    response.output = output
    return response


def _response_to_llm_response(response: Any, is_partial: bool = False) -> "LlmResponse":
    from google.adk.models.llm_response import LlmResponse  # type: ignore[import-untyped]  # no py.typed
    from google.genai import types as genai_types  # type: ignore[import-untyped]  # no py.typed

    llm_response = LlmResponse(
        content=genai_types.Content(
            role="model",
            parts=_response_output_to_parts(getattr(response, "output", None) or []),
        ),
        partial=is_partial,
    )
    usage_metadata = _usage_to_metadata(getattr(response, "usage", None))
    if usage_metadata is not None:
        llm_response.usage_metadata = usage_metadata
    return llm_response


def _parts_to_llm_response(
    parts: list[Any], is_partial: bool = False, usage: Any = None
) -> "LlmResponse":
    from google.adk.models.llm_response import LlmResponse  # type: ignore[import-untyped]  # no py.typed
    from google.genai import types as genai_types  # type: ignore[import-untyped]  # no py.typed

    llm_response = LlmResponse(
        content=genai_types.Content(role="model", parts=parts),
        partial=is_partial,
    )
    usage_metadata = _usage_to_metadata(usage)
    if usage_metadata is not None:
        llm_response.usage_metadata = usage_metadata
    return llm_response


class PortkeyAdk(_AdkBaseLlm):  # type: ignore[misc]  # _AdkBaseLlm may be a stub when google-adk is absent
    """ADK `BaseLlm` adapter backed by Portkey Async client."""

    def __init__(
        self, model: str, api_key: Optional[str] = None, **kwargs: Any
    ) -> None:  # type: ignore[override]  # BaseLlm.__init__ has a different signature
        if not _HAS_ADK:
            raise ImportError(
                "google-adk is not installed. Install with: pip install 'portkey-ai[adk]'"
            )

        sys_role = str(kwargs.pop("system_role", "developer")).lower()

        # Extract Portkey client kwargs before passing the rest to BaseLlm.
        client_args: dict[str, Any] = {}
        if api_key:
            client_args["api_key"] = api_key
        _CLIENT_KEYS = (
            "virtual_key",
            "base_url",
            "config",
            "provider",
            "Authorization",
        )
        for key in _CLIENT_KEYS:
            if key in kwargs:
                client_args[key] = kwargs.pop(key)
        client_args["strict_open_ai_compliance"] = kwargs.pop(
            "strict_open_ai_compliance", False
        )

        base_kwargs = {k: v for k, v in kwargs.items() if k != "model"}
        try:
            super().__init__(model=model, **base_kwargs)  # type: ignore[misc,call-arg]  # BaseLlm may be the stub; real BaseLlm signature varies by adk version
        except TypeError:
            super().__init__()  # type: ignore[misc,call-arg]  # fallback for older BaseLlm that takes no args
        self.model: str = model  # type: ignore[assignment]  # BaseLlm declares model as a Pydantic field with different type

        # Must be set AFTER super().__init__() -- Pydantic resets __dict__.
        self._system_role: str = (
            sys_role if sys_role in ("developer", "system") else "developer"
        )

        self._client = AsyncPortkey(**client_args)  # type: ignore[arg-type]  # client_args values are Any; AsyncPortkey expects specific types

        _RESERVED_ARG_KEYS = {"input", "tools", "stream", "text", "reasoning"}
        self._additional_args: dict[str, Any] = {
            k: v for k, v in kwargs.items() if k not in _RESERVED_ARG_KEYS
        }

    async def generate_content_async(
        self, llm_request: "LlmRequest", stream: bool = False
    ) -> AsyncGenerator["LlmResponse", None]:  # type: ignore[override,name-defined]  # return type differs from BaseLlm; LlmResponse is a forward ref
        maybe_append_user_content = getattr(self, "_maybe_append_user_content", None)
        if callable(maybe_append_user_content):
            maybe_append_user_content(llm_request)

        input_items, tools, text_config, instructions = _get_response_inputs(
            llm_request, self._system_role
        )
        reasoning = _get_reasoning_config(llm_request)

        response_args: dict[str, Any] = {
            "model": self.model,
            "input": input_items,
            **({"tools": tools} if tools else {}),
            **({"text": text_config} if text_config else {}),
            **({"instructions": instructions} if instructions else {}),
        }
        if reasoning:
            response_args["reasoning"] = reasoning
            response_args.setdefault("include", ["reasoning.encrypted_content"])

        response_args.update(self._additional_args)

        # Ensure adapter-required include entries aren't dropped by user overrides.
        if reasoning:
            include = response_args.get("include") or []
            if not isinstance(include, list):
                include = [include]
            if "reasoning.encrypted_content" not in include:
                include.append("reasoning.encrypted_content")
            response_args["include"] = include
        if tools and "tool_choice" not in response_args:
            response_args["tool_choice"] = "auto"

        if not stream:
            response = await self._client.responses.create(**response_args)
            yield _response_to_llm_response(response)
            return

        stream_response = await self._client.responses.create(
            stream=True, **response_args
        )
        final_response: Any = None
        streamed_function_calls_by_index: dict[int, Any] = {}
        streamed_function_calls_by_id: dict[str, Any] = {}

        async for event in stream_response:  # type: ignore[union-attr]  # create() returns union of Response|AsyncStream; we know it's AsyncStream here
            event_type: str | None = getattr(event, "type", None)

            if event_type == "response.reasoning_text.delta":
                delta: str = getattr(event, "delta", "")
                if delta:
                    yield _parts_to_llm_response(
                        [_build_text_part(delta, thought=True)],
                        is_partial=True,
                    )

            elif event_type == "response.output_text.delta":
                delta = getattr(event, "delta", "")
                if delta:
                    yield _parts_to_llm_response(
                        [_build_text_part(delta)],
                        is_partial=True,
                    )

            elif event_type == "response.output_item.added":
                item = getattr(event, "item", None)
                if getattr(item, "type", None) == "function_call":
                    output_index = getattr(
                        event, "output_index", len(streamed_function_calls_by_index)
                    )
                    if getattr(item, "arguments", None) is None:
                        item.arguments = ""
                    streamed_function_calls_by_index[output_index] = item
                    key = _function_call_key(item)
                    if key:
                        streamed_function_calls_by_id[key] = item

            elif event_type == "response.function_call_arguments.delta":
                output_index = getattr(event, "output_index", None)
                item = (
                    streamed_function_calls_by_index.get(output_index)
                    if output_index is not None
                    else None
                )
                if item is None:
                    item_id = getattr(event, "item_id", None)
                    if item_id is not None:
                        item = streamed_function_calls_by_id.get(str(item_id))
                delta = getattr(event, "delta", "")
                if item is not None and delta:
                    item.arguments = f"{getattr(item, 'arguments', '')}{delta}"

            elif event_type == "response.function_call_arguments.done":
                output_index = getattr(event, "output_index", None)
                item = (
                    streamed_function_calls_by_index.get(output_index)
                    if output_index is not None
                    else None
                )
                if item is None:
                    item_id = getattr(event, "item_id", None)
                    if item_id is not None:
                        item = streamed_function_calls_by_id.get(str(item_id))
                if item is not None:
                    arguments = getattr(event, "arguments", None)
                    if arguments is not None:
                        item.arguments = arguments
                    name = getattr(event, "name", None)
                    if name:
                        item.name = name

            elif event_type == "response.completed":
                final_response = getattr(event, "response", None)
                if final_response is not None and streamed_function_calls_by_index:
                    final_response = _merge_streamed_function_calls(
                        final_response, streamed_function_calls_by_index
                    )

        if final_response is not None:
            yield _response_to_llm_response(final_response)


__all__ = ["PortkeyAdk"]
