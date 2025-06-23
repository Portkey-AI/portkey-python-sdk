from typing import Any, Dict, Optional
from portkey_ai.api_resources.base_client import APIClient, AsyncAPIClient
from urllib.parse import urlencode
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.utils import GenericResponse
from portkey_ai.api_resources.utils import PortkeyApiPaths


class Providers(APIResource):
    def __init__(self, client: APIClient) -> None:
        super().__init__(client)

    def create(
        self,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
        key: Optional[str] = None,
        ai_provider_id: Optional[str] = None,
        workspace_id: Optional[str] = None,
        slug: Optional[str] = None,
        organisation_id: Optional[str] = None,
        note: Optional[str] = None,
        configuration: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> GenericResponse:
        body = {
            "name": name,
            "description": description,
            "key": key,
            "ai_provider_id": ai_provider_id,
            "workspace_id": workspace_id,
            "slug": slug,
            "organisation_id": organisation_id,
            "note": note,
            "configuration": configuration,
            **kwargs,
        }
        return self._post(
            f"{PortkeyApiPaths.PROVIDERS_API}",
            body=body,
            params=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def list(
        self,
        *,
        organisation_id: Optional[str] = None,
        workspace_id: Optional[str] = None,
        current_page: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> GenericResponse:
        query = {
            "organisation_id": organisation_id,
            "workspace_id": workspace_id,
            "current_page": current_page,
            "page_size": page_size,
        }
        filtered_query = {k: v for k, v in query.items() if v is not None}
        query_string = urlencode(filtered_query)
        return self._get(
            f"{PortkeyApiPaths.PROVIDERS_API}?{query_string}",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def retrieve(self, *, integration_id: Optional[str]) -> Any:
        return self._get(
            f"{PortkeyApiPaths.PROVIDERS_API}/{integration_id}",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def update(
        self,
        *,
        integration_id: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        key: Optional[str] = None,
        configuration: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> GenericResponse:
        body = {
            "name": name,
            "description": description,
            "key": key,
            "configuration": configuration,
            **kwargs,
        }
        return self._put(
            f"{PortkeyApiPaths.PROVIDERS_API}/{integration_id}",
            body=body,
            params=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def delete(
        self,
        *,
        integration_id: Optional[str],
    ) -> Any:
        return self._delete(
            f"{PortkeyApiPaths.PROVIDERS_API}/{integration_id}",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )


class AsyncProviders(AsyncAPIResource):
    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)
