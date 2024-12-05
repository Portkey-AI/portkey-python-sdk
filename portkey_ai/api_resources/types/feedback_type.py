from typing import Optional

from typing import List
from pydantic import BaseModel


class FeedbackResponse(BaseModel, extra="allow"):
    status: Optional[str] = None
    message: Optional[str] = None
    feedback_ids: Optional[List[str]] = None
