import json
import os
from typing import Optional
from portkey_ai.api_resources import apis
from portkey_ai.api_resources.apis.api_resource import APIResource
from portkey_ai.api_resources.base_client import APIClient
from portkey_ai.api_resources.exceptions import AuthenticationError
import requests


class Logger:
    def __init__(
        self,
        api_key: Optional[str] = None,
    ) -> None:
        api_key = api_key or os.getenv("PORTKEY_API_KEY")

        self.headers = {
            "Content-Type": "application/json",
            "x-portkey-api-key": api_key,
        }

        self.url = "https://api.portkey.ai/v1/logger"

        if api_key is None:
            raise ValueError("API key is required to use the Logger API")

    def log(
        self,
        log_object: dict,
    ):
        body = log_object


        self.headers.update(
            {
                "x-portkey-provider": Logger.get_provider(
                    body["requestHeaders"]["provider"]
                )
            }
        )

        response = requests.post(
            url=self.url, json=json.dumps(log_object, default='str'), headers=self.headers
        )
        return response.status_code

    @staticmethod
    def get_provider(provider):
        provider_dict = {
            "openai": "openai",
            "mistralai": "mistral-ai",
        }
        return provider_dict.get(provider, "openai") # placeholder
