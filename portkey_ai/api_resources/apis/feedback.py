from typing import Optional, Dict, Any, List
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.base_client import APIClient, AsyncAPIClient
from portkey_ai.api_resources.streaming import AsyncStream, Stream
from portkey_ai.api_resources.types.feedback_type import FeedbackResponse
from portkey_ai.api_resources.utils import PortkeyApiPaths


class Feedback(APIResource):
    def __init__(self, client: APIClient) -> None:
        super().__init__(client)

    def create(
        self,
        *,
        trace_id: Optional[str] = None,
        value: Optional[int] = None,
        weight: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> FeedbackResponse:
        body = dict(trace_id=trace_id, value=value, weight=weight, metadata=metadata)
        return self._post(
            PortkeyApiPaths.FEEDBACK_API,
            body=body,
            params=None,
            cast_to=FeedbackResponse,
            stream_cls=Stream[FeedbackResponse],
            stream=False,
            headers={},
        )

    def bulk_create(self, *, feedbacks: List[Dict[str, Any]]) -> FeedbackResponse:
        body = feedbacks
        return self._post(
            PortkeyApiPaths.FEEDBACK_API,
            body=body,
            params=None,
            cast_to=FeedbackResponse,
            stream_cls=Stream[FeedbackResponse],
            stream=False,
            headers={},
        )
    
    def update(
        self,
        *,
        feedback_id: Optional[str] = None,
        value: Optional[int] = None,
        weight: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> FeedbackResponse:
        body = dict(value=value, weight=weight, metadata=metadata)

        return self._put(
            f"{PortkeyApiPaths.FEEDBACK_API}/{feedback_id}",
            body=body,
            params=None,
            cast_to=FeedbackResponse,
            stream_cls=Stream[FeedbackResponse],
            stream=False,
            headers={},
        )


class AsyncFeedback(AsyncAPIResource):
    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)

    async def create(
        self,
        *,
        trace_id: Optional[str] = None,
        value: Optional[int] = None,
        weight: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> FeedbackResponse:
        body = dict(trace_id=trace_id, value=value, weight=weight, metadata=metadata)
        return await self._post(
            PortkeyApiPaths.FEEDBACK_API,
            body=body,
            params=None,
            cast_to=FeedbackResponse,
            stream_cls=AsyncStream[FeedbackResponse],
            stream=False,
            headers={},
        )

    async def bulk_create(self, *, feedbacks: List[Dict[str, Any]]) -> FeedbackResponse:
        body = feedbacks
        return await self._post(
            PortkeyApiPaths.FEEDBACK_API,
            body=body,
            params=None,
            cast_to=FeedbackResponse,
            stream_cls=AsyncStream[FeedbackResponse],
            stream=False,
            headers={},
        )
    
    async def update(
        self,
        *,
        feedback_id: Optional[str] = None,
        value: Optional[int] = None,
        weight: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> FeedbackResponse:
        body = dict(value=value, weight=weight, metadata=metadata)
        return await self._put(
            f"{PortkeyApiPaths.FEEDBACK_API}/{feedback_id}",
            body=body,
            params=None,
            cast_to=FeedbackResponse,
            stream_cls=Stream[FeedbackResponse],
            stream=False,
            headers={},
        )
