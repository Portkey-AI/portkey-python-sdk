import json
from typing import Any
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
        response = self.openai_client.with_raw_response.files.create(
            file=file, purpose=purpose, **kwargs
        )
        data = FileObject(**json.loads(response.text))
        data._headers = response.headers

        return data

    def list(self, **kwargs) -> FileList:
        response = self.openai_client.with_raw_response.files.list(**kwargs)
        data = FileList(**json.loads(response.text))
        data._headers = response.headers

        return data

    def retrieve(self, file_id, **kwargs) -> FileObject:
        response = self.openai_client.with_raw_response.files.retrieve(
            file_id=file_id, **kwargs
        )
        data = FileObject(**json.loads(response.text))
        data._headers = response.headers

        return data

    def delete(self, file_id, **kwargs) -> FileDeleted:
        response = self.openai_client.with_raw_response.files.delete(
            file_id=file_id, **kwargs
        )
        data = FileDeleted(**json.loads(response.text))
        data._headers = response.headers

        return data

    def content(self, file_id, **kwargs) -> Any:
        response = self.openai_client.files.content(file_id=file_id, **kwargs)
        return response

    def retrieve_content(self, file_id, **kwargs) -> Any:
        response = self.openai_client.files.content(file_id=file_id, **kwargs)
        return response

    def wait_for_processing(
        self,
        id: str,
        *,
        polling_interval: float = 5.0,
        max_wait_seconds: float = 30 * 60,
        **kwargs
    ) -> Any:
        response = self.openai_client.files.wait_for_processing(
            id=id,
            polling_interval=polling_interval,
            max_wait_seconds=max_wait_seconds,
            **kwargs
        )
        return response


class AsyncMainFiles(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    async def create(self, file, purpose, **kwargs) -> FileObject:
        response = await self.openai_client.with_raw_response.files.create(
            file=file, purpose=purpose, **kwargs
        )
        data = FileObject(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def list(self, **kwargs) -> FileList:
        response = await self.openai_client.with_raw_response.files.list(**kwargs)
        data = FileList(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def retrieve(self, file_id, **kwargs) -> FileObject:
        response = await self.openai_client.with_raw_response.files.retrieve(
            file_id=file_id, **kwargs
        )
        data = FileObject(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def delete(self, file_id, **kwargs) -> FileDeleted:
        response = await self.openai_client.with_raw_response.files.delete(
            file_id=file_id, **kwargs
        )
        data = FileDeleted(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def content(self, file_id, **kwargs) -> Any:
        response = await self.openai_client.files.content(file_id=file_id, **kwargs)
        return response

    async def retrieve_content(self, file_id, **kwargs) -> Any:
        response = await self.openai_client.files.content(file_id=file_id, **kwargs)
        return response

    async def wait_for_processing(
        self,
        id: str,
        *,
        polling_interval: float = 5.0,
        max_wait_seconds: float = 30 * 60,
        **kwargs
    ) -> Any:
        response = await self.openai_client.files.wait_for_processing(
            id=id,
            polling_interval=polling_interval,
            max_wait_seconds=max_wait_seconds,
            **kwargs
        )
        return response
