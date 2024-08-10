import json
from typing import Optional, Union
import typing
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.client import AsyncPortkey, Portkey
from portkey_ai.api_resources.types.embeddings_type import CreateEmbeddingResponse
from ..._vendor.openai._types import NotGiven, NOT_GIVEN


class Embeddings(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    @typing.no_type_check
    def create(
        self,
        *,
        input: str,
        model: Optional[str] = "portkey-default",
        dimensions: Union[int, NotGiven] = NOT_GIVEN,
        encoding_format: Union[str, NotGiven] = NOT_GIVEN,
        user: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs
    ) -> CreateEmbeddingResponse:
        response = self.openai_client.with_raw_response.embeddings.create(
            input=input,
            model=model,
            dimensions=dimensions,
            encoding_format=encoding_format,
            user=user,
            extra_body=kwargs,
        )

        data = CreateEmbeddingResponse(**json.loads(response.text))
        data._headers = response.headers

        return data


class AsyncEmbeddings(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    @typing.no_type_check
    async def create(
        self,
        *,
        input: str,
        model: Optional[str] = "portkey-default",
        dimensions: Union[int, NotGiven] = NOT_GIVEN,
        encoding_format: Union[str, NotGiven] = NOT_GIVEN,
        user: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs
    ) -> CreateEmbeddingResponse:
        response = await self.openai_client.with_raw_response.embeddings.create(
            input=input,
            model=model,
            dimensions=dimensions,
            encoding_format=encoding_format,
            user=user,
            extra_body=kwargs,
        )
        data = CreateEmbeddingResponse(**json.loads(response.text))
        data._headers = response.headers

        return data
