from typing import Any, Dict, Optional, Union
from portkey_ai._vendor.openai import NOT_GIVEN, NotGiven
from portkey_ai.api_resources.base_client import APIClient, AsyncAPIClient
from urllib.parse import urlencode
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.types.configs_type import (
    ConfigAddResponse,
    ConfigGetResponse,
    ConfigListResponse,
    ConfigUpdateResponse,
)
from portkey_ai.api_resources.utils import GenericResponse
from portkey_ai.api_resources.utils import PortkeyApiPaths


class Configs(APIResource):
    def __init__(self, client: APIClient) -> None:
        super().__init__(client)

    def create(
        self,
        *,
        name: Union[str, NotGiven] = NOT_GIVEN,
        config: Union[Dict[str, Any], NotGiven] = NOT_GIVEN,
        is_default: Union[int, NotGiven] = NOT_GIVEN,
        workspace_id: Union[str, NotGiven] = NOT_GIVEN,
    ) -> ConfigAddResponse:
        body = {
            "name": name,
            "config": config,
            "is_default": is_default,
            "workspace_id": workspace_id,
        }
        return self._post(
            f"{PortkeyApiPaths.CONFIG_API}",
            body=body,
            params=None,
            cast_to=ConfigAddResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def retrieve(self, *, slug: Optional[str]) -> ConfigGetResponse:
        return self._get(
            f"{PortkeyApiPaths.CONFIG_API}/{slug}",
            params=None,
            body=None,
            cast_to=ConfigGetResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def list(
        self,
        *,
        workspace_id: Union[str, NotGiven] = NOT_GIVEN,
    ) -> ConfigListResponse:
        query = {
            "workspace_id": workspace_id,
        }
        filtered_query = {k: v for k, v in query.items() if v is not NOT_GIVEN}
        query_string = urlencode(filtered_query)
        return self._get(
            f"{PortkeyApiPaths.CONFIG_API}?{query_string}",
            params=None,
            body=None,
            cast_to=ConfigListResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def update(
        self,
        *,
        slug: Union[str, NotGiven] = NOT_GIVEN,
        name: Union[str, NotGiven] = NOT_GIVEN,
        config: Union[Dict[str, Any], NotGiven] = NOT_GIVEN,
        status: Union[str, NotGiven] = NOT_GIVEN,
    ) -> ConfigUpdateResponse:
        body = {
            "slug": slug,
            "name": name,
            "config": config,
            "status": status,
        }
        return self._put(
            f"{PortkeyApiPaths.CONFIG_API}/{slug}",
            body=body,
            params=None,
            cast_to=ConfigUpdateResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    def delete(
        self,
        *,
        id: Union[str, NotGiven] = NOT_GIVEN,
        slug: Union[str, NotGiven] = NOT_GIVEN,
    ) -> Any:
        config_slug = None
        if id:
            import warnings

            warnings.warn(
                """You are using 'id' to delete a config.
This will be deprecated in the future.
Please use 'slug' instead.""",
                DeprecationWarning,
                stacklevel=2,
            )
            config_slug = id
        elif slug:
            config_slug = slug
        return self._delete(
            f"{PortkeyApiPaths.CONFIG_API}/{config_slug}",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )


class AsyncConfigs(AsyncAPIResource):
    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)

    async def create(
        self,
        *,
        name: Union[str, NotGiven] = NOT_GIVEN,
        config: Union[Dict[str, Any], NotGiven] = NOT_GIVEN,
        is_default: Union[int, NotGiven] = NOT_GIVEN,
        workspace_id: Union[str, NotGiven] = NOT_GIVEN,
    ) -> ConfigAddResponse:
        body = {
            "name": name,
            "config": config,
            "is_default": is_default,
            "workspace_id": workspace_id,
        }
        return await self._post(
            f"{PortkeyApiPaths.CONFIG_API}",
            body=body,
            params=None,
            cast_to=ConfigAddResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def retrieve(self, *, slug: Optional[str]) -> ConfigGetResponse:
        return await self._get(
            f"{PortkeyApiPaths.CONFIG_API}/{slug}",
            params=None,
            body=None,
            cast_to=ConfigGetResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def list(
        self,
        *,
        workspace_id: Union[str, NotGiven] = NOT_GIVEN,
    ) -> ConfigListResponse:
        query = {
            "workspace_id": workspace_id,
        }
        filtered_query = {k: v for k, v in query.items() if v is not NOT_GIVEN}
        query_string = urlencode(filtered_query)
        return await self._get(
            f"{PortkeyApiPaths.CONFIG_API}?{query_string}",
            params=None,
            body=None,
            cast_to=ConfigListResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def update(
        self,
        *,
        slug: Union[str, NotGiven] = NOT_GIVEN,
        name: Union[str, NotGiven] = NOT_GIVEN,
        config: Union[Dict[str, Any], NotGiven] = NOT_GIVEN,
        status: Union[str, NotGiven] = NOT_GIVEN,
    ) -> ConfigUpdateResponse:
        body = {
            "slug": slug,
            "name": name,
            "config": config,
            "status": status,
        }
        return await self._put(
            f"{PortkeyApiPaths.CONFIG_API}/{slug}",
            body=body,
            params=None,
            cast_to=ConfigUpdateResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )

    async def delete(
        self,
        *,
        id: Union[str, NotGiven] = NOT_GIVEN,
        slug: Union[str, NotGiven] = NOT_GIVEN,
    ) -> Any:
        config_slug = None
        if id:
            import warnings

            warnings.warn(
                """You are using 'id' to delete a config.
This will be deprecated in the future.
Please use 'slug' instead.""",
                DeprecationWarning,
                stacklevel=2,
            )
            config_slug = id
        elif slug:
            config_slug = slug
        return await self._delete(
            f"{PortkeyApiPaths.CONFIG_API}/{config_slug}",
            params=None,
            body=None,
            cast_to=GenericResponse,
            stream=False,
            stream_cls=None,
            headers={},
        )
