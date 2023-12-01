from __future__ import annotations

import os
from portkey_ai import Portkey
from dotenv import load_dotenv

# from tests.utils import assert_matches_type
load_dotenv(override=True)
base_url = os.environ.get("PORTKEY_BASE_URL")
api_key = os.environ.get("PORTKEY_API_KEY")
virtual_api_key = os.environ.get("COHERE_VIRTUAL_KEY")

print("starting the tests....")
portkey = Portkey(
    base_url=base_url,
    api_key=api_key,
    virtual_key=virtual_api_key,
)

print("starting the creation phase.")

completion = portkey.chat.completions.create(
    messages=[
        {"role": "system", "content": "You are an assistant"},
        {"role": "user", "content": "Hello!"},
    ]
)

print("completion :: ", completion)
