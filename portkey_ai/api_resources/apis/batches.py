import json
from typing import Dict, Optional, Union
import typing
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.client import AsyncPortkey, Portkey
from ..._vendor.openai._types import NotGiven, NOT_GIVEN

from portkey_ai.api_resources.types.batches_type import Batch, BatchList


class Batches(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    @typing.no_type_check
    def create(
        self,
        *,
        completion_window: str,
        endpoint: str,
        input_file_id: str,
        metadata: Union[Optional[Dict[str, str]], NotGiven] = NOT_GIVEN,
        **kwargs
    ) -> Batch:
        response = self.openai_client.with_raw_response.batches.create(
            completion_window=completion_window,
            endpoint=endpoint,
            input_file_id=input_file_id,
            metadata=metadata,
            extra_body=kwargs,
        )
        data = Batch(**json.loads(response.text))
        data._headers = response.headers

        return data

    def retrieve(self, batch_id, **kwargs) -> Batch:
        if kwargs:
            response = self.openai_client.with_raw_response.batches.retrieve(
                batch_id=batch_id, extra_body=kwargs
            )
        else:
            response = self.openai_client.with_raw_response.batches.retrieve(
                batch_id=batch_id
            )
        data = Batch(**json.loads(response.text))
        data._headers = response.headers

        return data

    def list(
        self,
        *,
        after: Union[str, NotGiven] = NOT_GIVEN,
        limit: Union[int, NotGiven] = NOT_GIVEN,
        **kwargs
    ) -> BatchList:
        response = self.openai_client.with_raw_response.batches.list(
            after=after, limit=limit
        )
        data = BatchList(**json.loads(response.text))
        data._headers = response.headers

        return data

    def cancel(self, batch_id: str, **kwargs) -> Batch:
        response = self.openai_client.with_raw_response.batches.cancel(
            batch_id=batch_id, extra_body=kwargs
        )
        data = Batch(**json.loads(response.text))
        data._headers = response.headers

        return data


class AsyncBatches(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    @typing.no_type_check
    async def create(
        self,
        *,
        completion_window: str,
        endpoint: str,
        input_file_id: str,
        metadata: Union[Optional[Dict[str, str]], NotGiven] = NOT_GIVEN,
        **kwargs
    ) -> Batch:
        response = await self.openai_client.with_raw_response.batches.create(
            completion_window=completion_window,
            endpoint=endpoint,
            input_file_id=input_file_id,
            metadata=metadata,
            extra_body=kwargs,
        )
        data = Batch(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def retrieve(self, batch_id, **kwargs) -> Batch:
        if kwargs:
            response = await self.openai_client.with_raw_response.batches.retrieve(
                batch_id=batch_id, extra_body=kwargs
            )
        else:
            response = await self.openai_client.with_raw_response.batches.retrieve(
                batch_id=batch_id
            )
        data = Batch(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def list(
        self,
        *,
        after: Union[str, NotGiven] = NOT_GIVEN,
        limit: Union[int, NotGiven] = NOT_GIVEN,
        **kwargs
    ) -> BatchList:
        response = await self.openai_client.with_raw_response.batches.list(
            after=after, limit=limit
        )
        data = BatchList(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def cancel(self, batch_id: str, **kwargs) -> Batch:
        response = await self.openai_client.with_raw_response.batches.cancel(
            batch_id=batch_id, extra_body=kwargs
        )
        data = Batch(**json.loads(response.text))
        data._headers = response.headers

        return data
