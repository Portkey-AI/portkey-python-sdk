import json
from typing import Union
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.client import AsyncPortkey, Portkey
from portkey_ai.api_resources.types.models_type import Model, ModelDeleted, ModelList
from ..._vendor.openai._types import NotGiven, NOT_GIVEN


class Models(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    def retrieve(
        self, model: str, *, timeout: Union[float, NotGiven] = NOT_GIVEN, **kwargs
    ) -> Model:
        if kwargs:
            response = self.openai_client.with_raw_response.models.retrieve(
                model=model, timeout=timeout, extra_body=kwargs
            )
        else:
            response = self.openai_client.with_raw_response.models.retrieve(
                model=model, timeout=timeout
            )
        data = Model(**json.loads(response.text))
        data._headers = response.headers
        return data

    def list(self, **kwargs) -> ModelList:
        response = self.openai_client.with_raw_response.models.list(**kwargs)
        data = ModelList(**json.loads(response.text))
        data._headers = response.headers
        return data

    def delete(
        self, model: str, *, timeout: Union[float, NotGiven] = NOT_GIVEN, **kwargs
    ) -> ModelDeleted:
        response = self.openai_client.with_raw_response.models.delete(
            model=model, timeout=timeout, extra_body=kwargs
        )
        data = ModelDeleted(**json.loads(response.text))
        data._headers = response.headers
        return data


class AsyncModels(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    async def retrieve(
        self, model: str, *, timeout: Union[float, NotGiven] = NOT_GIVEN, **kwargs
    ) -> Model:
        if kwargs:
            response = await self.openai_client.with_raw_response.models.retrieve(
                model=model, timeout=timeout, extra_body=kwargs
            )
        else:
            response = await self.openai_client.with_raw_response.models.retrieve(
                model=model, timeout=timeout
            )
        data = Model(**json.loads(response.text))
        data._headers = response.headers
        return data

    async def list(self, **kwargs) -> ModelList:
        response = await self.openai_client.with_raw_response.models.list(**kwargs)
        data = ModelList(**json.loads(response.text))
        data._headers = response.headers
        return data

    async def delete(
        self, model: str, *, timeout: Union[float, NotGiven] = NOT_GIVEN, **kwargs
    ) -> ModelDeleted:
        response = await self.openai_client.with_raw_response.models.delete(
            model=model, timeout=timeout, extra_body=kwargs
        )
        data = ModelDeleted(**json.loads(response.text))
        data._headers = response.headers
        return data
