import json
from typing import Iterable, List, Literal, Optional, Union
from portkey_ai._vendor.openai.types.fine_tuning.alpha import grader_run_params
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.client import AsyncPortkey, Portkey
from portkey_ai.api_resources.types.fine_tuning_alpha_grader_type import (
    GraderRunResponse,
    GraderValidateResponse,
)
from portkey_ai.api_resources.types.finetuning_checkpoint_permissions import (
    PermissionCreateResponse,
    PermissionDeleteResponse,
    PermissionRetrieveResponse,
)
from ..._vendor.openai._types import NotGiven, NOT_GIVEN
from ..._vendor.openai.types.fine_tuning import job_create_params

from portkey_ai.api_resources.types.fine_tuning_type import (
    FineTuningJob,
    FineTuningJobCheckpointList,
    FineTuningJobEventList,
    FineTuningJobList,
)


class FineTuning(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.jobs = Jobs(client)
        self.checkpoints = FineTuningCheckpoints(client)
        self.alpha = Alpha(client)


class Jobs(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.checkpoints = Checkpoints(client)

    def create(
        self,
        *,
        model: str,
        training_file: str,
        hyperparameters: Union[job_create_params.Hyperparameters, NotGiven] = NOT_GIVEN,
        integrations: Union[
            Optional[Iterable[job_create_params.Integration]], NotGiven
        ] = NOT_GIVEN,
        method: Union[job_create_params.Method, NotGiven] = NOT_GIVEN,
        seed: Union[Optional[int], NotGiven] = NOT_GIVEN,
        suffix: Union[Optional[str], NotGiven] = NOT_GIVEN,
        validation_file: Union[Optional[str], NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> FineTuningJob:
        response = self.openai_client.with_raw_response.fine_tuning.jobs.create(
            model=model,
            training_file=training_file,
            hyperparameters=hyperparameters,
            integrations=integrations,
            method=method,
            seed=seed,
            suffix=suffix,
            validation_file=validation_file,
            extra_body=kwargs,
        )
        data = FineTuningJob(**json.loads(response.text))
        data._headers = response.headers

        return data

    def retrieve(self, fine_tuning_job_id: str, **kwargs) -> FineTuningJob:
        if kwargs:
            response = self.openai_client.with_raw_response.fine_tuning.jobs.retrieve(
                fine_tuning_job_id=fine_tuning_job_id, extra_body=kwargs
            )
        else:
            response = self.openai_client.with_raw_response.fine_tuning.jobs.retrieve(
                fine_tuning_job_id=fine_tuning_job_id
            )
        data = FineTuningJob(**json.loads(response.text))
        data._headers = response.headers

        return data

    def list(
        self,
        *,
        after: Union[str, NotGiven] = NOT_GIVEN,
        limit: Union[int, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> FineTuningJobList:
        response = self.openai_client.with_raw_response.fine_tuning.jobs.list(
            after=after, limit=limit, **kwargs
        )
        data = FineTuningJobList(**json.loads(response.text))
        data._headers = response.headers

        return data

    def cancel(self, fine_tuning_job_id: str, **kwargs) -> FineTuningJob:
        response = self.openai_client.with_raw_response.fine_tuning.jobs.cancel(
            fine_tuning_job_id=fine_tuning_job_id, extra_body=kwargs
        )
        data = FineTuningJob(**json.loads(response.text))
        data._headers = response.headers

        return data

    def list_events(
        self,
        fine_tuning_job_id: str,
        *,
        after: Union[str, NotGiven] = NOT_GIVEN,
        limit: Union[int, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> FineTuningJobEventList:
        response = self.openai_client.with_raw_response.fine_tuning.jobs.list_events(
            fine_tuning_job_id=fine_tuning_job_id,
            after=after,
            limit=limit,
            extra_body=kwargs,
        )
        data = FineTuningJobEventList(**json.loads(response.text))
        data._headers = response.headers

        return data


class Checkpoints(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    def list(
        self,
        fine_tuning_job_id: str,
        *,
        after: Union[str, NotGiven] = NOT_GIVEN,
        limit: Union[int, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> FineTuningJobCheckpointList:
        response = (
            self.openai_client.with_raw_response.fine_tuning.jobs.checkpoints.list(
                fine_tuning_job_id=fine_tuning_job_id,
                after=after,
                limit=limit,
                **kwargs,
            )
        )

        data = FineTuningJobCheckpointList(**json.loads(response.text))
        data._headers = response.headers

        return data


class FineTuningCheckpoints(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.permissions = Permissions(client)


class Permissions(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    def create(
        self,
        fine_tuned_model_checkpoint: str,
        *,
        project_ids: List[str],
        **kwargs,
    ) -> PermissionCreateResponse:
        response = self.openai_client.with_raw_response.fine_tuning.checkpoints.permissions.create(  # noqa: E501
            fine_tuned_model_checkpoint=fine_tuned_model_checkpoint,
            project_ids=project_ids,
            extra_body=kwargs,
        )
        data = PermissionCreateResponse(**json.loads(response.text))
        data._headers = response.headers

        return data

    def retrieve(
        self,
        fine_tuned_model_checkpoint: str,
        *,
        after: Union[str, NotGiven] = NOT_GIVEN,
        limit: Union[int, NotGiven] = NOT_GIVEN,
        order: Union[Literal["ascending", "descending"], NotGiven] = NOT_GIVEN,
        project_id: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> PermissionRetrieveResponse:
        response = self.openai_client.with_raw_response.fine_tuning.checkpoints.permissions.retrieve(  # noqa: E501
            fine_tuned_model_checkpoint=fine_tuned_model_checkpoint,
            after=after,
            limit=limit,
            order=order,
            project_id=project_id,
            extra_body=kwargs,
        )
        data = PermissionRetrieveResponse(**json.loads(response.text))
        data._headers = response.headers

        return data

    def delete(
        self,
        permission_id: str,
        *,
        fine_tuned_model_checkpoint: str,
        **kwargs,
    ) -> PermissionDeleteResponse:
        response = self.openai_client.with_raw_response.fine_tuning.checkpoints.permissions.delete(  # noqa: E501
            permission_id=permission_id,
            fine_tuned_model_checkpoint=fine_tuned_model_checkpoint,
            extra_body=kwargs,
        )
        data = PermissionDeleteResponse(**json.loads(response.text))
        data._headers = response.headers

        return data


class Alpha(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.graders = Graders(client)


class Graders(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    def run(
        self,
        *,
        grader: grader_run_params.Grader,
        model_sample: str,
        item: Union[object, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> GraderRunResponse:
        response = self.openai_client.with_raw_response.fine_tuning.alpha.graders.run(
            grader=grader,
            model_sample=model_sample,
            item=item,
            extra_body=kwargs,
        )
        data = GraderRunResponse(**json.loads(response.text))
        data._headers = response.headers

        return data

    def validate(
        self,
        *,
        grader: grader_run_params.Grader,
        **kwargs,
    ) -> GraderValidateResponse:
        response = (
            self.openai_client.with_raw_response.fine_tuning.alpha.graders.validate(
                grader=grader,
                extra_body=kwargs,
            )
        )
        data = GraderValidateResponse(**json.loads(response.text))
        data._headers = response.headers

        return data


class AsyncFineTuning(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.jobs = AsyncJobs(client)
        self.checkpoints = AsyncFineTuningCheckpoints(client)
        self.alpha = AsyncAlpha(client)


class AsyncJobs(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.checkpoints = AsyncCheckpoints(client)

    async def create(
        self,
        *,
        model: str,
        training_file: str,
        hyperparameters: Union[job_create_params.Hyperparameters, NotGiven] = NOT_GIVEN,
        integrations: Union[
            Optional[Iterable[job_create_params.Integration]], NotGiven
        ] = NOT_GIVEN,
        method: Union[job_create_params.Method, NotGiven] = NOT_GIVEN,
        seed: Union[Optional[int], NotGiven] = NOT_GIVEN,
        suffix: Union[Optional[str], NotGiven] = NOT_GIVEN,
        validation_file: Union[Optional[str], NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> FineTuningJob:
        response = await self.openai_client.with_raw_response.fine_tuning.jobs.create(
            model=model,
            training_file=training_file,
            hyperparameters=hyperparameters,
            integrations=integrations,
            method=method,
            seed=seed,
            suffix=suffix,
            validation_file=validation_file,
            extra_body=kwargs,
        )
        data = FineTuningJob(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def retrieve(self, fine_tuning_job_id: str, **kwargs) -> FineTuningJob:
        if kwargs:
            response = (
                await self.openai_client.with_raw_response.fine_tuning.jobs.retrieve(
                    fine_tuning_job_id=fine_tuning_job_id, extra_body=kwargs
                )
            )
        else:
            response = (
                await self.openai_client.with_raw_response.fine_tuning.jobs.retrieve(
                    fine_tuning_job_id=fine_tuning_job_id
                )
            )

        data = FineTuningJob(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def list(
        self,
        *,
        after: Union[str, NotGiven] = NOT_GIVEN,
        limit: Union[int, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> FineTuningJobList:
        response = await self.openai_client.with_raw_response.fine_tuning.jobs.list(
            after=after, limit=limit, **kwargs
        )
        data = FineTuningJobList(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def cancel(self, fine_tuning_job_id: str, **kwargs) -> FineTuningJob:
        response = await self.openai_client.with_raw_response.fine_tuning.jobs.cancel(
            fine_tuning_job_id, extra_body=kwargs
        )
        data = FineTuningJob(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def list_events(
        self,
        fine_tuning_job_id: str,
        *,
        after: Union[str, NotGiven] = NOT_GIVEN,
        limit: Union[int, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> FineTuningJobEventList:
        response = (
            await self.openai_client.with_raw_response.fine_tuning.jobs.list_events(
                fine_tuning_job_id=fine_tuning_job_id,
                after=after,
                limit=limit,
                extra_body=kwargs,
            )
        )
        data = FineTuningJobEventList(**json.loads(response.text))
        data._headers = response.headers

        return data


class AsyncCheckpoints(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    async def list(
        self,
        fine_tuning_job_id: str,
        *,
        after: Union[str, NotGiven] = NOT_GIVEN,
        limit: Union[int, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> FineTuningJobCheckpointList:
        response = await self.openai_client.with_raw_response.fine_tuning.jobs.checkpoints.list(  # noqa: E501
            fine_tuning_job_id=fine_tuning_job_id,
            after=after,
            limit=limit,
            **kwargs,
        )

        data = FineTuningJobCheckpointList(**json.loads(response.text))
        data._headers = response.headers

        return data


class AsyncFineTuningCheckpoints(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.permissions = AsyncPermissions(client)


class AsyncPermissions(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    async def create(
        self,
        fine_tuned_model_checkpoint: str,
        *,
        project_ids: List[str],
        **kwargs,
    ) -> PermissionCreateResponse:
        response = await self.openai_client.with_raw_response.fine_tuning.checkpoints.permissions.create(  # noqa: E501
            fine_tuned_model_checkpoint=fine_tuned_model_checkpoint,
            project_ids=project_ids,
            extra_body=kwargs,
        )
        data = PermissionCreateResponse(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def retrieve(
        self,
        fine_tuned_model_checkpoint: str,
        *,
        after: Union[str, NotGiven] = NOT_GIVEN,
        limit: Union[int, NotGiven] = NOT_GIVEN,
        order: Union[Literal["ascending", "descending"], NotGiven] = NOT_GIVEN,
        project_id: Union[str, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> PermissionRetrieveResponse:
        response = await self.openai_client.with_raw_response.fine_tuning.checkpoints.permissions.retrieve(  # noqa: E501
            fine_tuned_model_checkpoint=fine_tuned_model_checkpoint,
            after=after,
            limit=limit,
            order=order,
            project_id=project_id,
            extra_body=kwargs,
        )
        data = PermissionRetrieveResponse(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def delete(
        self,
        permission_id: str,
        *,
        fine_tuned_model_checkpoint: str,
        **kwargs,
    ) -> PermissionDeleteResponse:
        response = await self.openai_client.with_raw_response.fine_tuning.checkpoints.permissions.delete(  # noqa: E501
            permission_id=permission_id,
            fine_tuned_model_checkpoint=fine_tuned_model_checkpoint,
            extra_body=kwargs,
        )
        data = PermissionDeleteResponse(**json.loads(response.text))
        data._headers = response.headers

        return data


class AsyncAlpha(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.graders = AsyncGraders(client)


class AsyncGraders(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    async def run(
        self,
        *,
        grader: grader_run_params.Grader,
        model_sample: str,
        item: Union[object, NotGiven] = NOT_GIVEN,
        **kwargs,
    ) -> GraderRunResponse:
        response = (
            await self.openai_client.with_raw_response.fine_tuning.alpha.graders.run(
                grader=grader,
                model_sample=model_sample,
                item=item,
                extra_body=kwargs,
            )
        )
        data = GraderRunResponse(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def validate(
        self,
        *,
        grader: grader_run_params.Grader,
        **kwargs,
    ) -> GraderValidateResponse:
        response = (
            await (
                self.openai_client.with_raw_response.fine_tuning.alpha.graders.validate(
                    grader=grader,
                    extra_body=kwargs,
                )
            )
        )
        data = GraderValidateResponse(**json.loads(response.text))
        data._headers = response.headers

        return data
