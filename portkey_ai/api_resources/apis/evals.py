import json
from typing import Any, Literal, Optional, Union
from portkey_ai._vendor.openai._types import omit, Omit
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.client import AsyncPortkey, Portkey
from portkey_ai.api_resources.types.evals_runs_output_items_type import (
    OutputItemListResponseList,
    OutputItemRetrieveResponse,
)
from portkey_ai.api_resources.types.evals_runs_type import (
    RunCancelResponse,
    RunCreateResponse,
    RunDeleteResponse,
    RunListResponseList,
    RunRetrieveResponse,
)
from portkey_ai.api_resources.types.evals_types import (
    EvalCreateResponse,
    EvalDeleteResponse,
    EvalListResponseList,
    EvalRetrieveResponse,
    EvalUpdateResponse,
)
from portkey_ai.api_resources.types.shared_types import Metadata
from portkey_ai.api_resources.utils import extract_extra_params


class Evals(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.runs = EvalsRuns(client)

    def create(
        self,
        *,
        data_source_config: Any,
        testing_criteria: Any,
        metadata: Union[Optional[Metadata], Omit] = omit,
        name: Union[str, Omit] = omit,
        **kwargs,
    ) -> EvalCreateResponse:
        extra_params = extract_extra_params(kwargs)
        response = self.openai_client.evals.create(
            data_source_config=data_source_config,
            testing_criteria=testing_criteria,
            metadata=metadata,
            name=name,
            **extra_params,
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
        metadata: Union[Optional[Metadata], Omit] = omit,
        name: Union[str, Omit] = omit,
        **kwargs,
    ) -> EvalUpdateResponse:
        extra_params = extract_extra_params(kwargs)
        response = self.openai_client.with_raw_response.evals.update(
            eval_id=eval_id,
            metadata=metadata,
            name=name,
            **extra_params,
        )

        data = EvalUpdateResponse(**json.loads(response.text))
        data._headers = response.headers

        return data

    def list(
        self,
        *,
        after: Union[str, Omit] = omit,
        limit: Union[int, Omit] = omit,
        order: Union[Literal["asc", "desc"], Omit] = omit,
        order_by: Union[Literal["created_at", "updated_at"], Omit] = omit,
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
        extra_params = extract_extra_params(kwargs)
        response = self.openai_client.with_raw_response.evals.delete(
            eval_id=eval_id,
            **extra_params,
        )

        data = EvalDeleteResponse(**json.loads(response.text))
        data._headers = response.headers

        return data


class EvalsRuns(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.output_items = OutputItems(client)

    def create(
        self,
        eval_id: str,
        *,
        data_source: Any,
        metadata: Union[Optional[Metadata], Omit] = omit,
        name: Union[str, Omit] = omit,
        **kwargs,
    ) -> RunCreateResponse:
        extra_params = extract_extra_params(kwargs)
        response = self.openai_client.with_raw_response.evals.runs.create(
            eval_id=eval_id,
            data_source=data_source,
            metadata=metadata,
            name=name,
            **extra_params,
        )
        data = RunCreateResponse(**json.loads(response.text))
        data._headers = response.headers

        return data

    def retrieve(
        self,
        run_id: str,
        *,
        eval_id: str,
    ) -> RunRetrieveResponse:
        response = self.openai_client.with_raw_response.evals.runs.retrieve(
            run_id=run_id,
            eval_id=eval_id,
        )
        data = RunRetrieveResponse(**json.loads(response.text))
        data._headers = response.headers

        return data

    def list(
        self,
        eval_id: str,
        *,
        after: Union[str, Omit] = omit,
        limit: Union[int, Omit] = omit,
        order: Union[Literal["asc", "desc"], Omit] = omit,
        status: Union[
            Literal["queued", "in_progress", "completed", "canceled", "failed"],
            Omit,
        ] = omit,
    ) -> RunListResponseList:
        response = self.openai_client.with_raw_response.evals.runs.list(
            eval_id=eval_id,
            after=after,
            limit=limit,
            order=order,
            status=status,
        )
        data = RunListResponseList(**json.loads(response.text))
        data._headers = response.headers

        return data

    def delete(
        self,
        run_id: str,
        *,
        eval_id: str,
        **kwargs,
    ) -> RunDeleteResponse:
        extra_params = extract_extra_params(kwargs)
        response = self.openai_client.with_raw_response.evals.runs.delete(
            run_id=run_id,
            eval_id=eval_id,
            **extra_params,
        )
        data = RunDeleteResponse(**json.loads(response.text))
        data._headers = response.headers

        return data

    def cancel(
        self,
        run_id: str,
        *,
        eval_id: str,
        **kwargs,
    ) -> RunCancelResponse:
        extra_params = extract_extra_params(kwargs)
        response = self.openai_client.with_raw_response.evals.runs.cancel(
            run_id=run_id,
            eval_id=eval_id,
            **extra_params,
        )
        data = RunCancelResponse(**json.loads(response.text))
        data._headers = response.headers

        return data


class OutputItems(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    def retrieve(
        self,
        output_item_id: str,
        *,
        eval_id: str,
        run_id: str,
    ) -> OutputItemRetrieveResponse:
        response = (
            self.openai_client.with_raw_response.evals.runs.output_items.retrieve(
                output_item_id=output_item_id,
                eval_id=eval_id,
                run_id=run_id,
            )
        )
        data = OutputItemRetrieveResponse(**json.loads(response.text))
        data._headers = response.headers

        return data

    def list(
        self,
        run_id: str,
        *,
        eval_id: str,
        after: Union[str, Omit] = omit,
        limit: Union[int, Omit] = omit,
        order: Union[Literal["asc", "desc"], Omit] = omit,
        status: Union[Literal["fail", "pass"], Omit] = omit,
    ) -> OutputItemListResponseList:
        response = self.openai_client.with_raw_response.evals.runs.output_items.list(
            run_id=run_id,
            eval_id=eval_id,
            after=after,
            limit=limit,
            order=order,
            status=status,
        )
        data = OutputItemListResponseList(**json.loads(response.text))
        data._headers = response.headers

        return data


class AsyncEvals(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.runs = AsyncEvalsRuns(client)

    async def create(
        self,
        *,
        data_source_config: Any,
        testing_criteria: Any,
        metadata: Union[Optional[Metadata], Omit] = omit,
        name: Union[str, Omit] = omit,
        **kwargs,
    ) -> EvalCreateResponse:
        extra_params = extract_extra_params(kwargs)
        response = await self.openai_client.evals.create(
            data_source_config=data_source_config,
            testing_criteria=testing_criteria,
            metadata=metadata,
            name=name,
            **extra_params,
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
        metadata: Union[Optional[Metadata], Omit] = omit,
        name: Union[str, Omit] = omit,
        **kwargs,
    ) -> EvalUpdateResponse:
        extra_params = extract_extra_params(kwargs)
        response = await self.openai_client.with_raw_response.evals.update(
            eval_id=eval_id,
            metadata=metadata,
            name=name,
            **extra_params,
        )

        data = EvalUpdateResponse(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def list(
        self,
        *,
        after: Union[str, Omit] = omit,
        limit: Union[int, Omit] = omit,
        order: Union[Literal["asc", "desc"], Omit] = omit,
        order_by: Union[Literal["created_at", "updated_at"], Omit] = omit,
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
        extra_params = extract_extra_params(kwargs)
        response = await self.openai_client.with_raw_response.evals.delete(
            eval_id=eval_id,
            **extra_params,
        )

        data = EvalDeleteResponse(**json.loads(response.text))
        data._headers = response.headers

        return data


class AsyncEvalsRuns(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.output_items = AsyncOutputItems(client)

    async def create(
        self,
        eval_id: str,
        *,
        data_source: Any,
        metadata: Union[Optional[Metadata], Omit] = omit,
        name: Union[str, Omit] = omit,
        **kwargs,
    ) -> RunCreateResponse:
        extra_params = extract_extra_params(kwargs)
        response = await self.openai_client.with_raw_response.evals.runs.create(
            eval_id=eval_id,
            data_source=data_source,
            metadata=metadata,
            name=name,
            **extra_params,
        )
        data = RunCreateResponse(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def retrieve(
        self,
        run_id: str,
        *,
        eval_id: str,
    ) -> RunRetrieveResponse:
        response = await self.openai_client.with_raw_response.evals.runs.retrieve(
            run_id=run_id,
            eval_id=eval_id,
        )
        data = RunRetrieveResponse(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def list(
        self,
        eval_id: str,
        *,
        after: Union[str, Omit] = omit,
        limit: Union[int, Omit] = omit,
        order: Union[Literal["asc", "desc"], Omit] = omit,
        status: Union[
            Literal["queued", "in_progress", "completed", "canceled", "failed"],
            Omit,
        ] = omit,
    ) -> RunListResponseList:
        response = await self.openai_client.with_raw_response.evals.runs.list(
            eval_id=eval_id,
            after=after,
            limit=limit,
            order=order,
            status=status,
        )
        data = RunListResponseList(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def delete(
        self,
        run_id: str,
        *,
        eval_id: str,
        **kwargs,
    ) -> RunDeleteResponse:
        extra_params = extract_extra_params(kwargs)
        response = await self.openai_client.with_raw_response.evals.runs.delete(
            run_id=run_id,
            eval_id=eval_id,
            **extra_params,
        )
        data = RunDeleteResponse(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def cancel(
        self,
        run_id: str,
        *,
        eval_id: str,
        **kwargs,
    ) -> RunCancelResponse:
        extra_params = extract_extra_params(kwargs)
        response = await self.openai_client.with_raw_response.evals.runs.cancel(
            run_id=run_id,
            eval_id=eval_id,
            **extra_params,
        )
        data = RunCancelResponse(**json.loads(response.text))
        data._headers = response.headers

        return data


class AsyncOutputItems(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    async def retrieve(
        self,
        output_item_id: str,
        *,
        eval_id: str,
        run_id: str,
    ) -> OutputItemRetrieveResponse:
        response = (
            await self.openai_client.with_raw_response.evals.runs.output_items.retrieve(
                output_item_id=output_item_id,
                eval_id=eval_id,
                run_id=run_id,
            )
        )
        data = OutputItemRetrieveResponse(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def list(
        self,
        run_id: str,
        *,
        eval_id: str,
        after: Union[str, Omit] = omit,
        limit: Union[int, Omit] = omit,
        order: Union[Literal["asc", "desc"], Omit] = omit,
        status: Union[Literal["fail", "pass"], Omit] = omit,
    ) -> OutputItemListResponseList:
        response = (
            await self.openai_client.with_raw_response.evals.runs.output_items.list(
                run_id=run_id,
                eval_id=eval_id,
                after=after,
                limit=limit,
                order=order,
                status=status,
            )
        )
        data = OutputItemListResponseList(**json.loads(response.text))
        data._headers = response.headers

        return data
