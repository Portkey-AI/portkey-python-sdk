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

CONFIGS_PATH = "./tests/configs/images"


def get_configs(folder_path) -> List[Dict[str, Any]]:
    config_files = []
    for dirpath, _, file_names in walk(folder_path):
        for f in file_names:
            config_files.append(read_json_file(os.path.join(dirpath, f)))

    return config_files


class TestImages:
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
        if k == "openai":
            for i in v["image"]:
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

        generation = portkey.images.generate(
            model=model, prompt="A cute baby sea otter", n=1, size="1024x1024"
        )

        assert type(generation.data[0].url) is str

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

        generation = portkey.images.generate(
            model="dall-e-3", prompt="A cute baby sea otter", n=1, size="1024x1024"
        )

        assert type(generation.data[0].url) is str

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

        portkey.images.generate(
            model="dall-e-3", prompt="A cute baby sea otter", n=1, size="1024x1024"
        )
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

        cached_generation = portkey_2.images.generate(
            model="dall-e-3", prompt="A cute baby sea otter", n=1, size="1024x1024"
        )

        assert type(cached_generation.data[0].url) is str

    # --------------------------
    # Test-4
    t4_params = []
    for i in get_configs(f"{CONFIGS_PATH}/loadbalance_with_two_apikeys"):
        t4_params.append((client, i))

    @pytest.mark.parametrize("client, config", t4_params)
    def test_method_loadbalance_with_two_apikeys(
        self, client: Any, config: Dict
    ) -> None:
        portkey = client(
            base_url=base_url,
            api_key=api_key,
            # virtual_key=virtual_api_key,
            trace_id=str(uuid4()),
            metadata=self.get_metadata(),
            config=config,
        )

        image = portkey.images.generate(
            prompt="A cute baby sea otter", n=1, size="1024x1024", response_format="b64_json"
        )

        assert type(image.data[0].b64_json) is str

    # --------------------------
    # Test-5
    t5_params = []
    for i in get_configs(f"{CONFIGS_PATH}/loadbalance_and_fallback"):
        t5_params.append((client, i))

    @pytest.mark.parametrize("client, config", t5_params)
    def test_method_loadbalance_and_fallback(self, client: Any, config: Dict) -> None:
        portkey = client(
            base_url=base_url,
            api_key=api_key,
            trace_id=str(uuid4()),
            config=config,
        )

        image = portkey.images.generate(
            prompt="A cute baby sea otter", n=1, size="1024x1024", response_format="b64_json"
        )

        assert type(image.data[0].b64_json) is str

    # --------------------------
    # Test-6
    t6_params = []
    for i in get_configs(f"{CONFIGS_PATH}/single_provider"):
        t6_params.append((client, i))

    @pytest.mark.parametrize("client, config", t6_params)
    def test_method_single_provider(self, client: Any, config: Dict) -> None:
        portkey = client(
            base_url=base_url,
            api_key=api_key,
            trace_id=str(uuid4()),
            config=config,
        )

        image = portkey.images.generate(
            model="dall-e-3", prompt="A cute baby sea otter", n=1, size="1024x1024"
        )

        assert type(image.data[0].url) is str

    # --------------------------
    # Test-7
    t7_params = []
    for i in get_configs(f"{CONFIGS_PATH}/single_provider"):
        t7_params.append((client, i))

    @pytest.mark.parametrize("client, config", t7_params)
    def test_method_all_params(self, client: Any, config: Dict) -> None:
        portkey = client(
            base_url=base_url,
            api_key=api_key,
            trace_id=str(uuid4()),
            config=config,
        )

        image = portkey.images.generate(
            prompt="A cute baby sea otter",
            model="dall-e-3",
            n=1,
            quality="standard",
            response_format="url",
            size="1024x1024",
            style="vivid",
            user="user-1234",
        )

        assert type(image.data[0].url) is str
