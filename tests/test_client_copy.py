from typing import List, Optional

import httpx
import pytest

from portkey_ai import AsyncPortkey, Portkey


@pytest.fixture
def requests() -> List[httpx.Request]:
    return []


@pytest.fixture
def transport(requests: List[httpx.Request]) -> httpx.MockTransport:
    def respond(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json={"id": "test", "choices": []})

    return httpx.MockTransport(respond)


@pytest.mark.parametrize("method", ["copy", "with_options"])
@pytest.mark.parametrize(
    "initial,override,expected",
    [
        (True, False, False),
        (True, None, True),
        (False, None, False),
        (False, True, True),
    ],
)
def test_copy_boolean_headers(
    method: str,
    initial: bool,
    override: Optional[bool],
    expected: bool,
    transport: httpx.MockTransport,
    requests: List[httpx.Request],
) -> None:
    with httpx.Client(transport=transport) as http_client:
        client = Portkey(
            api_key="test-key",
            http_client=http_client,
            debug=initial,
            cache_force_refresh=initial,
        )
        copied = getattr(client, method)(debug=override, cache_force_refresh=override)
        copied.chat.completions.create(model="test-model", messages=[])
        client.chat.completions.create(model="test-model", messages=[])

    for header in ("x-portkey-debug", "x-portkey-cache-force-refresh"):
        assert [request.headers[header] for request in requests] == [
            str(expected).lower(),
            str(initial).lower(),
        ]


@pytest.mark.asyncio
@pytest.mark.parametrize("method", ["copy", "with_options"])
@pytest.mark.parametrize(
    "initial,override,expected",
    [
        (True, False, False),
        (True, None, True),
        (False, None, False),
        (False, True, True),
    ],
)
async def test_async_copy_boolean_headers(
    method: str,
    initial: bool,
    override: Optional[bool],
    expected: bool,
    transport: httpx.MockTransport,
    requests: List[httpx.Request],
) -> None:
    async with httpx.AsyncClient(transport=transport) as http_client:
        client = AsyncPortkey(
            api_key="test-key",
            http_client=http_client,
            debug=initial,
            cache_force_refresh=initial,
        )
        copied = getattr(client, method)(debug=override, cache_force_refresh=override)
        await copied.chat.completions.create(model="test-model", messages=[])
        await client.chat.completions.create(model="test-model", messages=[])

    for header in ("x-portkey-debug", "x-portkey-cache-force-refresh"):
        assert [request.headers[header] for request in requests] == [
            str(expected).lower(),
            str(initial).lower(),
        ]
