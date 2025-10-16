from typing import Any, Dict, List, Optional
from portkey_ai.api_resources.base_client import APIClient, AsyncAPIClient
from urllib.parse import urlencode
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.types.guardrails_type import (
    GuardrailListResponse,
    GuardrailDetailResponse,
    GuardrailCreateResponse,
    GuardrailUpdateResponse,
)
from portkey_ai.api_resources.utils import GenericResponse
from portkey_ai.api_resources.utils import PortkeyApiPaths


class Guardrails(APIResource):
    def __init__(self, client: APIClient) -> None:
        super().__init__(client)

    def create(
        self,
        *,
        name: str,
        checks: List[Dict[str, Any]],
        actions: Dict[str, Any],
        workspace_id: Optional[str] = None,
        organisation_id: Optional[str] = None,
        **kwargs: Any,
    ) -> GuardrailCreateResponse:
        body = {
            "name": name,
            "checks": checks,
            "actions": actions,
            "workspace_id": workspace_id,
            "organisation_id": organisation_id,
            **kwargs,
        }
        return self._post(
            f"{PortkeyApiPaths.GUARDRAILS_API}",
            body=body,
            params=None,
            cast_to=GuardrailCreateResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def list(
        self,
        *,
        workspace_id: Optional[str] = None,
        organisation_id: Optional[str] = None,
        page_size: Optional[int] = 100,
        current_page: Optional[int] = 0,
    ) -> GuardrailListResponse:
        query = {
            "workspace_id": workspace_id,
            "organisation_id": organisation_id,
            "page_size": page_size,
            "current_page": current_page,
        }
        filtered_query = {k: v for k, v in query.items() if v is not None}
        query_string = urlencode(filtered_query)
        return self._get(
            f"{PortkeyApiPaths.GUARDRAILS_API}?{query_string}",
            params=None,
            body=None,
            cast_to=GuardrailListResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def retrieve(
        self,
        *,
        guardrail_id: str,
    ) -> GuardrailDetailResponse:
        return self._get(
            f"{PortkeyApiPaths.GUARDRAILS_API}/{guardrail_id}",
            params=None,
            body=None,
            cast_to=GuardrailDetailResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def update(
        self,
        *,
        guardrail_id: str,
        name: Optional[str] = None,
        checks: Optional[List[Dict[str, Any]]] = None,
        actions: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> GuardrailUpdateResponse:
        body = {
            "name": name,
            "checks": checks,
            "actions": actions,
            **kwargs,
        }
        return self._put(
            f"{PortkeyApiPaths.GUARDRAILS_API}/{guardrail_id}",
            body=body,
            params=None,
            cast_to=GuardrailUpdateResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def delete(
        self,
        *,
        guardrail_id: str,
    ) -> GenericResponse:
        return self._delete(
            f"{PortkeyApiPaths.GUARDRAILS_API}/{guardrail_id}",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )


class AsyncGuardrails(AsyncAPIResource):
    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)

    async def create(
        self,
        *,
        name: str,
        checks: List[Dict[str, Any]],
        actions: Dict[str, Any],
        workspace_id: Optional[str] = None,
        organisation_id: Optional[str] = None,
        **kwargs: Any,
    ) -> GuardrailCreateResponse:
        body = {
            "name": name,
            "checks": checks,
            "actions": actions,
            "workspace_id": workspace_id,
            "organisation_id": organisation_id,
            **kwargs,
        }
        return await self._post(
            f"{PortkeyApiPaths.GUARDRAILS_API}",
            body=body,
            params=None,
            cast_to=GuardrailCreateResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def list(
        self,
        *,
        workspace_id: Optional[str] = None,
        organisation_id: Optional[str] = None,
        page_size: Optional[int] = 100,
        current_page: Optional[int] = 0,
    ) -> GuardrailListResponse:
        query = {
            "workspace_id": workspace_id,
            "organisation_id": organisation_id,
            "page_size": page_size,
            "current_page": current_page,
        }
        filtered_query = {k: v for k, v in query.items() if v is not None}
        query_string = urlencode(filtered_query)
        return await self._get(
            f"{PortkeyApiPaths.GUARDRAILS_API}?{query_string}",
            params=None,
            body=None,
            cast_to=GuardrailListResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def retrieve(
        self,
        *,
        guardrail_id: str,
    ) -> GuardrailDetailResponse:
        return await self._get(
            f"{PortkeyApiPaths.GUARDRAILS_API}/{guardrail_id}",
            params=None,
            body=None,
            cast_to=GuardrailDetailResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def update(
        self,
        *,
        guardrail_id: str,
        name: Optional[str] = None,
        checks: Optional[List[Dict[str, Any]]] = None,
        actions: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> GuardrailUpdateResponse:
        body = {
            "name": name,
            "checks": checks,
            "actions": actions,
            **kwargs,
        }
        return await self._put(
            f"{PortkeyApiPaths.GUARDRAILS_API}/{guardrail_id}",
            body=body,
            params=None,
            cast_to=GuardrailUpdateResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def delete(
        self,
        *,
        guardrail_id: str,
    ) -> GenericResponse:
        return await self._delete(
            f"{PortkeyApiPaths.GUARDRAILS_API}/{guardrail_id}",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )
