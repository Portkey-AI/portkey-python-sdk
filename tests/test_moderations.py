from __future__ import annotations
import inspect

import os
from os import walk
from typing import Any, Dict, List
import pytest
from uuid import uuid4
from portkey_ai import Portkey
from time import sleep
from dotenv import load_dotenv
from .utils import read_json_file


load_dotenv(override=True)

base_url = os.environ.get("PORTKEY_BASE_URL")
api_key = os.environ.get("PORTKEY_API_KEY")
virtual_api_key = os.environ.get("OPENAI_VIRTUAL_KEY")

CONFIGS_PATH = "./tests/configs/moderations"


def get_configs(folder_path) -> List[Dict[str, Any]]:
    config_files = []
    for dirpath, _, file_names in walk(folder_path):
        for f in file_names:
            config_files.append(read_json_file(os.path.join(dirpath, f)))

    return config_files


class TestModerations:
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
            Authorization=f"{auth}",
            trace_id=str(uuid4()),
            metadata=self.get_metadata(),
        )

        moderations = portkey.moderations.create(
            input="I want to kill them.", model="text-moderation-stable"
        )

        assert isinstance(moderations.id, str) is True

    # --------------------------
    # Test -2
    t2_params = []
    for i in get_configs(f"{CONFIGS_PATH}/single_with_basic_config"):
        t2_params.append((client, i))

    @pytest.mark.parametrize("client, config", t2_params)
    def test_method_single_with_basic_config(self, client: Any, config: Dict) -> None:
        portkey = client(
            base_url=base_url,
            api_key=api_key,
            trace_id=str(uuid4()),
            metadata=self.get_metadata(),
            config=config,
        )

        moderations = portkey.moderations.create(
            input="I want to kill them.", model="text-moderation-stable"
        )

        assert isinstance(moderations.id, str) is True

    # --------------------------
    # Test-3
    t3_params = []
    for i in get_configs(f"{CONFIGS_PATH}/single_provider_with_vk_retry_cache"):
        t3_params.append((client, i))

    @pytest.mark.parametrize("client, config", t3_params)
    def test_method_single_provider_with_vk_retry_cache(
        self, client: Any, config: Dict
    ) -> None:
        # 1. Make a new cache the cache
        # 2. Make a cache hit and see if the response contains the data.
        random_id = str(uuid4())
        metadata = self.get_metadata()
        portkey = client(
            base_url=base_url,
            api_key=api_key,
            trace_id=random_id,
            virtual_key=virtual_api_key,
            metadata=metadata,
            config=config,
        )

        moderations = portkey.moderations.create(
            input="I want to kill them.", model="text-moderation-stable"
        )

        assert isinstance(moderations.id, str) is True
        # Sleeping for the cache to reflect across the workers. The cache has an
        # eventual consistency and not immediate consistency.
        sleep(20)
        portkey_2 = client(
            base_url=base_url,
            api_key=api_key,
            trace_id=random_id,
            virtual_key=virtual_api_key,
            metadata=metadata,
            config=config,
        )

        cached_moderations = portkey_2.moderations.create(
            input="I want to kill them.", model="text-moderation-stable"
        )

        assert isinstance(cached_moderations.id, str) is True
