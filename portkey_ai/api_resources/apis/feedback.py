from typing import Optional, Dict, Any
from portkey_ai.api_resources.apis.api_resource import APIResource
from portkey_ai.api_resources.base_client import APIClient
from portkey_ai.api_resources.streaming import Stream
from portkey_ai.api_resources.utils import GenericResponse, PortkeyApiPaths


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
    ) -> None:
        body = dict(trace_id=trace_id, value=value,
                    weight=weight, metadata=metadata)
        return self._post(
            PortkeyApiPaths.FEEDBACK_API,
            body=body,
            params=None,
            cast_to=GenericResponse,
            stream_cls=Stream[GenericResponse],
            stream=False,
            headers={},
        )
