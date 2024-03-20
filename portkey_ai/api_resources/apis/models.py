import json
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.client import AsyncPortkey, Portkey
from portkey_ai.api_resources.types.models_type import Model, ModelDeleted, ModelList


class Models(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    def list(self, **kwargs) -> ModelList:
        response = self.openai_client.with_raw_response.models.list(**kwargs)
        data = ModelList(**json.loads(response.text))
        data._headers = response.headers
        return data

    def retrieve(self, model, **kwargs) -> Model:
        response = self.openai_client.with_raw_response.models.retrieve(
            model=model, **kwargs
        )
        data = Model(**json.loads(response.text))
        data._headers = response.headers
        return data

    def delete(self, model, **kwargs) -> ModelDeleted:
        response = self.openai_client.with_raw_response.models.delete(
            model=model, **kwargs
        )
        data = ModelDeleted(**json.loads(response.text))
        data._headers = response.headers
        return data


class AsyncModels(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    async def list(self, **kwargs) -> ModelList:
        response = await self.openai_client.with_raw_response.models.list(**kwargs)
        data = ModelList(**json.loads(response.text))
        data._headers = response.headers
        return data

    async def retrieve(self, model, **kwargs) -> Model:
        response = await self.openai_client.with_raw_response.models.retrieve(
            model=model, **kwargs
        )
        data = Model(**json.loads(response.text))
        data._headers = response.headers
        return data

    async def delete(self, model, **kwargs) -> ModelDeleted:
        response = await self.openai_client.with_raw_response.models.delete(
            model=model, **kwargs
        )
        data = ModelDeleted(**json.loads(response.text))
        data._headers = response.headers
        return data
