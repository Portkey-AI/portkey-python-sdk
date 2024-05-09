from typing import Iterable, List, Optional, Union
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.client import AsyncPortkey, Portkey
from openai._types import NotGiven, NOT_GIVEN, FileTypes
from openai.types.beta import (
    vector_store_create_params,
    vector_store_update_params,
)

from portkey_ai.api_resources.types.vector_stores_type import (
    VectorStore,
    VectorStoreDeleted,
    VectorStoreFile,
    VectorStoreFileBatch,
    VectorStoreFileDeleted,
    VectorStoreFileList,
    VectorStoreList,
)


class VectorStores(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.files = VectorFiles(client)
        self.file_batches = VectorFileBatches(client)

    def create(
        self,
        *,
        expires_after: Union[
            vector_store_create_params.ExpiresAfter, NotGiven
        ] = NOT_GIVEN,
        file_ids: Union[List[str], NotGiven] = NOT_GIVEN,
        metadata: Union[Optional[object], NotGiven] = NOT_GIVEN,
        name: Union[str, NotGiven] = NOT_GIVEN,
    ) -> VectorStore:
        response = self.openai_client.with_raw_response.beta.vector_stores.create(
            expires_after=expires_after,
            file_ids=file_ids,
            metadata=metadata,
            name=name,
        )
        data = VectorStore(**json.loads(response.text))
        data._headers = response.headers

        return data

    def retrieve(
        self,
        vector_store_id: str,
        **kwargs,
    ) -> VectorStore:
        response = self.openai_client.with_raw_response.beta.vector_stores.retrieve(
            vector_store_id=vector_store_id,
            **kwargs,
        )
        data = VectorStore(**json.loads(response.text))
        data._headers = response.headers

        return data

    def update(
        self,
        vector_store_id: str,
        *,
        expires_after: Union[
            vector_store_update_params.ExpiresAfter, NotGiven
        ] = NOT_GIVEN,
        metadata: Union[Optional[object], NotGiven] = NOT_GIVEN,
        name: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> VectorStore:
        response = self.openai_client.with_raw_response.beta.vector_stores.update(
            vector_store_id=vector_store_id,
            expires_after=expires_after,
            metadata=metadata,
            name=name,
            **kwargs,
        )
        data = VectorStore(**json.loads(response.text))
        data._headers = response.headers

        return data

    def list(
        self,
        *,
        after: Union[str, NotGiven] = NOT_GIVEN,
        limit: Union[int, NotGiven] = NOT_GIVEN,
        order: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> VectorStoreList:
        response = self.openai_client.with_raw_response.beta.vector_stores.list(
            after=after,
            limit=limit,
            order=order,
            **kwargs,
        )
        data = VectorStoreList(**json.loads(response.text))
        data._headers = response.headers

        return data

    def delete(
        self,
        vector_store_id: str,
        **kwargs,
    ) -> VectorStoreDeleted:
        response = self.openai_client.with_raw_response.beta.vector_stores.delete(
            vector_store_id=vector_store_id,
            **kwargs,
        )
        data = VectorStoreDeleted(**json.loads(response.text))
        data._headers = response.headers

        return data


class VectorFiles(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    def create(
        self,
        vector_store_id: str,
        *,
        file_id: str,
        **kwargs,
    ) -> VectorStoreFile:
        response = self.openai_client.with_raw_response.beta.vector_stores.files.create(
            vector_store_id=vector_store_id,
            file_id=file_id,
            **kwargs,
        )
        data = VectorStoreFile(**json.loads(response.text))
        data._headers = response.headers

        return data

    def retrieve(
        self,
        file_id: str,
        *,
        vector_store_id: str,
        **kwargs,
    ) -> VectorStoreFile:
        response = (
            self.openai_client.with_raw_response.beta.vector_stores.files.retrieve(
                file_id=file_id,
                vector_store_id=vector_store_id,
                **kwargs,
            )
        )
        data = VectorStoreFile(**json.loads(response.text))
        data._headers = response.headers

        return data

    def list(
        self,
        vector_store_id: str,
        *,
        after: Union[str, NotGiven] = NOT_GIVEN,
        before: Union[str, NotGiven] = NOT_GIVEN,
        filter: Union[str, NotGiven] = NOT_GIVEN,
        limit: Union[int, NotGiven] = NOT_GIVEN,
        order: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> VectorStoreFileList:
        response = self.openai_client.with_raw_response.beta.vector_stores.files.list(
            vector_store_id=vector_store_id,
            after=after,
            before=before,
            filter=filter,
            limit=limit,
            order=order,
            **kwargs,
        )
        data = VectorStoreFileList(**json.loads(response.text))
        data._headers = response.headers

        return data

    def delete(
        self,
        file_id: str,
        *,
        vector_store_id: str,
        **kwargs,
    ) -> VectorStoreFileDeleted:
        response = self.openai_client.with_raw_response.beta.vector_stores.files.delete(
            file_id=file_id,
            vector_store_id=vector_store_id,
            **kwargs,
        )
        data = VectorStoreFileDeleted(**json.loads(response.text))
        data._headers = response.headers

        return data

    def create_and_poll(
        self,
        file_id: str,
        *,
        vector_store_id: str,
        poll_interval: Union[int, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> VectorStoreFile:
        response = self.openai_client.beta.vector_stores.files.create_and_poll(
            file_id=file_id,
            vector_store_id=vector_store_id,
            poll_interval=poll_interval,
            **kwargs,
        )
        data = response

        return data

    def poll(
        self,
        file_id: str,
        *,
        vector_store_id: str,
        poll_interval: Union[int, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> VectorStoreFile:
        response = self.openai_client.beta.vector_stores.files.poll(
            file_id=file_id,
            vector_store_id=vector_store_id,
            poll_interval=poll_interval,
            **kwargs,
        )
        data = response

        return data

    def upload(
        self,
        *,
        vector_store_id: str,
        file: FileTypes,
        **kwargs,
    ) -> VectorStoreFile:
        response = self.openai_client.beta.vector_stores.files.upload(
            vector_store_id=vector_store_id,
            file=file,
            **kwargs,
        )
        data = response
        return data
    
    def upload_and_poll(
        self,
        *,
        vector_store_id: str,
        file: FileTypes,
        poll_interval: Union[int, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> VectorStoreFile:
        response = self.openai_client.beta.vector_stores.files.upload_and_poll(
            vector_store_id=vector_store_id,
            file=file,
            poll_interval=poll_interval,
            **kwargs,
        )
        data = response
        return data


class VectorFileBatches(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    def create(
        self,
        vector_store_id: str,
        *,
        file_ids: List[str],
        **kwargs,
    ) -> VectorStoreFileBatch:
        response = self.openai_client.with_raw_response.beta.vector_stores.file_batches.create(
            vector_store_id=vector_store_id,
            file_ids=file_ids,
            **kwargs,
        )
        data = VectorStoreFileBatch(**json.loads(response.text))
        data._headers = response.headers

        return data
    
    def retrieve(
        self,
        batch_id:str,
        *,
        vector_store_id: str,
        **kwargs
    ) -> VectorStoreFileBatch:
        response = self.openai_client.with_raw_response.beta.vector_stores.file_batches.retrieve(
            batch_id=batch_id,
            vector_store_id=vector_store_id,
            **kwargs,
        )
        data = VectorStoreFileBatch(**json.loads(response.text))
        data._headers = response.headers

        return data 
    
    def cancel(
        self,
        batch_id:str,
        *,
        vector_store_id: str,
        **kwargs
    ) -> VectorStoreFileBatch:
        response = self.openai_client.with_raw_response.beta.vector_stores.file_batches.cancel(
            batch_id=batch_id,
            vector_store_id=vector_store_id,
            **kwargs,
        )
        data = VectorStoreFileBatch(**json.loads(response.text))
        data._headers = response.headers

        return data
    
    def create_and_poll(
            self,
            vector_store_id: str,
            *,
            file_ids: List[str],
            poll_interval: Union[int, NotGiven] = NOT_GIVEN,
            **kwargs,
    )-> VectorStoreFileBatch:
        response = self.openai_client.beta.vector_stores.file_batches.create_and_poll(
            vector_store_id=vector_store_id,
            file_ids=file_ids,
            poll_interval=poll_interval,
            **kwargs,
        )
        data = response
        return data
    
    def list_files(
        self,
        batch_id: str,
        *,
        vector_store_id: str,
        after: Union[str, NotGiven] = NOT_GIVEN,
        before: Union[str, NotGiven] = NOT_GIVEN,
        filter: Union[str, NotGiven] = NOT_GIVEN,
        limit: Union[int, NotGiven] = NOT_GIVEN,
        order: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> VectorStoreFileList:
        response = self.openai_client.with_raw_response.beta.vector_stores.file_batches.list_files(
            batch_id=batch_id,
            vector_store_id=vector_store_id,
            after=after,
            before=before,
            filter=filter,
            limit=limit,
            order=order,
            **kwargs,
        )
        data = VectorStoreFileBatch(**json.loads(response.text))
        data._headers = response.headers

        return data
    
    def poll(
        self,
        batch_id: str,
        *,
        vector_store_id: str,
        poll_interval: Union[int, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> VectorStoreFileBatch:
        response = self.openai_client.beta.vector_stores.file_batches.poll(
            batch_id=batch_id,
            vector_store_id=vector_store_id,
            poll_interval=poll_interval,
            **kwargs,
        )
        data = response

        return data
    
    def upload_and_poll(
        self,
        vector_store_id: str,
        *,
        files: Iterable[FileTypes],
        max_concurrency: int = 5,
        file_ids: List[str] = [],
        poll_interval_ms: Union[int, NotGiven] = NOT_GIVEN,
        **kwargs
    ) -> VectorStoreFileBatch:
        response = self.openai_client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store_id,
            files=files,
            max_concurrency=max_concurrency,
            file_ids=file_ids,
            poll_interval_ms=poll_interval_ms,
            **kwargs,
        )
        data = response

        return data


class AsyncVectorStores(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.files = AsyncVectorFiles(client)
        self.file_batches = AsyncVectorFileBatches(client)

    async def create(
        self,
        *,
        expires_after: Union[
            vector_store_create_params.ExpiresAfter, NotGiven
        ] = NOT_GIVEN,
        file_ids: Union[List[str], NotGiven] = NOT_GIVEN,
        metadata: Union[Optional[object], NotGiven] = NOT_GIVEN,
        name: Union[str, NotGiven] = NOT_GIVEN,
    ) -> VectorStore:
        response = await self.openai_client.with_raw_response.beta.vector_stores.create(
            expires_after=expires_after,
            file_ids=file_ids,
            metadata=metadata,
            name=name,
        )
        data = VectorStore(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def retrieve(
        self,
        vector_store_id: str,
        **kwargs,
    ) -> VectorStore:
        response = (
            await self.openai_client.with_raw_response.beta.vector_stores.retrieve(
                vector_store_id=vector_store_id,
                **kwargs,
            )
        )
        data = VectorStore(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def update(
        self,
        vector_store_id: str,
        *,
        expires_after: Union[
            vector_store_update_params.ExpiresAfter, NotGiven
        ] = NOT_GIVEN,
        metadata: Union[Optional[object], NotGiven] = NOT_GIVEN,
        name: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> VectorStore:
        response = await self.openai_client.with_raw_response.beta.vector_stores.update(
            vector_store_id=vector_store_id,
            expires_after=expires_after,
            metadata=metadata,
            name=name,
            **kwargs,
        )
        data = VectorStore(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def list(
        self,
        *,
        after: Union[str, NotGiven] = NOT_GIVEN,
        limit: Union[int, NotGiven] = NOT_GIVEN,
        order: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> VectorStoreList:
        response = await self.openai_client.with_raw_response.beta.vector_stores.list(
            after=after,
            limit=limit,
            order=order,
            **kwargs,
        )
        data = VectorStoreList(**json.loads(response.text))
        data._headers = response.headers

        return data
    
    async def delete(
        self,
        vector_store_id: str,
        **kwargs,
    ) -> VectorStoreDeleted:
        response = await self.openai_client.with_raw_response.beta.vector_stores.delete(
            vector_store_id=vector_store_id,
            **kwargs,
        )
        data = VectorStoreDeleted(**json.loads(response.text))
        data._headers = response.headers

        return data


class AsyncVectorFiles(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    async def create(
        self,
        vector_store_id: str,
        *,
        file_id: str,
        **kwargs,
    ) -> VectorStoreFile:
        response = await self.openai_client.with_raw_response.beta.vector_stores.files.create(
            vector_store_id=vector_store_id,
            file_id=file_id,
            **kwargs,
        )
        data = VectorStoreFile(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def retrieve(
        self,
        file_id: str,
        *,
        vector_store_id: str,
        **kwargs,
    ) -> VectorStoreFile:
        response = (
            await self.openai_client.with_raw_response.beta.vector_stores.files.retrieve(
                file_id=file_id,
                vector_store_id=vector_store_id,
                **kwargs,
            )
        )
        data = VectorStoreFile(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def list(
        self,
        vector_store_id: str,
        *,
        after: Union[str, NotGiven] = NOT_GIVEN,
        before: Union[str, NotGiven] = NOT_GIVEN,
        filter: Union[str, NotGiven] = NOT_GIVEN,
        limit: Union[int, NotGiven] = NOT_GIVEN,
        order: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> VectorStoreFileList:
        response = await self.openai_client.with_raw_response.beta.vector_stores.files.list(
            vector_store_id=vector_store_id,
            after=after,
            before=before,
            filter=filter,
            limit=limit,
            order=order,
            **kwargs,
        )
        data = VectorStoreFileList(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def delete(
        self,
        file_id: str,
        *,
        vector_store_id: str,
        **kwargs,
    ) -> VectorStoreFileDeleted:
        response = await self.openai_client.with_raw_response.beta.vector_stores.files.delete(
            file_id=file_id,
            vector_store_id=vector_store_id,
            **kwargs,
        )
        data = VectorStoreFileDeleted(**json.loads(response.text))
        data._headers = response

    async def create_and_poll(
        self,
        file_id: str,
        *,
        vector_store_id: str,
        poll_interval: Union[int, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> VectorStoreFile:
        response = await self.openai_client.beta.vector_stores.files.create_and_poll(
            file_id=file_id,
            vector_store_id=vector_store_id,
            poll_interval=poll_interval,
            **kwargs,
        )
        data = response

        return data
    
    async def poll(
        self,
        file_id: str,
        *,
        vector_store_id: str,
        poll_interval: Union[int, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> VectorStoreFile:
        response = await self.openai_client.beta.vector_stores.files.poll(
            file_id=file_id,
            vector_store_id=vector_store_id,
            poll_interval=poll_interval,
            **kwargs,
        )
        data = response

        return data
    
    async def upload(
        self,
        *,
        vector_store_id: str,
        file: FileTypes,
        **kwargs,
    ) -> VectorStoreFile:
        response = await self.openai_client.beta.vector_stores.files.upload(
            vector_store_id=vector_store_id,
            file=file,
            **kwargs,
        )
        data = response
        return data
    
    async def upload_and_poll(
        self,
        *,
        vector_store_id: str,
        file: FileTypes,
        poll_interval: Union[int, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> VectorStoreFile:
        response = await self.openai_client.beta.vector_stores.files.upload_and_poll(
            vector_store_id=vector_store_id,
            file=file,
            poll_interval=poll_interval,
            **kwargs,
        )
        data = response
        return data
    

class AsyncVectorFileBatches(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    async def create(
        self,
        vector_store_id: str,
        *,
        file_ids: List[str],
        **kwargs,
    ) -> VectorStoreFileBatch:
        response = await self.openai_client.with_raw_response.beta.vector_stores.file_batches.create(
            vector_store_id=vector_store_id,
            file_ids=file_ids,
            **kwargs,
        )
        data = VectorStoreFileBatch(**json.loads(response.text))
        data._headers = response.headers

        return data
    
    async def retrieve(
        self,
        batch_id:str,
        *,
        vector_store_id: str,
        **kwargs
    ) -> VectorStoreFileBatch:
        response = await self.openai_client.with_raw_response.beta.vector_stores.file_batches.retrieve(
            batch_id=batch_id,
            vector_store_id=vector_store_id,
            **kwargs,
        )
        data = VectorStoreFileBatch(**json.loads(response.text))
        data._headers = response.headers

        return data 
    
    async def cancel(
        self,
        batch_id:str,
        *,
        vector_store_id: str,
        **kwargs
    ) -> VectorStoreFileBatch:
        response = await self.openai_client.with_raw_response.beta.vector_stores.file_batches.cancel(
            batch_id=batch_id,
            vector_store_id=vector_store_id,
            **kwargs,
        )
        data = VectorStoreFileBatch(**json.loads(response.text))
        data._headers = response.headers

        return data
    
    async def create_and_poll(
            self,
            vector_store_id: str,
            *,
            file_ids: List[str],
            poll_interval: Union[int, NotGiven] = NOT_GIVEN,
            **kwargs,
    )-> VectorStoreFileBatch:
        response = await self.openai_client.beta.vector_stores.file_batches.create_and_poll(
            vector_store_id=vector_store_id,
            file_ids=file_ids,
            poll_interval=poll_interval,
            **kwargs,
        )
        data = response
        return data
    
    async def list_files(
        self,
        batch_id: str,
        *,
        vector_store_id: str,
        after: Union[str, NotGiven] = NOT_GIVEN,
        before: Union[str, NotGiven] = NOT_GIVEN,
        filter: Union[str, NotGiven] = NOT_GIVEN,
        limit: Union[int, NotGiven] = NOT_GIVEN,
        order: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> VectorStoreFileList:
        response = await self.openai_client.beta.with_raw_response.vector_stores.file_batches.list_files(
            batch_id=batch_id,
            vector_store_id=vector_store_id,
            after=after,
            before=before,
            filter=filter,
            limit=limit,
            order=order,
            **kwargs,
        )
        data = VectorStoreFileBatch(**json.loads(response.text))
        data._headers = response.headers

        return data
    
    async def poll(
        self,
        batch_id: str,
        *,
        vector_store_id: str,
        poll_interval: Union[int, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> VectorStoreFileBatch:
        response = await self.openai_client.beta.vector_stores.file_batches.poll(
            batch_id=batch_id,
            vector_store_id=vector_store_id,
            poll_interval=poll_interval,
            **kwargs,
        )
        data = response

        return data
    
    async def upload_and_poll(
        self,
        vector_store_id: str,
        *,
        files: Iterable[FileTypes],
        max_concurrency: int = 5,
        file_ids: List[str] = [],
        poll_interval_ms: Union[int, NotGiven] = NOT_GIVEN,
        **kwargs
    ) -> VectorStoreFileBatch:
        response = await self.openai_client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store_id,
            files=files,
            max_concurrency=max_concurrency,
            file_ids=file_ids,
            poll_interval_ms=poll_interval_ms,
            **kwargs,
        )
        data = response

        return data