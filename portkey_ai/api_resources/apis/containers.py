import json
from typing import Any, List, Literal, Union
from portkey_ai._vendor.openai.types import container_create_params
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.client import AsyncPortkey, Portkey
from portkey_ai.api_resources.types.container_files_types import (
    FileCreateResponse,
    FileListResponse,
    FileRetrieveResponse,
)
from portkey_ai.api_resources.types.containers_type import (
    ContainerCreateResponse,
    ContainerListResponse,
    ContainerRetrieveResponse,
)
from ..._vendor.openai._types import FileTypes, Omit, omit


class Containers(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.files = ContainersFiles(client)

    def create(
        self,
        *,
        name: str,
        expires_after: Union[container_create_params.ExpiresAfter, Omit] = omit,
        file_ids: Union[List[str], Omit] = omit,
        **kwargs,
    ) -> ContainerCreateResponse:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)
        response = self.openai_client.with_raw_response.containers.create(
            name=name,
            expires_after=expires_after,
            file_ids=file_ids,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        data = ContainerCreateResponse(**json.loads(response.text))
        data._headers = response.headers

        return data

    def retrieve(
        self,
        container_id: str,
        **kwargs,
    ) -> ContainerRetrieveResponse:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)
        if kwargs:
            response = self.openai_client.with_raw_response.containers.retrieve(
                container_id=container_id,
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            )
        else:
            response = self.openai_client.with_raw_response.containers.retrieve(
                container_id=container_id,
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            )
        data = ContainerRetrieveResponse(**json.loads(response.text))
        data._headers = response.headers

        return data

    def list(
        self,
        *,
        after: Union[str, Omit] = omit,
        limit: Union[int, Omit] = omit,
        order: Union[Literal["asc", "desc"], Omit] = omit,
        **kwargs,
    ) -> ContainerListResponse:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)
        response = self.openai_client.with_raw_response.containers.list(
            after=after,
            limit=limit,
            order=order,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        data = ContainerListResponse(**json.loads(response.text))
        data._headers = response.headers

        return data

    def delete(
        self,
        container_id: str,
        **kwargs,
    ) -> None:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)
        return self.openai_client.containers.delete(
            container_id=container_id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )


class ContainersFiles(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.content = Content(client)

    def create(
        self,
        container_id: str,
        *,
        file: Union[FileTypes, Omit] = omit,
        file_id: Union[str, Omit] = omit,
        **kwargs,
    ) -> FileCreateResponse:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)
        response = self.openai_client.with_raw_response.containers.files.create(
            container_id=container_id,
            file=file,
            file_id=file_id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        data = FileCreateResponse(**json.loads(response.text))
        data._headers = response.headers

        return data

    def retrieve(
        self,
        file_id: str,
        *,
        container_id: str,
        **kwargs,
    ) -> FileRetrieveResponse:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)
        if kwargs:
            response = self.openai_client.with_raw_response.containers.files.retrieve(
                file_id=file_id,
                container_id=container_id,
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            )
        else:
            response = self.openai_client.with_raw_response.containers.files.retrieve(
                file_id=file_id,
                container_id=container_id,
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            )
        data = FileRetrieveResponse(**json.loads(response.text))
        data._headers = response.headers

        return data

    def list(
        self,
        container_id: str,
        *,
        after: Union[str, Omit] = omit,
        limit: Union[int, Omit] = omit,
        order: Union[Literal["asc", "desc"], Omit] = omit,
        **kwargs,
    ) -> FileListResponse:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)
        response = self.openai_client.with_raw_response.containers.files.list(
            container_id=container_id,
            after=after,
            limit=limit,
            order=order,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        data = FileListResponse(**json.loads(response.text))
        data._headers = response.headers

        return data

    def delete(
        self,
        file_id: str,
        *,
        container_id: str,
        **kwargs,
    ) -> None:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)
        return self.openai_client.containers.files.delete(
            file_id=file_id,
            container_id=container_id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )


class Content(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    def retrieve(
        self,
        file_id: str,
        *,
        container_id: str,
        **kwargs,
    ) -> Any:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)
        if kwargs:
            response = self.openai_client.containers.files.content.retrieve(
                file_id=file_id,
                container_id=container_id,
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            )
        else:
            response = self.openai_client.containers.files.content.retrieve(
                file_id=file_id,
                container_id=container_id,
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            )
        return response


class AsyncContainers(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.files = AsyncContainersFiles(client)

    async def create(
        self,
        *,
        name: str,
        expires_after: Union[container_create_params.ExpiresAfter, Omit] = omit,
        file_ids: Union[List[str], Omit] = omit,
        **kwargs,
    ) -> ContainerCreateResponse:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)
        response = await self.openai_client.with_raw_response.containers.create(
            name=name,
            expires_after=expires_after,
            file_ids=file_ids,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        data = ContainerCreateResponse(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def retrieve(
        self,
        container_id: str,
        **kwargs,
    ) -> ContainerRetrieveResponse:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)
        if kwargs:
            response = await self.openai_client.with_raw_response.containers.retrieve(
                container_id=container_id,
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            )
        else:
            response = await self.openai_client.with_raw_response.containers.retrieve(
                container_id=container_id,
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            )
        data = ContainerRetrieveResponse(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def list(
        self,
        *,
        after: Union[str, Omit] = omit,
        limit: Union[int, Omit] = omit,
        order: Union[Literal["asc", "desc"], Omit] = omit,
        **kwargs,
    ) -> ContainerListResponse:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)
        response = await self.openai_client.with_raw_response.containers.list(
            after=after,
            limit=limit,
            order=order,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        data = ContainerListResponse(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def delete(
        self,
        container_id: str,
        **kwargs,
    ) -> None:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)
        return await self.openai_client.containers.delete(
            container_id=container_id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )


class AsyncContainersFiles(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.content = AsyncContent(client)

    async def create(
        self,
        container_id: str,
        *,
        file: Union[FileTypes, Omit] = omit,
        file_id: Union[str, Omit] = omit,
        **kwargs,
    ) -> FileCreateResponse:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)
        response = await self.openai_client.with_raw_response.containers.files.create(
            container_id=container_id,
            file=file,
            file_id=file_id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        data = FileCreateResponse(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def retrieve(
        self,
        file_id: str,
        *,
        container_id: str,
        **kwargs,
    ) -> FileRetrieveResponse:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)
        if kwargs:
            response = (
                await self.openai_client.with_raw_response.containers.files.retrieve(
                    file_id=file_id,
                    container_id=container_id,
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                )
            )
        else:
            response = (
                await self.openai_client.with_raw_response.containers.files.retrieve(
                    file_id=file_id,
                    container_id=container_id,
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                )
            )
        data = FileRetrieveResponse(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def list(
        self,
        container_id: str,
        *,
        after: Union[str, Omit] = omit,
        limit: Union[int, Omit] = omit,
        order: Union[Literal["asc", "desc"], Omit] = omit,
        **kwargs,
    ) -> FileListResponse:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)
        response = await self.openai_client.with_raw_response.containers.files.list(
            container_id=container_id,
            after=after,
            limit=limit,
            order=order,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        data = FileListResponse(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def delete(
        self,
        file_id: str,
        *,
        container_id: str,
        **kwargs,
    ) -> None:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)
        return await self.openai_client.containers.files.delete(
            file_id=file_id,
            container_id=container_id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )


class AsyncContent(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    async def retrieve(
        self,
        file_id: str,
        *,
        container_id: str,
        **kwargs,
    ) -> Any:
        extra_headers = kwargs.pop("extra_headers", None)
        extra_query = kwargs.pop("extra_query", None)
        extra_body = kwargs.pop("extra_body", None)
        timeout = kwargs.pop("timeout", None)
        if kwargs:
            response = await self.openai_client.containers.files.content.retrieve(
                file_id=file_id,
                container_id=container_id,
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            )
        else:
            response = await self.openai_client.containers.files.content.retrieve(
                file_id=file_id,
                container_id=container_id,
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            )
        return response
