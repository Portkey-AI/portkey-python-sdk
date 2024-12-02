from typing import Optional

from typing import List
from pydantic import BaseModel


class FeedbackResponse(BaseModel, extra="allow"):
    status: Optional[str]
    message: Optional[str]
    feedback_ids: Optional[List[str]]
