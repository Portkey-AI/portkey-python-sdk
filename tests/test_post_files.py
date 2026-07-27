from __future__ import annotations

from typing import Dict

import httpx
import pytest

from portkey_ai import AsyncPortkey, Portkey

BASE_URL = "https://api.portkey.ai/v1"


def _capture_transport(captured: Dict[str, object]) -> httpx.MockTransport:
    def handler(request: httpx.Request) -> httpx.Response:
        captured["content_type"] = request.headers.get("content-type", "")
        captured["content"] = request.content
        return httpx.Response(200, json={"success": True})

    return httpx.MockTransport(handler)


def test_sync_post_sends_multipart_files() -> None:
    captured: Dict[str, object] = {}
    with httpx.Client(
        transport=_capture_transport(captured), base_url=BASE_URL
    ) as http_client:
        client = Portkey(api_key="dummy", base_url=BASE_URL, http_client=http_client)

        client.post(
            url="/files",
            purpose="assistants",
            files={"file": ("hello.txt", b"hello world", "text/plain")},
        )

    assert "multipart/form-data" in captured["content_type"]
    body = captured["content"]
    assert b"hello.txt" in body
    assert b"hello world" in body


@pytest.mark.asyncio
async def test_async_post_sends_multipart_files() -> None:
    captured: Dict[str, object] = {}
    async with httpx.AsyncClient(
        transport=_capture_transport(captured), base_url=BASE_URL
    ) as http_client:
        client = AsyncPortkey(
            api_key="dummy", base_url=BASE_URL, http_client=http_client
        )

        await client.post(
            url="/files",
            purpose="assistants",
            files={"file": ("hello.txt", b"hello world", "text/plain")},
        )

    assert "multipart/form-data" in captured["content_type"]
    body = captured["content"]
    assert b"hello.txt" in body
    assert b"hello world" in body
