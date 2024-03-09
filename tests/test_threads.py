from __future__ import annotations

import os
from typing import Any, Dict, List
from uuid import uuid4

import pytest

from portkey_ai import Portkey
import inspect
from tests.utils import read_json_file

base_url = os.environ.get("PORTKEY_BASE_URL")
api_key = os.environ.get("PORTKEY_API_KEY")
virtual_api_key = os.environ.get("OPENAI_VIRTUAL_KEY")

CONFIGS_PATH = "./tests/configs/threads"


def get_configs(folder_path) -> List[Dict[str, Any]]:
    config_files = []
    for dirpath, _, file_names in os.walk(folder_path):
        for f in file_names:
            config_files.append(read_json_file(os.path.join(dirpath, f)))

    return config_files


class TestThreads:
    client = Portkey
    parametrize = pytest.mark.parametrize("client", [client], ids=["strict"])
    models = read_json_file("./tests/models.json")

    def get_metadata(self):
        return {
            "case": "testing",
            "function": inspect.currentframe().f_back.f_code.co_name,
            "random_id": str(uuid4()),
        }

    t2_params = []
    for i in get_configs(f"{CONFIGS_PATH}/single_with_basic_config"):
        t2_params.append((client, i))

    @pytest.mark.parametrize("client, provider, auth, model", t2_params)
    def test_method_single_with_vk_and_provider(
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
        thread = portkey.beta.threads.create()
        print(thread)
