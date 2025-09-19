import asyncio
import os
import sys

try:
    from google.adk.models.llm_request import LlmRequest
    from google.genai import types
    from portkey_ai.integrations.adk import PortkeyAdk
except Exception as e:  # pragma: no cover - example script
    print("This example requires the 'adk' extra: pip install 'portkey-ai[adk]'")
    raise


def build_request(model: str) -> "LlmRequest":  # type: ignore[name-defined]
    return LlmRequest(
        model=model,
        contents=[
            types.Content(
                role="user",
                parts=[types.Part.from_text(text="Give me a one-line programming joke (final only).")],
            )
        ],
    )


async def main() -> None:
    api_key = os.environ.get("PORTKEY_API_KEY")
    model = os.environ.get("MODEL_SLUG", "@openai/gpt-4o-mini")

    if not api_key:
        print("Set PORTKEY_API_KEY in your environment.", file=sys.stderr)
        sys.exit(1)

    llm = PortkeyAdk(api_key=api_key, model=model)

    # Non-streaming: returns a single final response
    req = build_request(model)
    final_text: list[str] = []
    async for resp in llm.generate_content_async(req, stream=False):
        if resp.content and getattr(resp.content, "parts", None):
            for p in resp.content.parts:
                if getattr(p, "text", None):
                    final_text.append(p.text)
    print("".join(final_text))


if __name__ == "__main__":  # pragma: no cover - example script
    asyncio.run(main())
