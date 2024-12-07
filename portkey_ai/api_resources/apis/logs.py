from typing import Any, Dict, List, Optional
from portkey_ai.api_resources.base_client import APIClient, AsyncAPIClient
from urllib.parse import urlencode
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.types.logs_type import (
    LogsExportCreateResponse,
    LogsExportListResponse,
    LogsExportUpdateResponse,
    LogsExportCancelResponse,
    LogsExportRetrieveResponse,
    LogsExportStartResponse,
    LogsExportDownloadResponse,
)
from portkey_ai.api_resources.utils import PortkeyApiPaths


class Logs(APIResource):
    def __init__(self, client: APIClient) -> None:
        super().__init__(client)
        self.exports = Exports(client)

    def create(
        self,
        *,
        request: Optional[Dict[str, Any]] = None,
        response: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Any:
        body = {
            "request": request,
            "response": response,
            "metadata": metadata,
        }
        response = self._post(
            f"{PortkeyApiPaths.LOGS_API}",
            body=body,
            params=None,
            cast_to=None,
            stream=False,
            stream_cls=None,
            headers={},
        )
        return response


class Exports(APIResource):
    def __init__(self, client: APIClient) -> None:
        super().__init__(client)

    def create(
        self,
        *,
        filters: Optional[Dict[str, Any]] = None,
        workspace_id: Optional[str] = None,
        description: Optional[str] = None,
        requested_data: Optional[List[str]] = None,
    ) -> LogsExportCreateResponse:
        body = {
            "filters": filters,
            "workspace_id": workspace_id,
            "description": description,
            "requested_data": requested_data,
        }
        return self._post(
            f"{PortkeyApiPaths.LOGS_EXPORT_API}",
            body=body,
            params=None,
            cast_to=LogsExportCreateResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def retrieve(self, *, export_id: str) -> LogsExportRetrieveResponse:
        return self._get(
            f"{PortkeyApiPaths.LOGS_EXPORT_API}/{export_id}",
            params=None,
            body=None,
            cast_to=LogsExportRetrieveResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def list(
        self,
        *,
        workspace_id: Optional[str] = None,
    ) -> LogsExportListResponse:
        query = {
            "workspace_id": workspace_id,
        }
        filtered_query = {k: v for k, v in query.items() if v is not None}
        query_string = urlencode(filtered_query)
        return self._get(
            f"{PortkeyApiPaths.LOGS_EXPORT_API}?{query_string}",
            params=None,
            body=None,
            cast_to=LogsExportListResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def update(
        self,
        *,
        export_id: Optional[str] = None,
        workspace_id: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
        requested_data: Optional[List[str]] = None,
    ) -> LogsExportUpdateResponse:
        body = {
            "workspace_id": workspace_id,
            "filters": filters,
            "requested_data": requested_data,
        }
        return self._put(
            f"{PortkeyApiPaths.LOGS_EXPORT_API}/{export_id}",
            body=body,
            params=None,
            cast_to=LogsExportUpdateResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def start(
        self,
        *,
        export_id: Optional[str],
    ) -> LogsExportStartResponse:
        return self._post(
            f"{PortkeyApiPaths.LOGS_EXPORT_API}/{export_id}/start",
            body=None,
            params=None,
            cast_to=LogsExportStartResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def cancel(
        self,
        *,
        export_id: Optional[str],
    ) -> LogsExportCancelResponse:
        return self._post(
            f"{PortkeyApiPaths.LOGS_EXPORT_API}/{export_id}/cancel",
            body=None,
            params=None,
            cast_to=LogsExportCancelResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def download(
        self,
        *,
        export_id: Optional[str],
    ) -> LogsExportDownloadResponse:
        return self._get(
            f"{PortkeyApiPaths.LOGS_EXPORT_API}/{export_id}/download",
            params=None,
            body=None,
            cast_to=LogsExportDownloadResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )


class AsyncLogs(AsyncAPIResource):
    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)
        self.exports = AsyncExports(client)

    async def create(
        self,
        *,
        request: Optional[Dict[str, Any]] = None,
        response: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Any:
        body = {
            "request": request,
            "response": response,
            "metadata": metadata,
        }
        return await self._post(
            f"{PortkeyApiPaths.LOGS_API}",
            body=body,
            params=None,
            cast_to=None,
            stream=False,
            stream_cls=None,
            headers={},
        )


class AsyncExports(AsyncAPIResource):
    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)

    async def create(
        self,
        *,
        filters: Optional[Dict[str, Any]] = None,
        workspace_id: Optional[str] = None,
        description: Optional[str] = None,
        requested_data: Optional[List[str]] = None,
    ) -> LogsExportCreateResponse:
        body = {
            "filters": filters,
            "workspace_id": workspace_id,
            "description": description,
            "requested_data": requested_data,
        }
        return await self._post(
            f"{PortkeyApiPaths.LOGS_EXPORT_API}",
            body=body,
            params=None,
            cast_to=LogsExportCreateResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def retrieve(self, *, export_id: str) -> LogsExportRetrieveResponse:
        return await self._get(
            f"{PortkeyApiPaths.LOGS_EXPORT_API}/{export_id}",
            params=None,
            body=None,
            cast_to=LogsExportRetrieveResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def list(
        self,
        *,
        workspace_id: Optional[str] = None,
    ) -> LogsExportListResponse:
        query = {
            "workspace_id": workspace_id,
        }
        filtered_query = {k: v for k, v in query.items() if v is not None}
        query_string = urlencode(filtered_query)
        return await self._get(
            f"{PortkeyApiPaths.LOGS_EXPORT_API}?{query_string}",
            params=None,
            body=None,
            cast_to=LogsExportListResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def update(
        self,
        *,
        export_id: Optional[str] = None,
        workspace_id: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
        requested_data: Optional[List[str]] = None,
    ) -> LogsExportUpdateResponse:
        body = {
            "workspace_id": workspace_id,
            "filters": filters,
            "requested_data": requested_data,
        }
        return await self._put(
            f"{PortkeyApiPaths.LOGS_EXPORT_API}/{export_id}",
            body=body,
            params=None,
            cast_to=LogsExportUpdateResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def start(
        self,
        *,
        export_id: Optional[str],
    ) -> LogsExportStartResponse:
        return await self._post(
            f"{PortkeyApiPaths.LOGS_EXPORT_API}/{export_id}/start",
            body=None,
            params=None,
            cast_to=LogsExportStartResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def cancel(
        self,
        *,
        export_id: Optional[str],
    ) -> LogsExportCancelResponse:
        return await self._post(
            f"{PortkeyApiPaths.LOGS_EXPORT_API}/{export_id}/cancel",
            body=None,
            params=None,
            cast_to=LogsExportCancelResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def download(
        self,
        *,
        export_id: Optional[str],
    ) -> LogsExportDownloadResponse:
        return await self._get(
            f"{PortkeyApiPaths.LOGS_EXPORT_API}/{export_id}/download",
            params=None,
            body=None,
            cast_to=LogsExportDownloadResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )
