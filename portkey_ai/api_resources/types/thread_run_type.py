import json
from typing import Dict, Literal, Optional, Union
import httpx
from .utils import parse_headers
from typing import List
from pydantic import BaseModel, PrivateAttr

__all__ = [
    "Run",
    "Usage",
    "LastError",
    "Function",
    "RequiredActionFunctionToolCall",
    "RequiredActionSubmitToolOutputs",
    "RequiredAction",
    "FunctionDefinition",
    "ToolAssistantToolsCode",
    "ToolAssistantToolsRetrieval",
    "ToolAssistantToolsFunction",
    "Tool",
    "RunList",
    "RunStep",
    "StepDetails",
    "ToolCallsStepDetails",
    "MessageCreationStepDetails",
    "MessageCreation",
    "ToolCall",
    "CodeInterpreter",
    "CodeInterpreterOutput",
    "CodeInterpreterOutputLogs",
    "CodeInterpreterOutputImage",
    "CodeInterpreterOutputImageImage",
    "CodeToolCall",
    "RetrievalToolCall",
    "FunctionToolCall",
    "FunctionParameters",
    "RunStepList",
]


class Function(BaseModel, extra="allow"):
    arguments: Optional[str]
    name: Optional[str]
    output: Optional[str] = None


class FunctionToolCall(BaseModel, extra="allow"):
    id: Optional[str]
    function: Function
    type: Literal["function"]


class RetrievalToolCall(BaseModel, extra="allow"):
    id: Optional[str]
    retrieval: Optional[object]
    type: Optional[str]


class CodeInterpreterOutputLogs(BaseModel, extra="allow"):
    logs: Optional[str]
    type: Optional[str]


class CodeInterpreterOutputImageImage(BaseModel, extra="allow"):
    file_id: Optional[str]


class CodeInterpreterOutputImage(BaseModel, extra="allow"):
    image: CodeInterpreterOutputImageImage
    type: Optional[str]


CodeInterpreterOutput = Union[CodeInterpreterOutputLogs, CodeInterpreterOutputImage]


class CodeInterpreter(BaseModel, extra="allow"):
    input: Optional[str]
    outputs: List[CodeInterpreterOutput]


class CodeToolCall(BaseModel, extra="allow"):
    id: Optional[str]
    code_interpreter: CodeInterpreter
    type: Optional[str]


ToolCall = Union[CodeToolCall, RetrievalToolCall, FunctionToolCall]


class ToolCallsStepDetails(BaseModel, extra="allow"):
    tool_calls: Optional[List[ToolCall]]
    type: Optional[str]


class MessageCreation(BaseModel, extra="allow"):
    message_id: Optional[str]


class MessageCreationStepDetails(BaseModel, extra="allow"):
    message_creation: Optional[MessageCreation]

    type: Optional[str]


StepDetails = Union[MessageCreationStepDetails, ToolCallsStepDetails]


class Usage(BaseModel, extra="allow"):
    completion_tokens: Optional[int]
    prompt_tokens: Optional[int]
    total_tokens: Optional[int]


class LastError(BaseModel, extra="allow"):
    code: Optional[str]
    message: Optional[str]


class FunctionRA(BaseModel, extra="allow"):
    arguments: Optional[str]
    name: Optional[str]


class RequiredActionFunctionToolCall(BaseModel, extra="allow"):
    id: Optional[str]
    function: Optional[FunctionRA]
    type: Optional[str]


class RequiredActionSubmitToolOutputs(BaseModel, extra="allow"):
    tool_calls: Optional[List[RequiredActionFunctionToolCall]]


class RequiredAction(BaseModel, extra="allow"):
    submit_tool_outputs: Optional[RequiredActionSubmitToolOutputs]
    type: Optional[str]


FunctionParameters = Dict[str, object]


class FunctionDefinition(BaseModel, extra="allow"):
    name: Optional[str]
    description: Optional[str] = None
    parameters: Optional[FunctionParameters] = None


class ToolAssistantToolsCode(BaseModel, extra="allow"):
    type: Optional[str]


class ToolAssistantToolsRetrieval(BaseModel, extra="allow"):
    type: Optional[str]


class ToolAssistantToolsFunction(BaseModel, extra="allow"):
    function: Optional[FunctionDefinition]
    type: Optional[str]


Tool = Union[
    ToolAssistantToolsCode, ToolAssistantToolsRetrieval, ToolAssistantToolsFunction
]


class Run(BaseModel, extra="allow"):
    id: Optional[str]
    assistant_id: Optional[str]
    cancelled_at: Optional[int] = None
    completed_at: Optional[int] = None
    created_at: Optional[int]
    expires_at: Optional[int]
    failed_at: Optional[int] = None
    file_ids: Optional[List[str]] = None
    instructions: Optional[str]
    last_error: Optional[LastError] = None
    metadata: Optional[object] = None
    model: Optional[str]
    object: Optional[str]
    required_action: Optional[RequiredAction] = None
    started_at: Optional[int] = None
    status: Optional[str]
    thread_id: Optional[str]
    tools: Optional[List[Tool]]
    usage: Optional[Usage] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def __str__(self):
        del self._headers
        return json.dumps(self.dict(), indent=4)

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)


class RunList(BaseModel, extra="allow"):
    object: Optional[str]
    data: Optional[List[Run]]
    first_id: Optional[str]
    last_id: Optional[str]
    has_more: Optional[bool]
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def __str__(self):
        del self._headers
        return json.dumps(self.dict(), indent=4)

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)


class RunStep(BaseModel, extra="allow"):
    id: Optional[str]
    assistant_id: Optional[str]
    cancelled_at: Optional[int] = None
    completed_at: Optional[int] = None
    created_at: Optional[int]
    expired_at: Optional[int] = None
    failed_at: Optional[int] = None
    last_error: Optional[LastError] = None
    metadata: Optional[object] = None
    object: Optional[str]
    run_id: Optional[str]
    status: Optional[str]
    step_details: Optional[StepDetails]
    thread_id: Optional[str]
    type: Optional[str]
    usage: Optional[Usage] = None
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def __str__(self):
        del self._headers
        return json.dumps(self.dict(), indent=4)

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)


class RunStepList(BaseModel, extra="allow"):
    object: Optional[str]
    data: Optional[List[RunStep]]
    first_id: Optional[str]
    last_id: Optional[str]
    has_more: Optional[bool]
    _headers: Optional[httpx.Headers] = PrivateAttr()

    def __str__(self):
        del self._headers
        return json.dumps(self.dict(), indent=4)

    def get_headers(self) -> Optional[Dict[str, str]]:
        return parse_headers(self._headers)
