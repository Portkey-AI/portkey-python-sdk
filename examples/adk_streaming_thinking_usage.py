"""ADK adapter example usage: streaming, thinking / reasoning, multi-provider.

Demonstrates the PortkeyAdk adapter across multiple providers (OpenAI,
Anthropic, Vertex/Gemini) in four modes:

  1. Non-streaming (basic)
  2. Non-streaming with thinking / reasoning
  3. Streaming (basic)
  4. Streaming with thinking / reasoning

Requires a valid Portkey API key.

Usage:
    PORTKEY_API_KEY=<key> python examples/adk_streaming_thinking_usage.py
"""

from __future__ import annotations

import asyncio
import os
import sys
import traceback
from typing import Any

_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from portkey_ai.integrations.adk import PortkeyAdk  # noqa: E402

try:
    from google.adk.models.llm_request import LlmRequest  # type: ignore
    from google.genai import types as genai_types  # type: ignore
except ImportError:
    print("google-adk is required: pip install 'portkey-ai[adk]'")
    sys.exit(1)


PORTKEY_API_KEY = os.environ.get("PORTKEY_API_KEY", "")

# (display_name, model_slug, supports_thinking)
MODELS: list[tuple[str, str, bool]] = [
    ("OpenAI GPT-5.3", "@openai/gpt-5.3-chat-latest", True),
    ("Anthropic Claude Sonnet 4.6", "@anthropic/claude-sonnet-4-6", True),
    ("Vertex Gemini 3 Flash", "@vertex-ai/gemini-3-flash-preview", True),
]

SIMPLE_PROMPT = "What is 2 + 2? Reply with just the number."
REASONING_PROMPT = (
    "A farmer has 17 sheep. All but 9 run away. How many sheep does the "
    "farmer have left? Think step by step, then give just the number."
)


def _build_request(
    model: str,
    prompt: str,
    *,
    enable_thinking: bool = False,
    thinking_budget: int = 4096,
) -> LlmRequest:
    """Build an LlmRequest with optional thinking config."""
    kwargs: dict[str, Any] = {
        "model": model,
        "contents": [
            genai_types.Content(
                role="user",
                parts=[genai_types.Part.from_text(text=prompt)],
            )
        ],
    }
    if enable_thinking:
        kwargs["config"] = genai_types.GenerateContentConfig(
            thinking_config=genai_types.ThinkingConfig(
                include_thoughts=True,
                thinking_budget=thinking_budget,
            ),
        )
    return LlmRequest(**kwargs)


def _print_parts(parts: Any, indent: str = "    ") -> None:
    """Print the parts of an LlmResponse in a readable format."""
    if not parts:
        print(f"{indent}(no parts)")
        return
    for i, p in enumerate(parts):
        thought = getattr(p, "thought", False)
        text = getattr(p, "text", None)
        fc = getattr(p, "function_call", None)
        thought_sig = getattr(p, "thought_signature", None)

        if thought and text:
            sig = f"  (signature: {thought_sig!r})" if thought_sig else ""
            print(f"{indent}[thought]{sig}")
            for line in text.splitlines():
                print(f"{indent}  {line}")
        elif text:
            print(f"{indent}[text]")
            for line in text.splitlines():
                print(f"{indent}  {line}")
        elif fc:
            print(
                f"{indent}[function_call] {getattr(fc, 'name', '?')}"
                f"({getattr(fc, 'args', {})})"
            )
        else:
            print(f"{indent}[unknown part] {type(p).__name__}")


async def run_non_streaming(
    llm: PortkeyAdk, prompt: str, *, enable_thinking: bool = False
) -> None:
    req = _build_request(llm.model, prompt, enable_thinking=enable_thinking)
    async for resp in llm.generate_content_async(req, stream=False):
        parts = getattr(resp.content, "parts", None) if resp.content else None
        _print_parts(parts)


async def run_streaming(
    llm: PortkeyAdk, prompt: str, *, enable_thinking: bool = False
) -> None:
    req = _build_request(llm.model, prompt, enable_thinking=enable_thinking)
    partial_count = 0
    async for resp in llm.generate_content_async(req, stream=True):
        parts = getattr(resp.content, "parts", None) if resp.content else None
        if getattr(resp, "partial", False):
            partial_count += 1
            for p in parts or []:
                text = getattr(p, "text", None)
                thought = getattr(p, "thought", False)
                if thought and text:
                    print(f"    [thought delta] {text[:120]}", end="")
                elif text:
                    print(text, end="")
        else:
            print()
            print(f"    --- final response ({partial_count} streaming chunks) ---")
            _print_parts(parts)


async def main() -> None:
    if not PORTKEY_API_KEY:
        print("Set PORTKEY_API_KEY environment variable.")
        sys.exit(1)

    for display_name, model_slug, supports_thinking in MODELS:
        print(f"\n{'=' * 60}")
        print(f"  {display_name}  ({model_slug})")
        print(f"{'=' * 60}")

        llm = PortkeyAdk(model=model_slug, api_key=PORTKEY_API_KEY)

        print(f"\n  Non-streaming | prompt: {SIMPLE_PROMPT!r}")
        try:
            await run_non_streaming(llm, SIMPLE_PROMPT)
        except Exception:
            traceback.print_exc()

        if supports_thinking:
            print(f"\n  Non-streaming + thinking | prompt: {REASONING_PROMPT!r}")
            try:
                await run_non_streaming(llm, REASONING_PROMPT, enable_thinking=True)
            except Exception:
                traceback.print_exc()

        print(f"\n  Streaming | prompt: {SIMPLE_PROMPT!r}")
        print("    ", end="")
        try:
            await run_streaming(llm, SIMPLE_PROMPT)
        except Exception:
            traceback.print_exc()

        if supports_thinking:
            print(f"\n  Streaming + thinking | prompt: {REASONING_PROMPT!r}")
            print("    ", end="")
            try:
                await run_streaming(llm, REASONING_PROMPT, enable_thinking=True)
            except Exception:
                traceback.print_exc()

    print()


if __name__ == "__main__":
    asyncio.run(main())
