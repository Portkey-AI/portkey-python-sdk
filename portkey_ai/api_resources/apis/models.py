import json
from typing import Union
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.client import AsyncPortkey, Portkey
from portkey_ai.api_resources.types.models_type import Model, ModelDeleted, ModelList
from portkey_ai.api_resources.utils import extract_extra_params
from ..._vendor.openai._types import NotGiven, NOT_GIVEN


class Models(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    def retrieve(
        self, model: str, *, timeout: Union[float, NotGiven] = NOT_GIVEN, **kwargs
    ) -> Model:
        extra_params = extract_extra_params(kwargs)
        response = self.openai_client.with_raw_response.models.retrieve(
            model=model, timeout=timeout, **extra_params
        )
        data = Model(**json.loads(response.text))
        data._headers = response.headers
        return data

    def list(self, **kwargs) -> ModelList:
        extra_params = extract_extra_params(kwargs)
        response = self.openai_client.with_raw_response.models.list(**extra_params)
        data = ModelList(**json.loads(response.text))
        data._headers = response.headers
        return data

    def delete(
        self, model: str, *, timeout: Union[float, NotGiven] = NOT_GIVEN, **kwargs
    ) -> ModelDeleted:
        extra_params = extract_extra_params(kwargs)
        response = self.openai_client.with_raw_response.models.delete(
            model=model, timeout=timeout, **extra_params
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
        extra_params = extract_extra_params(kwargs)
        response = await self.openai_client.with_raw_response.models.retrieve(
            model=model, timeout=timeout, **extra_params
        )
        data = Model(**json.loads(response.text))
        data._headers = response.headers
        return data

    async def list(self, **kwargs) -> ModelList:
        extra_params = extract_extra_params(kwargs)
        response = await self.openai_client.with_raw_response.models.list(**extra_params)
        data = ModelList(**json.loads(response.text))
        data._headers = response.headers
        return data

    async def delete(
        self, model: str, *, timeout: Union[float, NotGiven] = NOT_GIVEN, **kwargs
    ) -> ModelDeleted:
        extra_params = extract_extra_params(kwargs)
        response = await self.openai_client.with_raw_response.models.delete(
            model=model, timeout=timeout, **extra_params
        )
        data = ModelDeleted(**json.loads(response.text))
        data._headers = response.headers
        return data
