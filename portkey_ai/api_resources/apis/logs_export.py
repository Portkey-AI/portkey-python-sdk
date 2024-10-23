from typing import Any, Dict, List, Optional
from portkey_ai.api_resources.base_client import APIClient, AsyncAPIClient
from urllib.parse import urlencode
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.types.logs_export_type import (
    LogsExportCreateResponse,
    LogsExportListResponse,
    LogsExportUpdateResponse,
    LogsExportCancelResponse,
    LogsExportRetrieveResponse,
    LogsExportStartResponse,
    LogsExportDownloadResponse,
)
from portkey_ai.api_resources.utils import GenericResponse
from portkey_ai.api_resources.utils import PortkeyApiPaths


class LogsExport(APIResource):
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

    def retrieve(self, *, exportId: str) -> LogsExportRetrieveResponse:
        return self._get(
            f"{PortkeyApiPaths.LOGS_EXPORT_API}/{exportId}",
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
        exportId: Optional[str] = None,
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
            f"{PortkeyApiPaths.LOGS_EXPORT_API}/{exportId}",
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
        exportId: Optional[str],
    ) -> LogsExportStartResponse:
        return self._post(
            f"{PortkeyApiPaths.LOGS_EXPORT_API}/{exportId}/start",
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
        exportId: Optional[str],
    ) -> LogsExportCancelResponse:
        return self._post(
            f"{PortkeyApiPaths.LOGS_EXPORT_API}/{exportId}/cancel",
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
        exportId: Optional[str],
    ) -> LogsExportDownloadResponse:
        return self._get(
            f"{PortkeyApiPaths.LOGS_EXPORT_API}/{exportId}/download",
            params=None,
            body=None,
            cast_to=LogsExportDownloadResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )


class AsyncLogsExport(AsyncAPIResource):
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

    async def retrieve(self, *, exportId: str) -> LogsExportRetrieveResponse:
        return await self._get(
            f"{PortkeyApiPaths.LOGS_EXPORT_API}/{exportId}",
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
        exportId: Optional[str] = None,
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
            f"{PortkeyApiPaths.LOGS_EXPORT_API}/{exportId}",
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
        exportId: Optional[str],
    ) -> LogsExportStartResponse:
        return await self._post(
            f"{PortkeyApiPaths.LOGS_EXPORT_API}/{exportId}/start",
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
        exportId: Optional[str],
    ) -> LogsExportCancelResponse:
        return await self._post(
            f"{PortkeyApiPaths.LOGS_EXPORT_API}/{exportId}/cancel",
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
        exportId: Optional[str],
    ) -> LogsExportDownloadResponse:
        return await self._get(
            f"{PortkeyApiPaths.LOGS_EXPORT_API}/{exportId}/download",
            params=None,
            body=None,
            cast_to=LogsExportDownloadResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )