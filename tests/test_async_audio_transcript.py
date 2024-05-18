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
from .utils import read_json_file


load_dotenv(override=True)

base_url = os.environ.get("PORTKEY_BASE_URL")
api_key = os.environ.get("PORTKEY_API_KEY")
virtual_api_key = os.environ.get("OPENAI_VIRTUAL_KEY")

CONFIGS_PATH = "./tests/configs/audio"


def get_configs(folder_path) -> List[Dict[str, Any]]:
    config_files = []
    for dirpath, _, file_names in walk(folder_path):
        for f in file_names:
            config_files.append(read_json_file(os.path.join(dirpath, f)))

    return config_files


class TestAudioTranscript:
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
    # Test-4
    t4_params = []
    t4 = []
    for k, v in models.items():
        for i in v["chat"]:
            t4.append((client, k, os.environ.get(v["env_variable"]), i))

        t4_params.extend(t4)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("client, provider, auth, model", t4_params)
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

        audio_file = open("/Users/chandeep/Documents/Workspace/Portkey/SDK/python latest version/portkey-python-sdk/tests/configs/audio/speech.mp3", "rb")

        transcript = await portkey.audio.transcriptions.create(
          model="whisper-1",
          file=audio_file
        )

        assert isinstance(transcript.text, str) is True

    # --------------------------
    # Test -5
    t5_params = []
    for i in get_configs(f"{CONFIGS_PATH}/single_with_basic_config"):
        t5_params.append((client, i))

    @pytest.mark.asyncio
    @pytest.mark.parametrize("client, config", t5_params)
    async def test_method_single_with_basic_config(self, client: Any, config: Dict) -> None:
        portkey = client(
            base_url=base_url,
            api_key=api_key,
            trace_id=str(uuid4()),
            metadata=self.get_metadata(),
            config=config,
        )
        audio_file = open("/Users/chandeep/Documents/Workspace/Portkey/SDK/python latest version/portkey-python-sdk/tests/configs/audio/speech.mp3", "rb")

        transcript = await portkey.audio.transcriptions.create(
          model="whisper-1",
          file=audio_file
        )

        assert isinstance(transcript.text, str) is True

    # --------------------------
    # Test-6
    t6_params = []
    for i in get_configs(f"{CONFIGS_PATH}/single_provider_with_vk_retry_cache"):
        t6_params.append((client, i))

    @pytest.mark.asyncio
    @pytest.mark.parametrize("client, config", t6_params)
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

        audio_file = open("/Users/chandeep/Documents/Workspace/Portkey/SDK/python latest version/portkey-python-sdk/tests/configs/audio/speech.mp3", "rb")

        transcript = await portkey.audio.transcriptions.create(
          model="whisper-1",
          file=audio_file
        )

        assert isinstance(transcript.text, str) is True
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

        cached_transcript = await portkey_2.audio.transcriptions.create(
          model="whisper-1",
          file=audio_file
        )

        assert isinstance(cached_transcript.text, str) is True

