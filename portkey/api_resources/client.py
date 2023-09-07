"""Portkey implementation."""
import os
from typing import Optional
from .global_constants import (
    MISSING_API_KEY_ERROR_MESSAGE,
)
from .base_client import APIClient
from . import apis

__all__ = ["Portkey"]


class Portkey(APIClient):
    completion: apis.Completions
    chat_completion: apis.ChatCompletions

    def __init__(
        self, *, api_key: Optional[str] = None, base_url: Optional[str] = None
    ) -> None:
        if base_url is None:
            base_url = "https://api.portkey.ai"
        self.base_url = base_url
        self.api_key = api_key or os.environ.get("PORTKEY_API_KEY") or ""
        if not self.api_key:
            raise ValueError(MISSING_API_KEY_ERROR_MESSAGE)

        super().__init__(
            base_url=self.base_url,
            api_key=self.api_key,
        )
        self.completion = apis.Completions(self)
        self.chat_completion = apis.ChatCompletions(self)
