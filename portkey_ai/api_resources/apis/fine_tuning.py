import json
from typing import Iterable, Optional, Union
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.client import AsyncPortkey, Portkey
from openai._types import NotGiven, NOT_GIVEN
from openai.types.fine_tuning import job_create_params

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
            seed=seed,
            suffix=suffix,
            validation_file=validation_file,
            **kwargs,
        )
        data = FineTuningJob(**json.loads(response.text))
        data._headers = response.headers

        return data

    def retrieve(self, fine_tuning_job_id: str, **kwargs) -> FineTuningJob:
        response = self.openai_client.with_raw_response.fine_tuning.jobs.retrieve(
            fine_tuning_job_id=fine_tuning_job_id, **kwargs
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
            fine_tuning_job_id=fine_tuning_job_id, **kwargs
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
            fine_tuning_job_id=fine_tuning_job_id, after=after, limit=limit, **kwargs
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


class AsyncFineTuning(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.jobs = AsyncJobs(client)


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
            seed=seed,
            suffix=suffix,
            validation_file=validation_file,
            **kwargs,
        )
        data = FineTuningJob(**json.loads(response.text))
        data._headers = response.headers

        return data

    async def retrieve(self, fine_tuning_job_id: str, **kwargs) -> FineTuningJob:
        response = await self.openai_client.with_raw_response.fine_tuning.jobs.retrieve(
            fine_tuning_job_id=fine_tuning_job_id, **kwargs
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
            fine_tuning_job_id, **kwargs
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
                **kwargs,
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
        response = (
            await self.openai_client.with_raw_response.fine_tuning.jobs.checkpoints.list(
                fine_tuning_job_id=fine_tuning_job_id,
                after=after,
                limit=limit,
                **kwargs,
            )
        )

        data = FineTuningJobCheckpointList(**json.loads(response.text))
        data._headers = response.headers

        return data