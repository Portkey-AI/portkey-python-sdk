from portkey_ai.api_resources.instrumentation.tracing_configs.crewai import (
    crewai_tracing_config,
)

from portkey_ai.api_resources.instrumentation.tracing_configs.langchain import (
    langchain_tracing_config,
)
from portkey_ai.api_resources.instrumentation.tracing_configs.langchain_community import (
    langchain_community_tracing_config,
)
from portkey_ai.api_resources.instrumentation.tracing_configs.langgraph import (
    langgraph_tracing_config,
)

# from portkey_ai.api_resources.instrumentation.tracing_configs.litellm import (
#     litellm_tracing_config,
# )
# from portkey_ai.api_resources.instrumentation.tracing_configs.openai import (
#     openai_tracing_config,
# )

tracing_configs = {
    "crewai": crewai_tracing_config,
    "langchain": langchain_tracing_config,
    "langchain_community": langchain_community_tracing_config,
    "langgraph": langgraph_tracing_config,
    # "litellm": litellm_tracing_config,
    # "openai": openai_tracing_config,
}

__all__ = ["tracing_configs"]
