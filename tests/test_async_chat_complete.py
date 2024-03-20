from __future__ import annotations
import inspect

import os
from os import walk
from typing import Any, Dict, List
import pytest
from uuid import uuid4
from portkey_ai import AsyncPortkey
from time import sleep
from dotenv import load_dotenv
from .utils import read_json_file, check_chat_streaming_chunk


load_dotenv(override=True)
base_url = os.environ.get("PORTKEY_BASE_URL")
api_key = os.environ.get("PORTKEY_API_KEY")
virtual_api_key = os.environ.get("OPENAI_VIRTUAL_KEY")
CONFIGS_PATH = "./tests/configs/chat_completions"


def get_configs(folder_path) -> List[Dict[str, Any]]:
    config_files = []
    for dirpath, _, file_names in walk(folder_path):
        for f in file_names:
            config_files.append(read_json_file(os.path.join(dirpath, f)))

    return config_files


class TestChatCompletions:
    client = AsyncPortkey
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

    @pytest.mark.asyncio
    @pytest.mark.parametrize("client, provider, auth, model", t1_params)
    async def test_method_single_with_vk_and_provider(
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

        completion = await portkey.chat.completions.create(
            messages=[{"role": "user", "content": "Say this is a test"}],
            model=model,
            max_tokens=245,
        )

        assert type(completion.choices[0].message.content) is str

    # --------------------------
    # Test -2
    t2_params = []
    for i in get_configs(f"{CONFIGS_PATH}/single_with_basic_config"):
        t2_params.append((client, i))

    @pytest.mark.asyncio
    @pytest.mark.parametrize("client, config", t2_params)
    async def test_method_single_with_basic_config(
        self, client: Any, config: Dict
    ) -> None:
        """
        Test the creation of a chat completion with a virtual key using the specified
        Portkey client.

        This test method performs the following steps:
        1. Creates a Portkey client instance with the provided base URL, API key, trace
        ID, and configuration loaded from the 'single_provider_with_virtualkey.json'
        file.
        2. Calls the Portkey client's chat.completions.create method to generate a
        completion.
        3. Prints the choices from the completion.

        Args:
            client (Portkey): The Portkey client instance used for the test.

        Raises:
            Any exceptions raised during the test.

        Note:
            - Ensure that the 'single_provider_with_virtualkey.json' file exists and
            contains valid configuration data.
            - Modify the 'model' parameter and the 'messages' content as needed for your
            use case.
        """
        portkey = client(
            base_url=base_url,
            api_key=api_key,
            trace_id=str(uuid4()),
            metadata=self.get_metadata(),
            config=config,
        )

        completion = await portkey.chat.completions.create(
            messages=[{"role": "user", "content": "Say this is a test"}],
            model="gpt-3.5-turbo",
        )

        assert type(completion.choices[0].message.content) is str

    # --------------------------
    # Test-3
    t3_params = []
    for i in get_configs(f"{CONFIGS_PATH}/single_provider_with_vk_retry_cache"):
        t3_params.append((client, i))

    @pytest.mark.asyncio
    @pytest.mark.parametrize("client, config", t3_params)
    async def test_method_single_provider_with_vk_retry_cache(
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

        await portkey.chat.completions.create(
            messages=[{"role": "user", "content": "Say this is a test"}],
            model="gpt-3.5-turbo",
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

        cached_completion = portkey_2.chat.completions.create(
            messages=[{"role": "user", "content": "Say this is a test"}],
            model="gpt-3.5-turbo",
        )
        assert type(cached_completion.choices[0].message.content) is str

    # --------------------------
    # Test-4
    t4_params = []
    for i in get_configs(f"{CONFIGS_PATH}/loadbalance_with_two_apikeys"):
        t4_params.append((client, i))

    @pytest.mark.asyncio
    @pytest.mark.parametrize("client, config", t4_params)
    async def test_method_loadbalance_with_two_apikeys(
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

        completion = await portkey.chat.completions.create(
            messages=[{"role": "user", "content": "Say this is a test"}], max_tokens=245
        )

        assert type(completion.choices[0].message.content) is str

    # --------------------------
    # Test-5
    t5_params = []
    for i in get_configs(f"{CONFIGS_PATH}/loadbalance_and_fallback"):
        t5_params.append((client, i))

    @pytest.mark.asyncio
    @pytest.mark.parametrize("client, config", t5_params)
    async def test_method_loadbalance_and_fallback(
        self, client: Any, config: Dict
    ) -> None:
        portkey = client(
            base_url=base_url,
            api_key=api_key,
            trace_id=str(uuid4()),
            config=config,
        )

        completion = await portkey.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "Say this is just a loadbalance and fallback test test",
                }
            ],
        )

        assert type(completion.choices[0].message.content) is str

    # --------------------------
    # Test-6
    t6_params = []
    for i in get_configs(f"{CONFIGS_PATH}/single_provider"):
        t6_params.append((client, i))

    @pytest.mark.asyncio
    @pytest.mark.parametrize("client, config", t6_params)
    async def test_method_single_provider(self, client: Any, config: Dict) -> None:
        portkey = client(
            base_url=base_url,
            api_key=api_key,
            trace_id=str(uuid4()),
            config=config,
        )

        completion = await portkey.chat.completions.create(
            messages=[{"role": "user", "content": "Say this is a test"}],
            model="gpt-3.5-turbo",
        )

        assert type(completion.choices[0].message.content) is str


class TestChatCompletionsStreaming:
    client = AsyncPortkey
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

    @pytest.mark.asyncio
    @pytest.mark.parametrize("client, provider, auth, model", t1_params)
    async def test_method_single_with_vk_and_provider(
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

        completion = await portkey.chat.completions.create(
            messages=[{"role": "user", "content": "Say this is a test"}],
            model=model,
            max_tokens=245,
            stream=True,
        )

        async for chunk in completion:
            assert check_chat_streaming_chunk(chunk) is True

    # --------------------------
    # Test -2
    t2_params = []
    for i in get_configs(f"{CONFIGS_PATH}/single_with_basic_config"):
        t2_params.append((client, i))

    @pytest.mark.asyncio
    @pytest.mark.parametrize("client, config", t2_params)
    async def test_method_single_with_basic_config(
        self, client: Any, config: Dict
    ) -> None:
        """
        Test the creation of a chat completion with a virtual key using the specified
        Portkey client.

        This test method performs the following steps:
        1. Creates a Portkey client instance with the provided base URL, API key, trace
        ID, and configuration loaded from the 'single_provider_with_virtualkey.json'
        file.
        2. Calls the Portkey client's chat.completions.create method to generate a
        completion.
        3. Prints the choices from the completion.

        Args:
            client (Portkey): The Portkey client instance used for the test.

        Raises:
            Any exceptions raised during the test.

        Note:
            - Ensure that the 'single_provider_with_virtualkey.json' file exists and
            contains valid configuration data.
            - Modify the 'model' parameter and the 'messages' content as needed for your
            use case.
        """
        portkey = client(
            base_url=base_url,
            api_key=api_key,
            trace_id=str(uuid4()),
            metadata=self.get_metadata(),
            config=config,
        )

        completion = await portkey.chat.completions.create(
            messages=[{"role": "user", "content": "Say this is a test"}],
            model="gpt-3.5-turbo",
            stream=True,
        )

        async for chunk in completion:
            assert check_chat_streaming_chunk(chunk) is True

    # --------------------------
    # Test-3
    t3_params = []
    for i in get_configs(f"{CONFIGS_PATH}/single_provider_with_vk_retry_cache"):
        t3_params.append((client, i))

    @pytest.mark.asyncio
    @pytest.mark.parametrize("client, config", t3_params)
    async def test_method_single_provider_with_vk_retry_cache(
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

        await portkey.chat.completions.create(
            messages=[{"role": "user", "content": "Say this is a test"}],
            model="gpt-3.5-turbo",
            stream=True,
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

        cached_completion = portkey_2.chat.completions.create(
            messages=[{"role": "user", "content": "Say this is a test"}],
            model="gpt-3.5-turbo",
            stream=True,
        )

        async for chunk in cached_completion:
            assert check_chat_streaming_chunk(chunk) is True

    # --------------------------
    # Test-4
    t4_params = []
    for i in get_configs(f"{CONFIGS_PATH}/loadbalance_with_two_apikeys"):
        t4_params.append((client, i))

    @pytest.mark.asyncio
    @pytest.mark.parametrize("client, config", t4_params)
    async def test_method_loadbalance_with_two_apikeys(
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

        completion = await portkey.chat.completions.create(
            messages=[{"role": "user", "content": "Say this is a test"}],
            max_tokens=245,
            stream=True,
        )

        async for chunk in completion:
            assert check_chat_streaming_chunk(chunk) is True

    # --------------------------
    # Test-5
    t5_params = []
    for i in get_configs(f"{CONFIGS_PATH}/loadbalance_and_fallback"):
        t5_params.append((client, i))

    @pytest.mark.asyncio
    @pytest.mark.parametrize("client, config", t5_params)
    async def test_method_loadbalance_and_fallback(
        self, client: Any, config: Dict
    ) -> None:
        portkey = client(
            base_url=base_url,
            api_key=api_key,
            trace_id=str(uuid4()),
            config=config,
        )

        completion = await portkey.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "Say this is just a loadbalance and fallback test test",
                }
            ],
            stream=True,
        )
        async for chunk in completion:
            assert check_chat_streaming_chunk(chunk) is True

    # --------------------------
    # Test-6
    t6_params = []
    for i in get_configs(f"{CONFIGS_PATH}/single_provider"):
        t6_params.append((client, i))

    @pytest.mark.asyncio
    @pytest.mark.parametrize("client, config", t6_params)
    async def test_method_single_provider(self, client: Any, config: Dict) -> None:
        portkey = client(
            base_url=base_url,
            api_key=api_key,
            trace_id=str(uuid4()),
            config=config,
        )

        completion = await portkey.chat.completions.create(
            messages=[{"role": "user", "content": "Say this is a test"}],
            model="gpt-3.5-turbo",
            stream=True,
        )

        async for chunk in completion:
            assert check_chat_streaming_chunk(chunk) is True
