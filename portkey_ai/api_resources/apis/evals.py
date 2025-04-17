import json
from typing import Any, Literal, Optional, Union
from portkey_ai._vendor.openai._types import NOT_GIVEN, NotGiven
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.client import AsyncPortkey, Portkey
from portkey_ai.api_resources.types.evals_types import (
    EvalCreateResponse,
    EvalDeleteResponse,
    EvalListResponseList,
    EvalRetrieveResponse,
    EvalUpdateResponse,
)
from portkey_ai.api_resources.types.shared_types import Metadata


class Evals(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    def create(
        self,
        *,
        data_source_config: Any,
        testing_criteria: Any,
        metadata: Union[Optional[Metadata], NotGiven] = NOT_GIVEN,
        name: Union[str, NotGiven] = NOT_GIVEN,
        share_with_openai: Union[bool, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> EvalCreateResponse:
        response = self.openai_client.evals.create(
            data_source_config=data_source_config,
            testing_criteria=testing_criteria,
            metadata=metadata,
            name=name,
            share_with_openai=share_with_openai,
            extra_body=kwargs,
        )
        data = response

        return data  # type: ignore[return-value]

    def retrieve(
        self,
        eval_id: str,
    ) -> EvalRetrieveResponse:
        response = self.openai_client.with_raw_response.evals.retrieve(
            eval_id=eval_id,
        )

        data = EvalRetrieveResponse(**json.loads(response.text))
        data._headers = response.headers

        return data

    def update(
        self,
        eval_id: str,
        *,
        metadata: Union[Optional[Metadata], NotGiven] = NOT_GIVEN,
        name: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> EvalUpdateResponse:
        response = self.openai_client.with_raw_response.evals.update(
            eval_id=eval_id,
            metadata=metadata,
            name=name,
            extra_body=kwargs,
        )

        data = EvalUpdateResponse(**json.loads(response.text))
        data._headers = response.headers

        return data

    def list(
        self,
        *,
        after: Union[str, NotGiven] = NOT_GIVEN,
        limit: Union[int, NotGiven] = NOT_GIVEN,
        order: Union[Literal["asc", "desc"], NotGiven] = NOT_GIVEN,
        order_by: Union[Literal["created_at", "updated_at"], NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> EvalListResponseList:
        response = self.openai_client.with_raw_response.evals.list(
            after=after,
            limit=limit,
            order=order,
            order_by=order_by,
        )

        data = EvalListResponseList(**json.loads(response.text))
        data._headers = response.headers

        return data

    def delete(
        self,
        eval_id: str,
        **kwargs,
    ) -> EvalDeleteResponse:
        response = self.openai_client.with_raw_response.evals.delete(
            eval_id=eval_id,
            extra_body=kwargs,
        )

        data = EvalDeleteResponse(**json.loads(response.text))
        data._headers = response.headers

        return data


class AsyncEvals(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    async def create(
        self,
        *,
        data_source_config: Any,
        testing_criteria: Any,
        metadata: Union[Optional[Metadata], NotGiven] = NOT_GIVEN,
        name: Union[str, NotGiven] = NOT_GIVEN,
        share_with_openai: Union[bool, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> EvalCreateResponse:
        response = await self.openai_client.evals.create(
            data_source_config=data_source_config,
            testing_criteria=testing_criteria,
            metadata=metadata,
            name=name,
            share_with_openai=share_with_openai,
            extra_body=kwargs,
        )
        data = response

        return data  # type: ignore[return-value]

    async def retrieve(
        self,
        eval_id: str,
    ) -> EvalRetrieveResponse:
        response = await self.openai_client.with_raw_response.evals.retrieve(
            eval_id=eval_id,
        )

        data = EvalRetrieveResponse(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def update(
        self,
        eval_id: str,
        *,
        metadata: Union[Optional[Metadata], NotGiven] = NOT_GIVEN,
        name: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> EvalUpdateResponse:
        response = await self.openai_client.with_raw_response.evals.update(
            eval_id=eval_id,
            metadata=metadata,
            name=name,
            extra_body=kwargs,
        )

        data = EvalUpdateResponse(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def list(
        self,
        *,
        after: Union[str, NotGiven] = NOT_GIVEN,
        limit: Union[int, NotGiven] = NOT_GIVEN,
        order: Union[Literal["asc", "desc"], NotGiven] = NOT_GIVEN,
        order_by: Union[Literal["created_at", "updated_at"], NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> EvalListResponseList:
        response = await self.openai_client.with_raw_response.evals.list(
            after=after,
            limit=limit,
            order=order,
            order_by=order_by,
        )

        data = EvalListResponseList(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def delete(
        self,
        eval_id: str,
        **kwargs,
    ) -> EvalDeleteResponse:
        response = await self.openai_client.with_raw_response.evals.delete(
            eval_id=eval_id,
            extra_body=kwargs,
        )

        data = EvalDeleteResponse(**json.loads(response.text))
        data._headers = response.headers

        return data
