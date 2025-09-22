import asyncio
import os
import sys

try:
    from portkey_ai.integrations.strands import PortkeyStrands
except Exception:
    print(
        "This example requires the 'strands' extra: pip install 'portkey-ai[strands]'",
        file=sys.stderr,
    )
    raise


async def main() -> None:
    api_key = os.environ.get("PORTKEY_API_KEY")
    model_id = os.environ.get("MODEL_SLUG", "@openai/gpt-4o-mini")

    if not api_key:
        print("Set PORTKEY_API_KEY in your environment.", file=sys.stderr)
        sys.exit(1)

    model = PortkeyStrands(
        api_key=api_key,  # type: ignore[arg-type]
        model_id=model_id,  # type: ignore[arg-type]
    )

    # Minimal Strands-compatible message list (no Agent required)
    messages = [
        {"role": "user", "content": "Tell me a short programming joke."},
    ]

    print(f"Streaming with model: {model_id}")
    async for event in model.stream(messages=messages):
        # Events follow the Strands stream event shape produced by our adapter.
        if isinstance(event, dict) and "contentBlockDelta" in event:
            delta = event["contentBlockDelta"].get("delta", {})
            if isinstance(delta, dict) and "text" in delta:
                print(delta["text"], end="")
    print("\n-- stream done --")


if __name__ == "__main__":  # pragma: no cover - example script
    asyncio.run(main())
