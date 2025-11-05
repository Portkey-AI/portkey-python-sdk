from typing import Any, Dict, List, Optional, Union
from portkey_ai._vendor.openai import NOT_GIVEN, NotGiven
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
        workspace_id: Union[str, NotGiven] = NOT_GIVEN,
        organisation_id: Union[str, NotGiven] = NOT_GIVEN,
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
        workspace_id: Union[str, NotGiven] = NOT_GIVEN,
        organisation_id: Union[str, NotGiven] = NOT_GIVEN,
        page_size: Optional[int] = 100,
        current_page: Optional[int] = 0,
    ) -> GuardrailListResponse:
        query = {
            "workspace_id": workspace_id,
            "organisation_id": organisation_id,
            "page_size": page_size,
            "current_page": current_page,
        }
        filtered_query = {k: v for k, v in query.items() if v is not NOT_GIVEN}
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
        name: Union[str, NotGiven] = NOT_GIVEN,
        checks: Union[List[Dict[str, Any]], NotGiven] = NOT_GIVEN,
        actions: Union[Dict[str, Any], NotGiven] = NOT_GIVEN,
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
        workspace_id: Union[str, NotGiven] = NOT_GIVEN,
        organisation_id: Union[str, NotGiven] = NOT_GIVEN,
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
        workspace_id: Union[str, NotGiven] = NOT_GIVEN,
        organisation_id: Union[str, NotGiven] = NOT_GIVEN,
        page_size: Optional[int] = 100,
        current_page: Optional[int] = 0,
    ) -> GuardrailListResponse:
        query = {
            "workspace_id": workspace_id,
            "organisation_id": organisation_id,
            "page_size": page_size,
            "current_page": current_page,
        }
        filtered_query = {k: v for k, v in query.items() if v is not NOT_GIVEN}
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
        name: Union[str, NotGiven] = NOT_GIVEN,
        checks: Union[List[Dict[str, Any]], NotGiven] = NOT_GIVEN,
        actions: Union[Dict[str, Any], NotGiven] = NOT_GIVEN,
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
