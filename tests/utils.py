import json
from typing import Any, Dict


def read_json_file(path: str) -> Dict[str, Any]:
    return json.load(open(path, "r"))
