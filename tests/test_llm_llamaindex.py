from __future__ import annotations

import os
from typing import Any

import pytest

from tests.utils import read_json_file
from portkey_ai.llamaindex import LlamaIndexCallbackHandler


from llama_index.llms.openai import OpenAI
from llama_index.core import Settings
from llama_index.core.callbacks import CallbackManager
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
)
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.chat_engine.types import AgentChatResponse

api_key = os.environ.get("PORTKEY_API_KEY")


class TestLLMLlamaindex:
    client = LlamaIndexCallbackHandler
    parametrize = pytest.mark.parametrize("client", [client], ids=["strict"])
    models = read_json_file("./tests/models.json")

    t1_params = []
    t1 = []
    for k, v in models.items():
        if k == "llamaindex":
            for emdmodel in v["HuggingFaceEmbedding"]:
                t1.append((client, "HuggingFaceEmbedding", emdmodel))
            for emdmodel in v["OpenAIEmbedding"]:
                t1.append((client, "OpenAIEmbedding", emdmodel))

            t1_params.extend(t1)

    @pytest.mark.parametrize("client, provider, model", t1_params)
    def test_method_llamaindex(self, client: Any, provider: Any, model: Any) -> None:
        handler = client(
            api_key=api_key,
        )

        # embed_model_name = "sentence-transformers/all-MiniLM-L6-v2"
        if provider == "HuggingFaceEmbedding":
            embed_model = HuggingFaceEmbedding(model_name=model)
        if provider == "OpenAIEmbedding":
            embed_model = OpenAIEmbedding(model=model)

        docs = SimpleDirectoryReader(
            "/Users/chandeep/Documents/Workspace/Portkey/SDK/Notebook/data"
        ).load_data()
        index = VectorStoreIndex.from_documents(docs)

        Settings.callback_manager = CallbackManager([handler])
        Settings.llm = OpenAI()
        Settings.embed_model = embed_model

        chat_engine = index.as_chat_engine()
        chat_response = chat_engine.chat("What did the author do growing up?")

        assert isinstance(chat_response, AgentChatResponse) is True
