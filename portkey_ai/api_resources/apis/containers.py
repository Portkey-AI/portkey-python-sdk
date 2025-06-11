import json
from typing import List, Literal, Union
from portkey_ai._vendor.openai.types import container_create_params
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.client import AsyncPortkey, Portkey
from portkey_ai.api_resources.types.containers_type import (
    ContainerCreateResponse,
    ContainerListResponse,
    ContainerRetrieveResponse,
)
from ..._vendor.openai._types import NotGiven, NOT_GIVEN


class Containers(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        # self.files = ContainersFiles(client)

    def create(
        self,
        *,
        name: str,
        expires_after: Union[
            container_create_params.ExpiresAfter, NotGiven
        ] = NOT_GIVEN,
        file_ids: Union[List[str], NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> ContainerCreateResponse:
        response = self.openai_client.with_raw_response.containers.create(
            name=name,
            expires_after=expires_after,
            file_ids=file_ids,
            extra_body=kwargs,
        )
        data = ContainerCreateResponse(**json.loads(response.text))
        data._headers = response.headers

        return data

    def retrieve(
        self,
        container_id: str,
        **kwargs,
    ) -> ContainerRetrieveResponse:
        if kwargs:
            response = self.openai_client.with_raw_response.containers.retrieve(
                container_id=container_id,
                extra_body=kwargs,
            )
        else:
            response = self.openai_client.with_raw_response.containers.retrieve(
                container_id=container_id,
            )
        data = ContainerRetrieveResponse(**json.loads(response.text))
        data._headers = response.headers

        return data

    def list(
        self,
        *,
        after: Union[str, NotGiven] = NOT_GIVEN,
        limit: Union[int, NotGiven] = NOT_GIVEN,
        order: Union[Literal["asc", "desc"], NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> ContainerListResponse:
        response = self.openai_client.with_raw_response.containers.list(
            after=after,
            limit=limit,
            order=order,
            **kwargs,
        )
        data = ContainerListResponse(**json.loads(response.text))
        data._headers = response.headers

        return data

    def delete(
        self,
        container_id: str,
        **kwargs,
    ) -> None:
        return self.openai_client.containers.delete(
            container_id=container_id,
            extra_body=kwargs,
        )


class AsyncContainers(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        # self.files = AsyncContainersFiles(client)

    async def create(
        self,
        *,
        name: str,
        expires_after: Union[
            container_create_params.ExpiresAfter, NotGiven
        ] = NOT_GIVEN,
        file_ids: Union[List[str], NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> ContainerCreateResponse:
        response = await self.openai_client.with_raw_response.containers.create(
            name=name,
            expires_after=expires_after,
            file_ids=file_ids,
            extra_body=kwargs,
        )
        data = ContainerCreateResponse(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def retrieve(
        self,
        container_id: str,
        **kwargs,
    ) -> ContainerRetrieveResponse:
        if kwargs:
            response = await self.openai_client.with_raw_response.containers.retrieve(
                container_id=container_id,
                extra_body=kwargs,
            )
        else:
            response = await self.openai_client.with_raw_response.containers.retrieve(
                container_id=container_id,
            )
        data = ContainerRetrieveResponse(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def list(
        self,
        *,
        after: Union[str, NotGiven] = NOT_GIVEN,
        limit: Union[int, NotGiven] = NOT_GIVEN,
        order: Union[Literal["asc", "desc"], NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> ContainerListResponse:
        response = await self.openai_client.with_raw_response.containers.list(
            after=after,
            limit=limit,
            order=order,
            **kwargs,
        )
        data = ContainerListResponse(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def delete(
        self,
        container_id: str,
        **kwargs,
    ) -> None:
        return await self.openai_client.containers.delete(
            container_id=container_id,
            extra_body=kwargs,
        )
