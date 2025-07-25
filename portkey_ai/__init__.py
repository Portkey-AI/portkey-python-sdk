import os
from typing import Mapping, Optional, Union
from ._vendor import openai
from portkey_ai.api_resources import (
    LLMOptions,
    Modes,
    ModesLiteral,
    ProviderTypes,
    ProviderTypesLiteral,
    CacheType,
    CacheLiteral,
    Message,
    PortkeyResponse,
    Completion,
    AsyncCompletion,
    Params,
    Config,
    RetrySettings,
    ChatCompletion,
    AsyncChatCompletion,
    ChatCompletionsMessages,
    AsyncChatCompletionsMessages,
    createHeaders,
    Prompts,
    AsyncPrompts,
    Portkey,
    AsyncPortkey,
    Images,
    AsyncImages,
    Assistants,
    AsyncAssistants,
    Threads,
    AsyncThreads,
    Messages,
    AsyncMessages,
    MainFiles,
    AsyncMainFiles,
    Models,
    AsyncModels,
    Runs,
    AsyncRuns,
    Steps,
    AsyncSteps,
    Moderations,
    AsyncModerations,
    Audio,
    Transcriptions,
    Translations,
    Speech,
    AsyncAudio,
    AsyncTranscriptions,
    AsyncTranslations,
    AsyncSpeech,
    Batches,
    AsyncBatches,
    FineTuning,
    Jobs,
    Checkpoints,
    AsyncFineTuning,
    AsyncJobs,
    AsyncCheckpoints,
    VectorStores,
    VectorFiles,
    VectorFileBatches,
    AsyncVectorStores,
    AsyncVectorFiles,
    AsyncVectorFileBatches,
    Admin,
    Users,
    Invites,
    Workspaces,
    WorkspacesUsers,
    AsyncAdmin,
    AsyncUsers,
    AsyncInvites,
    AsyncWorkspaces,
    AsyncWorkspacesUsers,
    BetaChat,
    AsyncBetaChat,
    BetaCompletions,
    AsyncBetaCompletions,
    Uploads,
    Parts,
    AsyncUploads,
    AsyncParts,
    Configs,
    AsyncConfigs,
    ApiKeys,
    AsyncApiKeys,
    VirtualKeys,
    AsyncVirtualKeys,
    Logs,
    AsyncLogs,
    BetaRealtime,
    AsyncBetaRealtime,
    BetaSessions,
    AsyncBetaSessions,
    Responses,
    InputItems,
    AsyncResponses,
    AsyncInputItems,
    Labels,
    AsyncLabels,
    Collections,
    AsyncCollections,
    FineTuningCheckpoints,
    AsyncFineTuningCheckpoints,
    Permissions,
    AsyncPermissions,
    Evals,
    AsyncEvals,
    EvalsRuns,
    AsyncEvalsRuns,
    OutputItems,
    AsyncOutputItems,
    Alpha,
    AsyncAlpha,
    Graders,
    AsyncGraders,
    Containers,
    AsyncContainers,
    ContainersFiles,
    AsyncContainersFiles,
    Content,
    AsyncContent,
)

from portkey_ai.version import VERSION
from portkey_ai.api_resources.global_constants import (
    PORTKEY_BASE_URL,
    PORTKEY_API_KEY_ENV,
    PORTKEY_PROXY_ENV,
    PORTKEY_GATEWAY_URL,
)

api_key = os.environ.get(PORTKEY_API_KEY_ENV)
base_url = os.environ.get(PORTKEY_PROXY_ENV, PORTKEY_BASE_URL)
config: Optional[Union[Mapping, str]] = None
mode: Optional[Union[Modes, ModesLiteral]] = None

__version__ = VERSION
__all__ = [
    "LLMOptions",
    "Modes",
    "PortkeyResponse",
    "ModesLiteral",
    "ProviderTypes",
    "ProviderTypesLiteral",
    "CacheType",
    "CacheLiteral",
    "Message",
    "Completion",
    "AsyncCompletion",
    "ChatCompletionsMessages",
    "AsyncChatCompletionsMessages",
    "Params",
    "RetrySettings",
    "ChatCompletion",
    "AsyncChatCompletion",
    "Config",
    "api_key",
    "base_url",
    "PORTKEY_GATEWAY_URL",
    "createHeaders",
    "Prompts",
    "AsyncPrompts",
    "Portkey",
    "AsyncPortkey",
    "Images",
    "AsyncImages",
    "Assistants",
    "AsyncAssistants",
    "Threads",
    "AsyncThreads",
    "Messages",
    "AsyncMessages",
    "MainFiles",
    "AsyncMainFiles",
    "Models",
    "AsyncModels",
    "Runs",
    "AsyncRuns",
    "Steps",
    "AsyncSteps",
    "Moderations",
    "AsyncModerations",
    "Audio",
    "Transcriptions",
    "Translations",
    "Speech",
    "AsyncAudio",
    "AsyncTranscriptions",
    "AsyncTranslations",
    "AsyncSpeech",
    "Batches",
    "AsyncBatches",
    "FineTuning",
    "Jobs",
    "Checkpoints",
    "AsyncFineTuning",
    "AsyncJobs",
    "AsyncCheckpoints",
    "VectorStores",
    "VectorFiles",
    "VectorFileBatches",
    "AsyncVectorStores",
    "AsyncVectorFiles",
    "AsyncVectorFileBatches",
    "BetaChat",
    "AsyncBetaChat",
    "BetaCompletions",
    "AsyncBetaCompletions",
    "Uploads",
    "Parts",
    "AsyncUploads",
    "AsyncParts",
    "openai",
    "Admin",
    "Users",
    "Invites",
    "Workspaces",
    "WorkspacesUsers",
    "AsyncAdmin",
    "AsyncUsers",
    "AsyncInvites",
    "AsyncWorkspaces",
    "AsyncWorkspacesUsers",
    "Configs",
    "AsyncConfigs",
    "ApiKeys",
    "AsyncApiKeys",
    "VirtualKeys",
    "AsyncVirtualKeys",
    "Logs",
    "AsyncLogs",
    "BetaRealtime",
    "AsyncBetaRealtime",
    "BetaSessions",
    "AsyncBetaSessions",
    "Responses",
    "InputItems",
    "AsyncResponses",
    "AsyncInputItems",
    "Labels",
    "AsyncLabels",
    "Collections",
    "AsyncCollections",
    "FineTuningCheckpoints",
    "AsyncFineTuningCheckpoints",
    "Permissions",
    "AsyncPermissions",
    "Evals",
    "AsyncEvals",
    "EvalsRuns",
    "AsyncEvalsRuns",
    "OutputItems",
    "AsyncOutputItems",
    "Alpha",
    "AsyncAlpha",
    "Graders",
    "AsyncGraders",
    "Containers",
    "AsyncContainers",
    "ContainersFiles",
    "AsyncContainersFiles",
    "Content",
    "AsyncContent",
]
