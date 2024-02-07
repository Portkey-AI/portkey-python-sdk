from __future__ import annotations

from typing import Mapping, Optional, Union
from portkey_ai.api_resources import apis
from portkey_ai.api_resources.base_client import APIClient, AsyncAPIClient


class Portkey(APIClient):
    completions: apis.Completion
    chat: apis.ChatCompletion
    generations: apis.Generations
    prompts: apis.Prompts
    embeddings: apis.Embeddings

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        virtual_key: Optional[str] = None,
        config: Optional[Union[Mapping, str]] = None,
        provider: Optional[str] = None,
        trace_id: Optional[str] = None,
        metadata: Optional[str] = None,
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
            **kwargs,
        )

        self.completions = apis.Completion(self)
        self.chat = apis.ChatCompletion(self)
        self.generations = apis.Generations(self)
        self.prompts = apis.Prompts(self)
        self.embeddings = apis.Embeddings(self)
        self.feedback = apis.Feedback(self)

    def copy(
        self,
        *,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        virtual_key: Optional[str] = None,
        config: Optional[Union[Mapping, str]] = None,
        provider: Optional[str] = None,
        trace_id: Optional[str] = None,
        metadata: Optional[str] = None,
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

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        virtual_key: Optional[str] = None,
        config: Optional[Union[Mapping, str]] = None,
        provider: Optional[str] = None,
        trace_id: Optional[str] = None,
        metadata: Optional[str] = None,
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
            **kwargs,
        )

        self.completions = apis.AsyncCompletion(self)
        self.chat = apis.AsyncChatCompletion(self)
        self.generations = apis.AsyncGenerations(self)
        self.prompts = apis.AsyncPrompts(self)
        self.embeddings = apis.AsyncEmbeddings(self)
        self.feedback = apis.AsyncFeedback(self)

    def copy(
        self,
        *,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        virtual_key: Optional[str] = None,
        config: Optional[Union[Mapping, str]] = None,
        provider: Optional[str] = None,
        trace_id: Optional[str] = None,
        metadata: Optional[str] = None,
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
            **self.kwargs,
            **kwargs,
        )

    async def post(self, url: str, **kwargs):
        return await apis.AsyncPost(self).create(url=url, **kwargs)

    with_options = copy
