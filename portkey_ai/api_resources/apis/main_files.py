import json
from typing import Any, Union
import typing_extensions
from portkey_ai._vendor.openai._types import omit, Omit
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.client import AsyncPortkey, Portkey
from portkey_ai.api_resources.types.main_file_type import (
    FileDeleted,
    FileList,
    FileObject,
)


class MainFiles(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    def create(self, file, purpose, **kwargs) -> FileObject:
        extra_headers = kwargs.pop("extra_headers", {})
        response = self.openai_client.with_raw_response.files.create(
            file=file, purpose=purpose, extra_body=kwargs, extra_headers=extra_headers
        )
        data = FileObject(**json.loads(response.text))
        data._headers = response.headers

        return data

    def retrieve(self, file_id, **kwargs) -> FileObject:
        if kwargs:
            response = self.openai_client.with_raw_response.files.retrieve(
                file_id=file_id, extra_body=kwargs
            )
        else:
            response = self.openai_client.with_raw_response.files.retrieve(
                file_id=file_id
            )
        data = FileObject(**json.loads(response.text))
        data._headers = response.headers

        return data

    def list(
        self,
        *,
        purpose: Union[str, Omit] = omit,
        after: Union[str, Omit] = omit,
        limit: Union[int, Omit] = omit,
        order: Union[Any, Omit] = omit,
        **kwargs,
    ) -> FileList:
        response = self.openai_client.with_raw_response.files.list(
            purpose=purpose,
            after=after,
            limit=limit,
            order=order,
            **kwargs,
        )
        data = FileList(**json.loads(response.text))
        data._headers = response.headers

        return data

    def delete(self, file_id, **kwargs) -> FileDeleted:
        response = self.openai_client.with_raw_response.files.delete(
            file_id=file_id, extra_body=kwargs
        )
        data = FileDeleted(**json.loads(response.text))
        data._headers = response.headers

        return data

    def content(self, file_id, **kwargs) -> Any:
        if kwargs:
            response = self.openai_client.files.content(
                file_id=file_id, extra_body=kwargs
            )
        else:
            response = self.openai_client.files.content(file_id=file_id)
        return response

    @typing_extensions.deprecated("The `.content()` method should be used instead")
    def retrieve_content(self, file_id, **kwargs) -> Any:
        if kwargs:
            response = self.openai_client.files.content(
                file_id=file_id, extra_body=kwargs
            )
        else:
            response = self.openai_client.files.content(file_id=file_id)
        return response

    def wait_for_processing(
        self,
        id: str,
        *,
        poll_interval: float = 5.0,
        max_wait_seconds: float = 30 * 60,
    ) -> Any:
        response = self.openai_client.files.wait_for_processing(
            id=id,
            poll_interval=poll_interval,
            max_wait_seconds=max_wait_seconds,
        )
        return response


class AsyncMainFiles(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    async def create(self, file, purpose, **kwargs) -> FileObject:
        extra_headers = kwargs.pop("extra_headers", {})
        response = await self.openai_client.with_raw_response.files.create(
            file=file, purpose=purpose, extra_body=kwargs, extra_headers=extra_headers
        )
        data = FileObject(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def retrieve(self, file_id, **kwargs) -> FileObject:
        if kwargs:
            response = await self.openai_client.with_raw_response.files.retrieve(
                file_id=file_id, extra_body=kwargs
            )
        else:
            response = await self.openai_client.with_raw_response.files.retrieve(
                file_id=file_id
            )
        data = FileObject(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def list(
        self,
        *,
        purpose: Union[str, Omit] = omit,
        after: Union[str, Omit] = omit,
        limit: Union[int, Omit] = omit,
        order: Union[Any, Omit] = omit,
        **kwargs,
    ) -> FileList:
        response = await self.openai_client.with_raw_response.files.list(
            purpose=purpose,
            after=after,
            limit=limit,
            order=order,
            **kwargs,
        )
        data = FileList(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def delete(self, file_id, **kwargs) -> FileDeleted:
        response = await self.openai_client.with_raw_response.files.delete(
            file_id=file_id, extra_body=kwargs
        )
        data = FileDeleted(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def content(self, file_id, **kwargs) -> Any:
        if kwargs:
            response = await self.openai_client.files.content(
                file_id=file_id, extra_body=kwargs
            )
        else:
            response = await self.openai_client.files.content(file_id=file_id)
        return response

    @typing_extensions.deprecated("The `.content()` method should be used instead")
    async def retrieve_content(self, file_id, **kwargs) -> Any:
        if kwargs:
            response = await self.openai_client.files.content(
                file_id=file_id, extra_body=kwargs
            )
        else:
            response = await self.openai_client.files.content(file_id=file_id)
        return response

    async def wait_for_processing(
        self,
        id: str,
        *,
        poll_interval: float = 5.0,
        max_wait_seconds: float = 30 * 60,
    ) -> Any:
        response = await self.openai_client.files.wait_for_processing(
            id=id,
            poll_interval=poll_interval,
            max_wait_seconds=max_wait_seconds,
        )
        return response
