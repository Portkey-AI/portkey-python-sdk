from typing import Dict, Mapping, Union
from typing_extensions import TypeAlias

from portkey_ai._vendor.openai._types import Omit


__all__ = ["Metadata"]

Metadata: TypeAlias = Dict[str, str]
Headers = Mapping[str, Union[str, Omit]]
Query = Mapping[str, object]
Body = object
