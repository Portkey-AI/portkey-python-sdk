import json
import os
from typing import Any, List, Union
import typing
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.client import AsyncPortkey, Portkey
from portkey_ai.api_resources.types.upload_types import Upload, UploadPart
from ..._vendor.openai._types import FileTypes, Omit, omit


class Uploads(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.parts = Parts(client)

    @typing.no_type_check
    def upload_file_chunked(
        self,
        *,
        file: Union[os.PathLike[str], bytes],
        mime_type: str,
        purpose: Any,
        filename: Union[str, None] = None,
        bytes: Union[int, None] = None,
        part_size: Union[int, None] = None,
        md5: Union[str, Omit] = omit,
    ) -> Any:
        response = self.openai_client.uploads.upload_file_chunked(
            file=file,
            mime_type=mime_type,
            purpose=purpose,
            filename=filename,
            bytes=bytes,
            part_size=part_size,
            md5=md5,
        )
        return response

    def create(
        self, *, bytes: int, filename: str, mime_type: str, purpose: Any, **kwargs
    ) -> Upload:
        extra_headers = kwargs.pop("extra_headers", {})
        response = self.openai_client.with_raw_response.uploads.create(
            bytes=bytes,
            filename=filename,
            mime_type=mime_type,
            purpose=purpose,
            extra_body=kwargs,
            extra_headers=extra_headers,
        )
        data = Upload(**json.loads(response.text))
        data._headers = response.headers

        return data

    def cancel(self, upload_id: str, **kwargs) -> Upload:
        extra_headers = kwargs.pop("extra_headers", {})
        response = self.openai_client.with_raw_response.uploads.cancel(
            upload_id=upload_id, extra_body=kwargs, extra_headers=extra_headers
        )
        data = Upload(**json.loads(response.text))
        data._headers = response.headers

        return data

    def complete(
        self,
        upload_id: str,
        *,
        part_ids: List[str],
        md5: Union[str, Omit] = omit,
        **kwargs,
    ) -> Upload:
        extra_headers = kwargs.pop("extra_headers", {})
        response = self.openai_client.with_raw_response.uploads.complete(
            upload_id=upload_id,
            part_ids=part_ids,
            md5=md5,
            extra_body=kwargs,
            extra_headers=extra_headers,
        )
        data = Upload(**json.loads(response.text))
        data._headers = response.headers

        return data


class Parts(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    def create(self, upload_id: str, *, data: FileTypes, **kwargs) -> UploadPart:
        extra_headers = kwargs.pop("extra_headers", {})
        response = self.openai_client.with_raw_response.uploads.parts.create(
            upload_id=upload_id,
            data=data,
            extra_body=kwargs,
            extra_headers=extra_headers,
        )
        result = UploadPart(**json.loads(response.text))
        result._headers = response.headers

        return result


class AsyncUploads(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.parts = AsyncParts(client)

    @typing.no_type_check
    async def upload_file_chunked(
        self,
        *,
        file: Union[os.PathLike[str], bytes],
        mime_type: str,
        purpose: Any,
        filename: Union[str, None] = None,
        bytes: Union[int, None] = None,
        part_size: Union[int, None] = None,
        md5: Union[str, Omit] = omit,
    ) -> Any:
        response = await self.openai_client.uploads.upload_file_chunked(
            file=file,
            mime_type=mime_type,
            purpose=purpose,
            filename=filename,
            bytes=bytes,
            part_size=part_size,
            md5=md5,
        )
        return response

    async def create(
        self, *, bytes: int, filename: str, mime_type: str, purpose: Any, **kwargs
    ) -> Upload:
        extra_headers = kwargs.pop("extra_headers", {})
        response = await self.openai_client.with_raw_response.uploads.create(
            bytes=bytes,
            filename=filename,
            mime_type=mime_type,
            purpose=purpose,
            extra_body=kwargs,
            extra_headers=extra_headers,
        )
        data = Upload(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def cancel(self, upload_id: str, **kwargs) -> Upload:
        extra_headers = kwargs.pop("extra_headers", {})
        response = await self.openai_client.with_raw_response.uploads.cancel(
            upload_id=upload_id, extra_body=kwargs, extra_headers=extra_headers
        )
        data = Upload(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def complete(
        self,
        upload_id: str,
        *,
        part_ids: List[str],
        md5: Union[str, Omit] = omit,
        **kwargs,
    ) -> Upload:
        extra_headers = kwargs.pop("extra_headers", {})
        response = await self.openai_client.with_raw_response.uploads.complete(
            upload_id=upload_id,
            part_ids=part_ids,
            md5=md5,
            extra_body=kwargs,
            extra_headers=extra_headers,
        )
        data = Upload(**json.loads(response.text))
        data._headers = response.headers

        return data


class AsyncParts(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    async def create(self, upload_id: str, *, data: FileTypes, **kwargs) -> UploadPart:
        extra_headers = kwargs.pop("extra_headers", {})
        response = await self.openai_client.with_raw_response.uploads.parts.create(
            upload_id=upload_id,
            data=data,
            extra_body=kwargs,
            extra_headers=extra_headers,
        )
        result = UploadPart(**json.loads(response.text))
        result._headers = response.headers

        return result
