import json
from typing import Any, List, Union
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.client import AsyncPortkey, Portkey
from portkey_ai.api_resources.types.upload_types import Upload, UploadPart
from ..._vendor.openai._types import FileTypes, NotGiven, NOT_GIVEN


class Uploads(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.parts = Parts(client)

    def create(
        self, *, bytes: int, filename: str, mime_type: str, purpose: Any, **kwargs
    ) -> Upload:
        response = self.openai_client.with_raw_response.uploads.create(
            bytes=bytes,
            filename=filename,
            mime_type=mime_type,
            purpose=purpose,
            extra_body=kwargs,
        )
        data = Upload(**json.loads(response.text))
        data._headers = response.headers

        return data

    def cancel(self, upload_id: str, **kwargs) -> Upload:
        response = self.openai_client.with_raw_response.uploads.cancel(
            upload_id=upload_id, extra_body=kwargs
        )
        data = Upload(**json.loads(response.text))
        data._headers = response.headers

        return data

    def complete(
        self,
        upload_id: str,
        *,
        part_ids: List[str],
        md5: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs
    ) -> Upload:
        response = self.openai_client.with_raw_response.uploads.complete(
            upload_id=upload_id,
            part_ids=part_ids,
            md5=md5,
            extra_body=kwargs,
        )
        data = Upload(**json.loads(response.text))
        data._headers = response.headers

        return data


class Parts(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    def create(self, upload_id: str, *, data: FileTypes, **kwargs) -> UploadPart:
        response = self.openai_client.with_raw_response.uploads.parts.create(
            upload_id=upload_id,
            data=data,
            extra_body=kwargs,
        )
        result = UploadPart(**json.loads(response.text))
        result._headers = response.headers

        return result


class AsyncUploads(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.parts = AsyncParts(client)

    async def create(
        self, *, bytes: int, filename: str, mime_type: str, purpose: Any, **kwargs
    ) -> Upload:
        response = await self.openai_client.with_raw_response.uploads.create(
            bytes=bytes,
            filename=filename,
            mime_type=mime_type,
            purpose=purpose,
            extra_body=kwargs,
        )
        data = Upload(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def cancel(self, upload_id: str, **kwargs) -> Upload:
        response = await self.openai_client.with_raw_response.uploads.cancel(
            upload_id=upload_id, extra_body=kwargs
        )
        data = Upload(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def complete(
        self,
        upload_id: str,
        *,
        part_ids: List[str],
        md5: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs
    ) -> Upload:
        response = await self.openai_client.with_raw_response.uploads.complete(
            upload_id=upload_id,
            part_ids=part_ids,
            md5=md5,
            extra_body=kwargs,
        )
        data = Upload(**json.loads(response.text))
        data._headers = response.headers

        return data


class AsyncParts(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    async def create(self, upload_id: str, *, data: FileTypes, **kwargs) -> UploadPart:
        response = await self.openai_client.with_raw_response.uploads.parts.create(
            upload_id=upload_id,
            data=data,
            extra_body=kwargs,
        )
        result = UploadPart(**json.loads(response.text))
        result._headers = response.headers

        return result
