"""
The following change is brought to handle the cases for pydantic v1 and v2
Including (import sys) and
sys.modules["openai"] = vendored_openai
"""
import sys
from ..._vendor import openai as vendored_openai
from .chat_complete import (
    ChatCompletion,
    AsyncChatCompletion,
    ChatCompletionsMessages,
    AsyncChatCompletionsMessages,
)
from .complete import Completion, AsyncCompletion
from .generation import Generations, AsyncGenerations, Prompts, AsyncPrompts
from .feedback import Feedback, AsyncFeedback
from .create_headers import createHeaders
from .post import Post, AsyncPost
from .embeddings import Embeddings, AsyncEmbeddings
from .images import Images, AsyncImages
from .assistants import Assistants, AsyncAssistants
from .threads import (
    Threads,
    Messages,
    Runs,
    Steps,
    AsyncThreads,
    AsyncMessages,
    AsyncRuns,
    AsyncSteps,
)
from .main_files import MainFiles, AsyncMainFiles
from .models import Models, AsyncModels
from .moderations import Moderations, AsyncModerations
from .audio import (
    Audio,
    Transcriptions,
    Translations,
    Speech,
    AsyncAudio,
    AsyncTranscriptions,
    AsyncTranslations,
    AsyncSpeech,
)
from .batches import Batches, AsyncBatches
from .fine_tuning import (
    FineTuning,
    Jobs,
    Checkpoints,
    AsyncFineTuning,
    AsyncJobs,
    AsyncCheckpoints,
    FineTuningCheckpoints,
    Permissions,
    AsyncFineTuningCheckpoints,
    AsyncPermissions,
)
from .vector_stores import (
    VectorStores,
    VectorFiles,
    VectorFileBatches,
    AsyncVectorStores,
    AsyncVectorFiles,
    AsyncVectorFileBatches,
)
from .admin import (
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
)

from .beta_chat import (
    BetaChat,
    BetaCompletions,
    AsyncBetaChat,
    AsyncBetaCompletions,
)

from .beta_realtime import (
    BetaRealtime,
    AsyncBetaRealtime,
    BetaSessions,
    AsyncBetaSessions,
)

from .responses import (
    Responses,
    InputItems,
    AsyncResponses,
    AsyncInputItems,
)

from .uploads import (
    Uploads,
    Parts,
    AsyncUploads,
    AsyncParts,
)

from .evals import (
    Evals,
    AsyncEvals,
    EvalsRuns,
    AsyncEvalsRuns,
    OutputItems,
    AsyncOutputItems,
)

from .configs import Configs, AsyncConfigs

from .api_keys import ApiKeys, AsyncApiKeys
from .virtual_keys import VirtualKeys, AsyncVirtualKeys
from .logs import Logs, AsyncLogs

sys.modules["openai"] = vendored_openai  # For pydantic v1 and v2 compatibility

__all__ = [
    "Completion",
    "AsyncCompletion",
    "ChatCompletion",
    "AsyncChatCompletion",
    "ChatCompletionsMessages",
    "AsyncChatCompletionsMessages",
    "Generations",
    "AsyncGenerations",
    "Feedback",
    "AsyncFeedback",
    "Prompts",
    "AsyncPrompts",
    "createHeaders",
    "Post",
    "AsyncPost",
    "Embeddings",
    "AsyncEmbeddings",
    "Images",
    "AsyncImages",
    "Assistants",
    "AsyncAssistants",
    "MainFiles",
    "AsyncMainFiles",
    "Models",
    "AsyncModels",
    "Threads",
    "AsyncThreads",
    "Messages",
    "AsyncMessages",
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
    "BetaChat",
    "BetaCompletions",
    "AsyncBetaChat",
    "AsyncBetaCompletions",
    "Uploads",
    "Parts",
    "AsyncUploads",
    "AsyncParts",
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
]
