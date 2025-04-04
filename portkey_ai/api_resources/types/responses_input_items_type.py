from typing import Any, Dict, Optional, Union
from typing_extensions import Annotated, TypeAlias
import json
import httpx

from pydantic import BaseModel, PrivateAttr
from portkey_ai._vendor.openai.types.responses.response_computer_tool_call import (
    ResponseComputerToolCall,
)
from portkey_ai._vendor.openai.types.responses.response_computer_tool_call_output_item import (  # noqa: E501
    ResponseComputerToolCallOutputItem,
)
from portkey_ai._vendor.openai.types.responses.response_file_search_tool_call import (
    ResponseFileSearchToolCall,
)
from portkey_ai._vendor.openai.types.responses.response_function_tool_call_item import (
    ResponseFunctionToolCallItem,
)
from portkey_ai._vendor.openai.types.responses.response_function_tool_call_output_item import (  # noqa: E501
    ResponseFunctionToolCallOutputItem,
)
from portkey_ai._vendor.openai.types.responses.response_function_web_search import (
    ResponseFunctionWebSearch,
)
from portkey_ai._vendor.openai.types.responses.response_input_message_item import (
    ResponseInputMessageItem,
)
from portkey_ai._vendor.openai.types.responses.response_output_message import (
    ResponseOutputMessage,
)
from portkey_ai.api_resources.types.shared_types import PropertyInfo
from portkey_ai.api_resources.types.utils import parse_headers


class InputItemList(BaseModel, extra="allow"):
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def __str__(self):
        del self._headers
        return json.dumps(self.dict(), indent=4)

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)

    def __getitem__(self, key):
        return getattr(self, key, None)

    def get(self, key: str, default: Optional[Any] = None):
        return getattr(self, key, None) or default


# Keep the original TypeAlias for backward compatibility
InputItemListType: TypeAlias = Annotated[
    Union[
        ResponseInputMessageItem,
        ResponseOutputMessage,
        ResponseFileSearchToolCall,
        ResponseComputerToolCall,
        ResponseComputerToolCallOutputItem,
        ResponseFunctionWebSearch,
        ResponseFunctionToolCallItem,
        ResponseFunctionToolCallOutputItem,
    ],
    PropertyInfo(discriminator="type"),
]
