import json
from typing import Any, Iterable, List, Union
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.client import AsyncPortkey, Portkey
from portkey_ai.api_resources.utils import extract_extra_params
from ..._vendor.openai._types import Omit, omit
from portkey_ai.api_resources.types.moderations_type import ModerationCreateResponse


class Moderations(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    def create(
        self,
        *,
        input: Union[str, List[str], Iterable[Any]],
        model: Union[str, Omit] = omit,
        **kwargs
    ) -> ModerationCreateResponse:
        extra_params = extract_extra_params(kwargs)
        response = self.openai_client.with_raw_response.moderations.create(
            input=input, model=model, **extra_params
        )
        data = ModerationCreateResponse(**json.loads(response.text))
        data._headers = response.headers

        return data


class AsyncModerations(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    async def create(
        self,
        *,
        input: Union[str, List[str], Iterable[Any]],
        model: Union[str, Omit] = omit,
        **kwargs
    ) -> ModerationCreateResponse:
        extra_params = extract_extra_params(kwargs)
        response = await self.openai_client.with_raw_response.moderations.create(
            input=input, model=model, **extra_params
        )
        data = ModerationCreateResponse(**json.loads(response.text))
        data._headers = response.headers

        return data
