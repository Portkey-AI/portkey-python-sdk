import json
from typing import Dict, Optional, Union
import httpx
from .utils import parse_headers
from typing import List, Any
from pydantic import BaseModel, PrivateAttr
from openai.types.fine_tuning import FineTuningJobWandbIntegrationObject

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
]


class Error(BaseModel):
    code: str
    message: str
    param: Optional[str] = None


class Hyperparameters(BaseModel):
    n_epochs: Union[str, int]


class FineTuningJob(BaseModel):
    id: str
    created_at: int
    error: Optional[Error] = None
    fine_tuned_model: Optional[str] = None
    finished_at: Optional[int] = None
    hyperparameters: Hyperparameters
    model: str
    object: str
    organization_id: str
    result_files: List[str]
    seed: int
    status: str
    trained_tokens: Optional[int] = None
    training_file: str
    validation_file: Optional[str] = None
    estimated_finish: Optional[int] = None
    integrations: Optional[List[FineTuningJobWandbIntegrationObject]] = None
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


class FineTuningJobList(BaseModel):
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


class FineTuningJobEvent(BaseModel):
    id: str
    created_at: int
    level: str
    message: str
    object: str
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


class FineTuningJobEventList(BaseModel):
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


class Metrics(BaseModel):
    full_valid_loss: Optional[float] = None
    full_valid_mean_token_accuracy: Optional[float] = None
    step: Optional[float] = None
    train_loss: Optional[float] = None
    train_mean_token_accuracy: Optional[float] = None
    valid_loss: Optional[float] = None
    valid_mean_token_accuracy: Optional[float] = None


class FineTuningJobCheckpoint(BaseModel):
    id: str
    created_at: int
    fine_tuned_model_checkpoint: str
    fine_tuning_job_id: str
    metrics: Metrics
    object: str
    step_number: int
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


class FineTuningJobCheckpointList(BaseModel):
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
