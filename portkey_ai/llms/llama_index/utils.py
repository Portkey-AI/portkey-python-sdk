"""
Utility Tools for the Portkey Class.

This file module contains a collection of utility functions designed to enhance
the functionality and usability of the Portkey class
"""
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    pass

IMPORT_ERROR_MESSAGE = (
    "Llama-Index is not installed.Please install it with `pip install llama-index`."
)


def all_available_models():
    try:
        from llama_index.llms.anthropic_utils import CLAUDE_MODELS
        from llama_index.llms.openai_utils import (
            AZURE_TURBO_MODELS,
            GPT3_5_MODELS,
            GPT3_MODELS,
            GPT4_MODELS,
            TURBO_MODELS,
        )

        return {
            **GPT4_MODELS,
            **TURBO_MODELS,
            **GPT3_5_MODELS,
            **GPT3_MODELS,
            **AZURE_TURBO_MODELS,
            **CLAUDE_MODELS,
        }
    except ImportError as exc:
        raise Exception(IMPORT_ERROR_MESSAGE) from exc


def chat_models():
    try:
        from llama_index.llms.openai_utils import (
            AZURE_TURBO_MODELS,
            GPT4_MODELS,
            TURBO_MODELS,
        )

        return {
            **GPT4_MODELS,
            **TURBO_MODELS,
            **AZURE_TURBO_MODELS,
        }
    except ImportError as exc:
        raise Exception(IMPORT_ERROR_MESSAGE) from exc


DISCONTINUED_MODELS = {
    "code-davinci-002": 8001,
    "code-davinci-001": 8001,
    "code-cushman-002": 2048,
    "code-cushman-001": 2048,
}

DEFAULT_MODEL = "gpt-3.5-turbo"


CLUADE_MODEL_FULLVERSION_MAP = {
    "claude-instant-1": "claude-instant-1.2",
    "claude-2": "claude-2.0",
}

ALL_AVAILABLE_MODELS = all_available_models()

CHAT_MODELS = chat_models()


def is_chat_model(model: str) -> bool:
    """Check if a given model is a chat-based language model.

    This function takes a model name or identifier as input and determines whether
    the model is designed for chat-based language generation, conversation, or
    interaction.

    Args:
        model (str): The name or identifier of the model to be checked.

    Returns:
        bool: True if the provided model is a chat-based language model,
        False otherwise.
    """
    return model in CHAT_MODELS


def modelname_to_contextsize(modelname: str) -> int:
    """Calculate the maximum number of tokens possible to generate for a model.

    Args:
        modelname: The modelname we want to know the context size for.

    Returns:
        The maximum context size

    Example:
        .. code-block:: python

            max_tokens = modelname_to_contextsize("text-davinci-003")
    """
    # handling finetuned models
    if "ft-" in modelname:  # legacy fine-tuning
        modelname = modelname.split(":")[0]
    elif modelname.startswith("ft:"):
        modelname = modelname.split(":")[1]

    if modelname in DISCONTINUED_MODELS:
        raise ValueError(
            f"Model {modelname} has been discontinued. " "Please choose another model."
        )

    context_size = ALL_AVAILABLE_MODELS.get(modelname, None)

    if context_size is None:
        raise ValueError(
            f"Unknown model: {modelname}. Please provide a valid model name."
            "Known models are: " + ", ".join(ALL_AVAILABLE_MODELS.keys())
        )

    return context_size
