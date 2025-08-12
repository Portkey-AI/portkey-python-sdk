from typing import Union
from portkey_ai._vendor.openai._types import HeadersLike
from portkey_ai._vendor.openai.types.webhooks.unwrap_webhook_event import (
    UnwrapWebhookEvent,
)
from portkey_ai.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from portkey_ai.api_resources.client import AsyncPortkey, Portkey


class Webhooks(APIResource):
    def __init__(self, client: Portkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    def unwrap(
        self,
        payload: Union[str, bytes],
        headers: HeadersLike,
        *,
        secret: Union[str, None] = None,
    ) -> UnwrapWebhookEvent:
        return self.openai_client.webhooks.unwrap(
            payload=payload,
            headers=headers,
            secret=secret,
        )

    def verify_signature(
        self,
        payload: Union[str, bytes],
        headers: HeadersLike,
        *,
        secret: Union[str, None] = None,
        tolerance: int = 300,
    ) -> None:
        return self.openai_client.webhooks.verify_signature(
            payload=payload,
            headers=headers,
            secret=secret,
            tolerance=tolerance,
        )


class AsyncWebhooks(AsyncAPIResource):
    def __init__(self, client: AsyncPortkey) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    def unwrap(
        self,
        payload: Union[str, bytes],
        headers: HeadersLike,
        *,
        secret: Union[str, None] = None,
    ) -> UnwrapWebhookEvent:
        return self.openai_client.webhooks.unwrap(
            payload=payload,
            headers=headers,
            secret=secret,
        )

    def verify_signature(
        self,
        payload: Union[str, bytes],
        headers: HeadersLike,
        *,
        secret: Union[str, None] = None,
        tolerance: int = 300,
    ) -> None:
        return self.openai_client.webhooks.verify_signature(
            payload=payload,
            headers=headers,
            secret=secret,
            tolerance=tolerance,
        )
