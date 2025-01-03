import json
from typing import Dict, Optional
import httpx
from .utils import parse_headers
from typing import List, Any
from pydantic import BaseModel, PrivateAttr


__all__ = [
    "ModerationCreateResponse",
    "Categories",
    "CategoryAppliedInputTypes",
    "CategoryScores",
    "Moderation",
]


class Categories(BaseModel, extra="allow"):
    harassment: Optional[bool] = None
    harassment_threatening: Optional[bool] = None
    hate: Optional[bool] = None
    hate_threatening: Optional[bool] = None
    illicit: Optional[bool] = None
    illicit_violent: Optional[bool] = None
    self_harm: Optional[bool] = None
    self_harm_instructions: Optional[bool] = None
    self_harm_intent: Optional[bool] = None
    sexual: Optional[bool] = None
    sexual_minors: Optional[bool] = None
    violence: Optional[bool] = None
    violence_graphic: Optional[bool] = None


class CategoryAppliedInputTypes(BaseModel, extra="allow"):
    harassment: Optional[List[str]] = None
    harassment_threatening: Optional[List[str]] = None
    hate: Optional[List[str]] = None
    hate_threatening: Optional[List[str]] = None
    illicit: Optional[List[str]] = None
    illicit_violent: Optional[List[str]] = None
    self_harm: Optional[List[str]] = None
    self_harm_instructions: Optional[List[str]] = None
    self_harm_intent: Optional[List[str]] = None
    sexual: Optional[List[str]] = None
    sexual_minors: Optional[List[str]] = None
    violence: Optional[List[str]] = None
    violence_graphic: Optional[List[str]] = None


class CategoryScores(BaseModel, extra="allow"):
    harassment: Optional[float] = None
    harassment_threatening: Optional[float] = None
    hate: Optional[float] = None
    hate_threatening: Optional[float] = None
    illicit: Optional[float] = None
    illicit_violent: Optional[float] = None
    self_harm: Optional[float] = None
    self_harm_instructions: Optional[float] = None
    self_harm_intent: Optional[float] = None
    sexual: Optional[float] = None
    sexual_minors: Optional[float] = None
    violence: Optional[float] = None
    violence_graphic: Optional[float] = None


class Moderation(BaseModel, extra="allow"):
    categories: Optional[Categories] = None
    category_applied_input_types: Optional[CategoryAppliedInputTypes] = None
    category_scores: Optional[CategoryScores] = None
    flagged: Optional[bool] = None


class ModerationCreateResponse(BaseModel, extra="allow"):
    id: Optional[str] = None
    model: Optional[str] = None
    results: Optional[List[Moderation]] = None
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
