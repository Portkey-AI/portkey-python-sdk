import json
from typing import Dict, Optional, Union
import httpx
from .utils import parse_headers
from typing import List, Any
from pydantic import BaseModel, PrivateAttr

__all__ = [
    "Error",
    "Hyperparameters",
    "FineTuningJob",
    "FineTuningJobList",
    "FineTuningJobEvent",
    "FineTuningJobEventList",
    "Metrics",
    "FineTuningJobCheckpoint",
    "FineTuningJobCheckpointList",
    "FineTuningJobWandbIntegration",
    "FineTuningJobWandbIntegrationObject",
    "MethodDpoHyperparameters",
    "MethodSupervisedHyperparameters",
    "MethodDpo",
    "MethodSupervised",
    "Method",
]


class Error(BaseModel, extra="allow"):
    code: Optional[str] = None
    message: Optional[str] = None
    param: Optional[str] = None


class Hyperparameters(BaseModel, extra="allow"):
    batch_size: Optional[Union[str, int]] = None
    learning_rate_multiplier: Optional[Union[str, float]] = None
    n_epochs: Optional[Union[str, int]] = None


class FineTuningJobWandbIntegration(BaseModel, extra="allow"):
    project: Optional[str] = None
    entity: Optional[str] = None
    name: Optional[str] = None
    tags: Optional[List[str]] = None


class FineTuningJobWandbIntegrationObject(BaseModel, extra="allow"):
    type: Optional[str] = None
    wandb: Optional[FineTuningJobWandbIntegration] = None


class MethodDpoHyperparameters(BaseModel, extra="allow"):
    batch_size: Optional[Union[str, int]] = None
    beta: Optional[Union[str, float]] = None
    learning_rate_multiplier: Optional[Union[str, float]] = None
    n_epochs: Optional[Union[str, int]] = None


class MethodSupervisedHyperparameters(BaseModel, extra="allow"):
    batch_size: Optional[Union[str, int]] = None
    learning_rate_multiplier: Optional[Union[str, float]] = None
    n_epochs: Optional[Union[str, int]] = None


class MethodDpo(BaseModel, extra="allow"):
    hyperparameters: Optional[MethodDpoHyperparameters] = None


class MethodSupervised(BaseModel, extra="allow"):
    hyperparameters: Optional[MethodSupervisedHyperparameters] = None


class Method(BaseModel, extra="allow"):
    dpo: Optional[MethodDpo] = None
    supervised: Optional[MethodSupervised] = None
    type: Optional[str] = None


class MethodDpoHyperparameters(BaseModel, extra="allow"):
    batch_size: Optional[Union[str, int]] = None
    beta: Optional[Union[str, float]] = None
    learning_rate_multiplier: Optional[Union[str, float]] = None
    n_epochs: Optional[Union[str, int]] = None


class MethodSupervisedHyperparameters(BaseModel, extra="allow"):
    batch_size: Optional[Union[str, int]] = None
    learning_rate_multiplier: Optional[Union[str, float]] = None
    n_epochs: Optional[Union[str, int]] = None


class MethodDpo(BaseModel, extra="allow"):
    hyperparameters: Optional[MethodDpoHyperparameters] = None


class MethodSupervised(BaseModel, extra="allow"):
    hyperparameters: Optional[MethodSupervisedHyperparameters] = None


class Method(BaseModel, extra="allow"):
    dpo: Optional[MethodDpo] = None
    supervised: Optional[MethodSupervised] = None
    type: Optional[str] = None


class FineTuningJob(BaseModel, extra="allow"):
    id: Optional[str] = None
    created_at: Optional[int] = None
    error: Optional[Error] = None
    fine_tuned_model: Optional[str] = None
    finished_at: Optional[int] = None
    hyperparameters: Optional[Hyperparameters] = None
    model: Optional[str] = None
    object: Optional[str] = None
    organization_id: Optional[str] = None
    result_files: Optional[List[str]] = None
    seed: Optional[int] = None
    status: Optional[str] = None
    trained_tokens: Optional[int] = None
    training_file: Optional[str] = None
    validation_file: Optional[str] = None
    estimated_finish: Optional[int] = None
    integrations: Optional[List[FineTuningJobWandbIntegrationObject]] = None
    method: Optional[Method] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def __str__(self):
        del self._headers
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)


class FineTuningJobList(BaseModel, extra="allow"):
    object: Optional[str] = None
    data: Optional[List[FineTuningJob]] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def __str__(self):
        del self._headers
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)


class FineTuningJobEvent(BaseModel, extra="allow"):
    id: Optional[str] = None
    created_at: Optional[int] = None
    level: Optional[str] = None
    message: Optional[str] = None
    object: Optional[str] = None
    data: Optional[Any] = None
    type: Optional[str] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def __str__(self):
        del self._headers
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)


class FineTuningJobEventList(BaseModel, extra="allow"):
    object: Optional[str] = None
    data: Optional[List[FineTuningJobEvent]] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def __str__(self):
        del self._headers
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)


class Metrics(BaseModel, extra="allow"):
    full_valid_loss: Optional[float] = None
    full_valid_mean_token_accuracy: Optional[float] = None
    step: Optional[float] = None
    train_loss: Optional[float] = None
    train_mean_token_accuracy: Optional[float] = None
    valid_loss: Optional[float] = None
    valid_mean_token_accuracy: Optional[float] = None


class FineTuningJobCheckpoint(BaseModel, extra="allow"):
    id: Optional[str] = None
    created_at: Optional[int] = None
    fine_tuned_model_checkpoint: Optional[str] = None
    fine_tuning_job_id: Optional[str] = None
    metrics: Optional[Metrics] = None
    object: Optional[str] = None
    step_number: Optional[int] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def __str__(self):
        del self._headers
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)


class FineTuningJobCheckpointList(BaseModel, extra="allow"):
    object: Optional[str] = None
    data: Optional[List[FineTuningJobCheckpoint]] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def __str__(self):
        del self._headers
        return json.dumps(self.dict(), indent=4)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)
