from __future__ import annotations

import os
from typing import Any

import pytest

from tests.utils import read_json_file
from portkey_ai.llms.callback import PortkeyLangchain
from langchain.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

api_key = os.environ.get("PORTKEY_API_KEY")


class TestLLMLangchain:
    client = PortkeyLangchain
    parametrize = pytest.mark.parametrize("client", [client], ids=["strict"])
    models = read_json_file("./tests/models.json")

    t1_params = []
    t1 = []
    for k, v in models.items():
        if k == "langchain":
            for i in v["chat"]:
                t1.append((client, i))

            t1_params.extend(t1)

    @pytest.mark.parametrize("client, model", t1_params)
    def test_method_langchain_openai(
        self,  client: Any, model
    ) -> None:
        handler = client(
            api_key=api_key,
        )
        llm = ChatOpenAI(callbacks=[handler], model=model)
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are world class technical documentation writer."),
                ("user", "{input}"),
            ]
        )
        chain = LLMChain(llm=llm, prompt=prompt)
        

        assert isinstance(chain.invoke({"input": "what is langchain?"}).get('input'), str) is True
        assert isinstance(chain.invoke({"input": "what is langchain?"}).get('text'), str) is True
