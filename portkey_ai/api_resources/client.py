from __future__ import annotations

from typing import List, Mapping, Optional, Union
import httpx
from portkey_ai.api_resources import apis
from portkey_ai.api_resources.base_client import APIClient, AsyncAPIClient

# from openai import AsyncOpenAI, OpenAI
from .._vendor.openai import OpenAI, AsyncOpenAI
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
    moderations: apis.Moderations
    audio: apis.Audio
    batches: apis.Batches
    fine_tuning: apis.FineTuning
    uploads: apis.Uploads

    class beta:
        assistants: apis.Assistants
        threads: apis.Threads
        vector_stores: apis.VectorStores
        chat: apis.BetaChat

        def __init__(self, client: Portkey) -> None:
            self.assistants = apis.Assistants(client)
            self.threads = apis.Threads(client)
            self.vector_stores = apis.VectorStores(client)
            self.chat = apis.BetaChat(client)

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
        debug: Optional[bool] = None,
        cache_force_refresh: Optional[bool] = None,
        custom_host: Optional[str] = None,
        forward_headers: Optional[List[str]] = None,
        openai_project: Optional[str] = None,
        openai_organization: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        aws_access_key_id: Optional[str] = None,
        aws_session_token: Optional[str] = None,
        aws_region: Optional[str] = None,
        vertex_project_id: Optional[str] = None,
        vertex_region: Optional[str] = None,
        workers_ai_account_id: Optional[str] = None,
        azure_resource_name: Optional[str] = None,
        azure_deployment_id: Optional[str] = None,
        azure_api_version: Optional[str] = None,
        huggingface_base_url: Optional[str] = None,
        http_client: Optional[httpx.Client] = None,
        request_timeout: Optional[int] = None,
        strict_open_ai_compliance: Optional[bool] = None,
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
            debug=debug,
            cache_force_refresh=cache_force_refresh,
            custom_host=custom_host,
            forward_headers=forward_headers,
            openai_project=openai_project,
            openai_organization=openai_organization,
            aws_secret_access_key=aws_secret_access_key,
            aws_access_key_id=aws_access_key_id,
            aws_session_token=aws_session_token,
            aws_region=aws_region,
            vertex_project_id=vertex_project_id,
            vertex_region=vertex_region,
            workers_ai_account_id=workers_ai_account_id,
            azure_resource_name=azure_resource_name,
            azure_deployment_id=azure_deployment_id,
            azure_api_version=azure_api_version,
            huggingface_base_url=huggingface_base_url,
            cache_namespace=cache_namespace,
            http_client=http_client,
            request_timeout=request_timeout,
            strict_open_ai_compliance=strict_open_ai_compliance,
            **kwargs,
        )

        self.openai_client = OpenAI(
            api_key=OPEN_AI_API_KEY,
            base_url=self.base_url,
            default_headers=self.allHeaders,
            http_client=http_client,
            max_retries=0,
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
        self.moderations = apis.Moderations(self)
        self.audio = apis.Audio(self)
        self.batches = apis.Batches(self)
        self.fine_tuning = apis.FineTuning(self)
        self.uploads = apis.Uploads(self)
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
        debug: Optional[bool] = None,
        cache_force_refresh: Optional[bool] = None,
        custom_host: Optional[str] = None,
        forward_headers: Optional[List[str]] = None,
        openai_project: Optional[str] = None,
        openai_organization: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        aws_access_key_id: Optional[str] = None,
        aws_session_token: Optional[str] = None,
        aws_region: Optional[str] = None,
        vertex_project_id: Optional[str] = None,
        vertex_region: Optional[str] = None,
        workers_ai_account_id: Optional[str] = None,
        azure_resource_name: Optional[str] = None,
        azure_deployment_id: Optional[str] = None,
        azure_api_version: Optional[str] = None,
        huggingface_base_url: Optional[str] = None,
        http_client: Optional[httpx.Client] = None,
        request_timeout: Optional[int] = None,
        strict_open_ai_compliance: Optional[bool] = None,
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
            debug=debug or self.debug,
            cache_force_refresh=cache_force_refresh or self.cache_force_refresh,
            custom_host=custom_host or self.custom_host,
            forward_headers=forward_headers or self.forward_headers,
            openai_project=openai_project or self.openai_project,
            openai_organization=openai_organization or self.openai_organization,
            aws_secret_access_key=aws_secret_access_key or self.aws_secret_access_key,
            aws_access_key_id=aws_access_key_id or self.aws_access_key_id,
            aws_session_token=aws_session_token or self.aws_session_token,
            aws_region=aws_region or self.aws_region,
            vertex_project_id=vertex_project_id or self.vertex_project_id,
            vertex_region=vertex_region or self.vertex_region,
            workers_ai_account_id=workers_ai_account_id or self.workers_ai_account_id,
            azure_resource_name=azure_resource_name or self.azure_resource_name,
            azure_deployment_id=azure_deployment_id or self.azure_deployment_id,
            azure_api_version=azure_api_version or self.azure_api_version,
            huggingface_base_url=huggingface_base_url or self.huggingface_base_url,
            cache_namespace=cache_namespace or self.cache_namespace,
            http_client=http_client or self._client,
            request_timeout=request_timeout or self.request_timeout,
            strict_open_ai_compliance=strict_open_ai_compliance
            or self.strict_open_ai_compliance,
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
    moderations: apis.AsyncModerations
    audio: apis.AsyncAudio
    batches: apis.AsyncBatches
    fine_tuning: apis.AsyncFineTuning
    uploads: apis.AsyncUploads

    class beta:
        assistants: apis.AsyncAssistants
        threads: apis.AsyncThreads
        vector_stores: apis.AsyncVectorStores
        chat: apis.AsyncBetaChat

        def __init__(self, client: AsyncPortkey) -> None:
            self.assistants = apis.AsyncAssistants(client)
            self.threads = apis.AsyncThreads(client)
            self.vector_stores = apis.AsyncVectorStores(client)
            self.chat = apis.AsyncBetaChat(client)

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
        debug: Optional[bool] = None,
        cache_force_refresh: Optional[bool] = None,
        custom_host: Optional[str] = None,
        forward_headers: Optional[List[str]] = None,
        openai_project: Optional[str] = None,
        openai_organization: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        aws_access_key_id: Optional[str] = None,
        aws_session_token: Optional[str] = None,
        aws_region: Optional[str] = None,
        vertex_project_id: Optional[str] = None,
        vertex_region: Optional[str] = None,
        workers_ai_account_id: Optional[str] = None,
        azure_resource_name: Optional[str] = None,
        azure_deployment_id: Optional[str] = None,
        azure_api_version: Optional[str] = None,
        huggingface_base_url: Optional[str] = None,
        http_client: Optional[httpx.AsyncClient] = None,
        request_timeout: Optional[int] = None,
        strict_open_ai_compliance: Optional[bool] = None,
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
            debug=debug,
            cache_force_refresh=cache_force_refresh,
            custom_host=custom_host,
            forward_headers=forward_headers,
            openai_project=openai_project,
            openai_organization=openai_organization,
            aws_secret_access_key=aws_secret_access_key,
            aws_access_key_id=aws_access_key_id,
            aws_session_token=aws_session_token,
            aws_region=aws_region,
            vertex_project_id=vertex_project_id,
            vertex_region=vertex_region,
            workers_ai_account_id=workers_ai_account_id,
            azure_resource_name=azure_resource_name,
            azure_deployment_id=azure_deployment_id,
            azure_api_version=azure_api_version,
            huggingface_base_url=huggingface_base_url,
            cache_namespace=cache_namespace,
            http_client=http_client,
            request_timeout=request_timeout,
            strict_open_ai_compliance=strict_open_ai_compliance,
            **kwargs,
        )

        self.openai_client = AsyncOpenAI(
            api_key=OPEN_AI_API_KEY,
            base_url=self.base_url,
            default_headers=self.allHeaders,
            http_client=http_client,
            max_retries=0,
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
        self.moderations = apis.AsyncModerations(self)
        self.audio = apis.AsyncAudio(self)
        self.batches = apis.AsyncBatches(self)
        self.fine_tuning = apis.AsyncFineTuning(self)
        self.uploads = apis.AsyncUploads(self)
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
        debug: Optional[bool] = None,
        cache_force_refresh: Optional[bool] = None,
        custom_host: Optional[str] = None,
        forward_headers: Optional[List[str]] = None,
        openai_project: Optional[str] = None,
        openai_organization: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        aws_access_key_id: Optional[str] = None,
        aws_session_token: Optional[str] = None,
        aws_region: Optional[str] = None,
        vertex_project_id: Optional[str] = None,
        vertex_region: Optional[str] = None,
        workers_ai_account_id: Optional[str] = None,
        azure_resource_name: Optional[str] = None,
        azure_deployment_id: Optional[str] = None,
        azure_api_version: Optional[str] = None,
        huggingface_base_url: Optional[str] = None,
        http_client: Optional[httpx.AsyncClient] = None,
        request_timeout: Optional[int] = None,
        strict_open_ai_compliance: Optional[bool] = None,
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
            debug=debug or self.debug,
            cache_force_refresh=cache_force_refresh or self.cache_force_refresh,
            custom_host=custom_host or self.custom_host,
            forward_headers=forward_headers or self.forward_headers,
            openai_project=openai_project or self.openai_project,
            openai_organization=openai_organization or self.openai_organization,
            aws_secret_access_key=aws_secret_access_key or self.aws_secret_access_key,
            aws_access_key_id=aws_access_key_id or self.aws_access_key_id,
            aws_session_token=aws_session_token or self.aws_session_token,
            aws_region=aws_region or self.aws_region,
            vertex_project_id=vertex_project_id or self.vertex_project_id,
            vertex_region=vertex_region or self.vertex_region,
            workers_ai_account_id=workers_ai_account_id or self.workers_ai_account_id,
            azure_resource_name=azure_resource_name or self.azure_resource_name,
            azure_deployment_id=azure_deployment_id or self.azure_deployment_id,
            azure_api_version=azure_api_version or self.azure_api_version,
            huggingface_base_url=huggingface_base_url or self.huggingface_base_url,
            cache_namespace=cache_namespace or self.cache_namespace,
            http_client=http_client or self._client,
            request_timeout=request_timeout or self.request_timeout,
            strict_open_ai_compliance=strict_open_ai_compliance
            or self.strict_open_ai_compliance,
            **self.kwargs,
            **kwargs,
        )

    async def post(self, url: str, **kwargs):
        return await apis.AsyncPost(self).create(url=url, **kwargs)

    with_options = copy
