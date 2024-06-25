from portkey_ai.api_resources.base_client import APIClient, AsyncAPIClient
import asyncio


class APIResource:
    _client: APIClient
    # _get: Any
    # _patch: Any
    # _put: Any
    # _delete: Any

    def __init__(self, client: APIClient) -> None:
        self._client = client
        # self._get = client.get
        # self._patch = client.patch
        # self._put = client.put
        # self._delete = client.delete

    def _post(self, *args, **kwargs):
        return self._client._post(*args, **kwargs)

    def _put(self, *args, **kwargs):
        return self._client._put(*args, **kwargs)

    def _get(self, *args, **kwargs):
        return self._client._get(*args, **kwargs)

    def _delete(self, *args, **kwargs):
        return self._client._delete(*args, **kwargs)


class AsyncAPIResource:
    _client: AsyncAPIClient

    def __init__(self, client: AsyncAPIClient) -> None:
        self._client = client
        # self._get = client.get
        # self._patch = client.patch
        # self._put = client.put
        # self._delete = client.delete

    async def _post(self, *args, **kwargs):
        return await self._client._post(*args, **kwargs)

    async def _put(self, *args, **kwargs):
        return await self._client._put(*args, **kwargs)

    async def _sleep(self, seconds: float) -> None:
        await asyncio.sleep(seconds)
