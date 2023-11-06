import warnings
from typing import Literal, Optional, Union, Mapping, Any, overload
from portkey.api_resources.base_client import APIClient
from portkey.api_resources.global_constants import PROMPT_API
from portkey.api_resources.utils import (
    retrieve_config,
    GenericResponse,
)

from portkey.api_resources.streaming import Stream
from portkey.api_resources.apis.api_resource import APIResource


class Generations(APIResource):
    @classmethod
    def create(
        cls,
        *,
        prompt_id: str,
        config: Optional[Union[Mapping, str]] = None,
        variables: Optional[Mapping[str, Any]] = None,
    ) -> Union[GenericResponse, Stream[GenericResponse]]:
        warning_message = "This API has been deprecated. Please use the Prompt API for the saved prompt."  # noqa: E501
        warnings.warn(
            warning_message,
            DeprecationWarning,
            stacklevel=2,
        )
        if config is None:
            config = retrieve_config()
        _client = (
            APIClient()
            if isinstance(config, str)
            else APIClient(
                api_key=config.get("api_key"), base_url=config.get("base_url")
            )
        )
        body = {"variables": variables}
        response = cls(_client)._post(
            f"/v1/prompts/{prompt_id}/generate",
            body=body,
            mode=None,
            params=None,
            cast_to=GenericResponse,
            stream_cls=Stream[GenericResponse],
            stream=False,
        )
        response["warning"] = warning_message
        return response


class Prompt(APIResource):
    @classmethod
    @overload
    def create(
        cls,
        *,
        prompt_id: str,
        variables: Optional[Mapping[str, Any]] = None,
        config: Optional[Union[Mapping, str]] = None,
        stream: Literal[True],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        **kwargs,
    ) -> Stream[GenericResponse]:
        ...

    @classmethod
    @overload
    def create(
        cls,
        *,
        prompt_id: str,
        variables: Optional[Mapping[str, Any]] = None,
        config: Optional[Union[Mapping, str]] = None,
        stream: Literal[False] = False,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        **kwargs,
    ) -> GenericResponse:
        ...

    @classmethod
    @overload
    def create(
        cls,
        *,
        prompt_id: str,
        variables: Optional[Mapping[str, Any]] = None,
        config: Optional[Union[Mapping, str]] = None,
        stream: bool = False,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        **kwargs,
    ) -> Union[GenericResponse, Stream[GenericResponse]]:
        ...

    @classmethod
    def create(
        cls,
        *,
        prompt_id: str,
        variables: Optional[Mapping[str, Any]] = None,
        config: Optional[Union[Mapping, str]] = None,
        stream: bool = False,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        **kwargs,
    ) -> Union[GenericResponse, Stream[GenericResponse]]:
        if config is None:
            config = retrieve_config()
        _client = (
            APIClient()
            if isinstance(config, str)
            else APIClient(
                api_key=config.get("api_key"), base_url=config.get("base_url")
            )
        )
        body = {"variables": variables}
        return cls(_client)._post(
            # TODO: Update this API with new Rubeus API.
            PROMPT_API,
            body=body,
            mode=None,
            params=None,
            cast_to=GenericResponse,
            stream_cls=Stream[GenericResponse],
            stream=stream,
            headers={},
        )
