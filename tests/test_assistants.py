from __future__ import annotations

import os
from typing import Any, Dict, List
from uuid import uuid4

import pytest
from os import walk

from portkey_ai import Portkey
import inspect
from tests.utils import read_json_file

base_url = os.environ.get("PORTKEY_BASE_URL")
api_key = os.environ.get("PORTKEY_API_KEY")
virtual_api_key = os.environ.get("OPENAI_VIRTUAL_KEY")

CONFIGS_PATH = "./tests/configs/assistants"


def get_configs(folder_path) -> List[Dict[str, Any]]:
    config_files = []
    for dirpath, _, file_names in walk(folder_path):
        for f in file_names:
            config_files.append(read_json_file(os.path.join(dirpath, f)))

    return config_files


class TestAssistants:
    client = Portkey
    parametrize = pytest.mark.parametrize("client", [client], ids=["strict"])
    models = read_json_file("./tests/models.json")

    def get_metadata(self):
        return {
            "case": "testing",
            "function": inspect.currentframe().f_back.f_code.co_name,
            "random_id": str(uuid4()),
        }

    # --------------------------
    # Test-1

    t1_params = []
    t = []
    for k, v in models.items():
        for i in v["chat"]:
            t.append((client, k, os.environ.get(v["env_variable"]), i))

        t1_params.extend(t)

    @pytest.mark.parametrize("client, provider, auth, model", t1_params)
    def test_method_single_with_vk_and_provider(
        self, client: Any, provider: str, auth: str, model
    ) -> None:
        portkey = client(
            base_url=base_url,
            api_key=api_key,
            provider=f"{provider}",
            Authorization=f"Bearer {auth}",
            trace_id=str(uuid4()),
            metadata=self.get_metadata(),
        )
        assistant = portkey.beta.assistants.create(
            model=model,
        )
        print(assistant)

    # --------------------------
    # Test-3

    t3_params = []
    for i in get_configs(f"{CONFIGS_PATH}/single_provider"):
        t3_params.append((client, i))

    @pytest.mark.parametrize("client, config", t3_params)
    def test_method_all_params(
        self, client: Any, provider: str, auth: str, model
    ) -> None:
        metadata = self.get_metadata()
        portkey = client(
            base_url=base_url,
            api_key=api_key,
            provider=f"{provider}",
            Authorization=f"Bearer {auth}",
            trace_id=str(uuid4()),
            metadata=metadata,
        )
        assistant = portkey.beta.assistants.create(
            model=model,
            description="string",
            file_ids=["file-m9QiEaDT9Le28LydiUTsUwDv"],
            instructions="You are a personal math tutor."
            + "Write and run code to answer math questions.",
            metadata=metadata,
            name="Math Tutor",
            tools=[{"type": "code_interpreter"}],
        )
        print(assistant)
