from typing import Any, Dict, List, Optional, Union
from portkey_ai._vendor.openai import NOT_GIVEN, NotGiven
from portkey_ai.api_resources.base_client import APIClient, AsyncAPIClient
from urllib.parse import urlencode
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.types.api_keys_type import (
    ApiKeyAddResponse,
    ApiKeyGetResponse,
    ApiKeyListResponse,
)
from portkey_ai.api_resources.utils import GenericResponse
from portkey_ai.api_resources.utils import PortkeyApiPaths


class ApiKeys(APIResource):
    def __init__(self, client: APIClient) -> None:
        super().__init__(client)

    def create(
        self,
        *,
        type: Union[str, NotGiven] = NOT_GIVEN,
        sub_type: Union[str, NotGiven] = NOT_GIVEN,
        name: Union[str, NotGiven] = NOT_GIVEN,
        description: Union[str, NotGiven] = NOT_GIVEN,
        workspace_id: Union[str, NotGiven] = NOT_GIVEN,
        user_id: Union[str, NotGiven] = NOT_GIVEN,
        rate_limits: Union[List[Dict[str, Any]], NotGiven] = NOT_GIVEN,
        usage_limits: Union[Dict[str, Any], NotGiven] = NOT_GIVEN,
        scopes: Union[List[str], NotGiven] = NOT_GIVEN,
        defaults: Union[Dict[str, Any], NotGiven] = NOT_GIVEN,
        expires_at: Union[Any, NotGiven] = NOT_GIVEN,
        **kwargs: Any,
    ) -> ApiKeyAddResponse:
        body = {
            "type": type,
            "sub-type": sub_type,
            "name": name,
            "description": description,
            "workspace_id": workspace_id,
            "user_id": user_id,
            "rate_limits": rate_limits,
            "usage_limits": usage_limits,
            "scopes": scopes,
            "defaults": defaults,
            "expires_at": expires_at,
            **kwargs,
        }
        return self._post(
            f"{PortkeyApiPaths.API_KEYS_API}/{type}/{sub_type}",
            body=body,
            params=None,
            cast_to=ApiKeyAddResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def retrieve(self, *, id: Optional[str]) -> ApiKeyGetResponse:
        return self._get(
            f"{PortkeyApiPaths.API_KEYS_API}/{id}",
            params=None,
            body=None,
            cast_to=ApiKeyGetResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def list(
        self,
        *,
        page_size: Union[int, str, NotGiven] = NOT_GIVEN,
        current_page: Optional[int] = 0,
        workspace_id: Union[str, NotGiven] = NOT_GIVEN,
    ) -> ApiKeyListResponse:
        query = {
            "page_size": page_size,
            "current_page": current_page,
            "workspace_id": workspace_id,
        }
        filtered_query = {k: v for k, v in query.items() if v is not NOT_GIVEN}
        query_string = urlencode(filtered_query)
        return self._get(
            f"{PortkeyApiPaths.API_KEYS_API}?{query_string}",
            params=None,
            body=None,
            cast_to=ApiKeyListResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def update(
        self,
        *,
        id: Union[str, NotGiven] = NOT_GIVEN,
        name: Union[str, NotGiven] = NOT_GIVEN,
        description: Union[str, NotGiven] = NOT_GIVEN,
        rate_limits: Union[List[Dict[str, Any]], NotGiven] = NOT_GIVEN,
        usage_limits: Union[Dict[str, Any], NotGiven] = NOT_GIVEN,
        scopes: Union[List[str], NotGiven] = NOT_GIVEN,
        defaults: Union[Dict[str, Any], NotGiven] = NOT_GIVEN,
        expires_at: Union[Any, NotGiven] = NOT_GIVEN,
        **kwargs: Any,
    ) -> Any:
        body = {
            "id": id,
            "name": name,
            "description": description,
            "rate_limits": rate_limits,
            "usage_limits": usage_limits,
            "scopes": scopes,
            "defaults": defaults,
            "expires_at": expires_at,
            **kwargs,
        }
        return self._put(
            f"{PortkeyApiPaths.API_KEYS_API}/{id}",
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
        id: Optional[str],
    ) -> Any:
        return self._delete(
            f"{PortkeyApiPaths.API_KEYS_API}/{id}",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )


class AsyncApiKeys(AsyncAPIResource):
    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)

    async def create(
        self,
        *,
        type: Union[str, NotGiven] = NOT_GIVEN,
        sub_type: Union[str, NotGiven] = NOT_GIVEN,
        name: Union[str, NotGiven] = NOT_GIVEN,
        description: Union[str, NotGiven] = NOT_GIVEN,
        workspace_id: Union[str, NotGiven] = NOT_GIVEN,
        user_id: Union[str, NotGiven] = NOT_GIVEN,
        rate_limits: Union[List[Dict[str, Any]], NotGiven] = NOT_GIVEN,
        usage_limits: Union[Dict[str, Any], NotGiven] = NOT_GIVEN,
        scopes: Union[List[str], NotGiven] = NOT_GIVEN,
        defaults: Union[Dict[str, Any], NotGiven] = NOT_GIVEN,
        expires_at: Union[Any, NotGiven] = NOT_GIVEN,
        **kwargs: Any,
    ) -> ApiKeyAddResponse:
        body = {
            "type": type,
            "sub-type": sub_type,
            "name": name,
            "description": description,
            "workspace_id": workspace_id,
            "user_id": user_id,
            "rate_limits": rate_limits,
            "usage_limits": usage_limits,
            "scopes": scopes,
            "defaults": defaults,
            "expires_at": expires_at,
            **kwargs,
        }
        return await self._post(
            f"{PortkeyApiPaths.API_KEYS_API}/{type}/{sub_type}",
            body=body,
            params=None,
            cast_to=ApiKeyAddResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def retrieve(self, *, id: Optional[str]) -> ApiKeyGetResponse:
        return await self._get(
            f"{PortkeyApiPaths.API_KEYS_API}/{id}",
            params=None,
            body=None,
            cast_to=ApiKeyGetResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def list(
        self,
        *,
        page_size: Union[int, str, NotGiven] = NOT_GIVEN,
        current_page: Optional[int] = 0,
        workspace_id: Union[str, NotGiven] = NOT_GIVEN,
    ) -> ApiKeyListResponse:
        query = {
            "page_size": page_size,
            "current_page": current_page,
            "workspace_id": workspace_id,
        }
        filtered_query = {k: v for k, v in query.items() if v is not NOT_GIVEN}
        query_string = urlencode(filtered_query)
        return await self._get(
            f"{PortkeyApiPaths.API_KEYS_API}?{query_string}",
            params=None,
            body=None,
            cast_to=ApiKeyListResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def update(
        self,
        *,
        id: Union[str, NotGiven] = NOT_GIVEN,
        name: Union[str, NotGiven] = NOT_GIVEN,
        description: Union[str, NotGiven] = NOT_GIVEN,
        rate_limits: Union[List[Dict[str, Any]], NotGiven] = NOT_GIVEN,
        usage_limits: Union[Dict[str, Any], NotGiven] = NOT_GIVEN,
        scopes: Union[List[str], NotGiven] = NOT_GIVEN,
        defaults: Union[Dict[str, Any], NotGiven] = NOT_GIVEN,
        expires_at: Union[Any, NotGiven] = NOT_GIVEN,
        **kwargs: Any,
    ) -> Any:
        body = {
            "id": id,
            "name": name,
            "description": description,
            "rate_limits": rate_limits,
            "usage_limits": usage_limits,
            "scopes": scopes,
            "defaults": defaults,
            "expires_at": expires_at,
            **kwargs,
        }
        return await self._put(
            f"{PortkeyApiPaths.API_KEYS_API}/{id}",
            body=body,
            params=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def delete(
        self,
        *,
        id: Optional[str],
    ) -> Any:
        return await self._delete(
            f"{PortkeyApiPaths.API_KEYS_API}/{id}",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )
