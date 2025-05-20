import json
from typing import Dict, List, Literal, Optional, Union
from typing_extensions import TypeAlias
import httpx

from portkey_ai.api_resources.types.shared_types import Metadata
from .utils import parse_headers
from typing import Any
from pydantic import BaseModel, PrivateAttr


class GraderRunResponse(BaseModel, extra="allow"):
    metadata: Optional[Metadata] = None
    api_model_grader_token_usage_per_model: Optional[Dict[str, object]] = None
    reward: Optional[float] = None
    sub_rewards: Optional[Dict[str, object]] = None
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


class InputContentOutputText(BaseModel, extra="allow"):
    text: Optional[str] = None
    type: Optional[Literal["output_text"]] = None


class ResponseInputText(BaseModel, extra="allow"):
    text: Optional[str] = None
    type: Optional[Literal["input_text"]] = None


InputContent: TypeAlias = Union[str, ResponseInputText, InputContentOutputText]


class Input(BaseModel, extra="allow"):
    content: InputContent
    role: Optional[Literal["user", "assistant", "system", "developer"]] = None
    type: Optional[Literal["message"]] = None


class StringCheckGrader(BaseModel, extra="allow"):
    input: Optional[str] = None
    name: Optional[str] = None
    operation: Optional[Literal["eq", "ne", "like", "ilike"]] = None
    reference: Optional[str] = None
    type: Optional[Literal["string_check"]] = None


class TextSimilarityGrader(BaseModel, extra="allow"):
    evaluation_metric: Optional[
        Literal[
            "fuzzy_match",
            "bleu",
            "gleu",
            "meteor",
            "rouge_1",
            "rouge_2",
            "rouge_3",
            "rouge_4",
            "rouge_5",
            "rouge_l",
        ]
    ] = None
    input: Optional[str] = None
    name: Optional[str] = None
    reference: Optional[str] = None
    type: Optional[Literal["text_similarity"]] = None


class PythonGrader(BaseModel, extra="allow"):
    name: Optional[str] = None
    source: Optional[str] = None
    type: Optional[Literal["python"]] = None
    image_tag: Optional[str] = None


class ScoreModelGrader(BaseModel, extra="allow"):
    input: Optional[List[Input]] = None
    model: Optional[str] = None
    name: Optional[str] = None
    type: Optional[Literal["score_model"]] = None
    range: Optional[List[float]] = None
    sampling_params: Optional[object] = None


class LabelModelGrader(BaseModel, extra="allow"):
    input: Optional[List[Input]] = None
    labels: Optional[List[str]] = None
    model: Optional[str] = None
    name: Optional[str] = None
    passing_labels: Optional[List[str]] = None
    type: Optional[Literal["label_model"]] = None


Graders: TypeAlias = Union[
    StringCheckGrader,
    TextSimilarityGrader,
    PythonGrader,
    ScoreModelGrader,
    LabelModelGrader,
]


class MultiGrader(BaseModel, extra="allow"):
    calculate_output: Optional[str] = None
    graders: Optional[Dict[str, Graders]] = None
    name: Optional[str] = None
    type: Optional[Literal["multi"]] = None


Grader: TypeAlias = Union[
    StringCheckGrader, TextSimilarityGrader, PythonGrader, ScoreModelGrader, MultiGrader
]


class GraderValidateResponse(BaseModel, extra="allow"):
    grader: Optional[Grader] = None

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
