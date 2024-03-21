import json
from typing import Any, Dict


def read_json_file(path: str) -> Dict[str, Any]:
    return json.load(open(path, "r"))


def check_chat_streaming_chunk(chunk) -> bool:
    stop_reason = chunk.choices[0].finish_reason
    if type(stop_reason) is str:
        return chunk.choices[0].delta.content == ""
    else:
        return type(chunk.choices[0].delta.content) is str


def check_text_streaming_chunk(chunk) -> bool:
    return type(chunk.choices[0].text) is str
