from typing import Mapping, Optional, Union
from portkey.api_resources.apis.api_resource import APIResource
from portkey.api_resources.base_client import APIClient
from portkey.api_resources.global_constants import FEEDBACK_API
from portkey.api_resources.streaming import Stream
from portkey.api_resources.utils import GenericResponse


class Feedback(APIResource):
    @classmethod
    def create(
        cls,
        *,
        trace_id: Optional[str] = None,
        value: Optional[int] = None,
        weight: Optional[float] = None,
        config: Optional[Union[Mapping, str]] = None,
    ) -> None:
        _client = (
            APIClient()
            if isinstance(config, str) or config is None
            else APIClient(
                api_key=config.get("api_key"), base_url=config.get("base_url")
            )
        )
        body = dict(trace_id=trace_id, value=value, weight=weight)
        return cls(_client)._post(
            FEEDBACK_API,
            body=body,
            mode="",
            params=None,
            cast_to=GenericResponse,
            stream_cls=Stream[GenericResponse],
            stream=False,
            headers={},
        )
