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
        t2_params.append((client, i["virtual_key"]))

    @pytest.mark.parametrize("client, virtual_key", t2_params)
    def test_method_single_with_vk_and_provider(
        self, client: Any, virtual_key: str
    ) -> None:
        metadata = self.get_metadata()
        portkey = client(
            base_url=base_url,
            api_key=api_key,
            virtual_key=virtual_key,
            trace_id=str(uuid4()),
            metadata=metadata,
        )
        thread = portkey.beta.threads.create()

        assert type(thread.id) is str
        assert thread.object == "thread"

        retrieve_thread = portkey.beta.threads.retrieve(thread.id)

        assert retrieve_thread.id == thread.id
        assert retrieve_thread.object == "thread"
        assert type(retrieve_thread.metadata) is dict

        update_thread = portkey.beta.threads.update(
            thread.id,
            metadata={
                "modified": "true",
            },
        )

        assert update_thread.id == thread.id
        assert update_thread.object == "thread"
        assert type(update_thread.metadata) is dict
        assert update_thread.metadata["modified"] == "true"

        delete_thread = portkey.beta.threads.delete(thread.id)

        assert delete_thread.id == thread.id
        assert delete_thread.object == "thread.deleted"
        assert delete_thread.deleted is True
