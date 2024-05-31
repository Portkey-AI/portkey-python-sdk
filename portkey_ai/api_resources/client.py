from __future__ import annotations

from typing import Mapping, Optional, Union
from portkey_ai.api_resources import apis
from portkey_ai.api_resources.base_client import APIClient, AsyncAPIClient

from openai import AsyncOpenAI, OpenAI
from portkey_ai.api_resources.global_constants import (
    OPEN_AI_API_KEY,
)


class Portkey(APIClient):
    completions: apis.Completion
    chat: apis.ChatCompletion
    generations: apis.Generations
    prompts: apis.Prompts
    embeddings: apis.Embeddings
    feedback: apis.Feedback
    images: apis.Images
    files: apis.MainFiles
    models: apis.Models

    class beta:
        assistants: apis.Assistants
        threads: apis.Threads

        def __init__(self, client: Portkey) -> None:
            self.assistants = apis.Assistants(client)
            self.threads = apis.Threads(client)

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        virtual_key: Optional[str] = None,
        config: Optional[Union[Mapping, str]] = None,
        provider: Optional[str] = None,
        trace_id: Optional[str] = None,
        metadata: Union[Optional[dict[str, str]], str] = None,
        cache_namespace: Optional[str] = None,
        openai_project: Optional[str] = None,
        openai_organization: Optional[str] = None,
        **kwargs,
    ) -> None:
        super().__init__(
            api_key=api_key,
            base_url=base_url,
            virtual_key=virtual_key,
            config=config,
            provider=provider,
            trace_id=trace_id,
            metadata=metadata,
            cache_namespace=cache_namespace,
            openai_project=openai_project,
            openai_organization=openai_organization,
            **kwargs,
        )

        self.openai_client = OpenAI(
            api_key=OPEN_AI_API_KEY,
            base_url=self.base_url,
            default_headers=self.allHeaders,
        )

        self.completions = apis.Completion(self)
        self.chat = apis.ChatCompletion(self)
        self.generations = apis.Generations(self)
        self.prompts = apis.Prompts(self)
        self.embeddings = apis.Embeddings(self)
        self.feedback = apis.Feedback(self)
        self.images = apis.Images(self)
        self.files = apis.MainFiles(self)
        self.models = apis.Models(self)
        self.beta = self.beta(self)  # type: ignore

    def copy(
        self,
        *,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        virtual_key: Optional[str] = None,
        config: Optional[Union[Mapping, str]] = None,
        provider: Optional[str] = None,
        trace_id: Optional[str] = None,
        metadata: Union[Optional[dict[str, str]], str] = None,
        cache_namespace: Optional[str] = None,
        openai_project: Optional[str] = None,
        openai_organization: Optional[str] = None,
        **kwargs,
    ) -> Portkey:
        return self.__class__(
            api_key=api_key or self.api_key,
            base_url=base_url or self.base_url,
            virtual_key=virtual_key or self.virtual_key,
            config=config or self.config,
            provider=provider or self.provider,
            trace_id=trace_id or self.trace_id,
            metadata=metadata or self.metadata,
            cache_namespace=cache_namespace or self.cache_namespace,
            openai_project=openai_project or self.openai_project,
            openai_organization=openai_organization or self.openai_organization,
            **self.kwargs,
            **kwargs,
        )

    def post(self, url: str, **kwargs):
        return apis.Post(self).create(url=url, **kwargs)

    with_options = copy


class AsyncPortkey(AsyncAPIClient):
    completions: apis.AsyncCompletion
    chat: apis.AsyncChatCompletion
    generations: apis.AsyncGenerations
    prompts: apis.AsyncPrompts
    embeddings: apis.AsyncEmbeddings
    feedback: apis.AsyncFeedback
    images: apis.AsyncImages
    files: apis.AsyncMainFiles
    models: apis.AsyncModels

    class beta:
        assistants: apis.AsyncAssistants
        threads: apis.AsyncThreads

        def __init__(self, client: AsyncPortkey) -> None:
            self.assistants = apis.AsyncAssistants(client)
            self.threads = apis.AsyncThreads(client)

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        virtual_key: Optional[str] = None,
        config: Optional[Union[Mapping, str]] = None,
        provider: Optional[str] = None,
        trace_id: Optional[str] = None,
        metadata: Union[Optional[dict[str, str]], str] = None,
        cache_namespace: Optional[str] = None,
        openai_project: Optional[str] = None,
        openai_organization: Optional[str] = None,
        **kwargs,
    ) -> None:
        super().__init__(
            api_key=api_key,
            base_url=base_url,
            virtual_key=virtual_key,
            config=config,
            provider=provider,
            trace_id=trace_id,
            metadata=metadata,
            cache_namespace=cache_namespace,
            openai_project=openai_project,
            openai_organization=openai_organization,
            **kwargs,
        )

        self.openai_client = AsyncOpenAI(
            api_key=OPEN_AI_API_KEY,
            base_url=self.base_url,
            default_headers=self.allHeaders,
        )

        self.completions = apis.AsyncCompletion(self)
        self.chat = apis.AsyncChatCompletion(self)
        self.generations = apis.AsyncGenerations(self)
        self.prompts = apis.AsyncPrompts(self)
        self.embeddings = apis.AsyncEmbeddings(self)
        self.feedback = apis.AsyncFeedback(self)
        self.images = apis.AsyncImages(self)
        self.files = apis.AsyncMainFiles(self)
        self.models = apis.AsyncModels(self)
        self.beta = self.beta(self)  # type: ignore

    def copy(
        self,
        *,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        virtual_key: Optional[str] = None,
        config: Optional[Union[Mapping, str]] = None,
        provider: Optional[str] = None,
        trace_id: Optional[str] = None,
        metadata: Union[Optional[dict[str, str]], str] = None,
        cache_namespace: Optional[str] = None,
        openai_project: Optional[str] = None,
        openai_organization: Optional[str] = None,
        **kwargs,
    ) -> AsyncPortkey:
        return self.__class__(
            api_key=api_key or self.api_key,
            base_url=base_url or self.base_url,
            virtual_key=virtual_key or self.virtual_key,
            config=config or self.config,
            provider=provider or self.provider,
            trace_id=trace_id or self.trace_id,
            metadata=metadata or self.metadata,
            cache_namespace=cache_namespace or self.cache_namespace,
            openai_project=openai_project or self.openai_project,
            openai_organization=openai_organization or self.openai_organization,
            **self.kwargs,
            **kwargs,
        )

    async def post(self, url: str, **kwargs):
        return await apis.AsyncPost(self).create(url=url, **kwargs)

    with_options = copy
